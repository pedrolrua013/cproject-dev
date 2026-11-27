/* Tela de carregamento: aparece só na primeira página da visita (sessão do navegador).
   Some quando a página termina de carregar, com pelo menos 1,75 s para o frasco encher. */
(function () {
  var h = document.documentElement, k = "cp-ld";
  try { if (sessionStorage.getItem(k)) { h.classList.add("ld-off"); return } sessionStorage.setItem(k, "1") } catch (e) { }
  h.classList.add("ld-on");
  var t0 = Date.now(), MIN = 1750, MAX = 4000, feito = false;
  function fim() {
    if (feito) return; feito = true;
    setTimeout(function () {
      h.classList.add("ld-fim");
      setTimeout(function () { h.classList.remove("ld-on"); var el = document.getElementById("ld"); if (el) el.remove() }, 700);
    }, Math.max(0, MIN - (Date.now() - t0)));
  }
  if (document.readyState === "complete") fim(); else window.addEventListener("load", fim);
  setTimeout(fim, MAX);
})();
