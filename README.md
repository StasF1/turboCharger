# Описание
Программа проводит 0D расчёт турбокомпрессора. Написана на языке **_Python 2_**.

По результатам расчёта генерируются отчёты на языке **Markdown** (примеры отчётов представлены ниже), сохраняются рисунки с уже выставленными _размерами_ на них ([примеры рисунков](https://github.com/StasF1/turboCharger/wiki/Примеры-рисунков)). Всё это располагается в папке _results/_, создаваемой автоматически.

![inTurbineWheel-dflt](https://github.com/StasF1/turboCharger/wiki/images/inTurbineWheel.png)

Программа писалась для чтения отчётов  Markdown-редакторе [Typora](https://typora.io). Желательно использовать его для правильного отображения Latex-формул в файлах формата _.md_.

#### Примеры отчётов
|Вариант расчёта         |Настройки        |Отчёт                   |
|-----------------------:|----------------:|:-----------------------|
|     Компрессор         | По умолчанию    |[compressorReport.pdf](https://github.com/StasF1/turboCharger/releases/download/v1-beta/compressorReport.pdf)|
|Радиально-осевая турбина| По умолчанию    |[radialTurbineReport.pdf](https://github.com/StasF1/turboCharger/releases/download/v1-beta/radialTurbineReport.pdf)|
|Осевая турбина          | Не по умолчанию |[axialTurbineReport.pdf](https://github.com/StasF1/turboCharger/releases/download/v1-beta/axialTurbineReport.pdf)|

# Требования
1. [Python 2](https://www.python.org/downloads/)
2. Pillow - Python-модуль для редактирования изображений ([как его скачать](https://github.com/StasF1/turboCharger/issues/2))
3. Markdown-редактор ([Typora](https://typora.io), желательно)

# История версий
![GitHub release (latest by date)](https://img.shields.io/github/v/release/StasF1/turboCharger) ![GitHub All Releases](https://img.shields.io/github/downloads/StasF1/turboCharger/total)
### 📥 [Скачать текущую версию: _v1-beta_](https://github.com/StasF1/turboCharger/archive/v1-beta.zip) 📥

|Версия|Скачать|   |
|-----:|------:|:--|
|[1-beta](https://github.com/StasF1/turboCharger/releases/tag/v1-beta)|[v1-beta](https://github.com/StasF1/turboCharger/archive/v1-beta.zip)|**текущая _стабильная_ версия** (проверена на WindowsOS, macOS и Linux), добавлена возможность расчёта лопаточного диффузора компрессора|
|[0.3-alpha](https://github.com/StasF1/turboCharger/releases/tag/v0.3-alpha)|[v0.3](https://github.com/StasF1/turboCharger/archive/v0.3-alpha.zip)|добавлен расчёт осевой турбины|
|[0.2-alpha](https://github.com/StasF1/turboCharger/releases/tag/v0.2-alpha)|[v0.2](https://github.com/StasF1/turboCharger/archive/v0.2-alpha.zip)|добавлена возможность выставления значений с рисунков 2.2 и 3.7 автоматически с помощью весовых коэффициентов|
|[0.1-alpha](https://github.com/StasF1/turboCharger/releases/tag/v0.1-alpha)|[v0.1-alpha](https://github.com/StasF1/turboCharger/archive/v0.1-alpha.zip)|все значения коэффициентов задаются вручную|

# Порядок работы с программой
‼ Подробное руководство по работе с программой (текущей версии - v1-beta) выложено в [**Wiki**](https://github.com/StasF1/turboCharger/wiki).

_⚠ ВНИМАНИЕ:_ По завершении расчёта создаётся папка _results/_ со сгенерироваными в ней отчётами. Также в ней создаётся и аналогичная репозиторию файловая структура, что необходимо для сохранения в качестве бэкапа словарей (файлов с настройками, оканчивающиеся на _Dict.py_). Например, копия словаря _turbineDict.py_ будет располагаться в _results/turbine/radial/_. Таким образом, **папку _results/_ можно переименовать (например в _results001/_), чтоб не потерять словари настроек при проведении нового расчёта**. 

# Структура
```gitignore
turboCharger-1-beta
├── compressor
│   └── include         # include-файлы вложенные в compressorMain.py
├── etc                 # шрифты, бланки картинок и проч.
│   ├── compressor
│   └── turbine
│       ├── axial
│       └── radial
├── results*            # результаты расчётов и копии словарей (Dict.py-файлов)
│   ├── compressor
│   └── turbine
│       ├── axial
│       └── radial 
└── turbine
    ├── axial
    │   └── include     # include-файлы вложенные в turbineMain.py
    └── radial
        └── include     # include-файлы вложенные в turbineMain.py

# *создаётся при проведённом расчёте
```

---
# DEBUGGING
**[Типичные проблемы](https://github.com/StasF1/turboCharger/issues?utf8=✓&q=is%3Aissue+is%3Aclosed+label%3A%22good+first+issue%22+)** при первом запуске:

- [Pillow](https://github.com/StasF1/turboCharger/issues/2)
- [Make Python2 executable](https://github.com/StasF1/turboCharger/issues/3)

Также, в случае, если у вас **что-то не работет** и решения нет – не стесняйтесь нажимать на [`New Issue`](https://github.com/StasF1/turboCharger/issues?utf8=✓&q=) и создавать сообщение о возникшей проблеме.

---
Отдельная благодарность **Алексею Быкову** за проведённое тестирование кода и поиск ошибок.

