#!/usr/bin/env python3
"""Gera as páginas do site da CProject Lab.

Uso (na raiz do repositório):  python3 _tools/gerar-paginas.py

- Blocos grandes de HTML ficam em _tools/partes/*.html (portfólio, frasco, linhas, catálogo...).
- Textos estruturados (topos, etapas, perguntas frequentes, formulários, rodapé) ficam
  nos dicionários deste arquivo.
Rodar o script regrava as páginas, o sitemap e o cabeçalho/rodapé do 404 e da privacidade.
"""
import json, re
from pathlib import Path
from urllib.parse import quote

RAIZ = Path(__file__).resolve().parent.parent
PARTES = RAIZ / '_tools' / 'partes'
SITE = 'https://cproject.com.br'
VERSAO = '22'
HOJE = '2026-11-22'
CNPJ = ''  # preencher quando o CNPJ estiver ativo, ex.: '00.000.000/0001-00'
WHATS = '5513974177986'

SYM = json.loads((RAIZ / '_tools' / 'simbolos.json').read_text())


def parte(nome):
    return (PARTES / nome).read_text(encoding='utf-8').strip()


def wa(txt):
    return f'https://wa.me/{WHATS}?text=' + quote(txt, safe='')


def icone(k, cls='ic'):
    return f'<svg class="{cls}" viewBox="-52 -52 104 104" aria-hidden="true"><path fill="currentColor" fill-rule="evenodd" d="{SYM[k]}"/></svg>'


SETA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
WA_ICON = re.search(r'<svg.*?</svg>', (PARTES / 'whatsapp-flutuante.html').read_text(encoding='utf-8'), re.S).group(0)

# ---------------------------------------------------------------- linhas
LINHAS = [
    # slug, nome, símbolo, problema, descrição, gancho
    ('/sites-e-landing-pages/', 'Sites e landing pages', 'isotipo', 'Ser encontrado e escolhido',
     'Landing pages com preço fechado e sites completos, rápidos no celular e prontos para o Google.', 'A partir de R$ 297'),
    ('/sistemas-lab/', 'Sistemas Lab', 'quadrado', 'Organizar agenda e atendimento',
     'Sistemas de gestão personalizados para nichos, como clínicas odontológicas e barbearias.', 'A partir de R$ 89,90/mês'),
    ('/intelligence/', 'CProject Intelligence', 'asterisco', 'Ganhar tempo com IA',
     'Packs de IA por profissão, IA sob medida e automações que tiram tarefa repetitiva da equipe.', 'Packs a partir de R$ 79,90'),
    ('/growth/', 'CProject Growth', 'crescer', 'Atrair mais clientes',
     'Gestão de tráfego pago no Google e nas redes sociais, com plano único.', 'R$ 500/mês + verba'),
    ('/data/', 'CProject Data', 'igual', 'Decidir com base em números',
     'Templates de BI por segmento e dashboards sob medida com os seus dados.', 'Templates a partir de R$ 100'),
]


# ---------------------------------------------------------------- cabeçalho e rodapé
def cabecalho(atual):
    def cur(p):
        return ' aria-current="page"' if p == atual else ''
    sub = ''.join(f'<li><a href="{p}"{cur(p)}>{icone(s, "ic-s")}{n}</a></li>' for p, n, s, *_ in LINHAS)
    sol = ' aria-current="true"' if atual in [l[0] for l in LINHAS] else ''
    return f'''<a class="skip" href="#conteudo">Pular para o conteúdo</a><header class="nav" id="topo">
  <div class="in">
    <a class="logo" href="/" aria-label="CProject Lab, página inicial"><img src="/assets/brand/logo.svg" width="134" height="47" alt="CProject Lab"></a>
    <button class="burg" type="button" aria-label="Abrir menu" aria-expanded="false" aria-controls="menu"><span></span></button>
    <ul id="menu"><li><a href="/consultoria/"{cur('/consultoria/')}>Consultoria</a></li><li class="dd"><a href="/#solucoes"{sol}>Soluções</a><ul class="sub" aria-label="Soluções">{sub}</ul></li><li><a href="/catalogo/"{cur('/catalogo/')}>Catálogo</a></li><li><a href="/#portfolio">Portfólio</a></li></ul>
    <a class="btn nb" href="/consultoria/#formulario" data-origem="nav">Consultoria gratuita</a>
  </div>
</header>'''


