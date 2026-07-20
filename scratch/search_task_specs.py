import os, re

keywords = ['grid', '4x4', '5x5', 'Rojas', 'Libano', 'Líbano', 'distractor', '160', 'block', 'matrix', '4 x 4', '5 x 5']

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith(('.md', '.py', '.txt', '.json')) and not '.git' in root:
            fp = os.path.join(root, f)
            try:
                content = open(fp, 'r', encoding='utf-8', errors='ignore').read()
                matches = [kw for kw in keywords if kw.lower() in content.lower()]
                if matches:
                    lines = content.split('\n')
                    for i, line in enumerate(lines, 1):
                        if any(kw.lower() in line.lower() for kw in ['grid', '4x4', '5x5', 'matrix', '160 trials', 'block']):
                            print(f"{fp}:{i}: {line.strip()[:140]}")
            except Exception:
                pass
