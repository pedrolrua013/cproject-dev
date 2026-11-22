#!/usr/bin/env python3
"""Gera as páginas do site a partir das partes em _tools/partes/.

Uso (na raiz do repositório):  python3 _tools/gerar-paginas.py
Edite o conteúdo nos arquivos de _tools/partes/ e rode de novo: o script
regrava index.html, as páginas de cada linha, o catálogo, o sitemap e
atualiza o cabeçalho/rodapé do 404 e da política de privacidade.
"""
import json, re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PARTES = RAIZ / '_tools' / 'partes'
SITE = 'https://cproject.com.br'
VERSAO = '18'
HOJE = '2026-11-22'


def parte(nome):
    return (PARTES / nome).read_text(encoding='utf-8').strip()


LINHAS = [
    ('/sites-e-landing-pages/', 'Sites e landing pages'),
    ('/sistemas-lab/', 'Sistemas Lab'),
    ('/intelligence/', 'CProject Intelligence'),
    ('/growth/', 'CProject Growth'),
    ('/data/', 'CProject Data'),
]


def cabecalho(atual):
    def cur(path):
        return ' aria-current="page"' if path == atual else ''
    sub = ''.join(f'<li><a href="{p}"{cur(p)}>{n}</a></li>' for p, n in LINHAS)
    sol_atual = ' aria-current="true"' if atual in [p for p, _ in LINHAS] else ''
    return f'''<a class="skip" href="#conteudo">Pular para o conteúdo</a><header class="nav" id="topo">
  <div class="in">
    <a class="logo" href="/" aria-label="CProject Lab, página inicial"><img src="/assets/brand/logo.svg" width="134" height="47" alt="CProject Lab"></a>
    <button class="burg" type="button" aria-label="Abrir menu" aria-expanded="false" aria-controls="menu"><span></span></button>
    <ul id="menu"><li><a href="/#consultoria">Consultoria</a></li><li class="dd"><a href="/#solucoes"{sol_atual}>Soluções</a><ul class="sub" aria-label="Linhas de produto">{sub}</ul></li><li><a href="/catalogo/"{cur('/catalogo/')}>Catálogo</a></li><li><a href="/#portfolio">Portfólio</a></li><li><a href="/#diagnostico">Contato</a></li></ul>
    <a class="btn nb" href="/#diagnostico" data-origem="nav">Diagnóstico gratuito</a>
  </div>
</header>'''


ORG = json.loads(parte('jsonld-org.json'))


def jsonld(path, nome):
    if path == '/':
        return ORG
    trilha = [{'@type': 'ListItem', 'position': 1, 'name': 'Início', 'item': SITE + '/'}]
    trilha.append({'@type': 'ListItem', 'position': 2, 'name': nome, 'item': SITE + path})
    return {'@context': 'https://schema.org', '@graph': [
        {'@type': 'WebPage', '@id': SITE + path + '#pagina', 'url': SITE + path, 'name': nome,
         'isPartOf': {'@id': SITE + '/#site'}, 'about': {'@id': SITE + '/#org'}, 'inLanguage': 'pt-BR'},
        {'@type': 'BreadcrumbList', 'itemListElement': trilha}]}


