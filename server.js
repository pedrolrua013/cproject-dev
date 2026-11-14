// Servidor estático sem dependências para a pasta dist/ (uso opcional na Hostinger).
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const RAIZ = path.join(__dirname, 'dist');
const TIPOS = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'application/javascript; charset=utf-8', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.xml': 'application/xml', '.txt': 'text/plain; charset=utf-8', '.json': 'application/json' };
const SEG = { 'Strict-Transport-Security': 'max-age=63072000; includeSubDomains', 'Content-Security-Policy': "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'", 'X-Frame-Options': 'DENY', 'X-Content-Type-Options': 'nosniff', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Permissions-Policy': 'camera=(), microphone=(), geolocation=()' };
function enviar(res, status, arq) {
  const cab = { ...SEG, 'Content-Type': TIPOS[path.extname(arq)] || 'application/octet-stream' };
  if (arq.includes(`${path.sep}assets${path.sep}`)) cab['Cache-Control'] = 'public, max-age=31536000, immutable';
  res.writeHead(status, cab); fs.createReadStream(arq).pipe(res);
}
http.createServer((req, res) => {
  let url = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  const alvo = path.normalize(path.join(RAIZ, url));
  if (!alvo.startsWith(RAIZ)) { res.writeHead(400); return res.end(); }
  if (!url.endsWith('/') && !path.extname(url) && fs.existsSync(path.join(alvo, 'index.html'))) { res.writeHead(301, { Location: url + '/' }); return res.end(); }
  const arq = url.endsWith('/') ? path.join(alvo, 'index.html') : alvo;
  if (fs.existsSync(arq) && fs.statSync(arq).isFile()) return enviar(res, 200, arq);
  enviar(res, 404, path.join(RAIZ, '404.html'));
}).listen(process.env.PORT || 3000);
