#!/usr/bin/env python3
"""Gera o site estático da CProject (home, páginas de serviço, política, 404, sitemap)."""
import json, html, os, datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BASE = "https://cproject.com.br"
WA_NUM = "5513974177986"
WA_FMT = "+55 (13) 97417-7986"
EMAIL = "bruno.perescp@gmail.com"
IG = "https://instagram.com/cproject.dev"
HOJE = datetime.date.today().isoformat()
V = "4"  # versão dos assets

def wa(msg):
    from urllib.parse import quote
    return f"https://wa.me/{WA_NUM}?text={quote(msg)}"

E = html.escape

LOGO = '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 1.5 30.5 16 16 30.5 1.5 16Z" fill="#0D1C3A" stroke="#C9A86A" stroke-opacity=".6"/><path d="M19.6 12.2a5 5 0 1 0 0 7.6" fill="none" stroke="#C9A86A" stroke-width="2" stroke-linecap="round"/><circle cx="16" cy="16" r="1.4" fill="#64FFDA"/></svg>'
I_WA = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21h.01c5.46 0 9.91-4.45 9.91-9.91A9.85 9.85 0 0 0 12.04 2Zm5.79 14.06c-.24.68-1.42 1.3-1.95 1.35-.5.05-.97.24-3.27-.68-2.77-1.09-4.52-3.93-4.66-4.11-.13-.18-1.11-1.48-1.11-2.83 0-1.34.7-2 .95-2.28.25-.27.54-.34.72-.34h.52c.17 0 .39-.06.61.47.24.56.79 1.92.86 2.06.07.14.11.3.02.48-.09.18-.14.3-.27.46-.14.16-.29.36-.41.48-.14.14-.28.29-.12.56.16.27.71 1.17 1.52 1.9 1.05.93 1.93 1.22 2.2 1.36.27.14.43.11.59-.07.16-.18.68-.79.86-1.07.18-.27.36-.23.61-.14.25.09 1.59.75 1.86.89.27.14.45.2.52.32.07.11.07.66-.17 1.33Z"/></svg>'
I_MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="3"/><path d="m4 7 8 6 8-6"/></svg>'
I_IG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>'
I_SETA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
I_PACK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 3 7.5v9L12 21l9-4.5v-9Z"/><path d="m3 7.5 9 4.5 9-4.5M12 12v9"/></svg>'
I_SPARK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/></svg>'
I_DOC = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><path d="M6 3h8l4 4v14H6Z"/><path d="M14 3v4h4M9 12h6M9 16h6"/></svg>'

