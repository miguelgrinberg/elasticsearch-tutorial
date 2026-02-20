function getCurrentLang() {
  const lang = window.sessionStorage.getItem(storageKeyPrefix + 'lang');
  if (!lang) {
    const firstOption = document.querySelector('#lang-select option');
    return firstOption.value;
  }
  return lang;
}

document.addEventListener('DOMContentLoaded', () => {
  // insert language selector
  const langSelect = document.createElement('select');
  langSelect.setAttribute('id', 'lang-select');
  langSelect.innerHTML = `
    <option value="py">Python</option>
    <option value="js">JavaScript</option>
    <option value="go">Go</option>
  `;
  const iconContainer = document.querySelector('.content-icon-container');
  iconContainer.insertBefore(langSelect, iconContainer.firstChild);

  // language selector
  const lang = getCurrentLang();
  //const langSelect = document.getElementById('lang-select');
  langSelect.value = lang;
  langSelect.addEventListener('change', () => {
    const langSelect = document.getElementById('lang-select');
    const tab = document.querySelector(`[data-sync-group="lang"][data-sync-id="${langSelect.value}"]`);
    if (tab) {
      tab.click();
    }
  });

  // hook into tabbed components to update language identifiers
  document.querySelectorAll(".sd-tab-label").forEach((label) => {
    label.addEventListener('click', updateLang);
  });

  // update language identifiers
  updateLang();
});

function updateLang() {
  const lang = getCurrentLang();
  const langSelect = document.getElementById('lang-select');
  langSelect.value = lang;
  document.querySelectorAll('.lang-choices').forEach(elem => {
    if (!elem.langChoices) {
      const choices = {}
      elem.innerHTML.split(',').forEach(s => {
        if (!s.includes(':')) {
          choices[''] = s;
        }
        else {
          const [l, ...ids] = s.split(':');
          const langs = l.split('|');
          langs.forEach(lang => choices[lang] = ids.join(':'));
        }
      });
      elem.langChoices = choices;
    }

    let choice;
    if (elem.langChoices[lang]) {
      choice = elem.langChoices[lang];
    }
    else {
      choice = elem.langChoices[''] || '';
    }
    if (elem.classList.contains('lang-id')) {
      elem.innerHTML = '<code class="docutils literal notranslate"><span class="pre">' + choice + '</code>';
    }
    else {
      elem.innerHTML = choice;
    }
  });
}