def rodape():
    sol = ''.join(f'<li><a href="{p}">{n}</a></li>' for p, n, *_ in LINHAS)
    cnpj = f'<span>CNPJ {CNPJ}</span>' if CNPJ else ''
    return f'''<footer>
  <div class="in">
    <div class="fg">
      <div><a class="logo" href="/" aria-label="CProject Lab, página inicial"><img src="/assets/brand/logo.svg" width="134" height="47" alt="CProject Lab"></a>
        <p>Um laboratório que estuda o seu negócio e desenvolve as soluções que fazem ele crescer.</p><p class="f-loc">Baixada Santista, SP · atendimento em todo o Brasil</p></div>
      <div><h3 class="fh">Soluções</h3><ul><li><a href="/consultoria/">CProject Consulting</a></li>{sol}</ul></div>
      <div><h3 class="fh">Empresa</h3><ul><li><a href="/catalogo/">Catálogo</a></li><li><a href="/#portfolio">Portfólio</a></li><li><a href="/#quem-somos">Quem somos</a></li><li><a href="/sistemas-lab/#sorrirmos">Sorrirmos</a></li><li><a href="/sistemas-lab/#cortando">Cortando</a></li><li><a href="/politica-de-privacidade/">Política de privacidade</a></li></ul></div>
      <div><h3 class="fh">Contato</h3><ul><li><a href="{wa('Olá! Vim pelo site da CProject Lab.')}" target="_blank" rel="noopener" data-origem="rodape">WhatsApp +55 (13) 97417-7986</a></li><li><a href="mailto:contato@cproject.com.br">contato@cproject.com.br</a></li><li><a href="https://instagram.com/cproject.lab" target="_blank" rel="noopener">@cproject.lab</a></li></ul></div>
    </div>
    <div class="cp"><span>© 2026 CProject Lab</span>{cnpj}<span>Testar. Desenvolver. Inovar.</span></div>
  </div>
</footer>'''


# ---------------------------------------------------------------- componentes
def topo(eb, h1, lead, ctas, sym, trilha=True):
    bc = f'<nav aria-label="Trilha"><ol class="bc"><li><a href="/">Início</a></li><li aria-current="page">{eb}</li></ol></nav>' if trilha else ''
    bts = ''.join(f'<a class="btn{" o" if i else ""}" href="{h}"{" target=\"_blank\" rel=\"noopener\"" if h.startswith("http") else ""} data-origem="topo">{t}</a>' for i, (t, h) in enumerate(ctas))
    return f'<section class="ph sy-{sym}" aria-labelledby="h1"><div class="in">{bc}<span class="eb">{eb}</span><h1 id="h1">{h1}</h1><p class="lead">{lead}</p><div class="ctas">{bts}</div></div></section>'


def etapas(eb, titulo, texto, passos, cls='sec light'):
    lis = ''.join(f'<li class="tl-s" tabindex="0" data-i="{i}"><span class="tl-dot"><b>0{i + 1}</b></span><h3>{a}</h3><p>{b}</p></li>' for i, (a, b) in enumerate(passos))
    return f'''<section class="{cls}" aria-labelledby="t-como"><div class="in"><div class="hd rv"><span class="eb">{eb}</span><h2 id="t-como">{titulo}</h2><p>{texto}</p></div>
<div class="tl rv" style="--n:{len(passos)}" data-tl><div class="tl-line" aria-hidden="true"><i class="tl-fill"></i></div><ol>{lis}</ol></div></div></section>'''


def faq(itens, cls='sec light white', titulo='Perguntas frequentes'):
    ds = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in itens)
    return f'<section class="{cls}" id="faq" aria-labelledby="t-faq"><div class="in"><div class="hd rv"><span class="eb">Perguntas frequentes</span><h2 id="t-faq">{titulo}</h2></div><div class="faq rv">{ds}</div></div></section>'


SEGMENTOS = ['Saúde e odontologia', 'Beleza, estética e barbearia', 'Advocacia e serviços profissionais', 'Comércio e varejo',
             'Alimentação', 'Indústria, logística e comércio exterior', 'Educação', 'Imobiliário e construção', 'Outro']