SERVICOS = [
  {"slug": "sites-e-apps", "nome": "Sites & apps", "tit": "Criação de sites e aplicativos sob medida",
   "h1": "Sites e aplicativos sob medida, rápidos no celular e prontos para crescer",
   "title": "Criação de sites e apps sob medida | CProject",
   "desc": "Sites institucionais, landing pages e aplicativos web com painel próprio para sua equipe. Estúdio full-stack, do protótipo ao suporte pós-entrega.",
   "card": "Sites institucionais, landing pages e aplicativos web com experiência mobile fluida e performance de produto.",
   "lead": "Do site institucional ao aplicativo web: experiência pensada primeiro para o celular, carregamento rápido e um painel para a sua equipe atualizar o conteúdo sem depender de suporte técnico.",
   "entra": ["Site institucional, landing page ou aplicativo web (PWA)", "Painel administrativo para notícias, agenda, galerias e eventos", "Layout responsivo, pensado primeiro para o celular", "Publicação, domínio e hospedagem configurados", "SEO técnico básico: títulos, descrições e dados estruturados"],
   "quem": ["Organizações e fundações que precisam atualizar o site com frequência", "Negócios locais que querem ser encontrados no Google", "Projetos que começam pequenos e precisam evoluir sem refazer tudo"],
   "faq": [("O site vem com painel para eu atualizar sozinho?", "Quando o projeto pede, sim. No site da Fundação Virgínia Ferraz, por exemplo, a equipe gerencia álbuns, agenda, notícias e eventos por um painel próprio, sem depender de suporte técnico."),
           ("O site funciona bem no celular?", "Sim. O layout nasce pensado para o celular e depois se adapta a telas maiores."),
           ("Vocês usam template pronto?", "Não. Interface e código são feitos sob medida para o seu projeto, o que facilita evoluir depois sem retrabalho.")],
   "wa": "Olá! Vim pelo site e quero falar sobre um site ou aplicativo."},
  {"slug": "sistemas-sob-medida", "nome": "Sistemas internos", "tit": "Sistemas internos sob medida",
   "h1": "Sistemas sob medida para tirar a operação da planilha e do papel",
   "title": "Sistemas internos sob medida | CProject",
   "desc": "Sistemas web sob medida para agenda, cadastros, atendimento e processos que hoje dependem de planilha, papel ou WhatsApp manual.",
   "card": "Arquitetura sob medida para o fluxo de trabalho de cada operação, sem template genérico.",
   "lead": "Agenda em papel, atendimento manual no WhatsApp, planilha improvisada: mapeamos o processo que trava a operação e construímos o sistema que encaixa no jeito que a sua equipe já trabalha.",
   "entra": ["Diagnóstico do processo manual antes de qualquer tela", "Cadastros, agenda, controle de atendimentos e de etapas", "Acesso por login, com perfis para cada tipo de usuário", "Banco de dados com regras de acesso por linha (Supabase)", "Evolução em ciclos curtos, com você acompanhando cada entrega"],
   "quem": ["Operações pequenas e médias sem TI dedicado", "Times que perdem tempo copiando dado de um lugar para outro", "Negócios de agenda e atendimento, como clínicas e salões"],
   "faq": [("Preciso saber exatamente o que quero antes de começar?", "Não. O primeiro passo é um diagnóstico do processo atual, justamente para entender onde o sistema precisa entrar."),
           ("Em quanto tempo vejo algo funcionando?", "A primeira versão navegável sai em poucos dias, já com dados reais e fluxo de uso, não uma tela estática para aprovar."),
           ("Quem cuida do sistema depois da entrega?", "Ajustes e evolução são combinados direto com quem construiu, sem intermediário e sem fila de ticket.")],
   "wa": "Olá! Vim pelo site e quero falar sobre um sistema sob medida."},
  {"slug": "dashboards-e-bi", "nome": "Dashboards & BI", "tit": "Dashboards e BI",
   "h1": "Dashboards que transformam dados espalhados em decisão visual",
   "title": "Dashboards e BI sob medida | CProject",
   "desc": "Painéis de indicadores sob medida que reúnem dados de planilhas e sistemas em uma visão clara para decidir rápido.",
   "card": "Dados complexos transformados em decisão visual, sem planilha para garimpar.",
   "lead": "Os números do negócio costumam estar em planilhas, sistemas e conversas diferentes. Reunimos essas fontes em um painel único, com os indicadores que realmente orientam a sua decisão.",
   "entra": ["Levantamento dos indicadores que importam para a decisão", "Integração com planilhas, bancos de dados e sistemas existentes", "Painel web acessível de qualquer dispositivo", "Filtros por período, unidade, equipe ou produto", "Controle de quem pode ver o quê"],
   "quem": ["Gestores que montam relatório na mão toda semana", "Operações com dados espalhados em várias ferramentas", "Equipes que precisam acompanhar metas em tempo real"],
   "faq": [("Preciso trocar as ferramentas que já uso?", "Não necessariamente. O painel pode ler dados das planilhas e sistemas que você já usa."),
           ("O painel atualiza sozinho?", "Quando a fonte de dados permite integração, sim. Isso é definido no diagnóstico, caso a caso."),
           ("Funciona no celular?", "Sim. O painel é web e se adapta à tela do celular.")],
   "wa": "Olá! Vim pelo site e quero falar sobre um dashboard."},
  {"slug": "automacao-de-processos", "nome": "Automação de processos", "tit": "Automação de processos",
   "h1": "Automação de processos e WhatsApp para tirar tarefa repetitiva da equipe",
   "title": "Automação de processos e WhatsApp | CProject",
   "desc": "Integrações e automações que eliminam tarefas repetitivas, incluindo automações via WhatsApp para confirmação, lembretes e atendimento.",
   "card": "Integração entre sistemas que tira tarefa repetitiva da mão da equipe, incluindo automações via WhatsApp.",
   "lead": "Confirmar horário, mandar lembrete, copiar cadastro de um sistema para outro: tarefas que tomam horas da equipe e podem rodar sozinhas, inclusive pelo WhatsApp.",
   "entra": ["Mapeamento das tarefas repetitivas e do custo de cada uma", "Integração entre sistemas, formulários e planilhas", "Automações via WhatsApp para confirmações e lembretes", "Notificações automáticas para a equipe", "Registro do que foi executado, para conferência"],
   "quem": ["Negócios de agenda que confirmam horário um a um", "Equipes que digitam a mesma informação em vários lugares", "Operações que querem crescer sem aumentar retrabalho"],
   "faq": [("Dá para automatizar mensagens no WhatsApp?", "Sim. Confirmações, lembretes e avisos podem ser enviados automaticamente, seguindo as regras de uso do WhatsApp."),
           ("Preciso de um sistema novo para automatizar?", "Nem sempre. Muitas automações conectam as ferramentas que você já usa."),
           ("E se a automação falhar?", "As automações registram o que foi executado, para a equipe conferir e agir quando algo sair do esperado.")],
   "wa": "Olá! Vim pelo site e quero falar sobre automação de processos."},
]

