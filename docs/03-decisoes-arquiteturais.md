# 3. Registros de Decisão Arquitetural (ADRs)

Formato curto: **Contexto → Decisão → Alternativas → Consequências**. Cada ADR aponta para os RNFs de [`02-requisitos-e-atributos-de-qualidade.md`](02-requisitos-e-atributos-de-qualidade.md).

---

## ADR-01: Monolito modular em camadas + 2 microsserviços

- **Status:** aceita
- **Contexto:** equipe de 6 pessoas, MVP em 6 meses, orçamento limitado (R1–R3). Ao mesmo tempo, a busca recebe ~95% do tráfego e explode 10× nos picos (RNF09, RNF13), e o pagamento exige isolamento (RNF01).
- **Decisão:** a **Loja Core** é um monolito modular em camadas (apresentação → negócio → acesso a dados) com os módulos Carrinho, Pedidos/Checkout, Estoque, Clientes e Notificações. **Catálogo/Busca** e **Pagamento** são microsserviços separados.
- **Alternativas:** (a) monolito puro, descartado porque escalar a busca obrigaria a escalar tudo e o pagamento dividiria processo e credenciais com o resto; (b) microsserviços para cada caso de uso, descartado por exigir sagas entre estoque e pedido e operação complexa demais para a equipe.
- **Consequências:** (+) 3 deploys em vez de 7; consistência simples no checkout; escala onde importa. (−) módulos da Loja Core escalam juntos; é preciso disciplina para não acoplar módulos (regras de dependência verificadas no CI).

## ADR-02: Reserva de estoque e criação do pedido na mesma transação

- **Status:** aceita
- **Contexto:** "estoque e pagamento precisam bater" (estudo de caso da disciplina). Vender um item sem estoque gera cancelamento e reclamação.
- **Decisão:** Estoque e Pedidos ficam no mesmo banco (Aurora PostgreSQL). O checkout executa `reservar estoque + criar pedido` em **uma transação ACID**, com controle de concorrência (`SELECT ... FOR UPDATE` / versão otimista). A reserva expira em 15 min se o pagamento não for confirmado.
- **Alternativas:** saga com eventos de compensação entre serviços separados. Mais complexa e com janelas de inconsistência.
- **Consequências:** (+) zero overselling, lógica simples. (−) acoplamento físico entre os dois módulos, aceitável enquanto estiverem no mesmo deploy.

## ADR-03: Dados de cartão tokenizados no navegador (escopo PCI mínimo)

- **Status:** aceita
- **Contexto:** RNF01. Armazenar ou trafegar cartão exige certificação PCI-DSS completa, cara e demorada.
- **Decisão:** o número do cartão é digitado em **campos hospedados pelo gateway (iframe)**. A VitrineOn recebe apenas um **token** de uso único. O Serviço de Pagamento guarda somente token, status e valores.
- **Alternativas:** formulário próprio enviando o cartão ao nosso back-end (escopo PCI total); script do gateway montando os campos na nossa página sem iframe (escopo SAQ A-EP, maior).
- **Consequências:** (+) escopo **SAQ A**; um vazamento dos nossos bancos não expõe cartões. (−) dependemos dos recursos de UI do gateway.

## ADR-04: Pagamento com idempotência, webhook e circuit breaker

- **Status:** aceita
- **Contexto:** RNF07 e RNF08. Redes falham: um retry pode cobrar duas vezes; o gateway pode ficar lento na Black Friday.
- **Decisão:** toda cobrança usa `Idempotency-Key = id do pedido` (gravação condicional no DynamoDB + chave enviada ao gateway). O resultado final chega por **webhook assinado** e vira evento na fila. Chamadas ao gateway têm timeout de 3 s e **circuit breaker**.
- **Consequências:** (+) 0 cobranças duplicadas; falha do gateway não derruba o resto. (−) o pedido tem estado intermediário `AGUARDANDO_PAGAMENTO`, e a interface precisa lidar com isso.

## ADR-05: Adapter para o gateway de pagamento

- **Status:** aceita
- **Contexto:** RNF18 e R7: o gateway pode ser trocado por custo/taxa, ou ganhar um segundo gateway de contingência.
- **Decisão:** o Serviço de Pagamento define a interface `GatewayPort` (`criarCobranca`, `estornar`, `validarWebhook`). Cada gateway é uma implementação (padrão **Adapter**).
- **Consequências:** (+) troca afeta só uma classe/módulo. (−) recursos muito específicos de um gateway precisam ser generalizados.

## ADR-06: Busca em OpenSearch com cache, atualizada por eventos

- **Status:** aceita
- **Contexto:** RNF09 (p95 ≤ 200 ms) com catálogo de 50 mil SKUs, filtros e texto livre; RNF14 (estoque refletido em ≤ 5 s).
- **Decisão:** produtos ficam no DynamoDB (fonte da verdade do Catálogo) e são indexados no **OpenSearch**. Buscas populares e páginas de produto passam por **Redis** (cache-aside, TTL curto). O módulo Estoque publica `EstoqueAtualizado` e o Catálogo atualiza a disponibilidade no índice.
- **Alternativas:** `LIKE` no PostgreSQL (não escala para texto livre com facetas); consulta síncrona de estoque a cada busca (acopla Catálogo à Loja Core e aumenta latência).
- **Consequências:** (+) busca rápida e independente do checkout. (−) **consistência eventual** na vitrine. A verificação forte acontece na reserva (ADR-02).

## ADR-07: AWS com ECS Fargate em vez de Kubernetes

- **Status:** aceita
- **Contexto:** equipe com um DevOps em meio período (R1); necessidade de autoescalonamento (RNF13) e Multi-AZ (RNF05).
- **Decisão:** contêineres Docker em **ECS Fargate**, com serviços gerenciados (Aurora, DynamoDB, ElastiCache, OpenSearch, SQS/SNS, Cognito). Região **sa-east-1**.
- **Alternativas:** EKS/Kubernetes (mais flexível, mas exige operar o cluster); VMs EC2 (patches e escala manuais); serverless puro com Lambda (bom para picos, mas cold start e limites de tempo complicam o checkout).
- **Consequências:** (+) sem servidores para manter; escala automática. (−) maior dependência da AWS, mitigada por Docker, PostgreSQL e Terraform.
