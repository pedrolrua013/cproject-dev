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
    // escalonamento entre irmãos e limpeza após a entrada (libera o hover)
    $$('.rv').forEach(el => { const irm = [...el.parentElement.children].filter(c => c.classList.contains('rv')); const i = irm.indexOf(el); if (i > 0) el.style.setProperty('--d', Math.min(i, 6) * 0.08 + 's'); });
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { const el = e.target; el.classList.add('on'); io.unobserve(el); setTimeout(() => { el.classList.remove('rv', 'on'); el.style.removeProperty('--d'); }, 1500); } }), {rootMargin: '0px 0px -8% 0px'});
    $$('.rv').forEach(el => io.observe(el));
  } else $$('.rv').forEach(el => el.classList.add('on'));

  // luz que segue o cursor
  if (matchMedia('(hover:hover)').matches) {
    document.addEventListener('pointermove', e => {
      const c = e.target.closest('.card,.plan,.pack,.pp');
      if (!c) return;
      const r = c.getBoundingClientRect();
      c.style.setProperty('--mx', (e.clientX - r.left) + 'px'); c.style.setProperty('--my', (e.clientY - r.top) + 'px');
    }, {passive: true});
  }

  // paralaxe dos brilhos de fundo
  if (!reduz) {
    const secs = $$('.sec'); let tk = false;
    const par = () => { tk = false; const vh = innerHeight; secs.forEach(s => { const r = s.getBoundingClientRect(); if (r.bottom < -200 || r.top > vh + 200) return; const p = ((r.top + r.height / 2) - vh / 2) / (vh / 2 + r.height / 2); s.style.setProperty('--p', Math.max(-1, Math.min(1, p)).toFixed(3)); }); };
    addEventListener('scroll', () => { if (!tk) { tk = true; requestAnimationFrame(par); } }, {passive: true}); par();
  }

  // vídeos: carregam só perto da tela e pausam fora dela
  const vids = $$('video[data-src]');
  if (vids.length && 'IntersectionObserver' in window) {
    const vo = new IntersectionObserver(es => es.forEach(e => { const v = e.target;
      if (e.isIntersecting) { if (!v.src) v.src = v.dataset.src; if (!reduz) v.play().catch(() => {}); } else v.pause(); }), {rootMargin: '200px'});
    vids.forEach(v => vo.observe(v));
  }

  // hero: vídeo carrega depois da página (não pesa no carregamento)
  const hv = $('#hv');
  if (hv) {
    const mob = matchMedia('(max-width:640px)').matches;
    if (mob) hv.poster = hv.dataset.pm;
    if (reduz) hv.poster = hv.dataset.still;
    else {
      const go = () => { hv.src = mob ? hv.dataset.m : hv.dataset.d; hv.play().catch(() => {}); };
      const idle = () => ('requestIdleCallback' in window ? requestIdleCallback(go, {timeout: 2500}) : setTimeout(go, 800));
      document.readyState === 'complete' ? idle() : addEventListener('load', idle, {once: true});
      new IntersectionObserver(([e]) => { if (!hv.src) return; e.isIntersecting ? hv.play().catch(() => {}) : hv.pause(); }).observe(hv);
    }
  }

  // linha do tempo: preenche ao passar pelas etapas (desktop) ou com a rolagem (celular)
  $$('[data-tl]').forEach(tl => {
    const st = [...tl.querySelectorAll('.tl-s')], n = st.length;
    const marcar = k => { tl.style.setProperty('--f', n > 1 ? Math.max(0, k) / (n - 1) : 1); st.forEach((s, i) => { s.classList.toggle('done', i <= k); s.classList.toggle('now', i === k); }); };
    marcar(-1);
    const vertical = () => matchMedia('(max-width:820px)').matches;
    st.forEach((s, i) => { s.addEventListener('pointerenter', () => { if (!vertical()) marcar(i); }); s.addEventListener('focus', () => marcar(i)); });
    const rolar = () => {
      if (!vertical()) return;
      const r = tl.getBoundingClientRect(), alvo = innerHeight * .62;
      const f = Math.max(0, Math.min(1, (alvo - r.top - 32) / Math.max(1, r.height - 64)));
      tl.style.setProperty('--f', f);
      st.forEach((s, i) => { const on = s.getBoundingClientRect().top + 32 < alvo; s.classList.toggle('done', on); });
      const ult = st.filter(s => s.classList.contains('done')).pop(); st.forEach(s => s.classList.toggle('now', s === ult));
    };
    addEventListener('scroll', () => requestAnimationFrame(rolar), {passive: true}); rolar();
    if (reduz) marcar(n - 1);
  });

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
    const centro = el => el.offsetLeft - (tr.clientWidth - el.offsetWidth) / 2;
    const marcar = () => { const m = tr.scrollLeft + tr.clientWidth / 2; let best = items[0], d = 1e9; items.forEach(it => { const c = Math.abs(it.offsetLeft + it.offsetWidth / 2 - m); if (c < d) { d = c; best = it; } }); items.forEach(it => it.classList.toggle('cur', it === best)); };
    if (items[1]) tr.scrollLeft = centro(items[1]);
    marcar();
    tr.addEventListener('scroll', () => requestAnimationFrame(marcar), {passive: true});
    const setVh = () => $$('.vp').forEach(v => v.style.setProperty('--vh', v.clientHeight + 'px'));
    const atualizar = () => {
      const max = tr.scrollWidth - tr.clientWidth, x = tr.scrollLeft;
      if (bar) { bar.style.width = Math.max(12, tr.clientWidth / tr.scrollWidth * 100) + '%'; bar.style.transform = `translateX(${max > 0 ? x / max * (tr.scrollWidth / tr.clientWidth - 1) * 100 : 0}%)`; }
      btns.forEach(b => { b.disabled = +b.dataset.dir < 0 ? x <= 2 : x >= max - 2; });
    };
    const ir = d => tr.scrollBy({left: d * passo(), behavior: reduz ? 'auto' : 'smooth'});
    btns.forEach(b => b.addEventListener('click', () => { ir(+b.dataset.dir); parar(); }));
    tr.addEventListener('scroll', atualizar, {passive: true});
    addEventListener('resize', () => { setVh(); atualizar(); const c = tr.querySelector('.cur'); if (c) tr.scrollLeft = centro(c); });
    setVh(); atualizar();
    // avanço automático lento, pausa em interação, foco, aba oculta ou fora da tela
    let tm = null, visto = false, pausado = false;
    const tick = () => { if (pausado || !visto || document.hidden) return; const max = tr.scrollWidth - tr.clientWidth; if (tr.scrollLeft >= max - 2) tr.scrollTo({left: centro(items[0]), behavior: 'smooth'}); else ir(1); };
    const iniciar = () => { if (!reduz && !tm) tm = setInterval(tick, 4200); };
    const parar = () => { clearInterval(tm); tm = null; };
    ['pointerenter', 'focusin', 'touchstart'].forEach(ev => tr.addEventListener(ev, () => { pausado = true; }, {passive: true}));
    ['pointerleave', 'focusout'].forEach(ev => tr.addEventListener(ev, () => { pausado = false; }));
    if ('IntersectionObserver' in window) new IntersectionObserver(([e]) => { visto = e.isIntersecting; visto ? iniciar() : parar(); }, {threshold: .35}).observe(tr);
    tr.addEventListener('click', e => { const a = e.target.closest('a'); if (a) dataLayer.push({event: 'portfolio_click', site: a.href}); });
  }

  // formulário de diagnóstico -> e-mail (fallback: WhatsApp)
  const fm = $('#fm');
  if (fm) fm.addEventListener('submit', async e => {
    e.preventDefault();
    const msg = $('#fmsg'), bt = fm.querySelector('button[type=submit]');
    msg.className = 'fmsg'; msg.textContent = '';
    if (fm.querySelector('[name=site]').value) return;
    let ok = true;
    fm.querySelectorAll('[required]').forEach(c => {
      let v = c.value.trim().length > 1;
      if (c.name === 'whatsapp') v = c.value.replace(/\D/g, '').length >= 10;
      c.setAttribute('aria-invalid', !v); if (!v) ok = false;
    });
    if (!ok) { msg.className = 'fmsg err'; msg.textContent = 'Preencha nome, empresa, segmento, um WhatsApp com DDD e o que você busca.'; fm.querySelector('[aria-invalid=true]').focus(); return; }
    const d = Object.fromEntries(new FormData(fm));
    const txt = `Olá! Vim pelo site da CProject Lab e quero o diagnóstico gratuito.\n\nNome: ${d.nome}\nEmpresa: ${d.empresa}\nSegmento: ${d.segmento}\nWhatsApp: ${d.whatsapp}\n\n${d.busca}`;
    const wurl = 'https://wa.me/5513974177986?text=' + encodeURIComponent(txt);
    bt.disabled = true; msg.textContent = 'Enviando...';
    try {
      const r = await fetch('/api/diagnostico', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(d)});
      if (!r.ok) throw new Error(r.status);
      dataLayer.push({event: 'generate_lead', origem: 'diagnostico', segmento: d.segmento});
      fm.reset(); msg.className = 'fmsg ok';
      msg.textContent = 'Recebemos sua solicitação! Em breve entramos em contato pelo WhatsApp para marcar a entrevista inicial.';
    } catch (err) {
      msg.className = 'fmsg err';
      msg.innerHTML = 'Não conseguimos enviar agora. <a href="' + wurl + '" target="_blank" rel="noopener">Envie pelo WhatsApp</a> ou escreva para contato@cproject.com.br.';
    } finally { bt.disabled = false; }
  });
})();
/* CProject Lab · experiência imersiva do topo: os símbolos da marca flutuam em profundidade,
   reagem ao cursor e à rolagem, e o isotipo <=/> se monta no centro da cena. */
