"""Evidence-linked initial interpretation; never a product-fact inference."""
import re

VERSION = 'evidence-rules-v1'
RULES = [
    (r'辅食|宝宝|婴|减脂|减肥|无糖|无添加|热销|第一|100%', '声明与适用性核查', '先核对词中的排名、成分或人群表述', '核实标签、厂家资料及可靠依据；不据搜索词宣称排名、健康功效或特殊人群适用'),
    (r'退货|退款|售后|保修|坏了|失败|为什么|怎么办|很硬|回缩|不起', '问题排查与客服', '把具体问题整理为客服排查清单', '补齐操作条件、使用过程和售后范围，不凭词面断定原因'),
    (r'多少钱|价格|批发|起订|一斤|一袋|优惠', '价格与采购条件', '补齐同规格价格与采购条件说明', '需要实际规格、报价日期、运费、起订量；词面不提供真实价格'),
    (r'旗舰店|哪里买|在哪里买|正品|下单', '购买渠道', '检查购买入口、规格与履约说明', '核对渠道身份与实际授权，不因词中出现旗舰店就认定官方'),
    (r'区别|对比|哪个牌子|哪种|怎么选|分辨|是什么|代替', '选购与替代', '制作参数、用途与选择条件对照', '比较真实商品资料；替代方案需实测，不能仅凭词推荐品牌'),
    (r'规格|含量|蛋白|储存|保质|家用|小袋|kg|斤装', '商品信息', '检查规格、使用场景与保存说明', '补充包装标签和商品参数，不从关键词推定规格或含量'),
    (r'做|烙|饼|面包|馒头|饺子|发面|空气炸锅|烘焙|教程|配方', '用途与内容选题', '围绕这个用途做一次过程实测或答疑', '核对产品适用性、设备与操作条件；配方和结果需实测，不直接当商品卖点'),
]


def analyze(root, queries, interpretation=None):
    terms = {}
    for q in queries:
        if q.get('status') != 'ok':
            continue
        for s in q.get('suggestions', []):
            term = s['term']
            item = terms.setdefault(term, {'term': term, 'sources': []})
            source = {'query': q['query'], 'rank': s['rank'], 'captured_at': q['captured_at'], 'screenshot': s.get('screenshot') or next(iter(q.get('screenshots', [])), '')}
            if source not in item['sources']:
                item['sources'].append(source)
    groups = {}
    for term, item in terms.items():
        category, action, verify = ('待进一步判断', '结合商品与转化目标判断这条词的用途', '词面规则未覆盖，Agent需继续阅读原词和业务资料；不套用其他品类结论')
        for pattern, cat, task, boundary in RULES:
            if re.search(pattern, term):
                category, action, verify = cat, task, boundary
                break
        item.update(category=category, action=action, verification=verify)
        groups.setdefault(category, []).append(term)
    result = {'version': VERSION, 'root': root, 'method': '词面规则初步分析，非平台结论', 'business_context': '未提供具体商品资料，以下为待验证研究方向', 'unique_terms': len(terms), 'groups': [{'category': c, 'count': len(v), 'examples': v[:4]} for c, v in groups.items()], 'items': list(terms.values())}
    if interpretation is not None:
        if not isinstance(interpretation, list):
            raise ValueError('Agent解读必须是卡片列表')
        cards = []
        for card in interpretation:
            if not all(isinstance(card.get(k), str) and card[k].strip() for k in ['title', 'finding', 'action', 'verification']):
                raise ValueError('Agent解读卡片字段不完整')
            sources = card.get('source_terms')
            if not isinstance(sources, list) or not sources or any(t not in terms for t in sources):
                raise ValueError('Agent解读引用了不属于当前词根批次的词')
            cards.append({**{k: card[k] for k in ['title', 'finding', 'action', 'verification']}, 'source_terms': sources, 'sources': [s for t in sources for s in terms[t]['sources']]})
        result['interpretation'] = cards
    return result
