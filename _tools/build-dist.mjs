// Copia os arquivos públicos do site para dist/ (pasta de saída usada pela Hostinger).
import { cpSync, rmSync, mkdirSync } from 'node:fs';
const publicos = ['index.html', '404.html', 'robots.txt', 'sitemap.xml', '.htaccess', 'serve.json', 'assets', 'politica-de-privacidade', 'consultoria',
  'sites-e-landing-pages', 'sistemas-lab', 'intelligence', 'growth', 'data', 'catalogo'];
rmSync('dist', { recursive: true, force: true });
mkdirSync('dist');
for (const p of publicos) cpSync(p, `dist/${p}`, { recursive: true });
console.log('dist/ pronto');
