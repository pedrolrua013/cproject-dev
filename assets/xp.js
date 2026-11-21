/* CProject Lab · O experimento: o frasco da marca guiado pela rolagem.
   Líquido com física simples, bolhas, reação que solta os símbolos da marca e camadas de profundidade. */
(() => {
  const sec = document.querySelector('[data-xp]');
  if (!sec) return;
  const cv = sec.querySelector('canvas'), ctx = cv.getContext && cv.getContext('2d');
  if (!ctx) return;
  const reduz = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const steps = [...sec.querySelectorAll('.xp-steps li')];
  const pctEl = sec.querySelector('.xp-pct b');
  const SP = Object.values({"asterisco": "M -23.4,0 L -50,-9.4 L -31.8,-39.6 L -13.5,-23.0 L -19.0,-48.2 L 18.7,-48.2 L 12.9,-22.8 L 31.6,-39.6 L 50,-9.1 L 23.7,0 L 49.7,9.4 L 31.6,39.8 L 12.9,22.8 L 18.7,48.2 L -19.2,48.2 L -13.5,23.0 L -31.8,39.6 L -50,9.4 Z M -23.4,0", "chevrons": "M -8.4,0 L -49.2,40.8 L -40.0,50 L 9.8,0.0 L 9.8,-0.0 L 9.8,-0.0 L -40.0,-50 L -49.2,-40.8 Z M -8.4,0 M 30.9,0 L -9.8,40.8 L -0.7,50 L 49.2,0.0 L 49.2,-0.0 L 49.2,-0.0 L -0.7,-50 L -9.8,-40.8 Z M 30.9,0", "igual": "M -50,-42.4 L -50,-12.3 L 50,-12.3 L 50,-42.4 Z M -50,-42.4 M -50,12.3 L -50,42.4 L 50,42.4 L 50,12.3 Z M -50,12.3", "quadrado": "M 50,41.7 L -50,41.7 L -50,-41.7 L 50,-41.7 Z M 50,41.7", "barra": "M 19.1,-46.6 L -6.7,50 L -19.1,46.6 L 6.7,-50 Z M 19.1,-46.6"}).map(d => new Path2D(d));
  const MARKS = [.2, .44, .68, .9];
  const COR = [[195,177,215],[143,114,221],[178,154,232],[233,243,228]];
  const TONS = ['195,177,215', '233,243,228', '143,114,221'];
  const R = Math.random, cl = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
  let W = 0, H = 0, dpr = 1, mob = false, cx = 0, cy = 0, S = 0;
  let p = 0, f = 0, fv = 0, tilt = 0, tiltT = 0, lastTilt = 0, sl = 0, slv = 0, lastY = scrollY, sv = 0;
  let mx = 0, my = 0, tmx = 0, tmy = 0, flash = 0, fim = false, ativo = -1, pctV = -1, acc = 0, accE = 0;
  let bub = [], emi = [], far = [], near = [], sprites = [], raf = null, vis = false, t = 0;
  let inner, wall, lip;

  function cor(k) {
    const x = cl(k) * 3, i = Math.min(2, Math.floor(x)), u = x - i, a = COR[i], b = COR[i + 1];
    return [0, 1, 2].map(j => Math.round(a[j] + (b[j] - a[j]) * u)).join(',');
  }
  // contorno do frasco (erlenmeyer), em unidades de S, origem no centro
  function geo() {
    const k = S, P = (x, y) => [x * k, y * k];
    wall = new Path2D();
    wall.moveTo(...P(-.115, -.44)); wall.lineTo(...P(-.115, -.17)); wall.lineTo(...P(-.385, .40));
    wall.quadraticCurveTo(...P(-.42, .475), ...P(-.31, .475)); wall.lineTo(...P(.31, .475));
    wall.quadraticCurveTo(...P(.42, .475), ...P(.385, .40)); wall.lineTo(...P(.115, -.17)); wall.lineTo(...P(.115, -.44));
    lip = new Path2D(); lip.roundRect ? lip.roundRect(-.17 * k, -.5 * k, .34 * k, .06 * k, .022 * k) : lip.rect(-.17 * k, -.5 * k, .34 * k, .06 * k);
    const d = .018;
    inner = new Path2D();
    inner.moveTo(...P(-.115 + d, -.44)); inner.lineTo(...P(-.115 + d, -.17 + d * .5)); inner.lineTo(...P(-.385 + d * 1.1, .40));
    inner.quadraticCurveTo(...P(-.42 + d * 1.3, .475 - d), ...P(-.31 + d * .5, .475 - d)); inner.lineTo(...P(.31 - d * .5, .475 - d));
    inner.quadraticCurveTo(...P(.42 - d * 1.3, .475 - d), ...P(.385 - d * 1.1, .40)); inner.lineTo(...P(.115 - d, -.17 + d * .5)); inner.lineTo(...P(.115 - d, -.44)); inner.closePath();
  }
  const meia = y => y < -.17 ? .097 : .097 + (.367 - .097) * cl((y + .17) / .57);
  const nivel = k => .457 - (.457 + .3) * Math.pow(cl(k), .9);
  const sup = (xn, L) => L + sl * xn * .9 + Math.sin(xn * 9 + t * 2.2) * .006 + Math.sin(xn * 17 - t * 3.3) * .003 + sl * .15 * Math.sin(xn * 6 + t * 5);

  function montar() {
    dpr = Math.min(devicePixelRatio || 1, mob ? 1.5 : 2);
    W = cv.clientWidth; H = cv.clientHeight; mob = W < 760;
    cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
    if (mob) { cx = W * .47; cy = H * .46; S = Math.min(H * .46, W * .74); }
    else { cx = W * .67; cy = H * .53; S = Math.min(H * .74, W * .38); }
    geo();
    far = Array.from({length: mob ? 60 : 130}, () => ({x: R(), y: R(), z: .2 + R() * .8}));
    near = Array.from({length: mob ? 5 : 8}, (_, i) => ({s: i % SP.length, a: R() * 6.283, z0: R(), r: R() * 6.283, vr: (R() - .5) * .01}));
    sprites = SP.map(pth => {
      const c = document.createElement('canvas'); c.width = c.height = 160; const g = c.getContext('2d');
      if ('filter' in g) g.filter = 'blur(2.5px)';
      g.translate(80, 80); g.scale(1.15, 1.15); g.fillStyle = 'rgb(195,177,215)'; g.fill(pth); return c;
    });
  }

  function emitir(n, forte) {
    const ang = tilt, mxp = cx + Math.sin(ang) * .5 * S, myp = cy - Math.cos(ang) * .5 * S;
    for (let i = 0; i < n; i++) emi.push({x: mxp + (R() - .5) * S * .12, y: myp, vx: (R() - .5) * (forte ? 8 : 2.6), vy: -(forte ? 2 + R() * 6 : 1.4 + R() * 2.2), z: 0, r: R() * 6.283, vr: (R() - .5) * .05, s: Math.floor(R() * SP.length), c: TONS[Math.floor(R() * 3)], a: 0, m: forte ? 90 + R() * 60 : 150 + R() * 90});
  }

  function fundo(c) {
    // partículas distantes
    for (const o of far) {
      const x = o.x * W + mx * o.z * 30, y = (((o.y - p * o.z * .7) % 1 + 1) % 1) * H + my * o.z * 20;
      ctx.fillStyle = `rgba(195,177,215,${.12 + o.z * .3})`;
      ctx.beginPath(); ctx.arc(x, y, o.z * 1.5, 0, 6.283); ctx.fill();
    }
    // bancada em perspectiva
    const hy = cy + .5 * S, vx = cx - mx * 30, vy = hy - S * .45;
    ctx.save(); ctx.beginPath(); ctx.rect(0, hy, W, H - hy); ctx.clip();
    ctx.lineWidth = 1;
    const off = (p * 7) % 1;
    for (let i = 0; i < 16; i++) {
      const u = (i + off) / 16, y = hy + (H - hy + 40) * u * u;
      ctx.strokeStyle = `rgba(195,177,215,${.03 + u * .12})`; ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
    }
    ctx.strokeStyle = 'rgba(195,177,215,.07)';
    for (let j = -14; j <= 14; j++) { ctx.beginPath(); ctx.moveTo(vx, vy); ctx.lineTo(cx + j * W / 9, H + 40); ctx.stroke(); }
    ctx.restore();
    // brilho do líquido refletido na bancada
    ctx.save(); ctx.translate(cx, hy); ctx.scale(1, .2);
    const rg = ctx.createRadialGradient(0, 0, 0, 0, 0, S * .9);
    rg.addColorStop(0, `rgba(${c},${.12 + f * .38})`); rg.addColorStop(1, `rgba(${c},0)`);
    ctx.fillStyle = rg; ctx.beginPath(); ctx.arc(0, 0, S * .9, 0, 6.283); ctx.fill(); ctx.restore();
  }

  function frasco(c) {
    const L = nivel(f);
    ctx.save(); ctx.translate(cx + mx * 10, cy + my * 6); ctx.rotate(tilt);
    // vidro
    const gv = ctx.createLinearGradient(-.4 * S, 0, .4 * S, 0);
    gv.addColorStop(0, 'rgba(195,177,215,.10)'); gv.addColorStop(.5, 'rgba(195,177,215,.03)'); gv.addColorStop(1, 'rgba(143,114,221,.12)');
    ctx.fillStyle = gv; ctx.fill(inner);
    // líquido, sempre nivelado com o mundo
    ctx.save(); ctx.clip(inner); ctx.rotate(-tilt);
    if (f > .005) {
      const Ly = L * S, gl = ctx.createLinearGradient(0, Ly - S * .02, 0, .5 * S);
      gl.addColorStop(0, `rgba(${c},.95)`); gl.addColorStop(.3, 'rgba(143,114,221,.9)'); gl.addColorStop(1, 'rgba(59,40,111,.96)');
      ctx.fillStyle = gl; ctx.beginPath(); ctx.moveTo(-.6 * S, .8 * S);
      for (let i = 0; i <= 48; i++) { const xn = -.6 + i * 1.2 / 48; ctx.lineTo(xn * S, sup(xn, L) * S); }
      ctx.lineTo(.6 * S, .8 * S); ctx.closePath(); ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,.55)'; ctx.lineWidth = Math.max(1.5, S * .006); ctx.beginPath();
      for (let i = 0; i <= 48; i++) { const xn = -.6 + i * 1.2 / 48, y = sup(xn, L) * S; i ? ctx.lineTo(xn * S, y) : ctx.moveTo(xn * S, y); }
      ctx.stroke();
      ctx.globalCompositeOperation = 'lighter';
      const rg = ctx.createRadialGradient(0, Ly, 0, 0, Ly, S * .55);
      rg.addColorStop(0, `rgba(${c},${.1 + f * .2})`); rg.addColorStop(1, `rgba(${c},0)`);
      ctx.fillStyle = rg; ctx.fillRect(-S, -S, 2 * S, 2 * S);
      ctx.globalCompositeOperation = 'source-over';
      for (const b of bub) {
        ctx.beginPath(); ctx.arc(b.x * S, b.y * S, b.r * S, 0, 6.283);
        ctx.fillStyle = 'rgba(233,243,228,.16)'; ctx.fill();
        ctx.strokeStyle = 'rgba(255,255,255,.55)'; ctx.lineWidth = 1; ctx.stroke();
      }
    }
    ctx.restore();
    // reflexo no vidro
    ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    ctx.strokeStyle = 'rgba(255,255,255,.16)'; ctx.lineWidth = S * .018;
    ctx.beginPath(); ctx.moveTo(-.07 * S, -.38 * S); ctx.lineTo(-.07 * S, -.2 * S); ctx.lineTo(-.28 * S, .3 * S); ctx.stroke();
    // graduações = etapas
    MARKS.forEach((m, i) => {
      const y = (nivel(m) + .012) * S, on = f >= m - .005;
      ctx.fillStyle = on ? '#E9F3E4' : 'rgba(233,243,228,.22)';
      ctx.shadowColor = on ? 'rgba(233,243,228,.9)' : 'transparent'; ctx.shadowBlur = on ? 14 : 0;
      const w = .075 * S; ctx.beginPath();
      ctx.roundRect ? ctx.roundRect(.03 * S, y - S * .01, w, S * .02, S * .01) : ctx.rect(.03 * S, y - S * .01, w, S * .02); ctx.fill();
    });
    ctx.shadowBlur = 0;
    // parede: brilho neon + traço nítido
    const gw = ctx.createLinearGradient(0, -.5 * S, 0, .5 * S);
    gw.addColorStop(0, '#E9F3E4'); gw.addColorStop(.55, '#C3B1D7'); gw.addColorStop(1, '#E9F3E4');
    ctx.strokeStyle = gw; ctx.lineWidth = S * .034;
    ctx.shadowColor = `rgba(143,114,221,${.6 + f * .35})`; ctx.shadowBlur = S * (.06 + f * .06);
    ctx.stroke(wall); ctx.stroke(lip);
    ctx.shadowBlur = 0; ctx.stroke(wall); ctx.stroke(lip);
    ctx.restore();
  }

  function particulas() {
    for (const e of emi) {
      const k = e.a / e.m, al = Math.min(1, e.a / 18) * (1 - k), sc = S * .055 * (.5 + e.z * 2.4) / 100;
      if (al <= 0) continue;
      ctx.save(); ctx.translate(e.x, e.y); ctx.rotate(e.r); ctx.scale(sc, sc);
      ctx.fillStyle = `rgba(${e.c},${al * .75})`; ctx.fill(SP[e.s]); ctx.restore();
    }
    for (const o of near) {
      const z = ((o.z0 + p * 1.6 + t * .004) % 1), d = 1 / (1.18 - z), al = cl(z / .15) * cl((1 - z) / .2) * .3;
      const x = cx + Math.cos(o.a) * W * .14 * d + mx * d * 18, y = H / 2 + Math.sin(o.a) * H * .14 * d + my * d * 10, sz = S * .09 * d;
      ctx.save(); ctx.globalAlpha = al; ctx.translate(x, y); ctx.rotate(o.r + t * o.vr * 10);
      ctx.drawImage(sprites[o.s], -sz / 2, -sz / 2, sz, sz); ctx.restore();
    }
    if (flash > .01) {
      const g = ctx.createRadialGradient(cx, cy - .5 * S, 0, cx, cy - .5 * S, Math.max(W, H) * .8);
      g.addColorStop(0, `rgba(233,243,228,${flash * .55})`); g.addColorStop(.4, `rgba(143,114,221,${flash * .25})`); g.addColorStop(1, 'rgba(29,19,30,0)');
      ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
    }
  }

  function fisica() {
    const r = sec.getBoundingClientRect();
    p = cl(-r.top / Math.max(1, r.height - innerHeight));
    sv = scrollY - lastY; lastY = scrollY;
    mx += (tmx - mx) * .06; my += (tmy - my) * .06;
    tiltT = mob ? cl(sv * .004, -.12, .12) : tmx * .13 + cl(sv * .002, -.05, .05);
    lastTilt = tilt; tilt += (tiltT - tilt) * .08;
    const fT = cl((p - .04) / .84);
    fv += (fT - f) * .06; fv *= .78; f = cl(f + fv, 0, 1);
    slv += (tilt - lastTilt) * 1.8 + fv * .5 + cl(sv * .0004, -.02, .02);
    slv += -sl * .05; slv *= .94; sl = cl(sl + slv, -.35, .35);
    // bolhas
    if (f > .03) {
      acc += .15 + f * 1.6;
      while (acc >= 1) { acc--; const y = .44; bub.push({x: (R() * 2 - 1) * meia(y) * .8, y, r: .005 + R() * .012, v: .0025 + R() * .004, w: R() * 6.283}); }
    }
    const L = nivel(f);
    bub = bub.filter(b => { b.y -= b.v; b.v *= 1.01; b.w += .1; b.x += Math.sin(b.w) * .0012; const h = meia(b.y) - b.r; b.x = cl(b.x, -h, h); return b.y > sup(b.x, L) + b.r; });
    // reação saindo do gargalo
    accE += f > .12 ? f * f * (mob ? .12 : .2) : 0;
    while (accE >= 1) { accE--; emitir(1, false); }
    emi = emi.filter(e => { e.a++; e.x += e.vx * (1 + e.z); e.y += e.vy; e.vy *= .992; e.vx *= .99; e.z += .006; e.r += e.vr; return e.a < e.m; });
    flash *= .93;
    // interface
    const a = p < .27 ? 0 : p < .5 ? 1 : p < .72 ? 2 : 3;
    if (a !== ativo) { ativo = a; steps.forEach((li, i) => { li.classList.toggle('ativo', i === a); li.classList.toggle('feito', i < a); }); }
    const fz = p > .9;
    if (fz !== fim) { fim = fz; sec.classList.toggle('fim', fz); if (fz) { emitir(mob ? 26 : 40, true); flash = 1; } }
    sec.classList.toggle('ini', p < .03);
    const pc = Math.round(f * 100);
    if (pc !== pctV && pctEl) { pctV = pc; pctEl.textContent = pc; }
  }

  function quadro() {
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, W, H);
    const c = cor(f);
    fundo(c); frasco(c); particulas();
  }
  function passo() { t += 1 / 60; fisica(); quadro(); raf = vis ? requestAnimationFrame(passo) : null; }

  montar();
  if (reduz) { f = .78; p = .8; quadro(); addEventListener('resize', () => { montar(); quadro(); }); return; }
  sec.classList.add('on');
  sec.addEventListener('pointermove', e => { if (e.pointerType !== 'mouse') return; tmx = (e.clientX / innerWidth - .5) * 2; tmy = (e.clientY / innerHeight - .5) * 2; }, {passive: true});
  sec.addEventListener('pointerleave', () => { tmx = tmy = 0; });
  new IntersectionObserver(([e]) => { vis = e.isIntersecting; if (vis && !raf) { lastY = scrollY; raf = requestAnimationFrame(passo); } }).observe(sec);
  document.addEventListener('visibilitychange', () => { if (document.hidden) vis = false; else { const r = sec.getBoundingClientRect(); vis = r.bottom > 0 && r.top < innerHeight; if (vis && !raf) raf = requestAnimationFrame(passo); } });
  let tr; addEventListener('resize', () => { clearTimeout(tr); tr = setTimeout(montar, 150); });
  fisica(); quadro();
})();