def formulario(eb, titulo, texto, interesse, botao, nota=''):
    segs = ''.join(f'<option>{s}</option>' for s in SEGMENTOS)
    nota = f'<p class="ct-n">{nota}</p>' if nota else ''
    return f'''<section class="sec teal" id="formulario" aria-labelledby="t-ct">
  <span id="diagnostico" aria-hidden="true"></span>
  <div class="in ct">
    <div class="rv"><span class="eb">{eb}</span><h2 id="t-ct" style="font-size:var(--h2);margin-top:16px">{titulo}</h2>
      <p style="color:var(--tx-2);margin-top:16px">{texto}</p>{nota}
      <div class="ch">
        <a href="{wa('Olá! Vim pelo site da CProject Lab e quero conversar sobre: ' + interesse + '.')}" target="_blank" rel="noopener" data-origem="contato">{WA_ICON}<span><small>WhatsApp</small>+55 (13) 97417-7986</span></a>
        <a href="mailto:contato@cproject.com.br"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="3"/><path d="m4 7 8 6 8-6"/></svg><span><small>E-mail</small>contato@cproject.com.br</span></a>
        <a href="https://instagram.com/cproject.lab" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg><span><small>Instagram</small>@cproject.lab</span></a>
      </div></div>
    <form class="fm rv" id="fm" method="post" action="/api/diagnostico" novalidate aria-label="{titulo}">
      <input type="hidden" name="interesse" value="{interesse}">
      <div class="fl"><label for="f-nome">Nome</label><input id="f-nome" name="nome" autocomplete="name" maxlength="120" required></div>
      <div class="fl"><label for="f-emp">Empresa</label><input id="f-emp" name="empresa" autocomplete="organization" maxlength="120" required></div>
      <div class="fl"><label for="f-seg">Segmento</label><select id="f-seg" name="segmento" required><option value="">Selecione</option>{segs}</select></div>
      <div class="fl"><label for="f-wpp">WhatsApp</label><input id="f-wpp" name="whatsapp" type="tel" inputmode="tel" autocomplete="tel" maxlength="20" placeholder="(13) 90000-0000" required></div>
      <div class="fl w"><label for="f-msg">O que você busca?</label><textarea id="f-msg" name="busca" maxlength="2000" required placeholder="Ex.: mais clientes, organizar a agenda, automatizar o atendimento."></textarea></div>
      <div class="hp" aria-hidden="true"><label for="f-site">Site</label><input id="f-site" name="site" tabindex="-1" autocomplete="off"></div>
      <button class="btn" type="submit">{botao}</button>
      <p class="fmsg" id="fmsg" role="status" aria-live="polite">Usamos seus dados só para entrar em contato. Veja a <a href="/politica-de-privacidade/">política de privacidade</a>.</p>
    </form>
  </div>
</section>'''


NOTA_CONSULTORIA = 'Não sabe se é a solução certa? <a href="/consultoria/">Conheça a consultoria gratuita</a>.'

# ---------------------------------------------------------------- home
FAQ_HOME = [
    ('O que a CProject Lab faz?', 'Somos um laboratório que estuda soluções para potencializar negócios. Além da consultoria CProject Consulting, temos cinco linhas que podem ser contratadas separadamente: sites e landing pages, Sistemas Lab, CProject Intelligence (IA e automações), CProject Growth (tráfego pago) e CProject Data (dashboards e BI).'),
    ('Posso contratar só uma solução?', 'Sim. Cada solução pode ser contratada separadamente. A consultoria é indicada para quem ainda não sabe por onde começar ou quer um plano completo.'),
    ('Como funciona a consultoria gratuita?', 'Começa com uma entrevista inicial gratuita, em que entendemos o negócio, os fluxos, o que já existe e onde você quer chegar. Depois analisamos tudo e entregamos um plano de ação com as soluções recomendadas e o orçamento de cada uma.'),
    ('A entrevista inicial tem custo?', 'Não. A entrevista inicial é gratuita e sem compromisso de contratação.'),
    ('Vocês atendem fora da Baixada Santista?', 'Sim. Estamos na Baixada Santista e atendemos empresas de todo o Brasil de forma online.'),
    ('Como funciona o suporte depois da entrega?', 'Ajustes e evolução são conversados direto com quem construiu o projeto, sem intermediário e sem fila de ticket.'),
]

CLIENTES = ['Fundação Virgínia Ferraz', 'ISTV', 'Rotary Club São Caetano do Sul - Olímpico', 'Gelomac', 'DRC Compressores', 'Grupo Yamam', 'Beatriz Geraldi', 'Ingrid Krichinak', 'Marysol', 'Figueiredo Barros Advocacia', 'Bonomi Almeida']


