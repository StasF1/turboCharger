# Описание
Программа производит 0D расчёт турбокомпрессора (пока только компрессорной части, вторая часть на данный момент в работе). Написана на языке **_Python 2_**.

Если программа выводит ошибку, то её номер - соответсвующий пункт в методичке, в котором присутствуют некоторые ограничения и результат расчёта не удовлетворяет им.

# Порядок работы с программой

**Если что-то не работает смотрим вкладку *DEBUGGING* ниже**

## [Pillow](https://files.pythonhosted.org/packages/d0/3e/4cc798796d4c3cdb9bf8a000cd6a3f4073879696b514038e5bff78a86300/Pillow-2.5.3.win-amd64-py2.7.exe#md5=33c3a581ff1538b4f79b4651084090c8)
Так как программа редактирует изображения, с использованием Python-модуля _Pillow_, то его нужно [скачать](https://files.pythonhosted.org/packages/d0/3e/4cc798796d4c3cdb9bf8a000cd6a3f4073879696b514038e5bff78a86300/Pillow-2.5.3.win-amd64-py2.7.exe#md5=33c3a581ff1538b4f79b4651084090c8) и установить, если же он уже установлен – переходим к следующему шагу.

## Выбор типа проекта

В файле _commonDict.py_:

-  Для расчёта курсового проекта выставляем параметр  `projectType = "termPaper"` и изменяем данные для своего двигателя в соответвии с техническим заданием.

-  Для расчёта домашнего задания выставляем параметр `projectType = "HW"` и задаём степень повышения давления и расход 

## Компрессор

Заходим в папку _compressor_.
### Корректировка данных и компиляция 
1. В файле _compressorDict.py_ выставляем все возможные коэффиценты. Для выбора значений по умолчанию принимаем их как `"DEFAULT"` (где возможно это сделать понятно по комментарию в скобках вида: `(<X.XX> - default)`).
2. Так как графики на рисунке 2.2 были проинтерполированы, то для некоторых параметров (например `eta_KsStagn`, `H_KsStagn`, `phi_flow` и проч.) выставляются весовые коэффиценты *от 0 до 1*. Если весовой коэффициент принят как *0*, то значение параметра принимается по нижнему графику, если принят за *1* – по верхнему.
3. Для запуска расчёта копируем команду в Терминал **операционной системы** находясь в директрии проекта (в папке _compressor_): 

```bash
python Main.py
```
Или открываем файл _Main.py_ в IDLE (второго Python'a) и нажимаем **F5**.

5. По оценённому диаметру выставляем значения `eta_KsStagn`, `H_KsStagn`, `phi_flow` используя рисунок 2.2 [методичка Ю.А. Гришина]. Также с помощью этого рисунка выставляем значения `relD_1H` и `relD_1H`.
6. Повторяем процедуру указанную в **1-ом *и* 2-ом** пунктах, пока значения погрешностей не будут удовлетворять требуемым.

В итоге программа выдаст рассчитанные параметры и вычислит их погрешности с первоначально оценёнными значениями (или выставленными, в случае ДЗ).

Также генерируется отчёт _compressorReport.md_ на языке **Markdown**. И сохраняются рисунки с уже _выставленными размерами_ на них. Всё это располагается в папке _compressorReport_.

##### Пример получемых рисунков
![alt text](https://github.com/StasF1/READMEPictures/blob/master/turboCharger/compressor/dimensionedAxisCut.png)
![alt text](https://github.com/StasF1/READMEPictures/blob/master/turboCharger/compressor/dimensionedBlades.png)


## Турбина
Заходим в папку *turbine*.

### Корректировка данных и компиляция 

1. Для расчёта турбины должен быть рассчитан компрессор, после расчёта которого автоматически создаётся словарь _solvedParameters.py_ используемый для расчёта турбины.
2. В файле _turbineDict.py_ выставляем все возможные коэффиценты. Для выбора значений по умолчанию принимаем их как `"DEFAULT"` (где возможно это сделать понятно по комментарию в скобках вида: `(<X.XX> - default)`).
3. Так как графики на рисунке 3.7 были проинтерполированы, то для некоторых параметров (например`eta_Te`,`alpha_1` и проч.) выставляются весовые коэффиценты *от 0 до 1*. Если весовой коэффициент принят как *0*, то значение параметра принимается по нижнему графику, если принят за *1* – по верхнему.
4. Для запуска расчёта копируем команду в Терминал **операционной системы** находясь в директрии проекта (в папке _compressor_): 

```bash
python Main.py
```
Или открываем файл _Main.py_ в IDLE (второго Python'a) и нажимаем **F5**.

5. Повторяем процедуру указанную во **2-ом *и* 4-ом** пунктах, пока значения погрешностей не будут удовлетворять требуемым.

-----------------
# DEBUGGING
В случае, если у вас **что-то не работет** и решения нет – не стесняйтесь нажимать на `New Issue` и создавать сообщение о возникшей проблеме (см. вторую вкладку _Issues_ выше)

Также ниже описаны возможные ошибки и их решения.

## Make Python2 executable
Выдаёт ошибку:

```bash
'python' is not recognized as an internal or external command,
operable program or batch file.
```

Заходим в системные переменные и добавляем к уже существующей переменной _Path_ путь `C:\Python27` (или тот путь, где сохранён _Python27_).

## [Pillow](https://files.pythonhosted.org/packages/d0/3e/4cc798796d4c3cdb9bf8a000cd6a3f4073879696b514038e5bff78a86300/Pillow-2.5.3.win-amd64-py2.7.exe#md5=33c3a581ff1538b4f79b4651084090c8)
Выдаёт ошибку:

```bash
Traceback (most recent call last):
  File "Main.py", line 11, in <module>
    import PIL;             from PIL    import ImageFont, Image, ImageDraw
ImportError: No module named PIL
```

Так как программа редактирует изображения, с использованием Python-модуля _Pillow_, то его нужно [скачать](https://files.pythonhosted.org/packages/d0/3e/4cc798796d4c3cdb9bf8a000cd6a3f4073879696b514038e5bff78a86300/Pillow-2.5.3.win-amd64-py2.7.exe#md5=33c3a581ff1538b4f79b4651084090c8) и установить.