PASSOS = [("Diagnóstico", "Mapeamento do processo manual que está travando a operação, seja agenda em papel, atendimento manual no WhatsApp ou planilha improvisada."),
          ("Protótipo funcional", "Primeira versão navegável em poucos dias, já com dados reais e fluxo de uso, não uma tela estática para aprovar."),
          ("Construção incremental", "Ciclos curtos de desenvolvimento, com você acompanhando cada entrega e código pensado para evoluir sem retrabalho."),
          ("Entrega e suporte direto", "Sistema no ar, com ajustes e evolução conversando direto com quem construiu, sem intermediário.")]

FAQ_HOME = [("O que a CProject faz?", "A CProject reúne três frentes: um estúdio que desenvolve sites, sistemas, dashboards e automações sob medida; produtos próprios, como o CliniqLab e o Embelezando; e um hub de soluções prontas para profissionais, como packs de skills de IA."),
            ("Quanto tempo leva para ver algo funcionando?", "A primeira versão navegável sai em poucos dias, já com dados reais e fluxo de uso. Depois o projeto evolui em ciclos curtos, com você acompanhando cada entrega."),
            ("Vocês trabalham com template?", "Não. Interface e código são feitos sob medida para cada operação, o que facilita evoluir depois sem retrabalho."),
            ("Os produtos CliniqLab e Embelezando já estão disponíveis?", "O CliniqLab está em pré-lançamento e o Embelezando em desenvolvimento. Fale com a gente pelo WhatsApp para entrar na lista de espera."),
            ("Como funciona o suporte depois da entrega?", "Ajustes e evolução são conversados direto com quem construiu o projeto, sem intermediário e sem fila de ticket.")]

def head(title, desc, path, schema, extra=""):
    url = BASE + path
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#07122A">
<meta property="og:type" content="website"><meta property="og:locale" content="pt_BR"><meta property="og:site_name" content="CProject">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/assets/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="CProject: estúdio, produtos e hub">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{BASE}/assets/og.png">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/geist.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css?v={V}">
{extra}<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(",", ":"))}</script>
</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>'''

def nav(home=True, atual=""):
    p = "" if home else "/"
    links = [("Estúdio", f"{p}#estudio"), ("Produtos", f"{p}#produtos"), ("Hub", f"{p}#hub"), ("Case", f"{p}#case"), ("Contato", f"{p}#contato")]
    lis = "".join(f'<li><a href="{h}">{t}</a></li>' for t, h in links)
    return f'''<header class="nav" id="topo">
  <div class="in">
    <a class="logo" href="/" aria-label="CProject, página inicial">{LOGO}<span>CPr<i>oject</i></span></a>
    <button class="burg" type="button" aria-label="Abrir menu" aria-expanded="false" aria-controls="menu"><span></span></button>
    <ul id="menu">{lis}</ul>
    <a class="btn nb" href="{wa("Olá! Vim pelo site da CProject e quero conversar.")}" target="_blank" rel="noopener" data-origem="nav">Vamos conversar</a>
  </div>
</header>'''

def rodape():
    sv = "".join(f'<li><a href="/{s["slug"]}/">{s["nome"]}</a></li>' for s in SERVICOS)
    return f'''<footer>
  <div class="in">
    <div class="fg">
      <div><a class="logo" href="/" aria-label="CProject, página inicial">{LOGO}<span>CPr<i>oject</i></span></a>
        <p>Estúdio full-stack, produtos próprios e soluções prontas para profissionais, do rascunho ao produto no ar.</p></div>
      <div><h3 class="fh">Estúdio</h3><ul>{sv}</ul></div>
      <div><h3 class="fh">Ecossistema</h3><ul><li><a href="/#produtos">CliniqLab</a></li><li><a href="/#produtos">Embelezando</a></li><li><a href="/#hub">Packs de skills</a></li><li><a href="/#case">Case</a></li></ul></div>
      <div><h3 class="fh">Contato</h3><ul><li><a href="{wa("Olá! Vim pelo site da CProject.")}" target="_blank" rel="noopener" data-origem="rodape">WhatsApp {WA_FMT}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{IG}" target="_blank" rel="noopener">@cproject.dev</a></li><li><a href="/politica-de-privacidade/">Política de privacidade</a></li></ul></div>
    </div>
    <div class="cp"><span>© {datetime.date.today().year} CProject · Bruno C. Peres</span><span>Feito sob medida, do rascunho ao produto no ar.</span></div>
  </div>