def home():
    cards = ''.join(f'''<a class="sol-c rv" href="{p}"><span class="sol-i">{icone(s)}</span><span class="sol-l">{n}</span><h3>{prob}</h3><p>{d}</p><span class="sol-f"><b>{g}</b><span class="sol-go">Ver solução {SETA}</span></span></a>''' for p, n, s, prob, d, g in LINHAS)
    solucoes = f'''<section class="sec light" id="solucoes" aria-labelledby="t-sol">
  <div class="in">
    <div class="hd rv"><span class="eb">Soluções individuais</span><h2 id="t-sol">O que o seu negócio <em class="g">precisa resolver</em>?</h2><p>Escolha pelo problema. Cada solução pode ser contratada sozinha, e na consultoria gratuita a gente indica a combinação certa.</p></div>
    <div class="sol">{cards}</div>
  </div>
</section>'''
    destaque = f'''<section class="sec teal" id="sistemas-lab" aria-labelledby="t-dest">
  <div class="in dest">
    <div class="rv"><span class="eb">Sistemas Lab</span><h2 id="t-dest">Sistemas de gestão feitos <em class="g">para o seu nicho</em></h2><p>Cada Sistema Lab nasce do estudo da rotina de um segmento e já vem com o que aquele negócio precisa. Funciona por assinatura, sem projeto do zero.</p><div class="ctas"><a class="btn" href="/sistemas-lab/">Conhecer os Sistemas Lab</a></div></div>
    <div class="dest-c rv">
      <a class="dest-i" href="/sistemas-lab/#sorrirmos"><span class="mk"><b style="background:#8E80EF">S</b><span><span class="sl-n">Sorrirmos</span><span class="sl-x">Clínicas e consultórios odontológicos</span></span></span><span class="sl-m">A partir de R$ 89,90/mês</span>{SETA}</a>
      <a class="dest-i" href="/sistemas-lab/#cortando"><span class="mk"><b style="background:#D9468A">C</b><span><span class="sl-n">Cortando</span><span class="sl-x">Barbearias e salões de beleza</span></span></span><span class="sl-m">Planos em breve</span>{SETA}</a>
      <a class="dest-i dest-n" href="/sistemas-lab/#sistemas-lista"><span class="mk"><b style="background:var(--lav)">+</b><span><span class="sl-n">Próximo Sistema Lab</span><span class="sl-x">Sugira o seu segmento</span></span></span>{SETA}</a>
    </div>
  </div>
</section>'''
    clientes = ''.join(f'<li>{c}</li>' for c in CLIENTES)
    equipe = f'''<section class="sec light" id="quem-somos" aria-labelledby="t-eq">
  <div class="in">
    <div class="hd rv"><span class="eb">Quem constrói</span><h2 id="t-eq">Gente de verdade <em class="g">do outro lado</em></h2><p>Você conversa direto com quem desenvolve: desenvolvimento, negócios e marketing no mesmo time, do primeiro contato ao suporte.</p></div>
    {parte('equipe-cards.html')}
    <div class="cli rv"><p>Quem já trabalhou com a gente</p><ul>{clientes}</ul></div>
  </div>
</section>'''
    return '\n\n'.join([parte('hero.html'), parte('band.html'), parte('consultoria.html'), solucoes, destaque,
                        parte('portfolio.html').replace('class="sec light" id="portfolio"', 'class="sec light white" id="portfolio"'),
                        parte('manifesto.html').replace('id="lab"', 'id="manifesto"'), equipe,
                        faq(FAQ_HOME, 'sec light white', 'Antes de conversar'),
                        formulario('Consultoria gratuita', 'Vamos entender o seu negócio?', 'Preencha o formulário e entramos em contato para marcar a entrevista inicial gratuita. Se preferir, fale direto pelos canais abaixo.', 'Consultoria gratuita', 'Quero a consultoria gratuita')])


# ---------------------------------------------------------------- consultoria
FAQ_CONSULTORIA = [
    ('A consultoria tem custo?', 'A entrevista inicial é gratuita. Nela entendemos o seu negócio e, ao final, você recebe o plano de ação com as soluções recomendadas e o orçamento.'),
    ('Sou obrigado a contratar alguma solução depois?', 'Não. Você recebe o plano e o orçamento e decide com calma o que implementar e quando.'),
    ('E se eu já souber o que quero?', 'Você pode ir direto à solução: cada uma tem a sua página e pode ser contratada separadamente.'),
    ('Vocês atendem fora da Baixada Santista?', 'Sim. Estamos na Baixada Santista e atendemos empresas de todo o Brasil de forma online.'),
]


