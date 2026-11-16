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
V = "5"  # versão dos assets

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

FAQ_HOME = [("O que a CProject faz?", "A CProject reúne três frentes: um estúdio que desenvolve sites, sistemas, dashboards e automações sob medida; os Sistemas Lab, como o Sorrirmos e o Cortando; e soluções prontas, como landing pages, BI em template e packs de skills de IA."),
            ("Quanto custa o Sorrirmos?", "O Sorrirmos tem três planos: Starter por R$ 89,90 por mês, Professional por R$ 199,90 por mês e Max Clinic por R$ 499,90 por mês. Nos contratos mensais há uma taxa única de implantação de R$ 297; no plano anual a implantação é isenta."),
            ("Qual a diferença entre a landing page Template e a Hospedada?", "A Landing Page Template custa R$ 297 em pagamento único. A Hospedada custa R$ 297 de implantação mais R$ 50 por mês, e a CProject cuida da publicação e da hospedagem da página. Para design e textos totalmente sob medida, a Landing Page Personalizada parte de R$ 997."),
            ("O BI em template precisa de hospedagem?", "Não é obrigatório. O BI Template custa R$ 100 em pagamento único. Se preferir o painel publicado e mantido pela CProject, a opção BI Template + Hospedagem custa R$ 100 de implantação mais R$ 50 por mês."),
            ("E se eu precisar de algo fora dos planos?", "Sistemas, sites, automações e BI personalizados entram no CProject Custom, com orçamento feito a partir de uma conversa sobre o seu processo."),
            ("Vocês trabalham com template?", "Nos projetos sob medida, não: interface e código são feitos para cada operação. Os templates existem como opção mais rápida e econômica, com landing pages e painéis de BI prontos para adaptar à sua marca."),
            ("Como funciona o suporte depois da entrega?", "Ajustes e evolução são conversados direto com quem construiu o projeto, sem intermediário e sem fila de ticket.")]

