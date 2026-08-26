/* Three states: explicit light, explicit dark, and system (no data-theme set).
   The palette for all three already exists in style.css; this only sets the flag. */
(function () {
  var root = document.documentElement, KEY = 'gila-theme';
  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) { /* private mode, blocked storage */ }
  if (saved === 'light' || saved === 'dark') root.setAttribute('data-theme', saved);

  function label(btn) {
    var t = root.getAttribute('data-theme');
    btn.textContent = t === 'dark' ? 'Dark' : t === 'light' ? 'Light' : 'System';
    btn.setAttribute('aria-label', 'Colour theme: ' + btn.textContent + '. Click to change.');
  }
  document.addEventListener('DOMContentLoaded', function () {
    var btn = document.querySelector('.theme-toggle');
    if (!btn) return;
    label(btn);
    btn.addEventListener('click', function () {
      var t = root.getAttribute('data-theme');
      var next = t === 'light' ? 'dark' : t === 'dark' ? null : 'light';
      if (next) { root.setAttribute('data-theme', next); } else { root.removeAttribute('data-theme'); }
      try { next ? localStorage.setItem(KEY, next) : localStorage.removeItem(KEY); } catch (e) {}
      label(btn);
    });
  });
})();