def consultoria():
    passos = [('Entrevista inicial', 'Uma conversa gratuita para entender o negócio por completo: como funciona hoje, o que já existe e onde você quer chegar.'),
              ('Análise dos fluxos', 'Mapeamos atendimento, vendas e rotina para encontrar onde a empresa perde tempo, dinheiro ou cliente.'),
              ('Plano de ação', 'Você recebe um plano claro, com prioridades e as soluções que fazem sentido para o seu momento.'),
              ('Soluções e orçamento', 'Junto com o plano vai o orçamento de cada solução. Você decide o que implementar e quando.')]
    recebe = ''.join(f'<article class="card rv"><span class="n">{n}</span><h3>{h}</h3><p>{p}</p></article>' for n, h, p in [
        ('01', 'Plano de ação', 'Prioridades claras: o que fazer primeiro, o que pode esperar e por quê.'),
        ('02', 'Soluções recomendadas', 'Quais soluções fazem sentido para você (site, sistema, IA, tráfego ou dados) e como elas se conectam.'),
        ('03', 'Orçamento', 'O valor de cada solução, para decidir com calma o que implementar e quando.')])
    quem = '<ul class="sl-pts rv">' + ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in [
        ('Pequenos negócios locais', 'Comércios e serviços que querem sair do caderno e do WhatsApp manual.'),
        ('Profissionais liberais', 'Consultórios, escritórios e autônomos que precisam de agenda, presença e tempo.'),
        ('Empresas B2B médias', 'Operações com processos internos que pedem sistema, dados e automação.')]) + '</ul>'
    return '\n\n'.join([
        topo('CProject Consulting', 'Primeiro o negócio, <em class="g">depois</em> a tecnologia.',
             'A consultoria completa da CProject Lab: entendemos como a sua empresa funciona, onde ela perde tempo e cliente, e entregamos um plano de ação com as soluções certas e o orçamento. A entrevista inicial é gratuita.',
             [('Agendar minha consultoria gratuita', '#formulario'), ('Ver as soluções', '/#solucoes')], 'frasco'),
        etapas('Como funciona', 'Quatro etapas, <em class="g">um plano claro</em>', 'Do primeiro contato ao orçamento, sem jargão técnico e sem compromisso.', passos),
        f'<section class="sec light white" aria-labelledby="t-rec"><div class="in"><div class="hd rv"><span class="eb">O que você recebe</span><h2 id="t-rec">Tudo para decidir <em class="g">com segurança</em></h2></div><div class="sv s3">{recebe}</div></div></section>',
        f'<section class="sec teal" aria-labelledby="t-quem"><div class="in"><div class="hd rv"><span class="eb">Para quem é</span><h2 id="t-quem">Feita para quem quer crescer <em class="g">com método</em></h2></div>{quem}</div></section>',
        faq(FAQ_CONSULTORIA, 'sec light'),
        formulario('Consultoria gratuita', 'Agende a sua entrevista inicial', 'Conte um pouco sobre a sua empresa e entramos em contato para marcar a conversa.', 'CProject Consulting', 'Quero a consultoria gratuita')])