# ---------- planos (CProject Lab) ----------
# preço: (inteiro, centavos, sufixo) ou None quando em definição
PLANOS = [
  {"id": "sistemas", "aba": "Sistemas Lab", "titulo": "Sistemas Lab por assinatura",
   "intro": "Sistemas prontos da CProject para negócios que vivem de agenda e relacionamento com o cliente.",
   "produto": {"nome": "Sorrirmos", "cor": "#8E80EF", "letra": "S", "seg": "Gestão para clínicas odontológicas",
               "todos": ["Agenda e cadastro de pacientes em um só lugar", "Lembrete automático pelo WhatsApp na véspera da consulta", "Confirmação do paciente com um toque", "WhatsApp oficial, com o custo das mensagens já incluso", "Aceite de LGPD antes de qualquer envio"]},
   "planos": [
     {"nome": "Starter", "tag": "Para começar", "para": "Para o consultório que quer tirar a agenda do papel e parar de confirmar horário um a um.", "preco": ("89", "90", "/mês"), "cond": "+ R$ 297 de implantação no plano mensal"},
     {"nome": "Professional", "tag": "Para crescer", "para": "Para clínicas com agenda cheia, que precisam de lembretes e confirmações rodando todos os dias.", "preco": ("199", "90", "/mês"), "cond": "+ R$ 297 de implantação no plano mensal", "hl": True},
     {"nome": "Max Clinic", "tag": "Operação completa", "para": "Para clínicas com mais cadeiras e equipe maior, que precisam de tudo no mesmo sistema.", "preco": ("499", "90", "/mês"), "cond": "+ R$ 297 de implantação no plano mensal"},
   ],
   "nota": "Plano anual com implantação isenta. Os recursos de cada plano são apresentados na demonstração.",
   "extra": {"nome": "Cortando", "cor": "#D9468A", "letra": "C", "seg": "Gestão para barbearias e salões de beleza", "status": "Planos em definição",
             "txt": "Agenda, atendimento e equipe da barbearia em um só sistema.", "cta": "Quero ser avisado", "wa": "Olá! Quero ser avisado quando os planos do Cortando estiverem disponíveis."}},
  {"id": "landing", "aba": "Landing pages", "titulo": "Landing pages",
   "intro": "Do modelo pronto ao projeto sob medida, com WhatsApp, formulário e página preparada para o Google.",
   "planos": [
     {"nome": "Landing Page Template", "cta": "Quero a Template", "tag": "Mais rápida", "para": "Um modelo pronto da CProject adaptado à sua marca, para colocar a página no ar sem esperar um projeto inteiro.", "preco": ("297", None, ""), "cond": "pagamento único",
      "itens": ["Página única com as cores, o logo e os textos da sua marca", "Layout responsivo para celular e computador", "Botão de WhatsApp e formulário de contato", "Arquivos entregues para publicar onde preferir"]},
     {"nome": "Landing Page Hospedada", "cta": "Quero a Hospedada", "tag": "Sem dor de cabeça", "para": "O mesmo modelo, publicado e mantido no ar pela CProject.", "preco": ("297", None, ""), "cond": "de implantação + R$ 50/mês", "hl": True,
      "itens": ["Tudo da Landing Page Template", "Publicação e hospedagem por conta da CProject", "Certificado SSL e configuração do seu domínio", "Você não precisa cuidar de servidor"]},
     {"nome": "Landing Page Personalizada", "cta": "Quero a Personalizada", "tag": "Sob medida", "para": "Design, estrutura e textos criados do zero para a sua oferta e o seu público.", "preco": ("997", None, ""), "pre": "a partir de", "cond": "valor final conforme o escopo",
      "itens": ["Design próprio, sem modelo pronto", "Copy escrita para a sua oferta", "SEO por página e dados estruturados para o Google", "Medição de cliques no WhatsApp e no formulário"]},
   ]},
  {"id": "bi", "aba": "BI & dados", "titulo": "BI e inteligência de dados",
   "intro": "Painéis prontos para transformar planilha em indicador, sem montar relatório na mão toda semana.",
   "planos": [
     {"nome": "BI Template", "tag": "Para começar", "para": "Um painel modelo da CProject para organizar os indicadores do seu negócio.", "preco": ("100", None, ""), "cond": "pagamento único",
      "itens": ["Painel pronto com os indicadores principais", "Ajustado aos dados da sua planilha", "Visual limpo para decidir rápido"]},
     {"nome": "BI Template + Hospedagem", "cta": "Quero com hospedagem", "tag": "Acesso por link", "para": "O mesmo painel, publicado e mantido pela CProject.", "preco": ("100", None, ""), "cond": "de implantação + R$ 50/mês", "hl": True,
      "itens": ["Tudo do BI Template", "Painel publicado, acessível de qualquer dispositivo", "Hospedagem por conta da CProject"]},
   ],
   "nota": "Precisa de um BI com as suas fontes de dados e regras próprias? Veja o CProject Custom."},
  {"id": "skills", "aba": "Packs de skills", "titulo": "Packs de skills de IA",
   "intro": "Skills prontas para delegar à IA tarefas recorrentes, como redação, relatórios e atendimento. Do Mini ao Master, cada nível reúne mais skills.",
   "packs": [("Mini", "79", "90"), ("Essencial", "149", "90"), ("Avançado", "249", "90"), ("Completo", "349", "90"), ("Master", "499", "90")]},
  {"id": "eventos", "aba": "Event Coverage", "titulo": "Event Coverage",
   "intro": "Soluções da CProject para cobertura de eventos, em fase final de definição de preços.",
   "planos": [
     {"nome": "Event Coverage Kit", "tag": "Em breve", "para": "Kit para cobertura de eventos.", "preco": None, "cond": "preço em definição"},
     {"nome": "Event Coverage SaaS", "tag": "Em breve", "para": "Plataforma por assinatura para cobertura de eventos.", "preco": None, "cond": "preço em definição"},
   ]},
  {"id": "custom", "aba": "Custom", "titulo": "CProject Custom",
   "intro": "Quando nenhum plano encaixa, o projeto é feito do zero para o seu processo, com orçamento sob medida.",
   "custom": [("Sistemas personalizados", "Agenda, cadastros, atendimento e etapas do jeito que a sua equipe trabalha.", "/sistemas-sob-medida/"),
              ("Sites e plataformas", "Sites institucionais e plataformas web com painel próprio para a equipe.", "/sites-e-apps/"),
              ("Automações", "Integrações e automações, inclusive pelo WhatsApp, que tiram tarefa repetitiva da equipe.", "/automacao-de-processos/"),
              ("BI personalizado", "Painéis conectados às suas fontes de dados, com os indicadores que orientam a decisão.", "/dashboards-e-bi/")]},
]