</footer>
<a class="wa" href="{{WAF}}" target="_blank" rel="noopener" aria-label="Conversar no WhatsApp" data-origem="flutuante">{I_WA}</a>
<script src="/assets/site.js?v={V}" defer></script>
</body>
</html>
'''

ORG = {"@type": ["Organization", "ProfessionalService"], "@id": BASE + "/#org", "name": "CProject", "alternateName": "CProject Estúdio Digital",
       "url": BASE + "/", "logo": BASE + "/assets/icons/icon-512.png", "image": BASE + "/assets/og.png",
       "description": "Estúdio full-stack de sites, sistemas, dashboards e automações sob medida, com produtos próprios e soluções para profissionais.",
       "email": EMAIL, "telephone": "+55-13-97417-7986", "founder": {"@type": "Person", "name": "Bruno C. Peres"},
       "sameAs": [IG], "areaServed": {"@type": "Country", "name": "Brasil"},
       "contactPoint": {"@type": "ContactPoint", "telephone": "+55-13-97417-7986", "contactType": "customer service", "availableLanguage": "Portuguese"}}

def faq_schema(faq): return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
def faq_html(faq): return "".join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq)

def home():
    schema = {"@context": "https://schema.org", "@graph": [ORG,
        {"@type": "WebSite", "@id": BASE + "/#site", "url": BASE + "/", "name": "CProject", "inLanguage": "pt-BR", "publisher": {"@id": BASE + "/#org"}},
        faq_schema(FAQ_HOME)]}
    title = "CProject · Sites, sistemas e apps sob medida"
    desc = "Estúdio full-stack de sites, sistemas, dashboards e automações sob medida, com produtos próprios e soluções prontas para profissionais."
    sv = "".join(f'''<article class="card rv"><span class="n">0{i+1}</span><h3>{s["nome"]}</h3><p>{s["card"]}</p><a class="lk" href="/{s["slug"]}/">Ver {s["nome"].lower()} {I_SETA}</a></article>''' for i, s in enumerate(SERVICOS))
    ps = "".join(f'<article class="card rv"><h3>{t}</h3><p>{d}</p></article>' for t, d in PASSOS)
    out = head(title, desc, "/", schema, '<link rel="preload" href="/assets/fonts/jbmono.woff2" as="font" type="font/woff2" crossorigin>\n') + nav() + f'''
<main id="conteudo">
<section class="hero" aria-labelledby="h1">
  <canvas id="hero-cv" aria-hidden="true"></canvas>
  <div class="in">
    <span class="eb">CProject · estúdio, produtos e hub</span>
    <h1 id="h1">Sites, sistemas e apps <em class="g">sob medida</em>, do rascunho ao produto no ar.</h1>
    <p class="lead">Um estúdio full-stack que também cria produtos próprios e soluções prontas para profissionais.</p>
    <div class="ctas">
      <a class="btn" href="{wa("Olá! Vim pelo site da CProject e quero agendar a conversa de 15 minutos.")}" target="_blank" rel="noopener" data-origem="hero">{I_WA} Agendar conversa de 15 min</a>
      <a class="btn o" href="#produtos">Conhecer os produtos</a>
    </div>
    <div class="stack" aria-label="Tecnologias"><span>Next.js</span><span>React</span><span>Supabase</span><span>Vercel</span></div>
  </div>
</section>

