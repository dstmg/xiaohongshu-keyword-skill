from build_ecommerce_workbook import classify

for term, category in [
    ('口红在哪里买', '购买渠道'),
    ('连衣裙尺寸', '商品信息'),
    ('扫地机器人故障', '使用问题'),
    ('高筋面粉蛋白质含量', '商品信息'),
    ('洗发水哪个好', '选购比较'),
    ('沙发退货', '售后问题'),
    ('高筋面粉做吐司', '待人工判断'),
]:
    result = classify(term)
    assert result[0] == category, (term, result)
    assert 1 <= result[1] <= 10 and 1 <= result[2] <= 10
print('通用电商分类检查通过：7 个跨类目案例')
