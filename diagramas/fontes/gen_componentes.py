"""Gera diagramas/fontes/02-componentes.dot"""
import sys

ICON = '<IMG SRC="componente.png" SCALE="TRUE"/>'

def comp(nid, name, stereo, resp, fill="#E8F1FB", border="#2B5C8A", icon=True, width=None):
    ic = f'<TD FIXEDSIZE="TRUE" WIDTH="16" HEIGHT="13" ALIGN="RIGHT">{ICON}</TD>' if icon else '<TD></TD>'
    resp_html = "<BR/>".join(resp) if resp else ""
    return (f'  {nid} [shape=plain, label=<<TABLE BORDER="1" COLOR="{border}" BGCOLOR="{fill}" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4" STYLE="rounded">'
            f'<TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9" COLOR="#555555">«{stereo}»</FONT></TD>{ic}</TR>'
            f'<TR><TD COLSPAN="2"><B>{name}</B></TD></TR>'
            + (f'<TR><TD COLSPAN="2"><FONT POINT-SIZE="9" COLOR="#333333">{resp_html}</FONT></TD></TR>' if resp_html else '')
            + '</TABLE>>];\n')

def db(nid, name, tech, fill="#FDF0E1", border="#B36B00"):
    return f'  {nid} [shape=cylinder, style=filled, fillcolor="{fill}", color="{border}", label=<<FONT POINT-SIZE="9" COLOR="#555555">«database»</FONT><BR/><B>{name}</B><BR/><FONT POINT-SIZE="9">{tech}</FONT>>, margin="0.15,0.08"];\n'

out = []
w = out.append
w('''// Diagrama de Componentes - VitrineOn (E-commerce)
// Gerado a partir de gen_componentes.py — pode ser editado diretamente.
// Renderizar: dot -Tpng -Gdpi=170 02-componentes.dot -o ../02-componentes.png
digraph Componentes {
  graph [rankdir=TB, fontname="DejaVu Sans", fontsize=13, nodesep=0.45, ranksep=0.65, newrank=true, compound=true, pad=0.4,
         label=<<B>Diagrama de Componentes — VitrineOn (E-commerce)</B><BR/><FONT POINT-SIZE="11">Estilo: cliente-servidor + monolito modular em camadas + 2 microsserviços · Padrões: API Gateway, MVC, Repository, Adapter, Publish/Subscribe</FONT>>,
         labelloc=t, fontsize=18];
  node  [fontname="DejaVu Sans", fontsize=11];
  // subgrafos (clusters) usam fonte menor que o título
  edge  [fontname="DejaVu Sans", fontsize=9, color="#333333", arrowsize=0.7];
''')

# Front-end
w('  subgraph cluster_front { label=<<B>Front-end (clientes)</B>>; style="rounded,dashed"; color="#7A7A7A"; fontsize=13; margin=14;\n')
w(comp("lojaweb", "Loja Web", "component · SPA", ["Vitrine, busca, carrinho e checkout", "React (padrão MVC/MVVM no cliente)"], fill="#EAF7EA", border="#2E7D32"))
w(comp("admin", "Painel Administrativo", "component · SPA", ["Cadastro de produtos e", "atualização de estoque (UC04)"], fill="#EAF7EA", border="#2E7D32"))
w('  }\n')

# Borda
w('  subgraph cluster_borda { label=<<B>Borda / Entrada</B>>; style="rounded,dashed"; color="#7A7A7A"; fontsize=13; margin=14;\n')
w(comp("cdn", "CDN + WAF", "component", ["Entrega arquivos estáticos e imagens", "Bloqueia ataques e limita taxa"], fill="#F3EAFB", border="#6A1B9A"))
w(comp("apigw", "API Gateway", "component", ["Porta de entrada única da API", "Roteamento, autenticação JWT,", "throttling e CORS"], fill="#F3EAFB", border="#6A1B9A"))
w(comp("idp", "Identidade", "component", ["Cadastro/login de clientes e admins", "OAuth2/OIDC, MFA para admin"], fill="#F3EAFB", border="#6A1B9A"))
w('  }\n')

