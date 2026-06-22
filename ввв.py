import os
import re

for filename in os.listdir('.'):
    if filename.endswith('.py') and filename not in ['fix_bg.py', 'replace.py']:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Заменяем fg_color= на fg_color= ТОЛЬКО после ctk.
        lines = content.split('\n')
        new_lines = []

        for line in lines:
            if 'ctk.' in line and 'fg_color=' in line:
                line = re.sub(r'\bbg=', 'fg_color=', line)
            new_lines.append(line)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))

        print(f"✅ {filename}")

print("🎉 Готово!")