PORTFOLIO = [
  {"slug": "gelomac", "nome": "Gelomac", "seg": "Climatização comercial e industrial · Santos, SP", "url": "https://gelomac.com.br/", "host": "gelomac.com.br", "tags": ["Landing page", "SEO local", "Orçamento pelo WhatsApp"]},
  {"slug": "yamam", "nome": "Grupo Yamam", "seg": "Segurança patrimonial, portaria e limpeza · SP e Baixada Santista", "url": "https://grupo-yamam.vercel.app/", "host": "grupo-yamam.vercel.app", "tags": ["Site institucional", "SEO", "Blog"]},
  {"slug": "antonelze", "nome": "Antonelze", "seg": "Moda feminina e vestidos de festa · Santos, SP", "url": "https://antonelze.vercel.app/", "host": "antonelze.vercel.app", "tags": ["Vitrine de produtos", "Atendimento pelo WhatsApp"]},
  {"slug": "dream4team", "nome": "Dream4Team", "seg": "Estúdio independente de jogos", "url": "https://dream4team.vercel.app/", "host": "dream4team.vercel.app", "tags": ["Site institucional", "Portfólio de jogos"]},
  {"slug": "bonomi", "nome": "Bonomi Almeida", "seg": "Advocacia · Estado de São Paulo", "url": "https://bonomi-almeida.vercel.app/", "host": "bonomi-almeida.vercel.app", "tags": ["Site institucional", "Áreas de atuação"]},
]

TIME = [
  ("BP", "Bruno C. Peres", "Desenvolvimento", "Especialista em desenvolvimento de sistemas", "Desenvolvedor full-stack e product designer. Transforma o processo do cliente em sistema, da primeira tela ao banco de dados.", ["Full-stack", "Product design", "ADS · FATEC"]),
  ("GR", "Gustavo Recouso", "Desenvolvimento", "Especialista em desenvolvimento de sistemas", "Cuida da construção e da evolução dos sistemas, para que cada entrega rode com estabilidade e cresça sem retrabalho.", ["Sistemas", "Integrações", "Evolução contínua"]),
  ("PR", "Pedro Rua", "Marketing & analytics", "Analista de marketing e analytics", "Conecta produto, comunicação e dados: posicionamento, landing pages que convertem, CRM e painéis que mostram o que está funcionando.", ["Marketing", "CRM", "Analytics e BI"]),
]

def time_html():
    return "".join(f'''<article class="pp rv"><div class="av" aria-hidden="true"><span>{ini}</span></div><div class="pbody"><p class="pro">{E(area)}</p><h3>{E(nome)}</h3><p class="pr-r">{E(papel)}</p><p class="pr-d">{E(desc)}</p><ul class="pr-t">{"".join(f"<li>{E(t)}</li>" for t in tags)}</ul></div></article>''' for ini, nome, area, papel, desc, tags in TIME)

def preco_html(p):
    if not p["preco"]:
        return f'<div class="pr"><span class="val tbd">Em definição</span><span class="cond">{E(p["cond"])}</span></div>'
    inte, cent, suf = p["preco"]
    c = f'<i>,{cent}</i>' if cent else ''
    s = f'<small class="suf">{suf}</small>' if suf else ''
    pre = f'<span class="pre">{E(p["pre"])}</span>' if p.get("pre") else ''
    return f'<div class="pr">{pre}<span class="val"><small>R$</small><b>{inte}</b>{c}{s}</span><span class="cond">{E(p["cond"])}</span></div>'

def plano_html(p, grupo):
    hl = " hl" if p.get("hl") else ""
    badge = '<span class="pbadge">Recomendado</span>' if p.get("hl") else ""
    itens = "".join(f"<li>{E(i)}</li>" for i in p.get("itens", []))
    ul = f"<ul>{itens}</ul>" if itens else ""
    if p["preco"]:
        cta_t, msg = p.get("cta", f'Quero o {p["nome"]}'), f'Olá! Vim pelo site da CProject e quero contratar: {(grupo + " " + p["nome"]).strip()}.'
    else:
        cta_t, msg = "Quero ser avisado", f'Olá! Quero ser avisado quando o {p["nome"]} estiver disponível.'
    cls = "btn" if p.get("hl") else "btn o"
    return f'''<article class="plan{hl}">{badge}<div><p class="ptag">{E(p["tag"])}</p><h4>{E(p["nome"])}</h4><p class="pfor">{E(p["para"])}</p></div>{preco_html(p)}{ul}<a class="{cls}" href="{wa(msg)}" target="_blank" rel="noopener" data-origem="plano" data-plano="{E(p["nome"])}">{E(cta_t)}</a></article>'''