# Monolito
w('  subgraph cluster_core { label=<<B>«subsystem» Loja Core — monolito modular em camadas</B><BR/><FONT POINT-SIZE="10">um deploy · um banco · módulos com fronteiras claras</FONT>>; style="rounded,filled"; fillcolor="#F7FAFD"; color="#2B5C8A"; penwidth=1.6; margin=16; fontsize=14;\n')
w('    subgraph cluster_l1 { label="Camada de Apresentação (API)"; style="rounded"; color="#9DB7D1"; fontsize=10;\n')
w(comp("ctrl", "Controladores REST", "component", ["/carrinho · /pedidos · /estoque · /clientes", "Validação de entrada e DTOs"]))
w('    }\n')
w('    subgraph cluster_l2 { label="Camada de Regras de Negócio (módulos)"; style="rounded"; color="#9DB7D1"; fontsize=10;\n')
w(comp("mcar", "Carrinho", "module", ["UC02 Gerenciar Carrinho"]))
w(comp("mped", "Pedidos / Checkout", "module", ["UC03 Realizar Checkout", "Cria pedido e reserva estoque", "na mesma transação"]))
w(comp("mest", "Estoque", "module", ["UC04 Atualizar Estoque", "Reserva, baixa e auditoria"]))
w(comp("mcli", "Clientes", "module", ["Endereços e dados pessoais", "(LGPD: consentimento/exclusão)"]))
w(comp("mnot", "Notificações", "module", ["E-mails de pedido", "e de pagamento"]))
w('    }\n')
w('    subgraph cluster_l3 { label="Camada de Acesso a Dados"; style="rounded"; color="#9DB7D1"; fontsize=10;\n')
w(comp("repo", "Repositórios", "component", ["Padrão Repository (ORM)", "Isola SQL das regras de negócio"]))
w('    }\n')
w(db("dbcore", "Banco da Loja Core", "PostgreSQL · pedidos, estoque,<BR/>carrinhos, clientes"))
w('  }\n')

# Catálogo
w('  subgraph cluster_cat { label=<<B>«microsserviço» Catálogo e Busca</B><BR/><FONT POINT-SIZE="10">UC01 · escala sozinho nos picos</FONT>>; style="rounded,filled"; fillcolor="#FBFBF2"; color="#8B7500"; penwidth=1.6; margin=14; fontsize=14;\n')
w(comp("catapi", "API de Catálogo", "component", ["GET /produtos, /busca", "Cadastro de produtos (admin)"], fill="#FFF8DC", border="#8B7500"))
w(comp("cache", "Cache", "component", ["Cache-aside de produtos", "e buscas populares"], fill="#FFF8DC", border="#8B7500"))
w(db("idx", "Índice de Busca", "texto, filtros, facetas"))
w(db("dbcat", "Banco do Catálogo", "NoSQL · produtos e preços"))
w('  }\n')

# Pagamento
w('  subgraph cluster_pag { label=<<B>«microsserviço» Pagamento</B><BR/><FONT POINT-SIZE="10">UC05 · isolado por segurança (PCI)</FONT>>; style="rounded,filled"; fillcolor="#FDF5F5"; color="#B71C1C"; penwidth=1.6; margin=14; fontsize=14;\n')
w(comp("pagapi", "API de Pagamento", "component", ["Cria cobrança (idempotente)", "Recebe webhooks do gateway", "Circuit breaker + retry"], fill="#FDECEC", border="#B71C1C"))
w(comp("adapt", "Adaptador do Gateway", "component", ["Padrão Adapter (GatewayPort)", "Troca de gateway sem afetar", "o resto do sistema"], fill="#FDECEC", border="#B71C1C"))
w(db("dbpag", "Banco de Pagamentos", "NoSQL · transações e tokens<BR/>(nunca o cartão)"))
w('  }\n')

# Mensageria
w(comp("bus", "Barramento de Eventos", "component", ["Tópicos + filas com DLQ (publish/subscribe)", "EstoqueAtualizado · PagamentoConfirmado · PagamentoRecusado"], fill="#ECEFF1", border="#455A64"))