(() => {
  const cv = document.querySelector('canvas[data-lab]');
  if (!cv || !cv.getContext) return;
  const reduz = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const ctx = cv.getContext('2d');
  const SYM = {"asterisco": "M -23.4,0 L -50,-9.4 L -31.8,-39.6 L -13.5,-23.0 L -19.0,-48.2 L 18.7,-48.2 L 12.9,-22.8 L 31.6,-39.6 L 50,-9.1 L 23.7,0 L 49.7,9.4 L 31.6,39.8 L 12.9,22.8 L 18.7,48.2 L -19.2,48.2 L -13.5,23.0 L -31.8,39.6 L -50,9.4 Z M -23.4,0", "chevrons": "M -8.4,0 L -49.2,40.8 L -40.0,50 L 9.8,0.0 L 9.8,-0.0 L 9.8,-0.0 L -40.0,-50 L -49.2,-40.8 Z M -8.4,0 M 30.9,0 L -9.8,40.8 L -0.7,50 L 49.2,0.0 L 49.2,-0.0 L 49.2,-0.0 L -0.7,-50 L -9.8,-40.8 Z M 30.9,0", "frasco": "M 27.2,44.2 C 26.6,44.7 25.5,45.7 24.5,45.7 L -24.6,45.7 C -26.3,45.1 -28.5,43.8 -28.9,40.8 C -29.4,37.8 -28.4,34.9 -27.2,31.8 L -23.9,23.0 L -8.6,-16.9 L -8.5,-16.9 L -8.5,-40.1 L -11.2,-40.1 C -12.4,-40.3 -13.3,-41.4 -13.4,-42.8 C -13.4,-43.6 -13.1,-44.6 -12.5,-45.1 C -12.2,-45.5 -11.9,-45.6 -11.5,-45.6 L 11.7,-45.7 C 12.9,-45.3 13.6,-44.1 13.6,-42.8 C 13.4,-41.6 12.8,-40.2 11.5,-40.2 L 8.5,-40.1 L 8.5,-17.0 L 8.5,-16.9 L 21.0,15.7 L 27.2,31.9 C 28.2,34.5 29.0,37.2 29.0,39.6 C 29.0,41.4 28.5,43.0 27.2,44.2 M 32.7,38.3 L 32.8,38.2 L 32.3,35.0 L 32.2,34.9 L 32.2,34.8 L 30.9,30.8 L 21.6,6.6 L 12.3,-17.7 L 12.3,-29.3 L 12.3,-30.5 L 12.3,-36.0 C 15.2,-36.6 17.3,-39.5 17.3,-43.0 C 17.3,-44.7 16.8,-46.4 15.8,-47.7 C 14.7,-49.1 13.3,-49.9 11.7,-49.9 L -11.8,-50 L -11.9,-50 L -11.9,-49.9 C -14.3,-49.4 -16.2,-47.5 -16.9,-45.0 C -17.4,-42.8 -17.1,-40.5 -15.9,-38.7 C -15.0,-37.4 -13.7,-36.4 -12.3,-36.1 L -12.2,-17.9 L -22.7,9.4 L -30.8,30.6 C -32.8,35.7 -34.2,41.6 -30.5,46.5 C -28.9,48.4 -27.0,49.5 -24.7,49.9 L -24.7,50 L 24.9,49.9 L 25.0,49.9 C 27.8,49.2 30.1,47.4 31.6,44.9 C 31.6,44.8 31.6,44.8 31.6,44.8 C 31.7,44.7 31.8,44.6 31.8,44.4 C 31.8,44.3 31.8,44.1 31.9,44.0 C 32.0,43.8 32.0,43.7 32.1,43.5 L 32.7,41.7 L 32.6,41.2 C 32.6,41.2 32.6,41.1 32.6,41.0 C 32.6,40.9 32.6,40.9 32.6,40.9 L 32.7,40.8 L 32.8,38.9 C 32.8,38.7 32.8,38.6 32.7,38.5 C 32.7,38.4 32.7,38.3 32.7,38.3 M 21.1,42.1 C 21.0,42.1 20.8,42.2 20.7,42.3 C 20.2,42.5 19.7,42.8 19.0,42.8 L -19.3,42.8 L -19.3,42.8 C -22.5,42.2 -24.9,38.9 -24.6,35.6 L -24.4,33.9 C -24.3,32.1 -23.7,30.6 -23.0,29.0 C -22.9,28.6 -22.7,28.3 -22.6,27.9 L -13.9,5.0 L -6.2,5.0 C -3.7,5.0 -1.2,4.0 1.1,3.0 L 1.5,2.8 L 6.2,0.8 C 7.3,0.3 8.5,0.1 10.0,0.2 L 12.0,0.4 L 17.3,14.2 L 23.6,30.9 C 25.2,34.9 25.0,40.1 21.1,42.1 M 5.9,-12.4 L -1.3,-12.4 L -1.3,-16.7 L 5.9,-16.7 Z M 5.9,-12.4 M 5.9,-24.9 L 5.8,-20.6 L -1.3,-20.7 L -1.3,-24.9 Z M 5.9,-24.9 M 5.9,-29.6 L -1.3,-29.6 L -1.3,-33.8 L 5.8,-33.7 Z M 5.9,-29.6", "igual": "M -50,-42.4 L -50,-12.3 L 50,-12.3 L 50,-42.4 Z M -50,-42.4 M -50,12.3 L -50,42.4 L 50,42.4 L 50,12.3 Z M -50,12.3", "quadrado": "M 50,41.7 L -50,41.7 L -50,-41.7 L 50,-41.7 Z M 50,41.7", "barra": "M 19.1,-46.6 L -6.7,50 L -19.1,46.6 L 6.7,-50 Z M 19.1,-46.6"};
  const ISO = ["M -77.6,0 L -27.6,49.9 L -38.8,61.1 L -100,0.0 L -99.9,0 L -99.9,-0.0 L -38.8,-61.1 L -27.6,-49.9 Z M -77.6,0", "M -42.7,-17.9 L -42.7,-5.2 L -0.5,-5.2 L -0.5,-17.9 Z M -42.7,-17.9", "M -42.7,5.1 L -42.7,17.9 L -0.5,17.9 L -0.5,5.1 Z M -42.7,5.1", "M 48.9,-57.0 L 17.3,60.9 L 2.1,56.8 L 33.7,-61.1 Z M 48.9,-57.0", "M 100,-19.2 L 60.6,20.1 L 49.4,8.9 L 77.6,-19.2 L 49.4,-47.4 L 60.6,-58.6 L 99.8,-19.3 L 99.8,-19.3 Z M 100,-19.2"];
  const P = Object.fromEntries(Object.entries(SYM).map(([k, d]) => [k, new Path2D(d)]));
  const IP = ISO.map(d => new Path2D(d));
  const COR = ['195,177,215', '233,243,228', '150,122,224'];
  const ISO_PAR = [-26, -12, -12, 10, 26];
  let W = 0, H = 0, dpr = 1, itens = [], mx = 0, my = 0, tx = 0, ty = 0, px = -1e4, py = -1e4, sp = 0, raf = null, vis = true, t0 = performance.now();
  const mob = () => W < 760;

  function montar() {
    dpr = Math.min(devicePixelRatio || 1, 2);
    W = cv.clientWidth; H = cv.clientHeight;
    cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
    const ks = Object.keys(P), n = mob() ? 20 : 42;
    itens = Array.from({length: n}, (_, i) => ({
      k: ks[i % ks.length], x: Math.random() * 2.4 - 1.2, y: Math.random() * 2 - 1, z: Math.random(),
      r: Math.random() * 6.283, vr: (Math.random() - .5) * .006, vx: (Math.random() - .5) * .0007, vy: (Math.random() - .5) * .0007,
      c: i % 6 === 0 ? 1 : i % 3 === 0 ? 2 : 0, s: .55 + Math.random() * .75, ox: 0, oy: 0
    }));
  }

  function iso(t) {
    const m = mob(), sz = m ? Math.min(W * .62, 260) : Math.min(W * .34, H * .5, 430);
    const cx = m ? W * .5 : W * .74, cy = m ? H * .2 : H * .5;
    const k = sz / 200, ent = reduz ? 1 : Math.min(1, t / 1800), e = 1 - Math.pow(1 - ent, 3);
    const respira = reduz ? 0 : Math.sin(t / 1400) * .015;
    ctx.save();
    ctx.globalAlpha = (m ? .34 : .95) * e;
    const g = ctx.createLinearGradient(cx - sz / 2, cy - sz / 2, cx + sz / 2, cy + sz / 2);
    g.addColorStop(0, '#E9F3E4'); g.addColorStop(.45, '#C3B1D7'); g.addColorStop(1, '#8F72DD');
    ctx.fillStyle = g;
    ctx.shadowColor = 'rgba(150,122,224,.55)'; ctx.shadowBlur = m ? 18 : 34;
    IP.forEach((p, i) => {
      const sep = (1 - e) * (i - 2) * 70, par = ISO_PAR[i];
      ctx.save();
      ctx.translate(cx + sep + mx * par, cy + my * par * .6 - sp * (40 + i * 18));
      ctx.scale(k * (1 + respira), k * (1 + respira));
      ctx.fill(p);
      ctx.restore();
    });
    ctx.restore();
  }

  function quadro(t) {
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    const base = Math.min(W, H) * (mob() ? .07 : .055);
    const lista = itens.map(o => ({o, z: o.z + sp * .9})).filter(a => a.z < 1.25).sort((a, b) => a.z - b.z);
    for (const {o, z} of lista) {
      const f = .3 + z * 1.15;
      let sx = W / 2 + o.x * W * .5 * (.7 + z * .5) + mx * z * 60;
      let sy = H / 2 + o.y * H * .5 * (.7 + z * .5) + my * z * 40;
      const dx = sx - px, dy = sy - py, d = Math.hypot(dx, dy);
      if (d < 150 && !reduz) { const fz = (1 - d / 150) * 26; o.ox += (dx / (d || 1)) * fz * .12; o.oy += (dy / (d || 1)) * fz * .12; }
      o.ox *= .94; o.oy *= .94;
      sx += o.ox; sy += o.oy;
      const tam = base * f * o.s, a = Math.max(0, Math.min(1, (.1 + z * .55) * (z > 1 ? (1.25 - z) / .25 : 1)));
      const perto = d < 150 ? (1 - d / 150) * .35 : 0;
      ctx.save();
      ctx.translate(sx, sy); ctx.rotate(o.r); ctx.scale(tam / 100, tam / 100);
      ctx.fillStyle = `rgba(${COR[o.c]},${Math.min(1, a + perto)})`;
      ctx.fill(P[o.k]);
      ctx.restore();
    }
    iso(t);
  }

  function passo(now) {
    const t = now - t0;
    mx += (tx - mx) * .05; my += (ty - my) * .05;
    for (const o of itens) { o.x += o.vx; o.y += o.vy; o.r += o.vr; if (o.x > 1.3) o.x = -1.3; if (o.x < -1.3) o.x = 1.3; if (o.y > 1.1) o.y = -1.1; if (o.y < -1.1) o.y = 1.1; }
    quadro(t);
    raf = vis ? requestAnimationFrame(passo) : null;
  }

  montar();
  if (reduz) { quadro(99999); addEventListener('resize', () => { montar(); quadro(99999); }); return; }
  const alvo = cv.parentElement;
  alvo.addEventListener('pointermove', e => { const r = cv.getBoundingClientRect(); px = e.clientX - r.left; py = e.clientY - r.top; tx = (px / W - .5) * 2; ty = (py / H - .5) * 2; }, {passive: true});
  alvo.addEventListener('pointerleave', () => { px = py = -1e4; tx = ty = 0; });
  addEventListener('scroll', () => { sp = Math.max(0, Math.min(1, scrollY / (H || 1))); }, {passive: true});
  new IntersectionObserver(([e]) => { vis = e.isIntersecting; if (vis && !raf) raf = requestAnimationFrame(passo); }).observe(cv);
  document.addEventListener('visibilitychange', () => { vis = !document.hidden; if (vis && !raf) raf = requestAnimationFrame(passo); });
  let tr; addEventListener('resize', () => { clearTimeout(tr); tr = setTimeout(montar, 150); });
  raf = requestAnimationFrame(passo);
})();
(() => {
  const m = document.querySelector('[data-mani]');
  if (!m) return;
  const ws = [...m.querySelectorAll('.mani-w span')];
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) { ws.forEach(w => w.classList.add('on')); return; }
  const upd = () => { const r = m.getBoundingClientRect(), vh = innerHeight; const p = (vh - r.top) / (vh * .9); ws.forEach((w, i) => w.classList.toggle('on', p > .35 + i * .18)); };
  addEventListener('scroll', upd, {passive: true}); upd();
})();