# ---------------------------------------------------------------- páginas de produto
PRODUTOS = {
    '/sites-e-landing-pages/': dict(
        eb='Sites e landing pages', sym='isotipo', parte='linha-sites.html',
        h1='Seu negócio <em class="g">encontrado</em> e escolhido',
        lead='Sites e páginas criados para o seu público, rápidos no celular e prontos para transformar visita em contato.',
        ctas=[('Ver planos', '#sites'), ('Ver portfólio', '#portfolio')],
        extra=lambda: parte('portfolio.html').replace('<span class="eb">Portfólio</span>', '<span class="eb">Portfólio</span>'),
        passos=[('Briefing', 'Entendemos o negócio, o público e o objetivo da página.'),
                ('Estrutura e textos', 'Organizamos as seções e escrevemos os textos pensando em quem vai visitar.'),
                ('Desenvolvimento', 'Site rápido, responsivo e com SEO configurado, com você acompanhando.'),
                ('Publicação', 'Domínio, certificado de segurança e site no ar. Depois, manutenção por nossa conta.')],
        faq=[('O site aparece no Google?', 'Configuramos o SEO de cada página e os dados estruturados para o Google entender o seu negócio. A posição depende também da concorrência e do conteúdo, mas o site já sai preparado.'),
             ('Vocês cuidam de domínio e hospedagem?', 'Sim. Publicamos e mantemos o site no ar, com domínio, certificado de segurança e ajustes quando você precisar.'),
             ('Qual a diferença entre site e landing page?', 'O site apresenta a empresa como um todo, em várias páginas. A landing page é uma página única focada em uma oferta ou campanha.'),
             ('Quanto custa?', 'A Landing Page Template sai por R$ 297 em pagamento único; a Hospedada, por R$ 297 de implantação + R$ 50 por mês; a Personalizada, a partir de R$ 997. Sites completos são orçados conforme o escopo.')],
        form=('Sites e landing pages', 'Vamos criar o seu site?', 'Conte sobre o seu negócio e o que o site precisa ter. Respondemos com os próximos passos e o orçamento.', 'Quero um site')),
    '/sistemas-lab/': dict(
        eb='Sistemas Lab', sym='quadrado', parte='linha-sistemas.html',
        h1='Sistemas feitos para <em class="g">o seu nicho</em>',
        lead='Os Sistemas Lab são sistemas de gestão personalizados para nichos específicos. Cada um nasce do estudo da rotina de um segmento, já vem com o que aquele tipo de negócio precisa e funciona por assinatura.',
        ctas=[('Ver os sistemas e planos', '#sistemas-lista'), ('Quero uma demonstração', '#formulario')],
        passos=[('Demonstração', 'Mostramos o sistema funcionando e tiramos as dúvidas da sua equipe.'),
                ('Implantação', 'Configuramos o sistema com os dados e a rotina da sua empresa.'),
                ('Dia a dia', 'Agenda, atendimento e lembretes rodando, com a equipe já usando.'),
                ('Suporte e evolução', 'Suporte direto com quem desenvolve e novas funções que nascem do uso real.')],
        faq=[('Tem taxa de implantação?', 'Nos planos mensais do Sorrirmos há uma taxa única de implantação de R$ 297. No plano anual, a implantação é isenta.'),
             ('O custo das mensagens de WhatsApp está incluso?', 'Sim. O Sorrirmos usa o WhatsApp oficial e o custo das mensagens já está incluso nos planos.'),
             ('Como fica a LGPD?', 'O paciente dá o aceite antes de qualquer envio de mensagem.'),
             ('O meu segmento não tem um Sistema Lab. E agora?', 'Conte para a gente: novos Sistemas Lab nascem de nichos com a mesma necessidade. Se for urgente, um sistema sob medida pode ser indicado na consultoria.')],
        form=('Sistemas Lab', 'Quer ver o sistema funcionando?', 'Peça uma demonstração do Sorrirmos ou entre na lista do Cortando. Se o seu nicho ainda não tem sistema, conte qual é.', 'Quero uma demonstração')),
    '/intelligence/': dict(
        eb='CProject Intelligence', sym='asterisco', parte='linha-intelligence.html',
        h1='Inteligência artificial <em class="g">trabalhando</em> para o seu negócio',
        lead='Da IA pronta para usar à IA criada junto com a sua equipe, com automações que tiram tarefa repetitiva do dia a dia.',
        ctas=[('Ver catálogo de packs', '/catalogo/#packs'), ('Quero IA sob medida', '#formulario')],
        passos_titulo='Como funciona o Intelligence Sob Medida',
        passos=[('Reuniões iniciais', 'Entendemos a rotina da equipe e onde a IA pode ajudar de verdade.'),
                ('Mapeamento das tarefas', 'Escolhemos as tarefas que mais tomam tempo e que a IA resolve bem.'),
                ('Criação do pack', 'Montamos as skills, modelos e fluxos no padrão da sua empresa.'),
                ('Treinamento e acompanhamento', 'Treinamos a equipe e acompanhamos o uso para ajustar o que for preciso.')],
        faq=[('Preciso de algum programa específico?', 'Os packs são instalados no assistente de IA que você já usa. Na compra, orientamos a instalação e fazemos uma sessão de treinamento.'),
             ('E os dados sensíveis dos meus clientes?', 'Todo pack vem com orientações de uso seguro: o que pode e o que não pode ir para a IA, conforme a LGPD e o código de ética da profissão.'),
             ('A IA substitui o profissional?', 'Não. A IA apoia o trabalho, mas todo conteúdo técnico, jurídico ou clínico precisa ser revisado por quem responde por ele.'),
             ('Qual a diferença entre o pack pronto e o sob medida?', 'O pack pronto é feito para as tarefas comuns de uma profissão. O sob medida é criado em reuniões com a sua equipe, a partir dos seus documentos e processos.')],
        form=('CProject Intelligence', 'Vamos colocar a IA para trabalhar?', 'Conte quais tarefas mais tomam tempo da sua equipe. Respondemos com o caminho ideal: pack pronto, sob medida ou automação.', 'Quero falar sobre IA')),
    '/growth/': dict(
        eb='CProject Growth', sym='crescer', parte='linha-growth.html',
        h1='Mais clientes <em class="g">chegando até você</em>',
        lead='Gestão de tráfego pago no Google e nas redes sociais, com plano único de R$ 500 por mês e a verba dos anúncios definida com você.',
        ctas=[('Quero o Growth', '#formulario'), ('Ver o plano', '#growth')],
        passos=[('Briefing', 'Entendemos o negócio, o público, a região e o objetivo das campanhas.'),
                ('Criação das campanhas', 'Planejamos e criamos os anúncios no Google e nas redes sociais.'),
                ('Campanhas no ar', 'Publicamos e acompanhamos de perto o desempenho dos anúncios.'),
                ('Acompanhamento e ajustes', 'Conversamos sobre os resultados direto com quem gerencia e ajustamos o que for preciso.')],
        faq=[('A verba dos anúncios está inclusa nos R$ 500?', 'Não. Os R$ 500 por mês são pela gestão das campanhas. A verba dos anúncios é definida com você e fica por conta do cliente.'),
             ('Em quais plataformas vocês anunciam?', 'No Google e nas redes sociais. A escolha depende do seu público e do objetivo.'),
             ('Quanto devo investir em anúncios?', 'Depende da região, da concorrência e do objetivo. Definimos o valor junto com você no briefing.'),
             ('Recebo relatório dos resultados?', 'Sim. Todo mês você recebe um relatório com cliques, contatos e custo por contato.'),
             ('Combina com um site novo?', 'Sim. Anúncio bom precisa de uma página que converta: sites e landing pages da CProject Lab já saem preparados para isso.')],
        form=('CProject Growth', 'Vamos trazer mais clientes?', 'Conte sobre o seu negócio e a região que você atende. Respondemos com os próximos passos.', 'Quero o Growth')),
    '/data/': dict(
        eb='CProject Data', sym='igual', parte='linha-data.html',
        h1='Decisões com base em <em class="g">dados</em>',
        lead='Dashboards e BI que reúnem os números da empresa em um só lugar, sem montar relatório na mão toda semana.',
        ctas=[('Ver templates de BI', '/catalogo/#bi'), ('Quero um painel sob medida', '#formulario')],
        passos=[('Template ou briefing', 'Escolha um template do seu segmento ou conte quais números precisa acompanhar.'),
                ('Conexão dos dados', 'Ligamos o painel à sua planilha, sistema ou banco de dados.'),
                ('Configuração', 'Ajustamos indicadores, gráficos e filtros ao seu jeito de decidir.'),
                ('Painel no ar', 'Você acompanha tudo por um link, com os dados atualizados.')],
        faq=[('De onde vêm os dados?', 'Da sua planilha, do seu sistema ou do seu banco de dados. Conectamos as fontes ao painel.'),
             ('Qual a diferença entre o template e o com hospedagem?', 'No template, o painel roda na sua ferramenta e a atualização é feita por você. Com hospedagem, ele fica online num endereço próprio, com atualização automática e suporte contínuo.'),
             ('E se o meu segmento não tiver template?', 'Montamos um dashboard sob medida, com os seus indicadores e fontes de dados.')],
        form=('CProject Data', 'Quais números você quer enxergar?', 'Conte de onde vêm os dados da sua empresa e o que você precisa acompanhar.', 'Quero falar sobre dados')),
}