# Externos
w('  subgraph cluster_ext { label=<<B>Sistemas externos</B>>; style="rounded,dashed"; color="#7A7A7A"; fontsize=13; margin=14;\n')
w(comp("gw", "Gateway de Pagamento", "external system", ["Ator do UC05 (ex.: Mercado Pago,", "Stripe, PagSeguro)", "Tokeniza cartão · Pix"], fill="#FFFFFF", border="#000000", icon=False))
w(comp("mail", "Serviço de E-mail", "external system", ["Envio transacional"], fill="#FFFFFF", border="#000000", icon=False))
w('  }\n')

# Arestas síncronas
w('''
  // ---- Comunicação síncrona (HTTPS/REST) ----
  lojaweb -> cdn  [label="HTTPS"];
  admin   -> cdn  [label="HTTPS"];
  lojaweb -> idp  [label="login OIDC", style=solid, color="#6A1B9A", fontcolor="#6A1B9A"];
  cdn   -> apigw  [label="/api/*  HTTPS"];
  apigw -> idp    [label="valida JWT", color="#6A1B9A", fontcolor="#6A1B9A"];
  apigw -> ctrl   [label="REST /carrinho /pedidos\\n/estoque /clientes", lhead=cluster_core];
  apigw -> catapi [label="REST /produtos /busca"];
  apigw -> pagapi [label="REST /webhooks/pagamento"];

  ctrl -> mcar; ctrl -> mped; ctrl -> mest; ctrl -> mcli;
  mped -> mest [label="reserva", fontsize=8];
  mcar -> repo; mped -> repo; mest -> repo; mcli -> repo;
  repo -> dbcore [label="SQL"];

  mped  -> catapi [label="consulta preço\\n(REST)", color="#8B7500", fontcolor="#8B7500"];
  mped  -> pagapi [label="criar cobrança\\n(REST, chave de idempotência)", color="#B71C1C", fontcolor="#B71C1C", penwidth=1.4];

  catapi -> cache; catapi -> idx [label="consulta"]; catapi -> dbcat;
  pagapi -> adapt; pagapi -> dbpag;
  adapt  -> gw [label="HTTPS/REST\\n(token do cartão)", color="#B71C1C", fontcolor="#B71C1C"];
  lojaweb -> gw [label="SDK JS: cartão digitado\\ndireto no gateway (tokenização)", color="#B71C1C", fontcolor="#B71C1C", style=bold, constraint=false, weight=0];
  gw -> apigw [label="webhook HTTPS\\n(status do pagamento)", style=dashed, color="#B71C1C", fontcolor="#B71C1C", constraint=false];
  mnot -> mail [label="SMTP/API"];

  // ---- Comunicação assíncrona (eventos) ----
  mest   -> bus [style=dashed, color="#455A64", fontcolor="#455A64", label="publica\\nEstoqueAtualizado"];
  pagapi -> bus [style=dashed, color="#455A64", fontcolor="#455A64", label="publica\\nPagamentoConfirmado/Recusado"];
  bus -> catapi [style=dashed, color="#455A64", fontcolor="#455A64", label="consome\\nEstoqueAtualizado\\n(atualiza índice)"];
  bus -> mped   [style=dashed, color="#455A64", fontcolor="#455A64", label="consome Pagamento*\\n(confirma pedido)"];
  mped -> mnot  [label="pedido confirmado", fontsize=8];

  // ---- Legenda ----
  subgraph cluster_leg { label=<<B>Legenda</B>>; style="rounded"; color="#BBBBBB"; fontsize=10; margin=8;
    l1 [shape=plaintext, label="", width=0.1]; l2 [shape=plaintext, label="", width=0.1];
    l3 [shape=plaintext, label="", width=0.1]; l4 [shape=plaintext, label="", width=0.1];
    l1 -> l2 [label="chamada síncrona (HTTPS/REST)"];
    l3 -> l4 [label="evento assíncrono (fila/tópico)", style=dashed, color="#455A64"];
  }

  {rank=same; lojaweb; admin}
  {rank=same; cdn; idp}
  {rank=same; ctrl; catapi; pagapi}
  {rank=same; repo; bus; mail}
  {rank=same; dbcore; gw}
  {rank=same; l1; l2; l3; l4}
}
''')
open(sys.argv[1], "w").write("".join(out))
