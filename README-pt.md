# dsh-ppap-check — Verificação da completude dos elementos de submissão do PPAP

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-ppap-check` lê uma lista de elementos de submissão do PPAP —o cabeçalho da peça mais uma linha por elemento— e verifica o que a uma lista se pode exigir mecanicamente: que um elemento exigido pelo cliente tenha um registo de submissão, que um elemento submetido tenha data, que um elemento controlado (registo de projeto, FMEA, plano de controlo, fluxograma do processo, resultados dimensionais, MSA) tenha uma revisão, que a folha indique o número da peça e o nível de submissão, que os números de elemento sejam únicos e que não sobreviva nenhum marcador de modelo na coluna do elemento.

## Como é a saída

![Terminal demo of dsh-ppap-check: real output over its PP-001 fixture](https://raw.githubusercontent.com/PerryLink/dsh-ppap-check/main/docs/assets/dsh-ppap-check-demo.png)

Saída real deste plugin sobre o seu próprio fixture de teste `PP-001` — não é uma simulação. O pacote de regras não inventa citações, por isso cada achado nomeia a cláusula aplicada e avisa que o seu texto não foi obtido.

## O que ele responde

| Você pergunta | O que ele responde |
|---|---|
| Um elemento está marcado como exigido na coluna 是否要求, mas não há registo de submissão — isso é reportado? | Sim. `PP-001` assinala a linha quando a coluna `required` contém um valor que conta como exigido (`是`, `Y`, `yes`, `true`, `要求`, `√`) e a coluna `submitted` está vazia. Lê essa coluna da sua própria lista, nunca um catálogo de elementos incorporado — que elementos são exigidos depende do nível que o cliente indicar — e não julga se o conteúdo do que foi submetido é aceitável. |
| A linha consta como submetida, mas a célula da data está vazia. E se a data estiver preenchida mas cair depois do prazo do cliente? | `PP-002` assinala a linha cuja coluna `submitted` contém um valor que conta como submetido (`是`, `Y`, `yes`, `true`, `已提交`, `√`) e cuja célula `submittedAt` está em branco. Verifica apenas que a célula da data está preenchida: não verifica se a data cai dentro do prazo definido pelo plano de projeto do cliente. |
| A linha do plano de controlo está preenchida mas a célula da versão está vazia — é reportado? E os elementos que por natureza não têm versão? | `PP-003` olha para os nomes de elemento que correspondem a `conditionPattern` — registo de projeto, alteração de engenharia, DFMEA/PFMEA, plano de controlo, fluxograma do processo, resultados dimensionais, análise do sistema de medição, amostras, auxiliares de verificação, PSW, relatórios de material, capacidade inicial do processo — e reporta cada linha correspondente cuja célula `version` esteja vazia. Verifica apenas que a versão está preenchida, não que seja a correta ou a vigente; se um elemento realmente não tiver versão, restrinja o padrão. |
| Todas as linhas de elementos parecem completas, mas a ferramenta diz que falta o número da peça e o nível. No nosso formulário o nível fica em cada linha. | `PP-004` lê apenas o cabeçalho: `partNo` e `level` têm de estar ambos no topo do material. Se o seu formulário guarda o nível nas linhas de detalhe, altere os `fields` desta regra ou escreva uma verificação própria — a regra não procura esses valores dentro das linhas. |
| A célula do nível diz `Level 3`, mas o `PP-005` não diz nada sobre isso. | O `PP-005` vem com a lista `values` vazia, e vazia significa não configurada, pelo que se reporta em `skipped` em vez de passar em silêncio. Coloque em `values` as grafias de nível do seu cliente e ela assinalará qualquer valor fora da lista. Mesmo assim, verifica apenas se o valor está na sua lista — se o nível escolhido é o correto decide o cliente — e é por isso que está limitada a `info`. |
| A nossa lista foi copiada do modelo do ano passado: um nome de elemento ainda diz 【待填】 e duas linhas têm o mesmo número de elemento. | `PP-006` assinala um nome de elemento que ainda contém um marcador — `【`, `】`, `{{`, `}}`, `XXX`, `xxx`, `待填`, `待补充`, `TBD`, `todo`, uma lista `terms` ajustável ao seu modelo. `PP-007` assinala um número de elemento repetido em `elementNo`, comparando com os espaços em branco ignorados; um achado costuma significar que o elemento foi registado duas vezes ou que o número foi copiado mal, e qual das duas coisas é tem de ser confirmado por uma pessoa. |

## Normas que segue

| Documento | Número | Regras que o citam |
|---|---|---|
| 《生产件批准程序（PPAP）手册》 | AIAG PPAP（现行版次与条号本次未核实） | PP-001, PP-002, PP-003, PP-004, PP-005, PP-006, PP-007 |

**Boundary:** this plugin checks a **PPAP 提交要素清单** for what a checklist can be held to mechanically —
that an element the customer required carries a submission record, that a submitted element carries a date,
that a controlled element (design record, FMEA, control plan, process flow, dimensional results, MSA) carries
a revision, that the sheet names its part number and submission level, that element numbers are unique, and
that no template placeholder survives. It does **not** decide whether PPAP may be approved, whether the level
is right, or whether an element's content satisfies the customer. **The submission level is the customer's to
set, and this plugin ships no level-to-element mapping.**

> ### ⚠️ Read this before trusting a citation in the report
>
> **Every `excerpt` in this plugin's rule pack says, in so many words, that the clause text was not
> obtained.** The method lives in the automotive **AIAG《生产件批准程序（PPAP）手册》** (and the customer
> specific requirements under IATF 16949). The verification pass could not retrieve verbatim clause text, so
> rather than paraphrase a quotation the pack states the gap in the `excerpt` field itself and puts the
> honest reasoning in `note`. Every rule is therefore `warn` or `info`, and a test asserts that no rule
> claims a quotation it does not have. **When the text is in hand, two things must be done: replace each
> `excerpt` with the real clause, and raise `kind` to `direct`.**
>
> **Which elements must be submitted depends on the level the customer specifies** (Level 1–5), so `PP-001`
> reads the **checklist's own 是否要求 column** rather than any built-in list, and `PP-005`'s level vocabulary
> ships **empty** — with no vocabulary configured it reports itself in `skipped` instead of passing quietly.

## Compatibility

| Superfície | Estado |
|---|---|
| Harness | Faixa de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificada para aceitar tanto `0.2.0-rc.2` quanto `0.2.1-alpha.1`. **`engines.dsh` não é declarado**: não tem leitor e não pode recusar nenhum host |
| Node | `^22.19.0 || >=24.0.0` |
| Plataformas | Todas (ESM puro; sem código nativo, sem rede, sem chamada ao modelo) |
| Modo de ferramenta | Funciona em `native`, `ptc` e `both`; para um diretório inteiro use `ptc` |

## What it does

A tabela de regras, os campos e o comportamento detalhado estão em [README.md](README.md#what-it-does) (versão principal em inglês). O plugin apenas lista divergências literais frente às cláusulas citadas e indica em `skipped` cada verificação que não pôde ser executada.

## Install

```sh
dsh plugin --profile <name> add dsh-ppap-check
dsh --profile <name> --dump-config | grep 'dsh-ppap-check'
```

## Configuration

Todos os parâmetros ajustáveis ficam no esquema Schemastery de `src/config.ts`, portanto mudam pelo `cordis.yml` sem editar código; os limites por regra ficam no pacote de regras sob `rules/`.

| Chave | Tipo | Padrão | Descrição |
|---|---|---|---|
| `rulesFile` | string | `rules/ppap-check.yaml` | Caminho do pacote de regras, relativo à raiz do pacote |
| `disabledRules` | string[] | `[]` | Ids de regras a desativar; cada uma aparece em `skipped` |
| `onlyRules` | string[] | `[]` | Executar apenas estas regras; vazio executa todas |
| `skipNotes` | string | `""` | Nota acrescentada a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Orçamento de tempo limite cooperativo da ferramenta |

## Material format

Aceita JSON ou YAML. O exemplo completo de campos está em [README.md](README.md#material-format) (versão principal em inglês). Os campos são opcionais na camada de leitura e validados pelo motor, de modo que uma exportação parcial gera achados sobre o que falta em vez de falhar.

## Rule sources

Os dados das regras ficam separados do código: cada regra traz documento, número, cláusula na numeração própria da fonte, trecho literal e URL de origem. O carregador impõe que o trecho seja citação real de pelo menos oito caracteres e que uma verificação baseada apenas em princípio geral (`kind: derived-from-principle`, teto `warn`) ou em política local (`kind: institutional-configuration`, teto `info`) nunca seja declarada `error`.

Os limites verificados e as conclusões deliberadamente **não** afirmadas estão em [README.md](README.md#rule-sources) (versão principal em inglês) e em `rules/evidence/`.

## Troubleshooting

- **O plugin instala mas a ferramenta não aparece**: confirme que `main` resolve para `lib/index.mjs` e que `pnpm run build` o gerou.
- **`dsh plugin add` recusa o pacote**: a faixa de peers cobre `0.1.x` e `0.2.x`; fora dela, conceda isenção explícita com `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`.
- **Uma regra não executou**: leia o arranjo `skipped`.
- **`check` informa `manifest-peers` como falha**: problema conhecido do `dsh-plugin-dev`; o runtime aplica a compatibilidade na instalação.
- **Os horários parecem deslocados**: toda a aritmética é de hora local sobre as cadeias fornecidas.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-ppap-check
```

O último comando copia o kit compartilhado de `../_shared` para `src/shared/`; execute-o novamente após cada alteração compartilhada.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-ppap-check contributors.
