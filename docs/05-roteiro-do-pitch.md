# 5. Roteiro do Pitch (10–15 min)

> Público: **clientes e stakeholders** (diretoria da VitrineOn), não só técnicos. Fale de **risco, dinheiro e cliente**; use os termos técnicos só para sustentar o argumento.
> Slides: [`/apresentacao/pitch-vitrineon.pdf`](../apresentacao/pitch-vitrineon.pdf).

| Slide | Tempo | Mensagem principal | O que falar |
|---|---|---|---|
| 1. Capa | 0:30 | Quem sou e o que vou apresentar | "Vou mostrar uma loja virtual que aguenta a Black Friday e protege o cartão do cliente, com uma equipe de 6 pessoas." |
| 2. O desafio | 1:00 | O problema é de negócio | 10× de tráfego, cartão de crédito e 50 mil produtos. A regra de ouro: estoque e pagamento precisam bater. |
| 3. Casos de uso | 1:00 | O sistema é simples de entender | Cliente busca, monta carrinho e paga; administrador atualiza estoque; o checkout sempre inclui pagamento. |
| 4. Restrições | 1:00 | O contexto decide a arquitetura | Equipe pequena, orçamento curto, LGPD/PCI. "Por isso não vou propor a arquitetura da Netflix." |
| 5. Atributos | 1:30 | Segurança > Confiabilidade > Desempenho | Ler as metas com números. Explicar por que segurança vence disponibilidade quando os dois conflitam. |
| 6. Estilo | 1:30 | Escolha justificada, com alternativas | Mostrar as 3 opções. "Só separamos o que tem motivo real: a busca, para escalar, e o pagamento, para isolar." |
| 7. Componentes | 1:30 | Quem faz o quê | Percorrer da esquerda para a direita: front-end → API Gateway → Loja Core / Catálogo / Pagamento → filas. Apontar setas sólidas (síncronas) e tracejadas (eventos). |
| 8. Checkout seguro | 1:30 | O momento mais crítico está protegido | Os 5 passos. Destacar: cartão nunca passa por nós; idempotência evita cobrança dupla. |
| 9. Implantação | 1:30 | Onde tudo roda | AWS São Paulo, 2 zonas, sub-redes privadas, serviços gerenciados. "Cada caixa do diagrama anterior tem um lugar aqui." |
| 10. Black Friday | 1:00 | Escala onde o tráfego está | Catálogo 2 → 20, CDN, cache, escalonamento agendado. "E fora do pico a conta volta ao normal." |
| 11. E se der errado? | 1:00 | Falhas foram pensadas | Escolher 2 linhas da tabela e contar como história ("Imagine que a AWS perde um datacenter na Black Friday..."). |
| 12. Trade-offs | 1:00 | Maturidade: sabemos o que estamos abrindo mão | Consistência eventual na vitrine, NAT único, dependência da AWS e como cada um é mitigado. |
| 13. Fechamento | 0:30 | Frase final + perguntas | "Segura onde o risco é maior, escalável onde o tráfego é maior, e simples o bastante para entregar em 6 meses." |
| **Total** | **~14 min** | | |

## Perguntas prováveis (e respostas curtas)

| Pergunta | Resposta |
|---|---|
| Por que não microsserviços para tudo? | Equipe de 6 pessoas e prazo de 6 meses. Microsserviços cobram operação complexa e consistência difícil (sagas). Separamos só o que tinha motivo: escala e segurança. |
| E se o monolito ficar grande demais? | Ele é **modular**: cada módulo tem fronteira e schema próprios. Dá para extrair Pedidos ou Estoque depois, com o padrão Strangler Fig. |
| Por que não Kubernetes? | ECS Fargate dá escala automática e Multi-AZ sem operar um cluster. Com 1 DevOps em meio período, isso pesa. |
| Como garantem que não vendem sem estoque? | Reserva de estoque e criação do pedido na **mesma transação** do banco. Se faltar item, nada é gravado. |
| E se o cliente clicar duas vezes em "pagar"? | A cobrança usa a **chave de idempotência** (id do pedido): a segunda chamada devolve o mesmo resultado, sem nova cobrança. |
| Quanto custa? | Meta de até ~US$ 3 mil/mês fora do pico. A maior parte dos serviços cobra por uso e volta ao mínimo depois da Black Friday. A estimativa fina sai da AWS Pricing Calculator. |
| Por que AWS e não Azure/GCP? | Região em São Paulo, serviços gerenciados equivalentes e familiaridade da equipe. Docker, PostgreSQL e Terraform reduzem a dependência. |

## Dicas de apresentação

- Ensaie com cronômetro. Se passar de 15 min, encurte os slides 3 e 4.
- No slide de componentes, use o ponteiro ou zoom: o PNG está em alta resolução.
- Termine cada parte com o **atributo de qualidade** que ela atende. É isso que "vende" a arquitetura.
