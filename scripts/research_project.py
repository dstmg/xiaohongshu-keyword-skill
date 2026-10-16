"""Append validated capture batches to one research project (Python stdlib only)."""
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import tempfile


def atomic(path, text):
    fd, temp = tempfile.mkstemp(dir=path.parent, prefix='.stage-')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            stream.write(text)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def validate(data, source):
    assert isinstance(data.get('roots'), list) and data['roots'], 'roots required'
    assert all(isinstance(r, str) and r.strip() for r in data['roots']), 'invalid root'
    assert len(set(data['roots'])) == len(data['roots']), 'duplicate roots'
    seen = set()
    for q in data['queries']:
        assert q['query'] not in seen, 'duplicate query'
        seen.add(q['query'])
        assert q['depth'] in (0, 1), 'invalid depth'
        assert q['status'] in ('ok', 'empty', 'blocked', 'error', 'pending'), 'invalid status'
        assert q.get('captured_at'), 'timestamp required'
        terms = q.get('suggestions', [])
        assert bool(terms) == (q['status'] == 'ok'), 'status/suggestions mismatch'
        assert [s['rank'] for s in terms] == list(range(1, len(terms)+1)), 'invalid ranks'
        assert all(isinstance(s['term'], str) and s['term'].strip() for s in terms), 'invalid term'
        if q['status'] in ('ok', 'empty'):
            assert q.get('screenshots'), 'evidence required'
        for name in q.get('screenshots', []):
            p = (source / name).resolve()
            assert p.is_relative_to(source.resolve()) and p.is_file(), 'missing or unsafe evidence'


def root_queries(data, root):
    base = next((q for q in data['queries'] if q['query'] == root and q['depth'] == 0), None)
    if base is None:
        return [], False
    children = {s['term'] for s in base['suggestions']} - {root}
    qs = [base] + [q for q in data['queries'] if q['query'] in children and q['query'] != root]
    done = {q['query'] for q in qs if q['status'] in ('ok', 'empty')}
    return qs, base['status'] in ('ok', 'empty') and children.issubset(done)


def render(store):
    roots = {}
    batches = []
    for batch in store['batches']:
        mapping = {}
        for root in batch['capture']['roots']:
            qs, complete = root_queries(batch['capture'], root)
            item = dict(queries=qs, complete=complete, batch=batch['id'])
            mapping[root] = item
            if complete or root not in roots or not roots[root]['complete']:
                roots[root] = item
        dates = sorted({q['captured_at'][:10] for q in batch['capture']['queries']})
        batches.append(dict(id=batch['id'], roots=mapping, date=' / '.join(dates)))
    assets = Path(__file__).resolve().parent.parent / 'assets'
    payload = json.dumps(dict(roots=roots, batches=batches), ensure_ascii=False).replace('<', '\\u003c')
    template = (assets / 'research.html').read_text(encoding='utf-8')
    return template.replace('__CSS__', (assets / 'research.css').read_text(encoding='utf-8')).replace('__JS__', (assets / 'research.js').read_text(encoding='utf-8')).replace('__DATA__', payload)


def append(project, capture):
    project = Path(project)
    source = Path(capture).resolve()
    data = json.loads(source.read_text(encoding='utf-8-sig'))
    validate(data, source.parent)
    project.mkdir(parents=True, exist_ok=True)
    state = project / 'research-project.json'
    store = json.loads(state.read_text(encoding='utf-8')) if state.exists() else {'version': 1, 'batches': []}
    digest = hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:20]
    if any(b['id'] == digest for b in store['batches']):
        return 'duplicate: no change'
    # Copy evidence under immutable content-addressed names before rendering.
    for q in data['queries']:
        names = []
        for name in q.get('screenshots', []):
            raw = (source.parent / name).read_bytes()
            key = hashlib.sha256(raw).hexdigest()
            suffix = Path(name).suffix.lower()
            assert suffix in ('.png', '.jpg', '.jpeg', '.webp'), 'unsupported image'
            dest = project / 'evidence' / (key + suffix)
            dest.parent.mkdir(exist_ok=True)
            if not dest.exists():
                dest.write_bytes(raw)
            names.append(dest.relative_to(project).as_posix())
        q['screenshots'] = names
    store['batches'].append({'id': digest, 'capture': data})
    page = render(store)  # All validation/rendering happens before replacing current state.
    # One authoritative atomic file; report is a regenerable view of that file.
    atomic(state, json.dumps(store, ensure_ascii=False, indent=2))
    atomic(project / '小红书关键词研究.html', page)
    return str(project / '小红书关键词研究.html')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project', required=True, help='Existing project by default; choose another directory only for a new project')
    p.add_argument('--input', required=True)
    args = p.parse_args()
    print(append(args.project, args.input))
