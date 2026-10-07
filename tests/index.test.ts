import { describeTablePlugin } from './table-plugin-suite.ts'
import { Config } from '../src/config.ts'
import { parseMaterial, runCheck, SPEC } from '../src/model.ts'
import { buildView } from '../src/view.ts'
import { inject, name, resolvePackageFile, TOOL_NAME } from '../src/index.ts'

describeTablePlugin({
  name,
  inject,
  TOOL_NAME,
  resolvePackageFile,
  Config,
  rulesFile: 'rules/ppap-check.yaml',
  parseMaterial,
  runCheck,
  buildView,
  columnNames: SPEC.columns,
  samples: {
    good: {
      partNo: 'P-2026-001',
      partName: '前支架',
      supplier: '某某零部件有限公司',
      level: 'Level 3',
      rows: [
        {
          序号: '1',
          提交要素: '设计记录',
          是否要求: '是',
          是否提交: '是',
          提交日期: '2026-03-05',
          版本: 'B',
          责任人: '张工',
        },
      ],
    },
    unknownColumn: { rows: [{ 备注: '甲' }] },
  },
})
