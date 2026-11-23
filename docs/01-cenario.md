# 1. Cenário do Sistema — VitrineOn (E-commerce)

> **Origem:** este cenário parte do **Diagrama de Casos de Uso de E-commerce** feito pelo grupo na atividade anterior (Astah, `ecommerce Lucasb.asta`), reproduzido em [`/diagramas/01-casos-de-uso.png`](../diagramas/01-casos-de-uso.png).
> Os números de volume, equipe e orçamento abaixo são **premissas do grupo**: troque pelos valores do enunciado do professor se ele fornecer outros.

## 1.1 Descrição textual

A **VitrineOn** é uma varejista de médio porte (eletrônicos e acessórios) que hoje vende em loja física e quer abrir um **canal de vendas online**. A loja virtual precisa permitir que o **cliente** encontre produtos, monte um carrinho e finalize a compra pagando com **cartão de crédito ou Pix** através de um **gateway de pagamento externo**. O **administrador** da loja mantém o catálogo e **atualiza o estoque** pelo painel administrativo.

A empresa tem **picos fortes de acesso** em datas promocionais (Black Friday, Natal, Dia do Consumidor), quando o tráfego chega a cerca de **10 vezes** o normal. Uma indisponibilidade no checkout nesses dias significa venda perdida e dano à marca.

## 1.2 Atores e casos de uso (da atividade anterior)

| Ator | Tipo | Casos de uso |
|---|---|---|
| **Cliente** | Humano (primário) | UC01 Buscar Produtos · UC02 Gerenciar Carrinho · UC03 Realizar Checkout |
| **Administrador** | Humano (primário) | UC04 Atualizar Estoque |
| **Gateway de Pagamento** | Sistema externo (secundário) | UC05 Processar Pagamento |

Relacionamento: **UC03 Realizar Checkout `<<include>>` UC05 Processar Pagamento**, ou seja, todo checkout obrigatoriamente processa um pagamento.

### Detalhamento resumido

- **UC01 Buscar Produtos**: busca por texto, filtros (categoria, preço, marca) e ordenação; exibe preço e disponibilidade.
- **UC02 Gerenciar Carrinho**: adicionar, remover e alterar quantidade de itens; o carrinho persiste entre sessões e dispositivos do cliente logado.
- **UC03 Realizar Checkout**: confirma endereço e frete, **reserva o estoque**, gera o pedido e dispara o pagamento.
- **UC04 Atualizar Estoque**: o administrador ajusta quantidades individualmente ou por importação de planilha (CSV).
- **UC05 Processar Pagamento**: autorização no gateway; a confirmação chega de forma **assíncrona** (webhook).

## 1.3 Premissas de negócio e volume

| Item | Valor assumido |
|---|---|
| Catálogo | ~50 mil SKUs |
| Usuários simultâneos (dia comum) | ~2.000 |
| Usuários simultâneos (pico, Black Friday) | ~20.000 (10×) |
| Pedidos/dia (comum → pico) | ~1.500 → ~15.000 |
| Proporção de leitura × escrita | ~95% navegação/busca, 5% carrinho/checkout |
| Público | Brasil (servidores em São Paulo) |

## 1.4 Restrições

| ID | Restrição | Impacto na arquitetura |
|---|---|---|
| R1 | **Equipe pequena**: 6 pessoas (2 back-end, 2 front-end, 1 full-stack, 1 DevOps em meio período) | Preferir **serviços gerenciados** e poucos serviços, sem operar Kubernetes |
| R2 | **Orçamento limitado**: até ~US$ 3 mil/mês de nuvem fora de pico | Escalar sob demanda, pagar por uso, compartilhar cluster de banco entre serviços |
| R3 | **Prazo**: MVP em 6 meses | Reaproveitar serviços prontos (Cognito, gateway de pagamento, SES) |
| R4 | **Pagamento com cartão**: PCI-DSS | Dados de cartão **nunca** passam pelos nossos servidores (tokenização no gateway) |
| R5 | **LGPD**: dados pessoais de clientes brasileiros | Dados em região brasileira, criptografia, consentimento e direito de exclusão |
| R6 | **Alta disponibilidade** no checkout, principalmente em datas de pico | Multi-AZ, autoescalonamento, filas para desacoplar |
| R7 | Integração com **gateway de pagamento de terceiros** (pode ser trocado) | Isolar a integração atrás de um adaptador |
