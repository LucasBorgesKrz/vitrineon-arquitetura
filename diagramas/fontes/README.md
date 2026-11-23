# Fontes dos diagramas

Os diagramas foram descritos em **Graphviz (DOT)**, texto versionável no Git.

| Arquivo | Diagrama |
|---|---|
| `01-casos-de-uso.dot` | Casos de uso (reprodução do modelo Astah da atividade anterior) |
| `02-componentes.dot` | Componentes (gerado por `gen_componentes.py`) |
| `03-implantacao.dot` | Implantação UML (gerado por `gen_implantacao.py`) |
| `ator.png`, `componente.png` | Ícones UML usados nos diagramas |

## Como regerar os PNGs

```bash
# dentro desta pasta, com o Graphviz instalado (https://graphviz.org/download/)
python3 gen_componentes.py 02-componentes.dot     # opcional: só se editar o .py
python3 gen_implantacao.py 03-implantacao.dot      # opcional: só se editar o .py
dot -Tpng -Gdpi=150 01-casos-de-uso.dot -o ../01-casos-de-uso.png
dot -Tpng -Gdpi=170 02-componentes.dot  -o ../02-componentes.png
dot -Tpng -Gdpi=170 03-implantacao.dot  -o ../03-implantacao.png
```

Também é possível colar o conteúdo dos `.dot` em um editor on-line de Graphviz para visualizar e ajustar.
Se o professor exigir **Astah/Modelio**, os diagramas podem ser redesenhados na ferramenta usando estes PNGs como referência: os nomes dos componentes e nós são os mesmos do README.
