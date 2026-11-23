# 2. Requisitos Não-Funcionais e Atributos de Qualidade

## 2.1 Requisitos Não-Funcionais (RNFs)

Todo RNF tem uma **medida verificável**. Nada de "precisa ser rápido".

| ID | Requisito não-funcional | Métrica / critério de aceitação | Característica ISO 25010 |
|---|---|---|---|
| RNF01 | Dados de cartão não podem ser armazenados, processados ou trafegar pelos servidores da VitrineOn | 0 campos de PAN/CVV em logs, bancos ou payloads internos; escopo PCI **SAQ A** | Segurança → Confidencialidade |
| RNF02 | Toda comunicação deve ser criptografada | TLS 1.2+ em 100% das conexões externas e internas; dados em repouso com AES-256 (KMS) | Segurança → Confidencialidade |
| RNF03 | Acesso administrativo exige autenticação forte | MFA obrigatório para 100% das contas de administrador; sessão expira em 30 min de inatividade | Segurança → Autenticidade |
| RNF04 | Toda alteração de estoque e de pedido é rastreável | Log de auditoria com usuário, data/hora e valor anterior/novo, retido por 5 anos | Segurança → Responsabilização |
| RNF05 | Disponibilidade da loja (busca, carrinho, checkout) | **≥ 99,9%** ao mês (≤ 43 min de indisponibilidade/mês) | Confiabilidade → Disponibilidade |
| RNF06 | Falha de uma zona de disponibilidade não derruba a loja | Failover automático do banco em ≤ 60 s; perda de dados (RPO) ≤ 5 min; recuperação (RTO) ≤ 30 min | Confiabilidade → Recuperabilidade |
| RNF07 | Nenhum pedido pode ser cobrado em duplicidade nem perdido | Pagamento com **chave de idempotência**; mensagens com reentrega e fila de mensagens mortas (DLQ); 0 cobranças duplicadas | Confiabilidade → Tolerância a falhas |
| RNF08 | Indisponibilidade do gateway não derruba o restante da loja | Busca e carrinho continuam operando; checkout responde com mensagem amigável em ≤ 3 s (circuit breaker) | Confiabilidade → Tolerância a falhas |
| RNF09 | Tempo de resposta da **API de busca** | **p95 ≤ 200 ms** com 20 mil usuários simultâneos | Desempenho → Comportamento temporal |
| RNF10 | Tempo de resposta das operações de carrinho | p95 ≤ 300 ms | Desempenho → Comportamento temporal |
| RNF11 | Tempo de confirmação do checkout (sem contar o tempo do gateway) | p95 ≤ 1,5 s | Desempenho → Comportamento temporal |
| RNF12 | Carregamento da página inicial e de produto | LCP ≤ 2,5 s em 4G (Core Web Vitals) | Desempenho → Comportamento temporal |
| RNF13 | Suportar pico de 10× o tráfego normal | Autoescalonamento de 2 para até 20 instâncias por serviço em ≤ 3 min, sem intervenção manual | Desempenho → Capacidade |
| RNF14 | Atualização de estoque refletida na vitrine | Disponibilidade atualizada na busca em ≤ 5 s após a alteração | Adequação funcional → Correção |
| RNF15 | Implantar uma parte do sistema sem parar as outras | Deploy independente das 3 unidades (Loja Core, Catálogo, Pagamento), blue/green, sem downtime; ≥ 1 deploy/dia possível | Manutenibilidade → Modularidade |
| RNF16 | Facilidade de manter e testar | Cobertura de testes ≥ 70% nas regras de negócio; pipeline de CI ≤ 15 min | Manutenibilidade → Testabilidade |
| RNF17 | Diagnóstico rápido de incidentes | Logs centralizados e tracing distribuído; tempo médio de recuperação (MTTR) ≤ 1 h | Manutenibilidade → Analisabilidade |
| RNF18 | Trocar o gateway de pagamento sem reescrever o checkout | Troca afeta só o Serviço de Pagamento (adaptador) | Manutenibilidade → Modificabilidade |
| RNF19 | Checkout simples e acessível | Checkout em ≤ 3 etapas; layout responsivo (mobile-first); WCAG 2.1 nível AA | Usabilidade (Capacidade de interação) |
| RNF20 | Infraestrutura reproduzível | 100% da infraestrutura como código (Terraform); aplicações em contêineres Docker | Portabilidade (Flexibilidade) → Instalabilidade |
| RNF21 | Dados pessoais em conformidade com a LGPD | Dados hospedados no Brasil (sa-east-1); exclusão de conta atendida em ≤ 15 dias | Segurança / Conformidade |

## 2.2 Atributos de qualidade priorizados (ISO/IEC 25010)

> Nomes conforme a ISO/IEC 25010:2011. Na revisão de 2023, "Usabilidade" passou a se chamar **Capacidade de interação** e "Portabilidade" virou **Flexibilidade** (que inclui **Escalabilidade**). Escalabilidade não é uma característica isolada na versão 2011: aqui ela está tratada dentro de **Eficiência de desempenho → Capacidade**.

