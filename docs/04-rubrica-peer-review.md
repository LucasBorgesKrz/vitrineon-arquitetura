# 4. Rubrica de Peer Review: Avaliação Arquitetural entre Grupos

> Use esta rubrica para avaliar o projeto de **outro grupo**. Copie o modelo da seção 3 para uma *issue* no repositório do grupo avaliado (ou para um arquivo `peer-review-<grupo>.md`).
> **Regra de ouro:** nada de "achei legal". Todo comentário deve citar **um requisito, um atributo de qualidade ou uma decisão** e explicar o impacto.

## 1. Critérios e níveis

Cada critério recebe de **1 a 4**. Pontuação máxima: **40**.

| # | Critério | 4: Excelente | 3: Bom | 2: Parcial | 1: Insuficiente |
|---|---|---|---|---|---|
| C1 | **Análise do cenário e restrições** | Restrições (equipe, orçamento, prazo, regulação) extraídas do texto e ligadas a decisões | Restrições listadas, mas pouco ligadas às decisões | Restrições genéricas ("tem que ser bom") | Ausente |
| C2 | **RNFs mensuráveis** | Todo RNF tem métrica verificável (ex.: "p95 ≤ 200 ms") | Maioria com métrica | Poucos com métrica | Nenhum RNF mensurável |
| C3 | **Priorização dos atributos (ISO 25010)** | Ranking justificado pelo negócio, com trade-offs explícitos | Ranking justificado, sem trade-offs | Lista sem justificativa | Ausente ou fora da ISO 25010 |
| C4 | **Escolha do estilo arquitetural** | Estilo justificado pelos requisitos, com alternativas comparadas | Justificado, sem alternativas | Estilo citado sem justificativa ("usamos microsserviços porque é moderno") | Estilo não identificável |
| C5 | **Diagrama de Componentes** | Responsabilidades claras, comunicação (síncrona/assíncrona, protocolos) explícita, notação consistente | Componentes claros, comunicação pouco detalhada | Caixas sem responsabilidade definida | Ausente ou ilegível |
| C6 | **Diagrama de Implantação (UML)** | Nós, ambientes de execução, artefatos e caminhos de comunicação; redundância e redes visíveis | Mapeia o software na infraestrutura, com poucos detalhes | Lista de tecnologias sem relação com os componentes | Ausente |
| C7 | **Consistência entre diagramas** | Todo componente aparece em um nó de implantação (de preferência com tabela de mapeamento) | Pequenas omissões | Vários componentes "somem" na implantação | Diagramas não conversam |
| C8 | **Atendimento aos atributos priorizados** | Cada atributo top-3 tem táticas concretas no desenho (redundância, cache, isolamento...) | Táticas para parte dos atributos | Afirma que atende, sem mostrar como | Não relaciona |
| C9 | **Qualidade do documento (README)** | Bem estruturado, navegável, decisões rastreáveis (ADRs), repositório organizado (`/docs`, `/diagramas`, `/apresentacao`) | Bem escrito, alguma desorganização | Difícil de navegar | Incompleto |
| C10 | **Apresentação (pitch)** | Clara para stakeholders, no tempo (10–15 min), defende trade-offs e responde perguntas com segurança | Clara, pequenas falhas de tempo ou foco | Muito técnica ou superficial | Desorganizada |

**Conceito final:** 36–40 Excelente · 28–35 Bom · 20–27 Regular · < 20 Precisa de revisão.

## 2. Checklist de padrões e anti-padrões

Marque o que encontrou. Isso ajuda a escrever comentários específicos.

**Bons sinais**

- [ ] API Gateway (ou BFF) como porta de entrada única
- [ ] Cada microsserviço com seu próprio banco
- [ ] Comunicação assíncrona (filas/eventos) onde a resposta imediata não é necessária
- [ ] Redundância (Multi-AZ, réplicas, load balancer) para os componentes críticos
- [ ] Cache/CDN justificado por requisito de desempenho
- [ ] Dados sensíveis isolados e criptografados
- [ ] Observabilidade (logs, métricas, tracing) prevista
- [ ] Decisões com alternativas e trade-offs registrados

**Sinais de alerta (anti-padrões)**

- [ ] **Monolito distribuído**: microsserviços que compartilham o mesmo banco e as mesmas tabelas
- [ ] **Microsserviços sem motivo**: muitos serviços para uma equipe pequena, sem requisito de escala que justifique
- [ ] **Ponto único de falha** em componente crítico (um único servidor, um único banco sem réplica)
- [ ] **Camadas puladas**: tela acessando o banco diretamente
- [ ] **Chamadas síncronas em cadeia longa** (A → B → C → D) no caminho crítico
- [ ] Componente no diagrama de componentes que **não aparece** na implantação (ou vice-versa)
- [ ] RNF sem métrica ("o sistema deve ser rápido e seguro")
- [ ] Tecnologia escolhida sem relação com nenhum requisito

## 3. Modelo de feedback (copiar e preencher)

```markdown
## Peer Review: Grupo <nome> | Sistema: <sistema>
**Avaliadores:** <grupo avaliador>   **Data:** <dd/mm/aaaa>

### Notas
| C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | Total |
|----|----|----|----|----|----|----|----|----|-----|-------|
|    |    |    |    |    |    |    |    |    |     |  /40  |

### Pontos fortes (mínimo 2)
1. <decisão> atende ao <requisito/atributo> porque <motivo>.
2.

### Oportunidades de melhoria (mínimo 2)
1. <observação> pode causar <impacto no atributo X>. Sugestão: <alternativa>.
2.

### Pergunta para o grupo
- <uma pergunta que faria o grupo pensar sobre um trade-off>
```

## 4. Exemplos de comentários

| ❌ Comentário raso | ✅ Comentário profissional |
|---|---|
| "Achei o diagrama legal." | "O diagrama de componentes deixa clara a separação entre Catálogo e Pedidos, o que atende ao requisito de escalar a busca de forma independente." |
| "Muito complexo." | "A escolha de 8 microsserviços para uma equipe de 4 pessoas aumenta o custo de operação (manutenibilidade). Um monolito modular com 2 serviços extraídos atenderia aos mesmos RNFs de escala." |
| "Faltou segurança." | "O diagrama de implantação coloca o banco de dados em sub-rede pública. Isso contraria o atributo nº 1 (Segurança). Sugestão: sub-rede privada com acesso só pelos serviços." |
| "Não entendi o deploy." | "O 'Serviço de Pagamento' aparece no diagrama de componentes mas não em nenhum nó da implantação. Em qual contêiner ele roda?" |
| "Tá bom." | "A escolha de microsserviços atende ao requisito de escalabilidade, porém o diagrama não mostra o API Gateway, o que pode gerar acoplamento entre os clientes e os serviços internos." |

## 5. Versão Google Forms (opcional)

Para montar a rubrica como formulário:

1. Uma pergunta **"Escala linear 1–4"** para cada critério C1 a C10, com a descrição do nível 4 e do nível 1 nos rótulos.
2. Duas perguntas **"Parágrafo"** obrigatórias: *Pontos fortes* e *Oportunidades de melhoria*.
3. Uma pergunta **"Caixas de seleção"** com os itens do checklist da seção 2.
4. Uma pergunta **"Resposta curta"**: *Pergunta para o grupo*.