def pagina(path, titulo, desc, nome, corpo):
    ld = json.dumps(jsonld(path, nome), ensure_ascii=False, separators=(',', ':'))
    head = parte('head-comum.html')
    head = re.sub(r'\?v=\d+', '?v=' + VERSAO, head)
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{titulo}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}{path}">
<meta name="theme-color" content="#1D131E">
<meta property="og:type" content="website"><meta property="og:locale" content="pt_BR"><meta property="og:site_name" content="CProject Lab">
<meta property="og:title" content="{titulo}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/assets/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="CProject Lab: soluções digitais para potencializar o seu negócio">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{titulo}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{SITE}/assets/og.png">
{head}
<script type="application/ld+json">{ld}</script>
</head>
<body>
{cabecalho(path)}
<main id="conteudo">
{corpo}
</main>
{parte('rodape.html')}
{parte('whatsapp-flutuante.html')}
<script src="/assets/checkout.js?v={VERSAO}" defer></script>
<script src="/assets/site.js?v={VERSAO}" defer></script>
</body>
</html>
'''


def juntar(*nomes):
    return '\n\n'.join(parte(n) for n in nomes)


PAGINAS = [
    ('/', 'CProject Lab · Soluções digitais para potencializar o seu negócio',
     'Laboratório que estuda o seu negócio e desenvolve sites, sistemas de gestão, IA, automações e tráfego pago. Consultoria inicial gratuita. Baixada Santista e todo o Brasil.',
     'Início', juntar('hero.html', 'band.html', 'manifesto.html', 'consultoria.html', 'solucoes.html', 'portfolio.html', 'faq.html', 'diagnostico.html')),
    ('/sites-e-landing-pages/', 'Sites e landing pages · CProject Lab',
     'Sites institucionais e landing pages rápidos no celular, bem posicionados no Google e com contato direto pelo WhatsApp. Baixada Santista e todo o Brasil.',
     'Sites e landing pages', juntar('topo-sites.html', 'linha-sites.html', 'portfolio.html', 'cta-consultoria.html')),
    ('/sistemas-lab/', 'Sistemas Lab · Sistemas de gestão por nicho · CProject Lab',
     'Sistemas de gestão personalizados para nichos específicos, por assinatura: Sorrirmos para clínicas odontológicas e Cortando para barbearias.',
     'Sistemas Lab', juntar('topo-sistemas.html', 'linha-sistemas.html', 'cta-consultoria.html')),
    ('/intelligence/', 'CProject Intelligence · Packs de IA e automações · CProject Lab',
     'Packs de IA por profissão, IA personalizada para a sua empresa e automações, inclusive pelo WhatsApp.',
     'CProject Intelligence', juntar('topo-intelligence.html', 'linha-intelligence.html', 'cta-consultoria.html')),
    ('/growth/', 'CProject Growth · Gestão de tráfego pago · CProject Lab',
     'Gestão de tráfego pago no Google e nas redes sociais com plano único de R$ 500 por mês, mais a verba dos anúncios.',
     'CProject Growth', juntar('topo-growth.html', 'linha-growth.html', 'cta-consultoria.html')),
    ('/data/', 'CProject Data · Dashboards e BI · CProject Lab',
     'Templates de BI por segmento, integração de dados e dashboards sob medida para decidir com base em números.',
     'CProject Data', juntar('topo-data.html', 'linha-data.html', 'cta-consultoria.html')),
    ('/catalogo/', 'Catálogo · Packs de IA e templates de BI · CProject Lab',
     'Compre direto packs de IA por profissão e templates de BI por segmento, com preço fechado.',
     'Catálogo', juntar('topo-catalogo.html', 'catalogo-packs.html', 'catalogo-bi.html', 'cta-consultoria.html')),
]


def main():
    for path, titulo, desc, nome, corpo in PAGINAS:
        destino = RAIZ / (path.strip('/') or '.') / 'index.html'
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(pagina(path, titulo, desc, nome, corpo), encoding='utf-8')
        print('ok', path)
    # 404 e privacidade: só cabeçalho e rodapé
    for arq, path in [('404.html', '/404'), ('politica-de-privacidade/index.html', '/politica-de-privacidade/')]:
        p = RAIZ / arq
        t = p.read_text(encoding='utf-8')
        t = re.sub(r'<a class="skip".*?</header>', lambda m: cabecalho(path), t, count=1, flags=re.S)
        t = re.sub(r'<footer>.*?</footer>', lambda m: parte('rodape.html'), t, count=1, flags=re.S)
        t = re.sub(r'\?v=\d+', '?v=' + VERSAO, t)
        p.write_text(t, encoding='utf-8')
    urls = [p for p, *_ in PAGINAS] + ['/politica-de-privacidade/']
    (RAIZ / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + ''.join(f'  <url><loc>{SITE}{u}</loc><lastmod>{HOJE}</lastmod></url>\n' for u in urls) + '</urlset>\n', encoding='utf-8')


if __name__ == '__main__':
    main()