| Prioridade | Atributo | Justificativa | RNFs |
|---|---|---|---|
| **1º** | **Segurança** | A loja recebe pagamentos com **cartão de crédito** e guarda **dados pessoais** (nome, CPF, endereço). Um vazamento gera multa (LGPD, até 2% do faturamento), perda da credencial PCI e destrói a confiança no canal novo. É o único atributo cuja falha pode **inviabilizar o negócio**. | RNF01–04, RNF21 |
| **2º** | **Confiabilidade** (disponibilidade e tolerância a falhas) | Cada minuto fora do ar na Black Friday é venda perdida. Além disso, um erro no checkout que **cobre duas vezes** ou **perca um pedido pago** gera chargeback e reclamação no Procon. | RNF05–08 |
| **3º** | **Eficiência de desempenho** (tempo de resposta e capacidade/escalabilidade) | Busca lenta derruba conversão: a busca é a porta de entrada de quase toda compra, e o cliente desiste quando a página demora. O sistema precisa absorver **10× de tráfego** nos picos sem pagar por essa capacidade o ano inteiro (R2). | RNF09–13 |
| **4º** | **Manutenibilidade** | Equipe de **6 pessoas** (R1) precisa evoluir o produto rápido: deploy independente, código testável, observabilidade e possibilidade de trocar o gateway. | RNF15–18 |
| **5º** | **Usabilidade** | Checkout complicado causa abandono de carrinho. É importante, mas é resolvido principalmente no front-end e influencia pouco a arquitetura de servidores. | RNF19 |
| **6º** | **Portabilidade / Compatibilidade** | Contêineres e IaC evitam dependência de máquinas específicas e facilitam ambientes de teste. A integração com o gateway passa por API REST padrão. | RNF20, RNF18 |

### Por que Segurança vem antes de Disponibilidade?

Uma loja **fora do ar** perde vendas por algumas horas. Uma loja **que vaza cartões** pode perder o direito de aceitar cartões e responder judicialmente. Por isso, quando os dois atributos entram em conflito, a segurança vence. Exemplo: o painel administrativo exige MFA mesmo que isso deixe o login do administrador mais lento.

## 2.3 Cenários de qualidade (formato SEI: Fonte, Estímulo, Ambiente, Artefato, Resposta, Medida)

| Atributo | Fonte | Estímulo | Ambiente | Artefato | Resposta | Medida |
|---|---|---|---|---|---|---|
| Segurança | Atacante externo | Tenta capturar dados de cartão interceptando o checkout | Operação normal | Front-end e Serviço de Pagamento | Cartão é digitado no componente do gateway (iframe/SDK); servidores só recebem **token** | 0 dados de cartão nos nossos sistemas |
| Segurança | Bot | 5.000 requisições/min de força bruta no login | Operação normal | Borda (WAF) e Cognito | WAF limita taxa por IP; Cognito bloqueia a conta após 5 tentativas | Bloqueio em ≤ 1 min |
| Confiabilidade | Falha de infraestrutura | Zona de disponibilidade A cai | Black Friday | Banco de dados e serviços | Tarefas sobem na AZ B; Aurora promove a réplica | Failover ≤ 60 s; nenhum pedido pago perdido |
| Confiabilidade | Gateway de pagamento | Fica 10 min sem responder | Pico | Serviço de Pagamento | Circuit breaker abre; pedido fica "aguardando pagamento"; reserva de estoque expira em 15 min | Busca e carrinho seguem com 100% de disponibilidade |
| Desempenho | 20 mil clientes | Buscam produtos ao mesmo tempo | Black Friday | Serviço de Catálogo/Busca | Resultado servido pelo OpenSearch, com cache Redis/CDN | p95 ≤ 200 ms |
| Desempenho | Campanha de marketing | Tráfego sobe de 2 mil para 20 mil usuários em 10 min | Pico | Cluster ECS | Autoescalonamento por CPU e requisições | Novas tarefas em ≤ 3 min; erro HTTP 5xx < 0,1% |
| Manutenibilidade | Negócio | Decide trocar o gateway de pagamento | Desenvolvimento | Serviço de Pagamento | Nova implementação do adaptador `GatewayPort` | ≤ 2 semanas; nenhum outro serviço alterado |

## 2.4 Conflitos (trade-offs) reconhecidos

| Conflito | Decisão tomada |
|---|---|
| **Disponibilidade × Custo**: Multi-AZ dobra parte da infraestrutura | Multi-AZ só para o que é crítico (banco, Redis, serviços). Um único NAT Gateway, com endpoints VPC para reduzir tráfego por ele |
| **Modularidade × Equipe pequena**: microsserviços demais sobrecarregam 6 pessoas | **Monolito modular** (Carrinho, Pedidos, Estoque, Clientes) + **apenas 2 microsserviços** (Catálogo/Busca e Pagamento), todos em ECS Fargate (sem gerenciar servidores ou Kubernetes) |
| **Escalabilidade × Consistência**: separar Estoque e Pedidos em serviços diferentes exigiria transação distribuída (saga) | Estoque e Pedidos ficam **no mesmo monolito e no mesmo banco**, e a reserva de estoque + criação do pedido acontece em **uma única transação ACID** |
| **Isolamento de dados × Custo**: um banco relacional por serviço é caro | O monolito usa Aurora PostgreSQL; os dois microsserviços usam **tabelas DynamoDB próprias** (pagas por uso, escalam sozinhas no pico) |
| **Consistência × Desempenho**: estoque exato na vitrine exigiria consulta síncrona | Vitrine usa **consistência eventual** (≤ 5 s); a verificação forte acontece na **reserva** do checkout |