def produto(path):
    d = PRODUTOS[path]
    corpo = [topo(d['eb'], d['h1'], d['lead'], d['ctas'], d['sym']), parte(d['parte'])]
    if 'extra' in d:
        corpo.append(d['extra']())
    s1 = path == '/sites-e-landing-pages/'
    corpo.append(etapas('Como funciona', d.get('passos_titulo', 'Do primeiro contato <em class="g">ao resultado</em>'), 'Um processo simples, com você acompanhando cada etapa.', d['passos'],
                        'sec light white' if s1 else 'sec light'))
    corpo.append(faq(d['faq'], 'sec light' if s1 else 'sec light white'))
    i, t, x, b = d['form']
    corpo.append(formulario(d['eb'], t, x, i, b, NOTA_CONSULTORIA))
    return '\n\n'.join(corpo)


def catalogo():
    return '\n\n'.join([
        topo('Catálogo', 'Escolha e compre <em class="g">direto</em>', 'Packs de IA por profissão e templates de BI por segmento, com preço fechado e compra na hora.',
             [('Packs de IA', '#packs'), ('Templates de BI', '#bi')], 'chevrons'),
        parte('catalogo-packs.html'), parte('catalogo-bi.html'),
        formulario('Dúvidas sobre o catálogo', 'Ficou alguma dúvida?', 'Fale com a gente antes de comprar. Se o seu nicho ou segmento não estiver no catálogo, também dá para criar sob medida.', 'Catálogo', 'Enviar dúvida', NOTA_CONSULTORIA)])


# ---------------------------------------------------------------- montagem
ORG = json.loads(parte('jsonld-org.json'))


def faq_ld(itens):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in itens]}


def jsonld(path, nome, faqs):
    if path == '/':
        g = [x for x in ORG['@graph'] if x.get('@type') != 'FAQPage'] + [faq_ld(FAQ_HOME)]
        return {'@context': 'https://schema.org', '@graph': g}
    trilha = [{'@type': 'ListItem', 'position': 1, 'name': 'Início', 'item': SITE + '/'},
              {'@type': 'ListItem', 'position': 2, 'name': nome, 'item': SITE + path}]
    g = [{'@type': 'WebPage', '@id': SITE + path + '#pagina', 'url': SITE + path, 'name': nome,
          'isPartOf': {'@id': SITE + '/#site'}, 'about': {'@id': SITE + '/#org'}, 'inLanguage': 'pt-BR'},
         {'@type': 'BreadcrumbList', 'itemListElement': trilha}]
    if faqs:
        g.append(faq_ld(faqs))
    return {'@context': 'https://schema.org', '@graph': g}


