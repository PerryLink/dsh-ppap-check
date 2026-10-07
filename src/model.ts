/**
 * dsh-ppap-check — table shape and material contract.
 *
 * The plugin is data-only: this file declares which columns the material may use
 * and how they map onto canonical field names; the shared kit supplies the reader
 * and the check engine, and the rule pack declares every check. Adding a check
 * that fits an existing kind is a rule-pack edit, not a code change.
 */

import { canonicaliseRow, parseTable, type TableSpec } from './shared/table.ts'
import { runTableCheck, type TableCheckOptions, type TableInput } from './shared/rows.ts'
import type { Ruleset } from './shared/rules.ts'

/** Tool id exposed to the model, and the row id in `cordis.patch.yml`. */
export const TOOL_NAME = 'ppap_check'

/** The register's column aliases, declared once so both the spec and the guard see them. */
const COLUMNS = {
  elementNo: ['序号', '要素序号', '编号', 'elementNo', 'no'],
  element: ['提交要素', '要素', '要素名称', '提交项', 'element', 'item'],
  required: ['是否要求', '要求与否', '提交要求', 'required'],
  submitted: ['是否提交', '提交状态', '提交情况', 'submitted'],
  submittedAt: ['提交日期', '完成日期', '日期', 'submittedAt'],
  version: ['版本', '版次', '文件版本', 'version', 'revision'],
  owner: ['责任人', '负责人', '提交人', 'owner'],
  note: ['备注', '说明', 'note', 'remark'],
} as const

/** How the material declares its table. */
export const SPEC: TableSpec = {
  rowKeys: ['rows', 'items', 'elements', '要素'],
  columns: COLUMNS,
  header: {
  partNo: ['partNo', '零件号', '产品编号', '图号'],
  partName: ['partName', '零件名称', '产品名称'],
  supplier: ['supplier', '供应商', '供应商名称'],
  customer: ['customer', '顾客', '主机厂', '客户'],
  level: ['level', '提交等级', 'PPAP等级'],
  submittedAt: ['submittedAt', '提交日期', '批准日期'],
  status: ['status', '批准状态', '状态'],
  },
}

/** Fields the material must carry somewhere for the reader to accept it. */
export const REQUIRE_ANY_OF = [
  '提交要素',
  'element',
  '要素',
  '是否提交',
  'submitted',
  '序号',
  'elementNo',
]

/**
 * Parse the material and attach its canonical field names.
 * @param source - JSON or YAML text.
 * @param target - description of where the material came from.
 * @returns the normalized table, with each row's aliases resolved to field names.
 */
export function parseMaterial(source: string, target: string): TableInput {
  const table = parseTable(source, target, {
    ...SPEC,
    ...(REQUIRE_ANY_OF === undefined ? {} : { requireAnyOf: REQUIRE_ANY_OF }),
  })
  for (const row of table.rows) canonicaliseRow(row, SPEC)
  return table
}

/**
 * Run the rule pack against the material.
 * @param input - normalized table.
 * @param ruleset - validated rule pack.
 * @param options - plugin identity, clock value, rule selection and overrides.
 * @returns the report.
 */
export function runCheck(input: TableInput, ruleset: Ruleset, options: TableCheckOptions) {
  return runTableCheck(input, ruleset, options)
}

export type { TableCheckOptions, TableInput }
