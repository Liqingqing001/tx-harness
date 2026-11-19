"""Usage: python scripts/check_t01.py path/to/summary.csv"""
import csv
import sys
from decimal import Decimal

def check(path):
    with open(path, encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ['region', 'total'], '列名或顺序错误'
        rows = list(reader)
    assert len(rows) == 2, '应有两个区域且不能重复'
    actual = {r['region']: Decimal(r['total']) for r in rows}
    assert actual == {'华东': Decimal('150.50'), '华南': Decimal('200.00')}, actual
    assert all(len(r['total'].split('.')[-1]) == 2 and '.' in r['total'] for r in rows), '金额须保留两位小数'
    print('PASS: summary.csv 数值与格式；notes.md 和原文件需人工核查')

if __name__ == '__main__':
    check(sys.argv[1])
