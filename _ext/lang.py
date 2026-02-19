from docutils import nodes
from sphinx.util.logging import getLogger
from sphinx.util.docutils import SphinxRole
from sphinx_design.shared import SdDirective, WARNING_TYPE, create_component, is_component
from docutils.parsers.rst import directives

LOGGER = getLogger(__name__)


class LangIdentifierRole(SphinxRole):
    def run(self):
        node = nodes.inline(text=self.text, classes=['lang-choices', 'lang-id'])
        return [node], []


class LangTextRole(SphinxRole):
    def run(self):
        node = nodes.inline(text=self.text, classes=['lang-choices', 'lang-text'])
        return [node], []


class InvisibleTabSet(SdDirective):
    has_content = True
    option_spec = {
        "sync-group": directives.unchanged_required,
        "class": directives.class_option,
    }

    def run_with_defaults(self):
        self.assert_has_content()
        tab_set = create_component(
            "tab-set", classes=["sd-tab-set", "invisible-tab-set", *self.options.get("class", [])]
        )
        self.set_source_info(tab_set)
        self.state.nested_parse(self.content, self.content_offset, tab_set)
        valid_children = []
        for item in tab_set.children:
            if not is_component(item, "tab-item"):
                LOGGER.warning(
                    f"All children of a 'tab-set' "
                    f"should be 'tab-item' [{WARNING_TYPE}.tab]",
                    location=item,
                    type=WARNING_TYPE,
                    subtype="tab",
                )
                continue  # Skip invalid children instead of breaking
            if "sync_id" in item.children[0]:
                item.children[0]["sync_group"] = self.options.get("sync-group", "tab")
            valid_children.append(item)

        tab_set.children = valid_children
        return [tab_set]


def setup(app):
    app.add_role('lang-id', LangIdentifierRole())
    app.add_role('lang-text', LangTextRole())
    app.add_directive('invisible-tab-set', InvisibleTabSet)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
