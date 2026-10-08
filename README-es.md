# dsh-ppap-check — Verificación de la completitud de los elementos de presentación del PPAP

`dsh-ppap-check` lee una lista de elementos de presentación del PPAP —la cabecera de la pieza más una fila por elemento— y comprueba lo que a una lista se le puede exigir mecánicamente: que un elemento requerido por el cliente lleve un registro de presentación, que un elemento presentado lleve fecha, que un elemento controlado (registro de diseño, FMEA, plan de control, diagrama de flujo del proceso, resultados dimensionales, MSA) lleve una revisión, que la hoja indique su número de pieza y su nivel de presentación, que los números de elemento sean únicos y que no sobreviva ningún marcador de plantilla en la columna del elemento.

## Qué responde

| Usted pregunta | Qué responde |
|---|---|
| Un elemento está marcado como requerido en la columna 是否要求, pero no tiene registro de presentación, ¿se informa? | Sí. `PP-001` señala la fila cuando la columna `required` contiene un valor que cuenta como requerido (`是`, `Y`, `yes`, `true`, `要求`, `√`) y la columna `submitted` está vacía. Lee esa columna de su propia lista, nunca un catálogo de elementos incorporado —qué elementos se exigen depende del nivel que indique el cliente— y no juzga si el contenido de lo presentado es aceptable. |
| La fila figura como presentada, pero la celda de fecha está vacía. ¿Y si la fecha está puesta pero cae después del plazo del cliente? | `PP-002` señala la fila cuya columna `submitted` contiene un valor que cuenta como presentado (`是`, `Y`, `yes`, `true`, `已提交`, `√`) y cuya celda `submittedAt` está en blanco. Solo comprueba que la celda de la fecha esté rellena: no comprueba si la fecha cae dentro del plazo que fija el plan de proyecto del cliente. |
| La fila del plan de control está rellena pero su celda de versión está vacía, ¿se informa? ¿Y los elementos que por naturaleza no llevan versión? | `PP-003` mira los nombres de elemento que coinciden con `conditionPattern` —registro de diseño, cambio de ingeniería, DFMEA/PFMEA, plan de control, diagrama de flujo del proceso, resultados dimensionales, análisis del sistema de medición, muestras, auxiliares de verificación, PSW, informes de material, capacidad inicial del proceso— e informa cada fila coincidente cuya celda `version` esté vacía. Solo comprueba que la versión esté rellena, no que sea la correcta o la vigente; si un elemento realmente no lleva versión, restrinja el patrón. |
| Todas las filas de elementos parecen completas, pero la herramienta dice que falta el número de pieza y el nivel. En nuestro formulario el nivel va en cada fila. | `PP-004` lee solo la cabecera: `partNo` y `level` deben estar ambos en la parte superior del material. Si su formulario guarda el nivel en las filas de detalle, cambie los `fields` de esta regla o escriba una comprobación propia: la regla no busca esos valores dentro de las filas. |
| La celda del nivel dice `Level 3`, pero `PP-005` no dice nada al respecto. | `PP-005` viene con la lista `values` vacía, y vacía significa sin configurar, así que se informa a sí misma en `skipped` en lugar de pasar en silencio. Ponga en `values` las grafías de nivel de su cliente y señalará cualquier valor que no esté en la lista. Aun así solo comprueba que el valor esté en su lista —si el nivel elegido es el correcto lo decide el cliente—, y por eso está limitada a `info`. |
| Nuestra lista se copió de la plantilla del año pasado: un nombre de elemento todavía dice 【待填】 y dos filas llevan el mismo número de elemento. | `PP-006` señala un nombre de elemento que aún contiene un marcador —`【`, `】`, `{{`, `}}`, `XXX`, `xxx`, `待填`, `待补充`, `TBD`, `todo`, una lista `terms` ajustable a su plantilla—. `PP-007` señala un número de elemento repetido en `elementNo`, comparando con los espacios en blanco ignorados; un hallazgo suele significar que el elemento se registró dos veces o que el número se copió mal, y cuál de las dos cosas es debe confirmarlo una persona. |

