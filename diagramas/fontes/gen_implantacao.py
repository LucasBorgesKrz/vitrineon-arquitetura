"""Gera diagramas/fontes/03-implantacao.dot"""
import sys

def node3d(nid, stereo, name, lines=(), fill="#FFFFFF", border="#333333"):
    body = "<BR/>".join(lines)
    extra = f'<BR/><FONT POINT-SIZE="9">{body}</FONT>' if body else ""
    return (f'  {nid} [shape=box3d, style=filled, fillcolor="{fill}", color="{border}", margin="0.18,0.08", '
            f'label=<<FONT POINT-SIZE="9" COLOR="#555555">«{stereo}»</FONT><BR/><B>{name}</B>{extra}>];\n')

def artifacts_node(nid, title, arts, fill="#FFFFFF", border="#333333"):
    rows = "".join(
        f'<TR><TD ALIGN="LEFT" BGCOLOR="{c}" BORDER="1" COLOR="#777777"><FONT POINT-SIZE="8" COLOR="#555555">«artifact»</FONT><BR/><B>{a}</B><BR/><FONT POINT-SIZE="8">{d}</FONT></TD></TR>'
        for a, d, c in arts)
    return (f'  {nid} [shape=box3d, style=filled, fillcolor="{fill}", color="{border}", margin="0.1,0.06", '
            f'label=<<TABLE BORDER="0" CELLSPACING="4" CELLPADDING="3"><TR><TD><FONT POINT-SIZE="9" COLOR="#555555">«executionEnvironment»</FONT><BR/><B>{title}</B></TD></TR>{rows}</TABLE>>];\n')

ARTS = [
    ("loja-core (imagem Docker)", "monolito modular · 2 → 10 tarefas", "#E8F1FB"),
    ("catalogo-svc (imagem Docker)", "microsserviço · 2 → 20 tarefas", "#FFF8DC"),
    ("pagamento-svc (imagem Docker)", "microsserviço · 2 → 4 tarefas", "#FDECEC"),
]

o = []
w = o.append
w('''// Diagrama de Implantação (UML) - VitrineOn (E-commerce)
// Gerado a partir de gen_implantacao.py — pode ser editado diretamente.
// Renderizar: dot -Tpng -Gdpi=170 03-implantacao.dot -o ../03-implantacao.png
digraph Implantacao {
  graph [rankdir=TB, fontname="DejaVu Sans", fontsize=12, nodesep=0.35, ranksep=0.6, newrank=true, compound=true, pad=0.4,
         label=<<B>Diagrama de Implantação (UML) — VitrineOn (E-commerce)</B><BR/><FONT POINT-SIZE="11">AWS · região sa-east-1 (São Paulo) · 2 zonas de disponibilidade · contêineres Docker em ECS Fargate</FONT>>,
         labelloc=t, fontsize=18];
  node  [fontname="DejaVu Sans", fontsize=10];
  edge  [fontname="DejaVu Sans", fontsize=8, color="#333333", arrowsize=0.6];
''')

# Dispositivos
w('  subgraph cluster_devices { label=<<B>Dispositivos dos usuários</B>>; style="rounded,dashed"; color="#888888"; fontsize=12;\n')
w(node3d("dev_cli", "device", "Navegador / Celular do Cliente", ["«artifact» loja-web (bundle JS)", "SDK JS do gateway de pagamento"], fill="#EAF7EA", border="#2E7D32"))
w(node3d("dev_adm", "device", "Computador do Administrador", ["«artifact» painel-admin (bundle JS)"], fill="#EAF7EA", border="#2E7D32"))
w('  }\n')

# Edge global
w('  subgraph cluster_edge { label=<<B>«cloud» AWS — Borda global</B>>; style="rounded,filled"; fillcolor="#F9F4FC"; color="#6A1B9A"; fontsize=12;\n')
w(node3d("r53", "node", "Amazon Route 53", ["DNS · health checks"], fill="#F3EAFB", border="#6A1B9A"))
w(node3d("cf", "node", "Amazon CloudFront + AWS WAF", ["CDN (cache de site e imagens)", "regras OWASP · rate limit"], fill="#F3EAFB", border="#6A1B9A"))
w('  }\n')