def pagina(path, titulo, desc, nome, corpo, og, faqs=None):
    ld = json.dumps(jsonld(path, nome, faqs), ensure_ascii=False, separators=(',', ':'))
    head = re.sub(r'\?v=\d+', '?v=' + VERSAO, parte('head-comum.html'))
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
<meta property="og:image" content="{SITE}/assets/og/{og}.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{nome} · CProject Lab">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{titulo}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{SITE}/assets/og/{og}.png">
{head}
<script src="/_vercel/insights/script.js" defer></script>
<script type="application/ld+json">{ld}</script>
</head>
<body>
{cabecalho(path)}
<main id="conteudo">
{corpo}
</main>
{rodape()}
{parte('whatsapp-flutuante.html')}
<script src="/assets/checkout.js?v={VERSAO}" defer></script>
<script src="/assets/site.js?v={VERSAO}" defer></script>
</body>
</html>
'''


PAGINAS = [
    ('/', 'CProject Lab · Soluções digitais para potencializar o seu negócio',
     'Laboratório que estuda o seu negócio e desenvolve sites, sistemas de gestão, IA, automações e tráfego pago. Consultoria inicial gratuita. Baixada Santista e todo o Brasil.',
     'Início', home, 'home', None),
    ('/consultoria/', 'CProject Consulting · Consultoria gratuita · CProject Lab',
     'Entrevista inicial gratuita para entender o seu negócio e um plano de ação com as soluções certas e o orçamento.',
     'CProject Consulting', consultoria, 'consultoria', FAQ_CONSULTORIA),
    ('/sites-e-landing-pages/', 'Sites e landing pages · CProject Lab',
     'Sites institucionais e landing pages rápidos no celular, bem posicionados no Google e com contato direto pelo WhatsApp.',
     'Sites e landing pages', lambda: produto('/sites-e-landing-pages/'), 'sites', PRODUTOS['/sites-e-landing-pages/']['faq']),
    ('/sistemas-lab/', 'Sistemas Lab · Sistemas de gestão por nicho · CProject Lab',
     'Sistemas de gestão personalizados para nichos específicos, por assinatura: Sorrirmos para clínicas odontológicas e Cortando para barbearias.',
     'Sistemas Lab', lambda: produto('/sistemas-lab/'), 'sistemas-lab', PRODUTOS['/sistemas-lab/']['faq']),
    ('/intelligence/', 'CProject Intelligence · Packs de IA e automações · CProject Lab',
     'Packs de IA por profissão, IA sob medida para a sua empresa e automações, inclusive pelo WhatsApp.',
     'CProject Intelligence', lambda: produto('/intelligence/'), 'intelligence', PRODUTOS['/intelligence/']['faq']),
    ('/growth/', 'CProject Growth · Gestão de tráfego pago · CProject Lab',
     'Gestão de tráfego pago no Google e nas redes sociais com plano único de R$ 500 por mês, mais a verba dos anúncios.',
     'CProject Growth', lambda: produto('/growth/'), 'growth', PRODUTOS['/growth/']['faq']),
    ('/data/', 'CProject Data · Dashboards e BI · CProject Lab',
     'Templates de BI por segmento, integração de dados e dashboards sob medida para decidir com base em números.',
     'CProject Data', lambda: produto('/data/'), 'data', PRODUTOS['/data/']['faq']),
    ('/catalogo/', 'Catálogo · Packs de IA e templates de BI · CProject Lab',
     'Compre direto packs de IA por profissão e templates de BI por segmento, com preço fechado.',
     'Catálogo', catalogo, 'catalogo', None),
]


def main():
    for path, titulo, desc, nome, fn, og, faqs in PAGINAS:
        destino = RAIZ / (path.strip('/') or '.') / 'index.html'
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(pagina(path, titulo, desc, nome, fn(), og, faqs), encoding='utf-8')
        print('ok', path)
    for arq, path in [('404.html', '/404'), ('politica-de-privacidade/index.html', '/politica-de-privacidade/')]:
        p = RAIZ / arq
        t = p.read_text(encoding='utf-8')
        t = re.sub(r'<a class="skip".*?</header>', lambda m: cabecalho(path), t, count=1, flags=re.S)
        t = re.sub(r'<footer>.*?</footer>', lambda m: rodape(), t, count=1, flags=re.S)
        t = re.sub(r'\?v=\d+', '?v=' + VERSAO, t)
        p.write_text(t, encoding='utf-8')
    urls = [p for p, *_ in PAGINAS] + ['/politica-de-privacidade/']
    (RAIZ / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                      + ''.join(f'  <url><loc>{SITE}{u}</loc><lastmod>{HOJE}</lastmod></url>\n' for u in urls) + '</urlset>\n', encoding='utf-8')


if __name__ == '__main__':
    main()
