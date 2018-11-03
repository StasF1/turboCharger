# Описание
Программа производит 0D расчёт турбокомпрессора (пока только компрессорной части, вторая часть на данный момент в работе). Написана на языке **_Python 2_**.

Если программа выводит ошибку, то её номер - соответсвующий пункт в методичке, в котором присутствуют некоторые ограничения.

# Порядок работы с программой

## Выбор типа проекта

В файле _commonDict.py_:

-  Для расчёта курсового проекта выставляем параметр  `projectType = "termPaper"` и изменяем данные для своего двигателя в соответвии с техническим заданием.

-  Для расчёта домашнего задания выставляем параметр `projectType = "HW"` и задаём степень повышения давления и расход 

## Компрессор

Заходим в папку _compressor_.
### Корректировка данных и компиляция 
1. В файле _compressorDict.py_ выставляем все возможные коэффиценты. Для выбора значений по умолчанию принимаем их как `"DEFAULT"` (где возможно это сделать понятно по комментарию в скобках вида: `(<X.XX> - default)`).
2. Для оценки диаметра колеса любое из трёх значений `eta_KsStagn`, `H_KsStagn`, `phi_flow` принимаем как `"UNKNOWN"`. Тогда скрипт выдаст предварительную оценку диаметра.
3. Для запуска расчёта копируем команду в Терминал находясь в директрии проекта (в папке _compressor_): 

```bash
python Main.py
```
Или, если не работает (для Windows OS):
```bash
py -2 Main.py
```
5. По оценённому диаметру выставляем значения `eta_KsStagn`, `H_KsStagn`, `phi_flow` используя рисунок 2.2 [методичка Ю.А. Гришина]. Также с помощью этого рисунка выставляем значения `relD_1H` и `relD_1H`.
6. Повторяем процедуру указанную в **1-ом *и* 3-ем** пунктах, пока значения погрешностей не будут удовлетворять требуемым.

В итоге программа выдаст рассчитанные параметры и вычислит их погрешности с первоначально оценёнными значениями (или выставленными, в случае ДЗ).

Также генерируется отчёт _compressorReport.md_ на языке **Markdown**. И сохраняются рисунки с уже _выставленными размерами_ на них. Всё это располагается в папке _compressorReport_.

##### Пример получемых рисунков
![alt text](https://github.com/StasF1/READMEPictures/blob/master/turboCharger/compressor/dimensionedAxisCut.png)
![alt text](https://github.com/StasF1/READMEPictures/blob/master/turboCharger/compressor/dimensionedBlades.png)


## Турбина
-----------------
Заходим в папку *turbine*.

### Корректировка данных и компиляция 

1. Для расчёта турбины должен быть рассчитан компрессор, после расчёта которого автоматически создаётся словарь _solvedParameters.py_ используемый для расчёта турбины.
2. В файле _turbineDict.py_ выставляем все возможные коэффиценты. Для выбора значений по умолчанию принимаем их как `"DEFAULT"` (где возможно это сделать понятно по комментарию в скобках вида: `(<X.XX> - default)`).
3. Для запуска расчёта копируем команду в Терминал находясь в директрии проекта (в папке _compressor_): 

```bash
python Main.py
```
Или, если не работает (для Windows OS):
```bash
py -2 Main.py
```

4. Повторяем процедуру указанную во **2-ом *и* 3-ем** пунктах, пока значения погрешностей не будут удовлетворять требуемым.