def planos_html():
    abas, paineis = [], []
    for i, g in enumerate(PLANOS):
        sel = "true" if i == 0 else "false"
        abas.append(f'<button type="button" role="tab" id="tab-{g["id"]}" aria-controls="pn-{g["id"]}" aria-selected="{sel}" tabindex="{0 if i == 0 else -1}">{E(g["aba"])}</button>')
        corpo = ""
        if "produto" in g:
            pr = g["produto"]
            todos = "".join(f"<li>{E(t)}</li>" for t in pr["todos"])
            corpo += f'''<div class="phead"><div class="mk"><b style="background:{pr["cor"]}">{pr["letra"]}</b><div><h3>{pr["nome"]}</h3><p>{E(pr["seg"])}</p></div></div></div>'''
            corpo += '<div class="plans p3">' + "".join(plano_html(p, pr["nome"]) for p in g["planos"]) + '</div>'
            corpo += f'<div class="incl"><p class="ititle">Em todos os planos do {pr["nome"]}</p><ul>{todos}</ul></div>'
            corpo += f'<p class="pnote">{E(g["nota"])}</p>'
            x = g["extra"]
            corpo += f'''<article class="soon"><div class="mk"><b style="background:{x["cor"]}">{x["letra"]}</b><div><h3>{x["nome"]}</h3><p>{E(x["seg"])}</p></div></div><p class="stx">{E(x["txt"])}</p><span class="st c">{E(x["status"])}</span><a class="lk" href="{wa(x["wa"])}" target="_blank" rel="noopener" data-origem="cortando">{E(x["cta"])} {I_SETA}</a></article>'''
        elif "packs" in g:
            corpo += '<div class="packs">' + "".join(f'''<article class="pack"><h4>{n}</h4><div class="val"><small>R$</small><b>{a}</b><i>,{c}</i></div><a class="lk" href="{wa(f"Olá! Vim pelo site da CProject e quero o Pack de Skills {n}.")}" target="_blank" rel="noopener" data-origem="plano" data-plano="Pack {n}" aria-label="Escolher o pack {n}">Escolher {I_SETA}</a></article>''' for n, a, c in g["packs"]) + '</div>'
        elif "custom" in g:
            corpo += '<div class="custom">' + "".join(f'<article class="card"><h4>{E(t)}</h4><p>{E(d)}</p><a class="lk" href="{h}">Saiba mais {I_SETA}</a></article>' for t, d, h in g["custom"]) + '</div>'
            corpo += f'<div class="ctas"><a class="btn" href="{wa("Olá! Vim pelo site da CProject e quero um orçamento para um projeto sob medida.")}" target="_blank" rel="noopener" data-origem="custom">{I_WA} Pedir orçamento</a></div>'
        else:
            n = len(g["planos"])
            corpo += f'<div class="plans p{n}">' + "".join(plano_html(p, "") for p in g["planos"]) + '</div>'
            if g.get("nota"): corpo += f'<p class="pnote">{E(g["nota"])}</p>'
        paineis.append(f'''<div class="pane" role="tabpanel" id="pn-{g["id"]}" aria-labelledby="tab-{g["id"]}" tabindex="0"><div class="pintro"><h3 class="ptitle">{E(g["titulo"])}</h3><p>{E(g["intro"])}</p></div>{corpo}</div>''')
    return f'<div class="tabs" role="tablist" aria-label="Linhas de produto">{"".join(abas)}</div>' + "".join(paineis)