# Região
w('  subgraph cluster_region { label=<<B>«cloud region» AWS sa-east-1 (São Paulo)</B> — dados no Brasil (LGPD)>; style="rounded"; color="#FF9900"; penwidth=2; fontsize=13; margin=16;\n')

w('    subgraph cluster_entry { label=<<B>Entrada regional</B> (serviços gerenciados)>; style="rounded,filled"; fillcolor="#FBF6FD"; color="#B48CC8"; fontsize=11;\n')
w(node3d("apigw", "node", "Amazon API Gateway", ["HTTP API · autorizador JWT", "throttling · VPC Link"], fill="#F3EAFB", border="#6A1B9A"))
w(node3d("cognito", "node", "Amazon Cognito", ["user pools: clientes / admins", "MFA obrigatório p/ admin"], fill="#F3EAFB", border="#6A1B9A"))
w(node3d("s3", "node", "Amazon S3", ["«artifact» loja-web, painel-admin", "imagens de produtos"]))
w('    }\n')
w('    subgraph cluster_vpc { label=<<B>«VPC» 10.0.0.0/16</B>>; style="rounded,filled"; fillcolor="#F4F9F4"; color="#3F8F3F"; penwidth=1.5; fontsize=12; margin=14;\n')
w(node3d("alb", "node", "Application Load Balancer (interno)", ["distribui entre as 2 AZs · health check", "roteia /produtos → catálogo · /pagamentos → pagamento · resto → core"], fill="#FFFFFF", border="#3F8F3F"))

for az, sfx, extra in (("a", "A", True), ("b", "B", False)):
    w(f'      subgraph cluster_az{az} {{ label=<<B>Zona de Disponibilidade {sfx}</B> (sa-east-1{az})>; style="rounded,dashed"; color="#3F8F3F"; fontsize=11; margin=10;\n')
    if extra:
        w('        subgraph cluster_pub_a { label="Sub-rede pública"; style="rounded"; color="#9CCC9C"; fontsize=9;\n')
        w(node3d("nat", "node", "NAT Gateway", ["saída para a Internet", "(gateway de pagamento)"]))
        w('        }\n')
    w(f'        subgraph cluster_app_{az} {{ label="Sub-rede privada — aplicação"; style="rounded"; color="#9CCC9C"; fontsize=9;\n')
    w(artifacts_node(f"ecs_{az}", f"ECS Fargate — tarefas AZ {sfx}", ARTS, fill="#FFFFFF", border="#2B5C8A"))
    w('        }\n')
    w(f'        subgraph cluster_data_{az} {{ label="Sub-rede privada — dados"; style="rounded"; color="#9CCC9C"; fontsize=9;\n')
    if az == "a":
        w(node3d("aur_w", "node", "Aurora PostgreSQL — Writer", ["«artifact» banco loja_core", "pedidos · estoque · carrinhos · clientes"], fill="#FDF0E1", border="#B36B00"))
        w(node3d("redis_p", "node", "ElastiCache Redis — primário", ["cache do catálogo"], fill="#FDF0E1", border="#B36B00"))
        w(node3d("os_1", "node", "OpenSearch — nó 1", ["«artifact» índice produtos"], fill="#FDF0E1", border="#B36B00"))
    else:
        w(node3d("aur_r", "node", "Aurora PostgreSQL — Reader", ["réplica · failover automático ≤ 60 s"], fill="#FDF0E1", border="#B36B00"))
        w(node3d("redis_r", "node", "ElastiCache Redis — réplica", ["failover automático"], fill="#FDF0E1", border="#B36B00"))
        w(node3d("os_2", "node", "OpenSearch — nó 2", ["réplica do índice"], fill="#FDF0E1", border="#B36B00"))
    w('        }\n')
    w('      }\n')
w('    }\n')  # vpc
w('    subgraph cluster_managed { label=<<B>Serviços gerenciados de dados, mensageria e operação</B> (Multi-AZ por padrão · acessados via VPC endpoints)>; style="rounded,filled"; fillcolor="#FFFAF0"; color="#E0A040"; fontsize=11;\n')
w(node3d("ddb", "node", "Amazon DynamoDB", ["tabela catalogo (produtos/preços)", "tabela pagamentos · on-demand · PITR"], fill="#FDF0E1", border="#B36B00"))
w(node3d("msg", "node", "Amazon SNS + SQS", ["tópicos: estoque, pagamento", "filas + DLQ por consumidor"], fill="#ECEFF1", border="#455A64"))
w(node3d("ses", "node", "Amazon SES", ["e-mails transacionais"]))
w(node3d("sec", "node", "Secrets Manager + KMS", ["credenciais e chave do gateway", "criptografia em repouso"]))
w(node3d("obs", "node", "CloudWatch + X-Ray", ["logs, métricas, alarmes", "tracing distribuído"]))
w(node3d("ecr", "node", "Amazon ECR", ["registro de imagens Docker"]))
w('    }\n')
w('  }\n')  # region

