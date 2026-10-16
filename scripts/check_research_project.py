"""Behavior checks; no browser/network or production files."""
import json
from pathlib import Path
import tempfile
from research_project import append, render

with tempfile.TemporaryDirectory() as temp:
    base = Path(temp)
    (base / 'shot.png').write_bytes(b'test-image-fixture')
    capture = base / 'capture.json'
    project = base / 'project'
    def write(root='测试', status='empty'):
        capture.write_text(json.dumps({'roots': [root], 'queries': [dict(query=root, depth=0, status=status, captured_at='2026-10-16T00:00:00Z', screenshots=['shot.png'], suggestions=[])]}), encoding='utf-8')
    write()
    append(project, capture)
    old = (project / '小红书关键词研究.html').read_bytes()
    assert append(project, capture) == 'duplicate: no change'
    write('另一个词')
    append(project, capture)
    state = json.loads((project / 'research-project.json').read_text(encoding='utf-8'))
    assert len(state['batches']) == 2
    write(status='error')
    append(project, capture)
    state = json.loads((project / 'research-project.json').read_text(encoding='utf-8'))
    page = render(state)
    assert '"complete": true' in page
    before = (project / '小红书关键词研究.html').read_bytes()
    write('../not-a-real-file')
    bad = json.loads(capture.read_text())
    bad['queries'][0]['screenshots'] = ['../missing.png']
    capture.write_text(json.dumps(bad))
    try:
        append(project, capture)
        raise RuntimeError('invalid evidence accepted')
    except AssertionError:
        pass
    assert (project / '小红书关键词研究.html').read_bytes() == before
    assert len(list((project / 'evidence').iterdir())) == 1
print('PASS: append, duplicate, failed-batch fallback, invalid-evidence protection, evidence dedup')