<section class="sec" id="frentes" aria-labelledby="t-frentes">
  <div class="in">
    <div class="hd rv"><span class="eb">01 · Ecossistema</span><h2 id="t-frentes">Três frentes, <em class="g">um único fluxo</em></h2><p>O mesmo time que desenvolve sob medida para clientes constrói produtos próprios e empacota o que funciona em soluções prontas.</p></div>
    <div class="fr">
      <article class="card hl rv"><span class="n">ESTÚDIO</span><h3>Sob medida para a sua operação</h3><p>Sites, sistemas internos, dashboards e automações construídos do zero para o processo de cada cliente.</p><a class="lk" href="#estudio">Ver serviços {I_SETA}</a></article>
      <article class="card rv"><span class="n">PRODUTOS</span><h3>Sistemas próprios por assinatura</h3><p>Plataformas da CProject para segmentos específicos, começando por clínicas e salões de beleza.</p><a class="lk" href="#produtos">Ver produtos {I_SETA}</a></article>
      <article class="card rv"><span class="n">HUB</span><h3>Soluções prontas para profissionais</h3><p>Packs de skills de IA e materiais para quem quer ganhar tempo no dia a dia sem contratar um projeto inteiro.</p><a class="lk" href="#hub">Ver o hub {I_SETA}</a></article>
    </div>
  </div>
</section>

<section class="sec alt" id="estudio" aria-labelledby="t-estudio">
  <div class="in">
    <div class="hd rv"><span class="eb">02 · Estúdio</span><h2 id="t-estudio">Quatro serviços, da interface ao back-end</h2><p>Sem passar o projeto entre equipes diferentes no caminho: quem desenha é quem desenvolve e quem dá suporte.</p></div>
    <div class="sv">{sv}</div>
  </div>
</section>

<section class="sec" id="produtos" aria-labelledby="t-produtos">
  <div class="in">
    <div class="hd rv"><span class="eb">03 · Produtos</span><h2 id="t-produtos">Produtos próprios para <em class="g">quem atende com hora marcada</em></h2><p>Sistemas da CProject para negócios que vivem de agenda e relacionamento com o cliente.</p></div>
    <div class="pd">
      <article class="card rv"><div class="top"><div class="mk"><b style="background:#8E80EF">C</b><h3>CliniqLab</h3></div><span class="st">Pré-lançamento</span></div>
        <p>CRM por assinatura para dentistas, nutricionistas e psicólogos: agenda, relacionamento com pacientes e rotina do consultório em um só lugar.</p>
        <a class="lk" href="{wa("Olá! Quero entrar na lista de espera do CliniqLab.")}" target="_blank" rel="noopener" data-origem="cliniqlab">Entrar na lista de espera {I_SETA}</a></article>
      <article class="card rv"><div class="top"><div class="mk"><b style="background:#D9468A">E</b><h3>Embelezando</h3></div><span class="st c">Em desenvolvimento</span></div>
        <p>Sistema de gestão para salões de beleza e barbearias, pensado para a rotina de agenda, atendimento e equipe.</p>
        <a class="lk" href="{wa("Olá! Quero saber quando o Embelezando estiver disponível.")}" target="_blank" rel="noopener" data-origem="embelezando">Quero ser avisado {I_SETA}</a></article>
    </div>
  </div>
</section>

<section class="sec alt" id="hub" aria-labelledby="t-hub">
  <div class="in hub">
    <div class="hd rv"><span class="eb">04 · Hub para profissionais</span><h2 id="t-hub">Soluções prontas para <em class="g">trabalhar melhor com IA</em></h2><p>Nem todo mundo precisa de um sistema sob medida. Para profissionais que querem ganhar tempo agora, o hub reúne ferramentas prontas, construídas a partir do que usamos nos nossos próprios projetos.</p>
      <div class="ctas"><a class="btn" href="{wa("Olá! Quero saber sobre os packs de skills da CProject.")}" target="_blank" rel="noopener" data-origem="hub">Quero ser avisado do lançamento</a></div></div>
    <div class="pk">
      <article class="card rv"><span class="ic">{I_PACK}</span><div><h3>Packs de skills de IA</h3><p>Conjuntos de skills prontas para delegar tarefas recorrentes à IA, como redação, relatórios e atendimento.</p><span class="st c" style="margin-top:12px">Em breve</span></div></article>
      <article class="card rv"><span class="ic">{I_SPARK}</span><div><h3>Conteúdo e formação em IA</h3><p>Materiais práticos para aplicar inteligência artificial na rotina profissional, sem jargão técnico.</p><span class="st c" style="margin-top:12px">Em breve</span></div></article>
      <article class="card rv"><span class="ic">{I_DOC}</span><div><h3>Modelos e templates</h3><p>Estruturas prontas de processos, páginas e painéis para adaptar ao seu negócio.</p><span class="st c" style="margin-top:12px">Em breve</span></div></article>
    </div>
  </div>