def portfolio_html():
    cards = []
    for i, p in enumerate(PORTFOLIO):
        tags = "".join(f"<span>{E(t)}</span>" for t in p["tags"])
        cards.append(f'''<li class="pf"><a href="{p["url"]}" target="_blank" rel="noopener" aria-label="{E(p["nome"])}: abrir o site em nova aba"><div class="shot"><div class="bar"><i></i><i></i><i></i><span>{p["host"]}</span></div><div class="vp"><img src="/assets/portfolio/pf-{p["slug"]}-560.webp" srcset="/assets/portfolio/pf-{p["slug"]}-560.webp 560w, /assets/portfolio/pf-{p["slug"]}.webp 960w" sizes="(max-width:640px) 84vw, 560px" width="560" height="1050" loading="lazy" decoding="async" alt="Página inicial do site {E(p["nome"])}"></div></div><div class="pfm"><div><h3>{E(p["nome"])}</h3><p>{E(p["seg"])}</p></div><span class="go" aria-hidden="true">↗</span></div><div class="tags">{tags}</div></a></li>''')
    return "".join(cards)

def offer_catalog():
    itens = []
    for g in PLANOS:
        nome_g = g["titulo"]
        for p in g.get("planos", []):
            o = {"@type": "Offer", "name": (g["produto"]["nome"] + " " + p["nome"]) if "produto" in g else p["nome"], "priceCurrency": "BRL", "seller": {"@id": BASE + "/#org"}, "url": BASE + "/#planos"}
            if p["preco"]:
                inte, cent, suf = p["preco"]
                o["price"] = f'{inte}.{cent or "00"}'
                if suf: o["priceSpecification"] = {"@type": "UnitPriceSpecification", "price": o["price"], "priceCurrency": "BRL", "unitCode": "MON"}
                if p.get("pre"): o["description"] = "Preço a partir de"
            else:
                continue
            itens.append(o)
        for n, a, c in g.get("packs", []):
            itens.append({"@type": "Offer", "name": f"Pack de Skills {n}", "price": f"{a}.{c}", "priceCurrency": "BRL", "seller": {"@id": BASE + "/#org"}, "url": BASE + "/#planos"})
    return {"@type": "OfferCatalog", "name": "Catálogo CProject Lab", "itemListElement": itens}

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
    links = [("Estúdio", f"{p}#estudio"), ("Planos", f"{p}#planos"), ("Portfólio", f"{p}#portfolio"), ("Dúvidas", f"{p}#faq"), ("Contato", f"{p}#contato")]
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
        <p>Estúdio full-stack, Sistemas Lab e soluções prontas para profissionais, do rascunho ao produto no ar.</p></div>
      <div><h3 class="fh">Estúdio</h3><ul>{sv}</ul></div>
      <div><h3 class="fh">Ecossistema</h3><ul><li><a href="/#planos">Sorrirmos</a></li><li><a href="/#planos">Cortando</a></li><li><a href="/#planos">Landing pages e BI</a></li><li><a href="/#planos">Packs de skills</a></li><li><a href="/#portfolio">Portfólio</a></li></ul></div>
      <div><h3 class="fh">Contato</h3><ul><li><a href="{wa("Olá! Vim pelo site da CProject.")}" target="_blank" rel="noopener" data-origem="rodape">WhatsApp {WA_FMT}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{IG}" target="_blank" rel="noopener">@cproject.dev</a></li><li><a href="/politica-de-privacidade/">Política de privacidade</a></li></ul></div>
    </div>
    <div class="cp"><span>© {datetime.date.today().year} CProject</span><span>Feito sob medida, do rascunho ao produto no ar.</span></div>
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
       "email": EMAIL, "telephone": "+55-13-97417-7986", "founder": {"@type": "Person", "name": "Bruno C. Peres"}, "employee": [{"@type": "Person", "name": "Bruno C. Peres", "jobTitle": "Especialista em desenvolvimento de sistemas"}, {"@type": "Person", "name": "Gustavo Recouso", "jobTitle": "Especialista em desenvolvimento de sistemas"}, {"@type": "Person", "name": "Pedro Rua", "jobTitle": "Analista de marketing e analytics"}],
       "sameAs": [IG], "areaServed": {"@type": "Country", "name": "Brasil"},
       "contactPoint": {"@type": "ContactPoint", "telephone": "+55-13-97417-7986", "contactType": "customer service", "availableLanguage": "Portuguese"}}

def faq_schema(faq): return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
def faq_html(faq): return "".join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq)