# Externos
w('  subgraph cluster_ext { label=<<B>Sistemas externos (Internet)</B>>; style="rounded,dashed"; color="#888888"; fontsize=12;\n')
w(node3d("gw", "external node", "Gateway de Pagamento", ["API REST + webhooks", "tokenização de cartão · Pix"], fill="#FFFFFF", border="#000000"))
w(node3d("gh", "external node", "GitHub + GitHub Actions", ["repositório · CI/CD", "Terraform (infra como código)"], fill="#FFFFFF", border="#000000"))
w('  }\n')

w('''
  // ---- Caminhos de comunicação ----
  dev_cli -> r53 [label="DNS"];
  dev_cli -> cf  [label="HTTPS (TLS 1.2+)"];
  dev_adm -> cf  [label="HTTPS"];
  dev_cli -> cognito [label="login OIDC", color="#6A1B9A", fontcolor="#6A1B9A"];
  dev_cli -> gw  [label="HTTPS · tokenização do cartão\\n(cartão nunca passa pela VitrineOn)", color="#B71C1C", fontcolor="#B71C1C", style=bold, constraint=false];
  cf -> s3    [label="arquivos estáticos (OAC)"];
  cf -> apigw [label="/api/* HTTPS"];
  apigw -> cognito [label="valida JWT", color="#6A1B9A", fontcolor="#6A1B9A"];
  apigw -> alb [label="VPC Link (privado)"];
  alb -> ecs_a [label="HTTP :8080"];
  alb -> ecs_b [label="HTTP :8080"];

  ecs_a -> aur_w [label="TLS :5432"];
  ecs_b -> aur_w [label="TLS :5432"];
  aur_w -> aur_r [label="replicação", style=dashed, dir=both, color="#B36B00", fontcolor="#B36B00"];
  ecs_a:sw -> redis_p:w [headlabel=":6379", labeldistance=2.5, labelangle=-30];
  redis_p -> redis_r [label="replicação", style=dashed, color="#B36B00", fontcolor="#B36B00"];
  ecs_a:se -> os_1:e [label="HTTPS"];
  os_1 -> os_2 [style=dashed, dir=both, color="#B36B00", label="cluster", fontcolor="#B36B00"];

  ecs_a -> ddb [label="VPC endpoint"];
  ecs_b -> msg [label="VPC endpoint\\n(publica/consome eventos)", color="#455A64", fontcolor="#455A64"];
  ecs_b -> ses [label="e-mail", color="#777777", fontcolor="#777777"];
  // ordem vertical (arestas invisíveis só para layout)
  aur_w -> redis_p -> os_1 [style=invis];
  aur_r -> redis_r -> os_2 [style=invis];
  os_1 -> ddb [style=invis]; os_2 -> sec [style=invis];
  ddb -> obs [style=invis]; sec -> ecr [style=invis];
  ecs_a -> nat [label="pagamento-svc", color="#B71C1C", fontcolor="#B71C1C"];
  nat -> gw [label="HTTPS (cobrança)", color="#B71C1C", fontcolor="#B71C1C"];
  gw -> apigw [label="webhook HTTPS", style=dashed, color="#B71C1C", fontcolor="#B71C1C", constraint=false];
  gh -> ecr [label="docker push", constraint=false];
  gh -> alb [label="deploy blue/green (ECS)", style=dashed, color="#555555", constraint=false];

  {rank=same; dev_cli; dev_adm}
  {rank=same; r53; cf}
  {rank=same; ecs_a; ecs_b}
  {rank=same; aur_w; aur_r}
  {rank=same; apigw; cognito; s3}
  {rank=same; alb; nat}
  {rank=same; ddb; msg; ses; sec}
  {rank=same; obs; ecr; gh}
}
''')
open(sys.argv[1], "w").write("".join(o))
