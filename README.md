# Turing


Этот проект содержит скрипты для генерации и симуляции работы **машины Тьюринга**.  
Он позволяет создавать описание машины в текстовом формате, генерировать случайные ленты и запускать симуляцию с выводом результата в файл.

---

## Содержание

- `generator.py` — генератор файлов для машины Тьюринга и ленты.
- `simulator.py` — симулятор машины Тьюринга.
- `Turing/` — пример папки с `machine.txt` и `tape.txt`.
- `output.txt` — результат работы симулятора.

---

## Установка

1. Установите Python 3.8 или выше.
2. Скачайте файлы `generator.py` и `simulator.py` в одну папку.
3. (Опционально) Создайте виртуальное окружение:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate      # Windows

## Генерация файлов
```bash
python generator.py <template> <outdir> <length>
<template> — шаблон машины:
  invert — инвертирует 0 → 1 и 1 → 0
  erase — стирает все символы
  binary_increment — прибавляет 1 к бинарному числу на ленте
<outdir> — папка для сохранения файлов (machine.txt и tape.txt)
<length> — длина случайной ленты

## Запуск симуляции
```bash
python simulator.py <machine.txt> <tape.txt> <output.txt>
  <machine.txt> — описание машины
  <tape.txt> — начальная лента
  <output.txt> — файл для записи результата


 
