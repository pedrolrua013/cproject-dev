(() => {
  const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
  const reduz = matchMedia('(prefers-reduced-motion: reduce)').matches;
  window.dataLayer = window.dataLayer || [];

  // nav
  const nav = $('.nav');
  const onScroll = () => nav && nav.classList.toggle('s', scrollY > 12);
  addEventListener('scroll', onScroll, {passive: true}); onScroll();
  const burg = $('.burg');
  if (burg) {
    burg.addEventListener('click', () => { const o = nav.classList.toggle('open'); burg.setAttribute('aria-expanded', o); });
    $$('.nav ul a').forEach(a => a.addEventListener('click', () => { nav.classList.remove('open'); burg.setAttribute('aria-expanded', 'false'); }));
    addEventListener('keydown', e => { if (e.key === 'Escape' && nav.classList.contains('open')) { nav.classList.remove('open'); burg.setAttribute('aria-expanded', 'false'); burg.focus(); } });
  }

  // reveal
  if ('IntersectionObserver' in window && !reduz) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('on'); io.unobserve(e.target); } }), {rootMargin: '0px 0px -8% 0px'});
    $$('.rv').forEach(el => io.observe(el));
  } else $$('.rv').forEach(el => el.classList.add('on'));

  // whatsapp: evento
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href*="wa.me"]');
    if (a) dataLayer.push({event: 'whatsapp_click', page: location.pathname, origem: a.dataset.origem || 'link'});
  });

  // hero: constelação
  const cv = $('#hero-cv');
  if (cv) {
    const ctx = cv.getContext('2d');
    let W, H, dpr, pts = [], raf = null, visivel = true, mx = -999, my = -999;
    const cores = ['201,168,106', '100,255,218'];
    function montar() {
      dpr = Math.min(devicePixelRatio || 1, 2);
      W = cv.clientWidth; H = cv.clientHeight;
      cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const n = Math.round(Math.min(110, Math.max(36, W * H / 14000)));
      pts = Array.from({length: n}, (_, i) => ({
        x: W * (0.35 + Math.random() * 0.65), y: Math.random() * H,
        vx: (Math.random() - .5) * .22, vy: (Math.random() - .5) * .22,
        r: i % 9 === 0 ? 2.6 : 1.2 + Math.random() * 1.1, c: i % 5 === 0 ? 1 : 0
      }));
      if (W < 640) pts.forEach(p => p.x = Math.random() * W);
    }
    function quadro() {
      ctx.clearRect(0, 0, W, H);
      const lim = W < 640 ? 90 : 130;
      for (let i = 0; i < pts.length; i++) {
        const a = pts[i];
        for (let j = i + 1; j < pts.length; j++) {
          const b = pts[j], dx = a.x - b.x, dy = a.y - b.y, d = Math.hypot(dx, dy);
          if (d < lim) { ctx.strokeStyle = `rgba(${cores[a.c && b.c ? 1 : 0]},${(1 - d / lim) * .28})`; ctx.lineWidth = .8; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); }
        }
        const dm = Math.hypot(a.x - mx, a.y - my);
        if (dm < 160) { ctx.strokeStyle = `rgba(100,255,218,${(1 - dm / 160) * .35})`; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(mx, my); ctx.stroke(); }
      }
      for (const p of pts) { ctx.fillStyle = `rgba(${cores[p.c]},${p.r > 2 ? .95 : .7})`; ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.283); ctx.fill(); }
    }
    function passo() {
      for (const p of pts) { p.x += p.vx; p.y += p.vy; if (p.x < 0 || p.x > W) p.vx *= -1; if (p.y < 0 || p.y > H) p.vy *= -1; }
      quadro(); raf = visivel ? requestAnimationFrame(passo) : null;
    }
    montar(); quadro();
    if (!reduz) {
      new IntersectionObserver(([e]) => { visivel = e.isIntersecting; if (visivel && !raf) raf = requestAnimationFrame(passo); }).observe(cv);
      document.addEventListener('visibilitychange', () => { visivel = !document.hidden; if (visivel && !raf) raf = requestAnimationFrame(passo); });
      cv.parentElement.addEventListener('pointermove', e => { const r = cv.getBoundingClientRect(); mx = e.clientX - r.left; my = e.clientY - r.top; }, {passive: true});
      cv.parentElement.addEventListener('pointerleave', () => { mx = my = -999; });
      raf = requestAnimationFrame(passo);
    }
    let t; addEventListener('resize', () => { clearTimeout(t); t = setTimeout(() => { montar(); quadro(); }, 200); });
  }

  // planos: abas
  const pl = $('.pl');
  if (pl) {
    pl.classList.add('js');
    const tabs = [...pl.querySelectorAll('[role=tab]')], panes = [...pl.querySelectorAll('[role=tabpanel]')];
    const abrir = (t, foco) => {
      tabs.forEach(x => { const on = x === t; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1; });
      panes.forEach(p => { p.hidden = p.id !== t.getAttribute('aria-controls'); });
      if (foco) t.focus();
      t.scrollIntoView({block: 'nearest', inline: 'nearest', behavior: reduz ? 'auto' : 'smooth'});
      dataLayer.push({event: 'plan_tab', aba: t.id.replace('tab-', '')});
    };
    panes.forEach((p, i) => { p.hidden = i !== 0; });
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => abrir(t));
      t.addEventListener('keydown', e => {
        const k = {ArrowRight: 1, ArrowLeft: -1}[e.key];
        if (k) { e.preventDefault(); abrir(tabs[(i + k + tabs.length) % tabs.length], true); }
        if (e.key === 'Home') { e.preventDefault(); abrir(tabs[0], true); }
        if (e.key === 'End') { e.preventDefault(); abrir(tabs[tabs.length - 1], true); }
      });
    });
  }

  // portfólio: carrossel
  const tr = $('#pft');
  if (tr) {
    const bar = $('#pfbar'), btns = $$('.pfb'), items = [...tr.children];
    const passo = () => (items[0]?.getBoundingClientRect().width || 400) + parseFloat(getComputedStyle(tr).columnGap || 16);
    const setVh = () => $$('.vp').forEach(v => v.style.setProperty('--vh', v.clientHeight + 'px'));
    const atualizar = () => {
      const max = tr.scrollWidth - tr.clientWidth, x = tr.scrollLeft;
      if (bar) { bar.style.width = Math.max(12, tr.clientWidth / tr.scrollWidth * 100) + '%'; bar.style.transform = `translateX(${max > 0 ? x / max * (tr.scrollWidth / tr.clientWidth - 1) * 100 : 0}%)`; }
      btns.forEach(b => { b.disabled = +b.dataset.dir < 0 ? x <= 2 : x >= max - 2; });
    };
    const ir = d => tr.scrollBy({left: d * passo(), behavior: reduz ? 'auto' : 'smooth'});
    btns.forEach(b => b.addEventListener('click', () => { ir(+b.dataset.dir); parar(); }));
    tr.addEventListener('scroll', atualizar, {passive: true});
    addEventListener('resize', () => { setVh(); atualizar(); });
    setVh(); atualizar();
    // avanço automático lento, pausa em interação, foco, aba oculta ou fora da tela
    let tm = null, visto = false, pausado = false;
    const tick = () => { if (pausado || !visto || document.hidden) return; const max = tr.scrollWidth - tr.clientWidth; if (tr.scrollLeft >= max - 2) tr.scrollTo({left: 0, behavior: 'smooth'}); else ir(1); };
    const iniciar = () => { if (!reduz && !tm) tm = setInterval(tick, 4200); };
    const parar = () => { clearInterval(tm); tm = null; };
    ['pointerenter', 'focusin', 'touchstart'].forEach(ev => tr.addEventListener(ev, () => { pausado = true; }, {passive: true}));
    ['pointerleave', 'focusout'].forEach(ev => tr.addEventListener(ev, () => { pausado = false; }));
    if ('IntersectionObserver' in window) new IntersectionObserver(([e]) => { visto = e.isIntersecting; visto ? iniciar() : parar(); }, {threshold: .35}).observe(tr);
    tr.addEventListener('click', e => { const a = e.target.closest('a'); if (a) dataLayer.push({event: 'portfolio_click', site: a.href}); });
  }

  // formulário -> WhatsApp
  const fm = $('#fm');
  if (fm) fm.addEventListener('submit', e => {
    e.preventDefault();
    const msg = $('#fmsg'); msg.className = 'fmsg'; msg.textContent = '';
    if (fm.querySelector('[name=site]').value) return;
    let ok = true;
    fm.querySelectorAll('[required]').forEach(c => { const v = c.value.trim().length > 1; c.setAttribute('aria-invalid', !v); if (!v) ok = false; });
    if (!ok) { msg.className = 'fmsg err'; msg.textContent = 'Preencha nome, interesse e uma linha sobre o que você precisa.'; fm.querySelector('[aria-invalid=true]').focus(); return; }
    const d = Object.fromEntries(new FormData(fm));
    const txt = `Olá! Vim pelo site da CProject.\n\nNome: ${d.nome}\n${d.empresa ? 'Empresa: ' + d.empresa + '\n' : ''}Interesse: ${d.interesse}\n\n${d.mensagem}`;
    const url = 'https://wa.me/5513974177986?text=' + encodeURIComponent(txt);
    dataLayer.push({event: 'whatsapp_click', page: location.pathname, origem: 'formulario'});
    const w = window.open(url, '_blank', 'noopener');
    msg.innerHTML = w ? 'Abrimos o WhatsApp com sua mensagem pronta. É só enviar.' : 'Se o WhatsApp não abriu, <a href="' + url + '" target="_blank" rel="noopener">toque aqui</a> ou escreva para bruno.perescp@gmail.com.';
  });
})();