</section>

<section class="sec" id="abordagem" aria-labelledby="t-ab">
  <div class="in">
    <div class="hd rv"><span class="eb">05 · Abordagem</span><h2 id="t-ab">Como o projeto acontece</h2><p>Nada de tela solta ou protótipo estático: cada etapa já entrega algo que roda de verdade.</p></div>
    <div class="ps">{ps}</div>
  </div>
</section>

<section class="sec alt" id="case" aria-labelledby="t-case">
  <div class="in cs">
    <div class="rv"><span class="eb">06 · Case</span><h2 id="t-case" style="font-size:var(--h2);margin-top:16px">Fundação Virgínia Ferraz</h2>
      <p style="color:var(--tx-2);margin-top:16px">Site institucional da Fundação Virgínia Ferraz, organização sem fins lucrativos ligada à ISTV, a serviço da cultura, da educação e da cidadania na Baixada Santista. Além da apresentação pública, o projeto inclui um painel administrativo próprio para a equipe gerenciar álbuns, agenda, notícias e eventos sem depender de suporte técnico.</p>
      <div class="meta"><div><small>Páginas</small><b>8</b></div><div><small>Áreas de atuação</small><b>6</b></div><div><small>Painel admin</small><b>Sim</b></div></div>
      <div class="tags"><span>Next.js</span><span>Vercel</span><span>Painel administrativo</span><span>No ar</span></div>
      <div class="ctas"><a class="btn o" href="https://fvf-site-dun.vercel.app/" target="_blank" rel="noopener">Visitar o site ↗</a></div></div>
    <figure class="mock rv" aria-hidden="true"><div class="bar"><i></i><i></i><i></i><span>fvf-site-dun.vercel.app</span></div><div class="bd"><div class="t"></div><div style="width:84%"></div><div style="width:70%"></div><div class="g"><span></span><span></span><span></span></div><div style="width:52%"></div></div></figure>
  </div>
</section>

<section class="sec" id="quem" aria-labelledby="t-quem">
  <div class="in cs">
    <div class="rv"><span class="eb">07 · Quem constrói</span><h2 id="t-quem" style="font-size:var(--h2);margin-top:16px">Um fluxo, do briefing ao suporte</h2>
      <p style="color:var(--tx-2);margin-top:16px">A CProject é conduzida por Bruno C. Peres, que reúne desenvolvimento full-stack, product design e relacionamento com o cliente em um único fluxo de trabalho. O mesmo time acompanha o projeto do briefing ao suporte pós-entrega, sem repasse entre áreas no caminho.</p>
      <div class="pills"><span>Full-stack</span><span>Comunicação direta</span><span>Entrega incremental</span><span>Código sob medida</span><span>Suporte pós-entrega</span></div></div>
    <dl class="ft rv"><div><dt>Responsável</dt><dd>Bruno C. Peres</dd></div><div><dt>Formação</dt><dd>ADS, FATEC</dd></div><div><dt>Papéis</dt><dd>Full-stack + Product Design</dd></div><div><dt>Stack</dt><dd>Next.js · React · Supabase</dd></div><div><dt>Instagram</dt><dd><a href="{IG}" target="_blank" rel="noopener">@cproject.dev</a></dd></div></dl>
  </div>
</section>

<section class="sec alt" id="faq" aria-labelledby="t-faq">
  <div class="in">
    <div class="hd rv"><span class="eb">08 · Perguntas frequentes</span><h2 id="t-faq">Antes de conversar</h2></div>
    <div class="faq rv">{faq_html(FAQ_HOME)}</div>
  </div>
</section>

