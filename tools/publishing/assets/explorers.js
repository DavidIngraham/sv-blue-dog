// Shared with the Markdown import: local Pages builds use their own data assets.
import {renderExplorer} from './design-explorer.js';
import {renderRiskExplorer} from './risk-explorer.js';

for (const [kind, render, path] of [
  ['design-explorer', renderExplorer, './design-explorer/design.json'],
  ['risk-explorer', renderRiskExplorer, './risk/risks.json'],
]) {
  for (const code of document.querySelectorAll(`code.language-${kind}`)) {
    const root = document.createElement('section');
    root.setAttribute('aria-label', kind === 'design-explorer' ? 'Explore candidate geometry' : 'Explore project risks');
    root.textContent = 'Loading interactive view…';
    code.parentElement.replaceWith(root);
    try {
      await render(root, new URL(path, import.meta.url));
      root.dataset.explorer = 'ready';
    } catch (error) {
      root.textContent = 'The interactive view could not load. Reload this page to try again.';
      root.dataset.explorer = 'failed';
      console.error(error);
    }
  }
}
