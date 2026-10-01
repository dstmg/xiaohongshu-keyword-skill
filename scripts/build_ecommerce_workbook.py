"""Optional generic ecommerce interpretation; collection remains the core capability."""
import argparse
import re
from pathlib import Path
from build_baking_workbook import enhance


def classify(term):
    rules = [
        (r'招聘|面试|工资', '非零售需求', 1, 1, '排除招聘等非商品运营需求'),
        (r'代理|加盟|经销', '渠道合作', 8, 3, '人工核实合作条件，不推断零售购买意图'),
        (r'上涨原因|涨价原因|行情', '行情信息', 4, 7, '核实行情来源与日期'),
        (r'在哪里买|哪里买|购买|下单|旗舰店|正品店', '购买渠道', 10, 6, '核实购买渠道、商品规格及履约条件'),
        (r'批发|供货|供应商|起订', '批量采购', 9, 6, '核实起订量、供货、包装与运费'),
        (r'退货|退款|售后|保修', '售后问题', 3, 8, '明确售后范围、条件及办理方式'),
        (r'坏了|故障|失败|怎么办|不能|不起|不出', '使用问题', 4, 9, '结合商品资料或实测整理排查步骤'),
        (r'区别|对比|测评|哪个牌子|哪种好|哪个好|怎么选', '选购比较', 7, 9, '比较可核实的参数、用途及适用限制'),
        (r'多少钱|价格|到手价|优惠', '价格优惠', 8, 6, '标明规格、价格日期及优惠条件'),
        (r'尺寸|规格|型号|材质|成分|参数|含量|保质|储存', '商品信息', 6, 8, '检查详情页是否回答规格、参数或保存问题'),
        (r'教程|做法|配方|怎么用|怎么做|安装|搭配|清洗', '使用方法', 4, 9, '提供经过核实的使用步骤与注意事项'),
    ]
    for pattern, category, purchase, content, action in rules:
        if re.search(pattern, term):
            return category, purchase, content, '未确认', '', action
    return '待人工判断', 4, 4, '未确认', '', '通用规则未覆盖；结合类目与商品人工判断，不套用其他类目规则'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    print('路径、去重词、待采集:', enhance(args.input, args.output, classify, '电商需求分类', 'ecommerce-v1-20260930'))