<section class="sec" id="contato" aria-labelledby="t-ct">
  <div class="in ct">
    <div class="rv"><span class="eb">09 · Contato</span><h2 id="t-ct" style="font-size:var(--h2);margin-top:16px">Vamos conversar 15 minutos sobre o seu processo?</h2>
      <p style="color:var(--tx-2);margin-top:16px">Sem proposta engessada nem jargão técnico: só entender a dor da operação e ver se faz sentido construir algo sob medida, usar um dos nossos produtos ou começar pelo hub.</p>
      <div class="ch">
        <a href="{wa("Olá! Vim pelo site da CProject e quero conversar.")}" target="_blank" rel="noopener" data-origem="contato">{I_WA}<span><small>WhatsApp</small>{WA_FMT}</span></a>
        <a href="mailto:{EMAIL}">{I_MAIL}<span><small>E-mail</small>{EMAIL}</span></a>
        <a href="{IG}" target="_blank" rel="noopener">{I_IG}<span><small>Instagram</small>@cproject.dev</span></a>
      </div></div>
    <form class="fm rv" id="fm" novalidate aria-label="Enviar mensagem pelo WhatsApp">
      <div class="fl"><label for="f-nome">Nome</label><input id="f-nome" name="nome" autocomplete="name" required></div>
      <div class="fl"><label for="f-emp">Empresa</label><input id="f-emp" name="empresa" autocomplete="organization"></div>
      <div class="fl w"><label for="f-int">Interesse</label><select id="f-int" name="interesse" required><option value="">Selecione</option><option>Site ou aplicativo</option><option>Sistema sob medida</option><option>Dashboard ou BI</option><option>Automação de processos</option><option>CliniqLab</option><option>Embelezando</option><option>Packs de skills de IA</option><option>Outro assunto</option></select></div>
      <div class="fl w"><label for="f-msg">O que você precisa?</label><textarea id="f-msg" name="mensagem" required placeholder="Conte em poucas linhas o processo que hoje dá trabalho."></textarea></div>
      <div class="hp" aria-hidden="true"><label for="f-site">Site</label><input id="f-site" name="site" tabindex="-1" autocomplete="off"></div>
      <button class="btn" type="submit">{I_WA} Enviar pelo WhatsApp</button>
      <p class="fmsg" id="fmsg" role="status" aria-live="polite">A mensagem abre pronta no WhatsApp. Nenhum dado fica salvo no site.</p>
    </form>
  </div>
</section>
</main>
''' + rodape().replace("{WAF}", E(wa("Olá! Vim pelo site da CProject e quero conversar.")))
    return out

def servico(s):
    path = f'/{s["slug"]}/'
    outros = [o for o in SERVICOS if o is not s]
    schema = {"@context": "https://schema.org", "@graph": [ORG,
        {"@type": "Service", "name": s["tit"], "description": s["desc"], "provider": {"@id": BASE + "/#org"}, "areaServed": {"@type": "Country", "name": "Brasil"}, "url": BASE + path},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Início", "item": BASE + "/"}, {"@type": "ListItem", "position": 2, "name": s["tit"], "item": BASE + path}]},
        faq_schema(s["faq"])]}
    lis = lambda xs: "".join(f"<li>{E(x)}</li>" for x in xs)
    ps = "".join(f'<article class="card rv"><h3>{t}</h3><p>{d}</p></article>' for t, d in PASSOS)
    ot = "".join(f'<article class="card rv"><span class="n">ESTÚDIO</span><h3>{o["nome"]}</h3><p>{o["card"]}</p><a class="lk" href="/{o["slug"]}/">Ver {o["nome"].lower()} {I_SETA}</a></article>' for o in outros)
    return head(s["title"], s["desc"], path, schema) + nav(False) + f'''
<main id="conteudo">
<section class="ph" aria-labelledby="h1">
  <div class="in">
    <nav aria-label="Trilha"><ol class="bc"><li><a href="/">Início</a></li><li><a href="/#estudio">Estúdio</a></li><li aria-current="page">{s["nome"]}</li></ol></nav>
    <h1 id="h1">{E(s["h1"])}</h1>
    <p class="lead">{E(s["lead"])}</p>
    <div class="ctas"><a class="btn" href="{wa(s["wa"])}" target="_blank" rel="noopener" data-origem="servico">{I_WA} Falar sobre {s["nome"].lower()}</a><a class="btn o" href="#como">Como funciona</a></div>
  </div>
</section>
<section class="sec alt" aria-labelledby="t-entra">
  <div class="in two">
    <article class="card rv"><span class="n">ESCOPO</span><h2 id="t-entra" class="sr">O que entra</h2><h3>O que entra no projeto</h3><ul>{lis(s["entra"])}</ul></article>
    <article class="card rv"><span class="n">PARA QUEM</span><h3>Para quem faz sentido</h3><ul>{lis(s["quem"])}</ul></article>
  </div>
</section>
<section class="sec" id="como" aria-labelledby="t-como">
  <div class="in"><div class="hd rv"><span class="eb">Como funciona</span><h2 id="t-como">Do diagnóstico ao sistema no ar</h2></div><div class="ps">{ps}</div></div>
