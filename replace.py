import os

# Словарь замен
replacements = {
    'import tkinter as tk': 'import customtkinter as ctk',
    'tk.Button': 'ctk.CTkButton',
    'tk.Frame': 'ctk.CTkFrame',
    'ctk.CTkLabel': 'ctk.CTkLabel',
    'tk.Entry': 'ctk.CTkEntry',
    'tk.StringVar': 'ctk.StringVar',
    'tk.IntVar': 'ctk.IntVar',
    'tk.DoubleVar': 'ctk.DoubleVar',
    'tk.BooleanVar': 'ctk.BooleanVar',
}

# Проходим по всем .py файлам
for filename in os.listdir('.'):
    if filename.endswith('.py') and filename != 'replace.py':  # Исключаем сам скрипт
        print(f" Обработка: {filename}")

        # Читаем файл
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Делаем замены
        for old, new in replacements.items():  # ← ИСПРАВЛЕНО: было s.items()
            if old in content:
                content = content.replace(old, new)
                print(f"   ✅ Заменено: {old} → {new}")

        # Записываем обратно
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Готово: {filename}\n")

print("🎉 Все файлы обработаны!")