## Normas que sigue

| Documento | Número | Reglas que lo citan |
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

| Superficie | Estado |
|---|---|
| Harness | Rango de peers `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — verificado para aceptar tanto `0.2.0-rc.2` como `0.2.1-alpha.1`. **No se declara `engines.dsh`**: no tiene lector y no puede rechazar ningún host |
| Node | `^22.19.0 || >=24.0.0` |
| Plataformas | Todas (ESM puro; sin código nativo, sin red, sin llamada al modelo) |
| Modo de herramienta | Funciona en `native`, `ptc` y `both`; para un directorio completo use `ptc` |

## What it does

La tabla de reglas, los campos y el comportamiento detallado están en [README.md](README.md#what-it-does) (versión principal en inglés). El plugin sólo enumera divergencias literales frente a las cláusulas citadas e indica en `skipped` cada comprobación que no pudo ejecutarse.

## Install

```sh
dsh plugin --profile <name> add dsh-ppap-check
dsh --profile <name> --dump-config | grep 'dsh-ppap-check'
```

## Configuration

Todos los parámetros ajustables viven en el esquema Schemastery de `src/config.ts`, por lo que se cambian desde `cordis.yml` sin tocar el código; los umbrales por regla están en el paquete de reglas bajo `rules/`.

| Clave | Tipo | Predeterminado | Descripción |
|---|---|---|---|
| `rulesFile` | string | `rules/ppap-check.yaml` | Ruta del paquete de reglas, relativa a la raíz del paquete |
| `disabledRules` | string[] | `[]` | Ids de reglas que se dejan de ejecutar; cada una aparece en `skipped` |
| `onlyRules` | string[] | `[]` | Ejecutar solo estas reglas; vacío ejecuta todas |
| `skipNotes` | string | `""` | Nota añadida a cada motivo de `skipped` |
| `timeoutMs` | number | `120000` | Presupuesto de tiempo de espera cooperativo de la herramienta |

## Material format

Acepta JSON o YAML. El ejemplo completo de campos está en [README.md](README.md#material-format) (versión principal en inglés). Los campos son opcionales en la capa de lectura y los valida el motor, de modo que una exportación parcial produce hallazgos sobre lo que falta en lugar de un fallo.

## Rule sources

Los datos de las reglas están separados del código: cada regla lleva documento, número, cláusula en la numeración propia de la fuente, extracto literal y URL de origen. El cargador impone que el extracto sea una cita real de al menos ocho caracteres y que una comprobación basada sólo en un principio general (`kind: derived-from-principle`, tope `warn`) o en una política local (`kind: institutional-configuration`, tope `info`) nunca se declare `error`.

Los límites verificados y las conclusiones deliberadamente **no** afirmadas están en [README.md](README.md#rule-sources) (versión principal en inglés) y en `rules/evidence/`.

## Troubleshooting

- **El plugin se instala pero la herramienta no aparece**: compruebe que `main` resuelve a `lib/index.mjs` y que `pnpm run build` lo generó.
- **`dsh plugin add` rechaza el paquete**: la faixa de peers cubre `0.1.x` y `0.2.x`; fuera de ella, conceda una exención explícita con `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`.
- **Una regla no se ejecutó**: lea el arreglo `skipped`.
- **`check` informa `manifest-peers` como fallo**: es un problema conocido de `dsh-plugin-dev`; el runtime aplica la compatibilidad al instalar.
- **Los horarios parecen desplazados**: toda la aritmética es de hora local sobre las cadenas entregadas.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-ppap-check
```

El último comando copia el kit compartido de `../_shared` a `src/shared/`; vuelva a ejecutarlo tras cada cambio compartido.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-ppap-check contributors.
