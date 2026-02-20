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


def setup(app):
    app.add_role('lang-id', LangIdentifierRole())
    app.add_role('lang-text', LangTextRole())

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