</section>
<section class="sec alt" aria-labelledby="t-faq">
  <div class="in"><div class="hd rv"><span class="eb">Perguntas frequentes</span><h2 id="t-faq">Dúvidas sobre {s["nome"].lower()}</h2></div><div class="faq rv">{faq_html(s["faq"])}</div>
    <div class="ctas"><a class="btn" href="{wa(s["wa"])}" target="_blank" rel="noopener" data-origem="servico-faq">{I_WA} Conversar sobre o meu projeto</a></div></div>
</section>
<section class="sec" aria-labelledby="t-outros">
  <div class="in"><div class="hd rv"><span class="eb">Outros serviços</span><h2 id="t-outros">Também no estúdio</h2></div><div class="sv" style="grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr))">{ot}</div></div>
</section>
</main>
''' + rodape().replace("{WAF}", E(wa(s["wa"])))

def politica():
    schema = {"@context": "https://schema.org", "@graph": [ORG, {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Início", "item": BASE + "/"}, {"@type": "ListItem", "position": 2, "name": "Política de privacidade", "item": BASE + "/politica-de-privacidade/"}]}]}
    return head("Política de privacidade | CProject", "Como a CProject trata dados pessoais no site: sem cookies de rastreamento, contato apenas pelos canais que você escolher.", "/politica-de-privacidade/", schema) + nav(False) + f'''
<main id="conteudo">
<section class="ph" aria-labelledby="h1"><div class="in"><nav aria-label="Trilha"><ol class="bc"><li><a href="/">Início</a></li><li aria-current="page">Privacidade</li></ol></nav><h1 id="h1">Política de privacidade</h1><p class="lead">Atualizada em {datetime.date.today().strftime("%d/%m/%Y")}.</p></div></section>
<section class="sec" style="padding-top:0"><div class="in prose">
<h2>Quem somos</h2><p>Este site é da CProject, conduzida por Bruno C. Peres. Contato para assuntos de privacidade: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Quais dados coletamos</h2><p>O site não usa cookies de rastreamento, ferramentas de análise ou publicidade. O formulário de contato não grava dados no site: ele apenas monta uma mensagem que é aberta no seu WhatsApp, e o envio só acontece se você confirmar.</p>
<h2>Serviços de terceiros</h2><ul><li><b>WhatsApp (Meta):</b> recebe as mensagens que você decidir enviar pelos botões e pelo formulário, conforme a política de privacidade do WhatsApp.</li><li><b>Vercel:</b> hospeda o site e pode registrar dados técnicos de acesso, como endereço IP, para segurança e funcionamento.</li><li><b>Instagram e e-mail:</b> usados apenas quando você escolhe falar com a gente por esses canais.</li></ul>
<h2>Para que usamos os dados</h2><p>Para responder ao seu contato e, se você quiser, conversar sobre um projeto ou produto. Não vendemos nem compartilhamos dados para fins de marketing.</p>
<h2>Seus direitos (LGPD)</h2><p>Você pode pedir acesso, correção ou exclusão dos dados que nos enviou, escrevendo para <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div></section>
</main>
''' + rodape().replace("{WAF}", E(wa("Olá! Vim pelo site da CProject.")))

def nao_achou():
    return head("Página não encontrada | CProject", "A página que você procurou não existe.", "/404", {"@context": "https://schema.org", "@graph": [ORG]}).replace('<link rel="canonical" href="' + BASE + '/404">', '<meta name="robots" content="noindex">') + nav(False) + f'''
<main id="conteudo"><section class="ph" aria-labelledby="h1"><div class="in"><span class="eb">Erro 404</span><h1 id="h1">Esta página não existe, mas o resto do site sim.</h1><p class="lead">O endereço pode ter mudado. Volte para o início ou fale com a gente.</p><div class="ctas"><a class="btn" href="/">Voltar ao início</a><a class="btn o" href="/#contato">Contato</a></div></div></section></main>
''' + rodape().replace("{WAF}", E(wa("Olá! Vim pelo site da CProject.")))

def escrever(rel, txt):
    p = RAIZ / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(txt, encoding="utf-8")

escrever("index.html", home())
for s in SERVICOS: escrever(f'{s["slug"]}/index.html', servico(s))
escrever("politica-de-privacidade/index.html", politica())
escrever("404.html", nao_achou())
urls = ["/"] + [f'/{s["slug"]}/' for s in SERVICOS] + ["/politica-de-privacidade/"]
escrever("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{BASE}{u}</loc><lastmod>{HOJE}</lastmod></url>\n" for u in urls) + "</urlset>\n")
escrever("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
print("ok", urls)
