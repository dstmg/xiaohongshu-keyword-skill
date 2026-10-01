from build_baking_workbook import classify

cases = {
    '南顺面粉批发': ('批量采购', 9, 6),
    '南顺面粉价格上涨原因': ('行情信息', 4, 7),
    '高筋面粉推荐做包子': ('用途适配', 6, 9),
    '高筋面粉不出膜': ('制作问题', 4, 9),
    '高筋面粉蛋白质含量': ('原料参数', 6, 8),
    '高筋面粉在哪里买': ('购买渠道', 10, 6),
    '面粉工厂招聘': ('非零售需求', 1, 1),
    '南顺面粉25kg': ('商用规格线索', 7, 5),
}
for term, expected in cases.items():
    assert classify(term)[:3] == expected, (term, classify(term), expected)
print('烘焙分类测试通过:', len(cases))
