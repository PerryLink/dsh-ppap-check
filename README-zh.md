# dsh-ppap-check — PPAP 提交要素齐备性核对

[![DSH Market](https://raw.githubusercontent.com/2BingLing/dsh-market/master/assets/readme/badge-listed-en.svg)](https://dsh.market/)

`dsh-ppap-check` 读取一份 PPAP 提交要素清单——表头加每个要素一行——核对这份清单自身能被机械核对的部分：顾客要求的要素是否留下提交记录、已提交的要素是否填写提交日期、受控要素（设计记录、FMEA、控制计划、过程流程图、尺寸结果、测量系统分析）是否填写版本、清单是否写明零件号与提交等级、要素序号是否唯一、要素栏是否残留模板占位符。

## 实际输出长什么样

![Terminal demo of dsh-ppap-check: real output over its PP-001 fixture](https://raw.githubusercontent.com/PerryLink/dsh-ppap-check/main/docs/assets/dsh-ppap-check-demo.png)

本插件对自己 `PP-001` 测试夹具的**真实输出**，不是示意图。规则库不伪造引文，因此每条发现都会同时写明所引条款，以及该条款原文本次未取得。

## 它回答什么问题

| 你会问 | 它怎么答 |
|---|---|
| 「是否要求」栏标了要求，却没有提交记录，能查出来吗？ | 能。`PP-001` 在 `required` 栏取到表示「要求」的取值（`是`、`Y`、`yes`、`true`、`要求`、`√`）而 `submitted` 栏为空时逐行报出。它读的是你这张清单自己的那一栏，而不是任何内置要素清单——哪些要素属于要求提交取决于顾客指定的等级；它也不判断已提交的要素内容是否合格。 |
| 某行标了已提交，但提交日期栏空着；如果日期填了却晚于顾客的时限呢？ | `PP-002` 在 `submitted` 栏取到表示已提交的取值（`是`、`Y`、`yes`、`true`、`已提交`、`√`）而 `submittedAt` 栏为空时逐行报出。它只核对日期栏是否填写，不判断日期是否落在顾客项目计划规定的时限内。 |
| 控制计划这一行的版本栏空着，会被报出吗？那些本来就没有版本的要素呢？ | `PP-003` 只核对名称命中 `conditionPattern` 的要素——设计记录、工程更改、DFMEA／PFMEA、控制计划、过程流程图、尺寸结果、测量系统分析、样件、检查辅具、PSW、材料报告、初始过程能力——命中且 `version` 栏为空时逐条报出。它只核对版本栏是否填写，不判断版本是否正确、是否是最新版；若确有要素本来不需要版本，请收窄该模式。 |
| 每个要素行看着都齐了，工具却说清单没写零件号与等级。可我们的表式把等级记在每一行上。 | `PP-004` 只读表头：`partNo` 与 `level` 必须都在材料顶层。若本机构表式把等级记在明细行，请调整本条的 `fields` 或另建一条检查——本条不会到明细行里去找这两个值。 |
| 等级栏写的是 `Level 3`，可 `PP-005` 什么也不说。 | `PP-005` 的 `values` 清单出厂为空，空即未配置，因此本条在 `skipped` 里如实报告自己没能执行，而不是静默通过。把顾客口径的等级写法填进 `values`，清单里不在册的取值就会被报出。即便如此，它也只核对所填值是否在册——等级选得对不对是顾客的决定——这也是本条封顶 `info` 的原因。 |
| 我们的清单是照去年的模板抄的：一个要素名称还写着【待填】，两行又都编了同一个要素序号。 | `PP-006` 会报出仍含占位符的要素名称——`【`、`】`、`{{`、`}}`、`XXX`、`xxx`、`待填`、`待补充`、`TBD`、`todo`，这份 `terms` 清单可按本机构模板调整。`PP-007` 会报出 `elementNo` 中重复的要素序号，比较时忽略空白字符；命中通常意味着重复登记或序号抄错，究竟是哪一种需人工确认。 |

## 依据的标准

| 文件 | 文号 | 引用它的规则 |
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

| 项目 | 状态 |
|---|---|
| Harness | 对等版本范围 `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` —— 已实测同时接受 `0.2.0-rc.2` 与 `0.2.1-alpha.1`。**刻意不声明 `engines.dsh`**：它没有任何读取者，也无法拒装任何宿主 |
| Node | `^22.19.0 || >=24.0.0` |
| 平台 | 全平台（纯 ESM；无原生代码、无联网、不调用模型） |
| 工具模式 | `native` / `ptc` / `both` 均可；批量校验整个目录时建议 `ptc`，schema 成本只付一次 |

## What it does

规则表、字段说明与行为细节见 [README.md](README.md#what-it-does)（英文主版本）。本插件只列出材料与所引条款之间的字面差异，并对无法执行的检查在 `skipped` 中逐项说明。

## Install

```sh
dsh plugin --profile <name> add dsh-ppap-check
dsh --profile <name> --dump-config | grep 'dsh-ppap-check'
```

## Configuration

全部可调参数都在 `src/config.ts` 的 Schemastery schema 中，只改 `cordis.yml` 即可生效，无需改代码；逐条阈值在 `rules/` 下的规则库文件里。

| 键 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `rulesFile` | string | `rules/ppap-check.yaml` | 规则库文件路径，相对插件包根目录 |
| `disabledRules` | string[] | `[]` | 要停用的规则 id 列表；每条都会出现在 `skipped` 中 |
| `onlyRules` | string[] | `[]` | 只执行这些规则 id；留空表示执行全部规则 |
| `skipNotes` | string | `""` | 附加到每条 `skipped` 说明后的备注 |
| `timeoutMs` | number | `120000` | 工具协作式超时预算（毫秒） |

## Material format

支持 JSON 与 YAML。完整字段示例见 [README.md](README.md#material-format)（英文主版本）。字段在读取层是可选的，由检查引擎校验，因此部分导出的材料会产生"缺项"类差异，而不是让程序崩溃。

## Rule sources

规则数据与代码分离，每条规则都带文件名、文号、按原文自身编号体系的条款号、逐字摘录与来源地址。加载期强制：摘录必须是真实引文且不少于八个字符；依据仅为原则性条款（`kind: derived-from-principle`，严重级上限 `warn`）或本机构配置（`kind: institutional-configuration`，上限 `info`）的检查不得标为 `error`。夸大依据的规则库会在加载期失败，而不会产出一份看起来很有底气的报告。

核验中确认的边界与"刻意没有作出的结论"见 [README.md](README.md#rule-sources)（英文主版本）与随包的 `rules/evidence/` 目录。

## Troubleshooting

- **插件装上了但工具不出现**：确认 `main` 指向 `lib/index.mjs` 且 `pnpm run build` 已生成该文件；`main` 写错会让加载器静默跳过该条目。
- **`dsh plugin add` 报版本不兼容**：peer 范围覆盖 `0.1.x` 与 `0.2.x`；若运行时在其之外，可显式豁免：`dsh plugin --profile <name> allow-version <包名@版本> --dsh-version <runtime> --accept-risk`
- **某条规则没有执行**：查看 `skipped` 数组，其中写明了规则 id 与原因。
- **`check` 报 `manifest-peers` 失败**：静态检查器比对的是一份早于 0.2 世代的硬编码 peer 范围；安装期的 peer 校验以运行时为准。这是 `dsh-plugin-dev` 的已知上游问题。
- **时间看起来偏移**：全部计算都是对输入字符串做墙上时钟运算，不做时区换算。

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-ppap-check
```

第 4 项把 `../_shared` 的共享件同步进 `src/shared/`；每次改动共享件后都要重跑。

## License

[Apache License 2.0](LICENSE) © 2026 dsh-ppap-check contributors.
