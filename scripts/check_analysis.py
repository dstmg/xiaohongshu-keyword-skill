"""Check automatic interpretation grounding and report integration."""
from analyze_research import analyze
from research_project import render
q = dict(query='测试商品', depth=0, status='ok', captured_at='2026-10-17T00:00:00Z', screenshots=['evidence/test.png'], suggestions=[{'term': t, 'rank': i+1} for i,t in enumerate(['测试商品多少钱', '测试商品热销第一名', '测试商品怎么做', '<script>测试</script>'])])
a = analyze('测试商品', [q])
assert a['unique_terms'] == 4
assert a['items'][1]['category'] == '声明与适用性核查'
assert a['items'][3]['category'] == '待进一步判断'
assert all(x['sources'][0]['screenshot'] == 'evidence/test.png' for x in a['items'])
page = render({'batches':[{'id':'one', 'capture':{'roots':['测试商品'], 'queries':[q]}}]})
assert 'id="analysisCards"' in page and 'renderAnalysis(entries)' in page
assert '<script>测试</script>' not in page
assert '\\u003cscript>' in page
assert 'method' in page and '声明与适用性核查' in page
assert q['suggestions'][0]['term'] == '测试商品多少钱'
card = dict(title='价格说明', finding='发现价格问法', action='核对报价', verification='需要真实规格和日期', source_terms=['测试商品多少钱'])
assert analyze('测试商品', [q], [card])['interpretation'][0]['sources'][0]['rank'] == 1
try:
    analyze('测试商品', [q], [{**card, 'source_terms':['不属于本批的词']}])
    raise AssertionError('cross-batch evidence accepted')
except ValueError:
    pass
print('PASS: automatic analysis, evidence grounding, safety/unknown routing, HTML integration/escaping, raw preservation')
