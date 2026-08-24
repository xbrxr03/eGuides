// Grove Editorial — copy-to-clipboard for .code-block / .copy-btn pairs.
// Usage: <div class="code-block"><button class="copy-btn">Copy</button><pre>...</pre></div>
(function () {
  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta);
  }

  function showCopied(btn) {
    var original = btn.textContent;
    btn.textContent = 'Copied!';
    btn.classList.add('copied');
    setTimeout(function () {
      btn.textContent = original;
      btn.classList.remove('copied');
    }, 1500);
  }

  document.addEventListener('click', function (e) {
    var btn = e.target.closest('.copy-btn');
    if (!btn) return;
    var block = btn.closest('.code-block');
    var codeEl = block && block.querySelector('pre');
    if (!codeEl) return;
    var text = codeEl.innerText;

    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(
        function () { showCopied(btn); },
        function () { fallbackCopy(text); showCopied(btn); }
      );
    } else {
      fallbackCopy(text);
      showCopied(btn);
    }
  });
})();