def home():
    schema = {"@context": "https://schema.org", "@graph": [ORG,
        {"@type": "WebSite", "@id": BASE + "/#site", "url": BASE + "/", "name": "CProject", "inLanguage": "pt-BR", "publisher": {"@id": BASE + "/#org"}},
        faq_schema(FAQ_HOME)]}
    schema["@graph"][0] = dict(ORG, hasOfferCatalog=offer_catalog())
    title = "CProject · Sistemas, landing pages e BI com preço claro"
    desc = "Sistemas Lab como o Sorrirmos a partir de R$ 89,90/mês, landing pages a partir de R$ 297, BI em template e projetos sob medida. Estúdio full-stack."
    sv = "".join(f'''<article class="card rv"><span class="n">0{i+1}</span><h3>{s["nome"]}</h3><p>{s["card"]}</p><a class="lk" href="/{s["slug"]}/">Ver {s["nome"].lower()} {I_SETA}</a></article>''' for i, s in enumerate(SERVICOS))
    ps = "".join(f'<article class="card rv"><h3>{t}</h3><p>{d}</p></article>' for t, d in PASSOS)
    out = head(title, desc, "/", schema, '<link rel="preload" href="/assets/fonts/jbmono.woff2" as="font" type="font/woff2" crossorigin>\n') + nav() + f'''
<main id="conteudo">
<section class="hero" aria-labelledby="h1">
  <canvas id="hero-cv" aria-hidden="true"></canvas>
  <div class="in">
    <span class="eb">CProject · estúdio, Sistemas Lab e soluções prontas</span>
    <h1 id="h1">Sites, sistemas e apps <em class="g">sob medida</em>, do rascunho ao produto no ar.</h1>
    <p class="lead">Um estúdio full-stack com sistemas por assinatura, landing pages e BI de preço fechado, e projetos sob medida quando o plano não basta.</p>
    <div class="ctas">
      <a class="btn" href="{wa("Olá! Vim pelo site da CProject e quero agendar a conversa de 15 minutos.")}" target="_blank" rel="noopener" data-origem="hero">{I_WA} Agendar conversa de 15 min</a>
      <a class="btn o" href="#planos">Ver planos e preços</a>
    </div>
    <div class="stack" aria-label="Tecnologias"><span>Next.js</span><span>React</span><span>Supabase</span><span>Vercel</span></div>
  </div>
</section>

<section class="sec" id="frentes" aria-labelledby="t-frentes">
  <div class="in">
    <div class="hd rv"><span class="eb">01 · Ecossistema</span><h2 id="t-frentes">Três frentes, <em class="g">um único fluxo</em></h2><p>O mesmo time que desenvolve sob medida para clientes constrói sistemas próprios e empacota o que funciona em soluções de preço fechado.</p></div>
    <div class="fr">
      <article class="card hl rv"><span class="n">ESTÚDIO</span><h3>Sob medida para a sua operação</h3><p>Sites, sistemas internos, dashboards e automações construídos do zero para o processo de cada cliente.</p><a class="lk" href="#estudio">Ver serviços {I_SETA}</a></article>
      <article class="card rv"><span class="n">SISTEMAS LAB</span><h3>Sistemas próprios por assinatura</h3><p>Sorrirmos para clínicas odontológicas, a partir de R$ 89,90 por mês, e Cortando para barbearias, em breve.</p><a class="lk" href="#planos">Ver planos {I_SETA}</a></article>
      <article class="card rv"><span class="n">SOLUÇÕES PRONTAS</span><h3>Preço fechado, entrega rápida</h3><p>Landing pages a partir de R$ 297, BI em template a partir de R$ 100 e packs de skills de IA a partir de R$ 79,90.</p><a class="lk" href="#planos">Ver preços {I_SETA}</a></article>
    </div>
  </div>
</section>

<section class="sec alt" id="estudio" aria-labelledby="t-estudio">
  <div class="in">
    <div class="hd rv"><span class="eb">02 · Estúdio</span><h2 id="t-estudio">Quatro serviços, da interface ao back-end</h2><p>Sem passar o projeto entre equipes diferentes no caminho: quem desenha é quem desenvolve e quem dá suporte.</p></div>
    <div class="sv">{sv}</div>
  </div>
</section>

<section class="sec" id="planos" aria-labelledby="t-planos">
  <div class="in">
    <div class="hd rv"><span class="eb">03 · Planos e preços</span><h2 id="t-planos">Escolha por onde <em class="g">começar</em></h2><p>Catálogo CProject Lab: sistemas por assinatura, soluções de preço fechado e projetos sob orçamento. Escolha a linha e veja os valores.</p></div>
    <div class="pl rv" id="produtos">{planos_html()}</div>
  </div>
</section>

<section class="sec alt" id="portfolio" aria-labelledby="t-pf">
  <div class="in">
    <div class="hd pfh rv"><div><span class="eb">04 · Portfólio</span><h2 id="t-pf">Sites e landing pages <em class="g">no ar</em></h2><p>Projetos publicados para negócios de segmentos diferentes. Arraste para ver mais projetos e abra cada site para navegar.</p></div>
      <div class="pfnav"><button type="button" class="pfb" data-dir="-1" aria-label="Projeto anterior"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg></button><button type="button" class="pfb" data-dir="1" aria-label="Próximo projeto">{I_SETA}</button></div></div>
  </div>
  <div class="pfw rv"><ul class="pft" id="pft" aria-label="Projetos do portfólio">{portfolio_html()}</ul></div>
  <div class="in"><div class="pfp" aria-hidden="true"><i id="pfbar"></i></div></div>
</section>

<section class="sec" id="abordagem" aria-labelledby="t-ab">
  <div class="in">
    <div class="hd rv"><span class="eb">05 · Abordagem</span><h2 id="t-ab">Como o projeto acontece</h2><p>Nada de tela solta ou protótipo estático: cada etapa já entrega algo que roda de verdade.</p></div>
    <div class="ps">{ps}</div>
  </div>
</section>

<section class="sec alt" id="quem" aria-labelledby="t-quem">
  <div class="in">
    <div class="hd rv"><span class="eb">06 · Quem constrói</span><h2 id="t-quem">A IA acelera. <em class="g">Gente de verdade responde.</em></h2><p>Usamos inteligência artificial em todo o processo para entregar mais rápido. Mas cada projeto tem especialistas com nome e sobrenome, que entendem o seu negócio, decidem com você e respondem pelo resultado do briefing ao suporte.</p></div>
    <div class="team">{time_html()}</div>
    <div class="pills rv"><span>Comunicação direta</span><span>Entrega incremental</span><span>IA com revisão humana</span><span>Suporte pós-entrega</span></div>
  </div>
</section>

<section class="sec" id="faq" aria-labelledby="t-faq">
  <div class="in">
    <div class="hd rv"><span class="eb">07 · Perguntas frequentes</span><h2 id="t-faq">Antes de conversar</h2></div>
    <div class="faq rv">{faq_html(FAQ_HOME)}</div>
  </div>
</section>

<section class="sec alt" id="contato" aria-labelledby="t-ct">
  <div class="in ct">
    <div class="rv"><span class="eb">08 · Contato</span><h2 id="t-ct" style="font-size:var(--h2);margin-top:16px">Vamos conversar 15 minutos sobre o seu processo?</h2>
      <p style="color:var(--tx-2);margin-top:16px">Sem proposta engessada nem jargão técnico: só entender a dor da operação e ver se faz sentido começar por um plano pronto ou construir algo sob medida.</p>
      <div class="ch">
        <a href="{wa("Olá! Vim pelo site da CProject e quero conversar.")}" target="_blank" rel="noopener" data-origem="contato">{I_WA}<span><small>WhatsApp</small>{WA_FMT}</span></a>
        <a href="mailto:{EMAIL}">{I_MAIL}<span><small>E-mail</small>{EMAIL}</span></a>
        <a href="{IG}" target="_blank" rel="noopener">{I_IG}<span><small>Instagram</small>@cproject.dev</span></a>
      </div></div>
    <form class="fm rv" id="fm" novalidate aria-label="Enviar mensagem pelo WhatsApp">
      <div class="fl"><label for="f-nome">Nome</label><input id="f-nome" name="nome" autocomplete="name" required></div>
      <div class="fl"><label for="f-emp">Empresa</label><input id="f-emp" name="empresa" autocomplete="organization"></div>
      <div class="fl w"><label for="f-int">Interesse</label><select id="f-int" name="interesse" required><option value="">Selecione</option><option>Sorrirmos</option><option>Cortando</option><option>Landing page</option><option>BI e dashboards</option><option>Packs de skills de IA</option><option>Event Coverage</option><option>Projeto sob medida (Custom)</option><option>Outro assunto</option></select></div>
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
