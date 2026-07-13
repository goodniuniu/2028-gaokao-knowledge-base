# -*- coding: utf-8 -*-
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

date_dir = os.path.join(os.path.dirname(__file__), '日期词表')
files = sorted([f for f in os.listdir(date_dir) if f.endswith('.md')])

total = 0
print('+' + '-' * 50 + '+')
print(f'| {"日期":10} | {"词数":6} | {"验证":6} |')
print('+' + '-' * 50 + '+')
for f in files:
    filepath = os.path.join(date_dir, f)
    with open(filepath, 'r', encoding='utf-8') as fh:
        count = len([l for l in fh if l.startswith('|') and '单词' not in l and '---' not in l])
    total += count
    status = 'OK' if (count == 123 or count == 122) else 'ERR'
    print(f'| {f[:-3]:10} | {count:6} | {status:6} |')
print('+' + '-' * 50 + '+')
print(f'总计: {total} 词')
print(f'预期: 6008 词')
print(f'差异: {total - 6008}')
