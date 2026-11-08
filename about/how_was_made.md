
![[Обложка.png|440]]
# 1 Описание и структура работы

## 1.1 Описание проекта

Я поставила перед собой цель создать своё мини приложение на Питоне - игру кликер с котиком. Это совсем небольшая игра для души.

## 1.2 Структура работы

Решение задачи было разбито на несколько частей:

1. Создание дизайна окон (все окна представлены в файле фигмы);
2. Создание окон на Питоне в библиотеке Tkinter;
3. Анимация элементов дизайна на питоне;
4. Создание звуковых эффектов.

# 2 Реализация

## 2.1 Дизайн игры

---
[Файл Фигмы с дизайном проекта](https://www.figma.com/design/XD7V6qreXn8q2WpRB7qBi4/Cat-Clicker?node-id=51-397&t=xX2j1Tok4aYF7Bf3-1)

Для начала нужно было определиться с общей стилистикой, я выбрала самую подходящую милую атмосферу и придерживалась её во всех элементах интерфейса. Макеты окон игры на рисунках 1, 2 и 3.

> Изначально игра включала только два состояния: основное окно и финал игры, где можно запустить игру заново, но по ходу работы я добавила ещё одно состояние - стартовое окно, в котором всего лишь одна кнопка - кнопка старта игры.

![[Первая страница.png]]
Рисунок 1 - Стартовое окно

![[Главная страница.png]]
Рисунок 2 - Главное окно 

![[Победа.png]]
Рисунок 3 - Финальное окно

## 2.2 Коды страниц игры

После создания дизайна я приступила к написанию кода. Первое что нужно сделать - подключить все библиотеки и создать окно:

```python
from tkinter import *
from tkinter import ttk
from tkinter import Tk, Button
import sys
import winsound
import subprocess

# Создание окна
window = Tk()
window.title("Cat Clicker")
window.geometry('600x600')
window.resizable(False, False)

#Переменные для фоновых изображений
bg = PhotoImage(file="fon.png")
bg2 = PhotoImage(file='fon1.png')

# Create Canvas
canvas = Canvas(window, width=600, height=600)
canvas.pack(fill="both", expand=True)

# Display image
canvas.create_image(0, 0, image=bg,
                     anchor="nw")
                     
image_on_canvas = canvas.create_image(0, 0, image=bg,
                     anchor="nw")
```

Уже на первом этапе создаю переменные для двух фоновых изображений, это нужно для будущей анимации. После того как главное окно готово нужно также прописать переменные и для остальных элементов интерфейса:

```python
# Изображения разных состяний котика
cat_image = PhotoImage(file="cute_cat.png")
cat2 = PhotoImage(file="cute_cat2.png")
cat3 = PhotoImage(file='cute_cat3.png')
cat4 = PhotoImage(file = 'cute_cat4.png')

# Варианты кнопочек
click_img = PhotoImage(file ='Click_1.png')
click_img2 = PhotoImage(file ='Click_2.png')
restart_img = PhotoImage(file = 'restart_bttn.png')
restart_img2 = PhotoImage(file = 'restart_bttn2.png')
start_img = PhotoImage(file = 'start_btn1.png')
start_img2 = PhotoImage(file = 'start_btn2.png')

# Звуки
bg_sound_file = "bg_sound3.mp3"
click_sound_file = 'multi_click.mp3'
```

Само собой прописываю как должны выглядеть кнопки, задаю им соответствующие размеры, какие картинки на них должны быть и остальное:

```python
'''Кнопка старта игры'''
start_button = Button(canvas, width=320, height=96,
                      image = start_img,
                      command = lambda: (main(), play_bg_sound(bg_sound_file), click_sound(click_sound_file)),
                      borderwidth=0,
                      highlightthickness=0)
start_button.bind("<Button-1>", start_button_press)
start_button.bind("<ButtonRelease-1>", start_button_release)
start_button.place(x = 140, y = 252)

'''Кнопка клика'''
click_button = Button(canvas, width=232, height=65,
                      image = click_img,
                      bg = "#F9E9E0",
                      command = lambda: (Click(), click_sound(click_sound_file)),
                      borderwidth=0,
                      highlightthickness=0)
click_button.bind("<Button-1>", click_button_press)
click_button.bind("<ButtonRelease-1>", click_button_release)

'''Кнопка, для рестарта игры'''
restart_btn = Button(canvas, width=232, height=65,
                     image=restart_img,
                     bg="#F9E9E0",
                     command = lambda: (restart(), click_sound(click_sound_file)),
                     borderwidth=0,
                     highlightthickness=0,
                     bd = 0,
                     relief=FLAT)
restart_btn.bind("<Button-1>", restart_button_press)
restart_btn.bind("<ButtonRelease-1>", restart_button_release)
```

Вместе с кнопками прописываю оставшиеся элементы интерфейса - лейблы:

```python
# Лейбл с каркинкой котика
label = ttk.Label(image = cat_image,
                  padding=8,
                  background="#F9E9E0")

# Подсчёт очков
point_label = Label(text = f'POINTS: {points}',
                    font = ('Comic Sans MS', 20),
                    fg = '#DE7A6C', bg = '#F9E9E0')

# Подсчёт уровня
level_label = Label(text = 'LEVEL: 0/4',
                      font = ('Comic Sans MS', 20),
                      fg = '#DE7A6C', bg = '#F9E9E0')
```

На последок прописываю фенкцю для расположения ранее прописанных элементов, чтобы вызвать их в кнопке старта игры:

```python
def main():
    start_button.destroy()
    
    label.place(x = 80, y = 154)
    click_button.place(x=185, y=494)
    point_label.place(x=215, y=56)
    level_label.place(x=215, y=105)
```

Самая интересная часть кода: функционал кнопки клика и счётчиков очков и уровня. Суть состоит в том, что при нажатии на кнопку у игрока накапливаются очки (1 клик = 1 очко), и каждые 10 очков игрок получает новый уровень. Максимальный уровень - 40, по Достижению 40го уровня игрок победил. После победы есть возможность начать игру заново. Реализовано всё это через одну функцию, в которой также прописаны элементы конца игры: лейбл _“WIN!”_ и кнопка рестарт.

> Помимо всего прочего по достижению нового уровня котик меняет свое состояние на более весёлое :3

Функция, которая реализует эту задумку:

```python
points = 0
level = 0

def Click():
    global points
    global level

    points += 1
    point_label.config(text=f"POINTS: {points}")

    if points == 10:
        level += 1
        level_label['text'] = f'LEVEL: {level}/4'
        label['image'] = cat2
        play_sound('levelup_sound.wav')
    if points == 20:
        level += 1
        level_label['text'] = f'LEVEL: {level}/4'
        label['image'] = cat3
        play_sound('levelup_sound.wav')
    if points == 30:
        level += 1
        level_label['text'] = f'LEVEL: {level}/4'
        label['image'] = cat4
        play_sound('levelup_sound.wav')

    if points > 40:
        level_label.destroy()
        point_label.destroy()
        label.destroy()
        click_button.destroy()
        pygame.mixer.Channel(0).stop()
        play_sound('win.wav')

        end_label = Label(text='WIN!',
                          font=('Comic Sans MS', 100),
                          fg='#DE7A6C', bg='#F9E9E0')
        end_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        restart_btn.place(x=185, y=430)
        
def restart():
    # Закрытие текущего окна
    window.destroy()
    # Перезапуск программы с помощью subprocess.call
    subprocess.call([sys.executable, sys.argv[0]], shell=False)
```

## 2.3 Анимации

Самое первое и самое простое - анимирование фона из двух картинок:

```python
current_img = 0

def bg_animation():
    global current_img

    if current_img == 0:
        canvas.itemconfig(image_on_canvas, image = bg2)
        current_img = 1
    else:
        canvas.itemconfig(image_on_canvas, image=bg)
        current_img = 0

    # Планируем следующий переключатель изображения через 500 миллисекунд
    canvas.after(500, bg_animation)
```

Далее прописываю функции для анимации зажатия кнопок, которые будут вызываться методом **.bind()**:

```python
def click_button_press(event):
    click_button.config(image=click_img2)
def click_button_release(event):
    click_button.config(image=click_img)

def restart_button_press(event):
    restart_btn.config(image=restart_img2)
def restart_button_release(event):
    restart_btn.config(image=restart_img)

def start_button_press(event):
    start_button.config(image = start_img2)
def start_button_release(event):
    start_button.config(image = start_img)
```

## 2.4 Звуки

Звуки в интерфейсе играют очень важную роль и я решила их также реализвать. Пришлось изрядно помучиться, но я это осилила. Для реализации этой задумки мне понадобилось использовать библиотеку **pygame**, а также использовать **каналы** звуков.

> **Звуки в игре я поделила на три категории:**

1. Фоновая музыка;
2. Звук присвоения нового уровня и победы;
3. Звук нажатия на кнопку.

Для каждой категории своя отдельная функция и канал, чтобы звуки не спорили между собой. Также прописала функцию для остановки фоновой музыки, так как в момент победы играет звук отдельный для этого звук:

```python
'''Фоновая музыка'''
def play_bg_sound(sound_file):
    vol = 0
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.Channel(0).play(pygame.mixer.Sound(sound_file), lopps = -1)
    # -1 означает зацикленное воспроизведение

    pygame.mixer.music.set_volume(vol)

'''Функция завершения музыки'''
def stop_bg_sound():
    pygame.mixer.Channel(0).stop()

'''Звук клика'''
def click_sound(sound_file):
    pygame.mixer.Channel(1).play(pygame.mixer.Sound(sound_file))
    
'''Остальные звуки'''
def play_sound(sound_file):
    pygame.mixer.Channel(2).play(pygame.mixer.Sound(sound_file))
```

# 3 Итоговый код

```python
import os
import sys
import subprocess

from tkinter import *
from tkinter import ttk
from tkinter import Tk, Button
import pygame

# Функция для правильного поиска путей (работает в PyCharm и в .exe)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

window = Tk()
window.title("Cat Clicker")
window.geometry('600x600')
window.resizable(False, False)

# --- ЗАГРУЗКА КАРТИНОК С ПРАВИЛЬНЫМИ ПУТЯМИ ---
bg = PhotoImage(file=resource_path("assets/images/fon.png"))
bg2 = PhotoImage(file=resource_path("assets/images/fon1.png"))

# Create Canvas
canvas = Canvas(window, width=600, height=600)
canvas.pack(fill="both", expand=True)

# Display image
canvas.create_image(0, 0, image=bg, anchor="nw")
image_on_canvas = canvas.create_image(0, 0, image=bg, anchor="nw")

cat_image = PhotoImage(file=resource_path("assets/images/cute_cat.png"))
cat2 = PhotoImage(file=resource_path("assets/images/cute_cat2.png"))
cat3 = PhotoImage(file=resource_path("assets/images/cute_cat3.png"))
cat4 = PhotoImage(file=resource_path("assets/images/cute_cat4.png"))

click_img = PhotoImage(file=resource_path("assets/images/Click_1.png"))
click_img2 = PhotoImage(file=resource_path("assets/images/Click_2.png"))
restart_img = PhotoImage(file=resource_path("assets/images/restart_bttn.png"))
restart_img2 = PhotoImage(file=resource_path("assets/images/restart_bttn2.png"))
start_img = PhotoImage(file=resource_path("assets/images/start_btn1.png"))
start_img2 = PhotoImage(file=resource_path("assets/images/start_btn2.png"))

# --- ПУТИ К ЗВУКАМ ---
bg_sound_file = resource_path("assets/sounds/bg_sound3.mp3")
click_sound_file = resource_path("assets/sounds/multi_click.mp3")
levelup_sound_file = resource_path("assets/sounds/levelup_sound.wav")
win_sound_file = resource_path("assets/sounds/win.wav")

def play_bg_sound(sound_file):
    vol = 0.5  # Сделал звук слышимым (0 = выключено)
    pygame.init()
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(vol)
        # Используем отдельный канал для фоновой музыки, чтобы не конфликтовать с кликами
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(sound_file))
        pygame.mixer.Channel(0).set_volume(vol)
    except Exception as e:
        print(f"Ошибка загрузки звука: {e}")

def stop_bg_sound():
    pygame.mixer.Channel(0).stop()

def click_sound(sound_file):
    try:
        pygame.mixer.Channel(1).play(pygame.mixer.Sound(sound_file))
    except Exception as e:
        print(f"Ошибка клика: {e}")

def play_sound(sound_file):
    try:
        pygame.mixer.Channel(2).play(pygame.mixer.Sound(sound_file))
    except Exception as e:
        print(f"Ошибка звука: {e}")

def bg_anim():
    if canvas['image'] == bg:
        canvas['image'] = bg2
    canvas.after(800, bg_animation)

def click_button_press(event):
    click_button.config(image=click_img2)
def click_button_release(event):
    click_button.config(image=click_img)

def restart_button_press(event):
    restart_btn.config(image=restart_img2)
def restart_button_release(event):
    restart_btn.config(image=restart_img)

def start_button_press(event):
    start_button.config(image = start_img2)
def start_button_release(event):
    start_button.config(image = start_img)

points = 0
level = 0
def Click():
    global points
    global level

    points += 1
    point_label.config(text=f"POINTS: {points}")

    if points == 10:
        level += 1
        level_label['text'] = f'LEVEL: {level}/4'
        label['image'] = cat2
        play_sound(levelup_sound_file)
    if points == 20:
        level += 1
        level_label['text'] = f'LEVEL: {level}/4'
        label['image'] = cat3
        play_sound(levelup_sound_file)
    if points == 30:
        level += 1
        level_label['text'] = f'LEVEL: {level}/4'
        label['image'] = cat4
        play_sound(levelup_sound_file)

    if points > 40:
        level_label.destroy()
        point_label.destroy()
        label.destroy()
        click_button.destroy()
        pygame.mixer.Channel(0).stop()
        play_sound(win_sound_file)

        end_label = Label(text='WIN!',
                          font=('Comic Sans MS', 100),
                          fg='#DE7A6C', bg='#F9E9E0')
        end_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        restart_btn.place(x=185, y=430)

current_img = 0
def bg_animation():
    global current_img

    if current_img == 0:
        canvas.itemconfig(image_on_canvas, image = bg2)
        current_img = 1
    else:
        canvas.itemconfig(image_on_canvas, image=bg)
        current_img = 0

    # Планируем следующий переключатель изображения через 500 миллисекунд
    canvas.after(500, bg_animation)

def restart():
    # Закрытие текущего окна
    window.destroy()
    # Перезапуск программы
    if getattr(sys, 'frozen', False):
        # Если запущено из .exe
        subprocess.call([sys.executable])
    else:
        # Если запущено из PyCharm
        subprocess.call([sys.executable, sys.argv[0]])

start_button = Button(canvas, width=320, height=96,
                      image = start_img,
                      command = lambda: (main(), play_bg_sound(bg_sound_file), click_sound(click_sound_file)),
                      borderwidth=0,
                      highlightthickness=0)
start_button.bind("<Button-1>", start_button_press)
start_button.bind("<ButtonRelease-1>", start_button_release)
start_button.place(x = 140, y = 252)

click_button = Button(canvas, width=232, height=65,
                      image = click_img,
                      command = lambda: (Click(), click_sound(click_sound_file)),
                      borderwidth=0,
                      highlightthickness=0)
click_button.bind("<Button-1>", click_button_press)
click_button.bind("<ButtonRelease-1>", click_button_release)

restart_btn = Button(canvas, width=232, height=65,
                     image=restart_img,
                     command = lambda: (restart(), click_sound(click_sound_file)),
                     borderwidth=0,
                     highlightthickness=0)
restart_btn.bind("<Button-1>", restart_button_press)
restart_btn.bind("<ButtonRelease-1>", restart_button_release)

label = ttk.Label(image = cat_image,
                  padding=8,
                  background="#F9E9E0")

point_label = Label(text = f'POINTS: {points}',
                    font = ('Comic Sans MS', 20),
                    fg = '#DE7A6C', bg = '#F9E9E0')

level_label = Label(text = 'LEVEL: 0/4',
                    font = ('Comic Sans MS', 20),
                    fg = '#DE7A6C', bg = '#F9E9E0')

def main():
    start_button.destroy()
    label.place(x = 80, y = 154)
    click_button.place(x=185, y=494)
    point_label.place(x=215, y=56)
    level_label.place(x=215, y=105)

bg_animation()

window.mainloop()
```

# 4 Преобразование кода игры в десктопное приложение

---
[Источник](https://habr.com/ru/companies/vdsina/articles/557316/)

С помощью [Auto PY to EXE](https://pypi.org/project/auto-py-to-exe/) можно с лёгкостью преобразовывать файлы `.py` в файлы `.exe`. Благодаря этому ваш проект на Python будет работать как десктопное приложение и вы сможете запускать приложение на других машинах без необходимости установки Python.  
  
В этой статье я расскажу, как преобразовать проект на Python в исполняемый файл. Решение будет работать вне зависимости от количества файлов `.py` в приложении. Стоит учесть, что Auto PY to EXE работает только с Python 3.5 или выше.  
  

## Установка Auto PY to EXE

### Установка через pip

При помощи следующей команды можно установить текущую версию Auto PY to EXE.  
  
```
$ pip install auto-py-to-exe
```

### Установка с GitHub
  
Также можно выполнить установку напрямую с GitHub. Для установки Auto PY to EXE с GitHub необходимо сначала клонировать репозиторий GitHub.  
  
```
$ git clone https://github.com/brentvollebregt/auto-py-to-exe.git
```

  
Затем нужно перейти в папку `auto-py-to-exe`.  
  
```
$ cd auto-py-to-exe
```

  
Теперь необходимо запустить файл `setup.py`.  
  
```
$ python setup.py install
```

  
Можно также проверить версию при помощи следующей команды:  
  
```
auto-py-to-exe --version
```

  
![](https://habrastorage.org/r/w1560/webt/bn/0j/gy/bn0jgyd3pkcy6jwzyolsccii5p4.png)

_Проверяем версию_  
Текущая версия Auto PY to EXE 2.9.0 и теперь она установлена на ваш компьютер.  
  

## Открываем приложение
  
Чтобы открыть Auto PY to EXE, нужно выполнить в терминале следующую команду:  
  
```
$ auto-py-to-exe
```

  
Откроется удобное приложение с GUI:  

![](https://habrastorage.org/r/w1560/webt/-q/0h/td/-q0htdaht-sq6kvocxsvg8uj_jw.png)

_Интерфейс пользователя Auto PY to EXE_  
Теперь с помощью этого интерфейса можно преобразовать файл `.py` в `.exe`.  
  
## Процесс преобразования

## Шаг 1. Добавляем местоположение файла

  
Для преобразования `.py` в `.exe` сначала необходимо указать путь к файлу Python. Достаточно перейти к местоположению файла, который нужно преобразовать, а затем добавить путь.  
  
Пример:  
  

![](https://habrastorage.org/r/w1560/webt/ur/k3/el/urk3elfsknvnclyi6ptai2a6cwi.png)

  
_Добавляем местоположение файла_  
  
Я добавил местоположение основного файла Python моего проекта. Здесь я использую для примера один из своих проектов на Python. Это приложение с GUI, визуализирующее различные алгоритмы сортировки. О создании этого проекта можно прочитать здесь: [Build a Sorting Algorithm Visualizer in Python](https://python.plainenglish.io/build-a-sorting-algorithm-visualizer-in-python-f6f4afb1c98a)  
  

### Шаг 2. Выбор «One Directory» или «One File»

  
В интерфейсе есть опция выбора «One Directory» или «One File». Мой проект на Python содержит несколько других файлов, поэтому я выбрал «One Directory». Эта опция создаст папку со всеми необходимыми файлами, а также с файлом `.exe`.  
  

![](https://habrastorage.org/r/w1560/webt/1q/0b/ke/1q0bke0knhmrhfs6v3r7rp19wsi.png)

  
_One directory или One file_  
  

### Шаг 3. Выбор «Console Based» или «Window Based»

  
После этого нужно будет выбрать тип приложения: консольное (Console Based) или оконное (Window Based). Если выбрать «Window Based», то это скроет весь консольный вывод приложения. Если ваш проект генерирует консольный вывод, то нужно выбрать «Console Based». Если у вас приложение с GUI или вам не нужно отображать пользователю консольный вывод, то выберите «Window Based». Я выбрал второй вариант, потому что моё приложение имеет GUI.  
  

![](https://habrastorage.org/r/w1560/webt/2z/zf/os/2zzfosmtxoykfbnrr2lldomdk8s.png)

  
_Console Based или Window Based_  
  

### Шаг 4. Преобразование

  
Далее отобразятся другие опции, такие как добавление значков, дополнительных файлов и т.д. Выберите нужные опции самостоятельно. Ну а наш файл `.py` уже к преобразованию. Достаточно нажать на кнопку **CONVERT .PY TO .EXE** .  
  

![](https://habrastorage.org/r/w1560/webt/k-/l9/cs/k-l9cs345exaadehiatwl7prcow.png)

  
_Нажмите кнопку для преобразования_  
  
Для завершения процесса придётся немного подождать.  
  

## Папка с результатами

  
После завершения процесса можно будет выбрать опцию открытия папки с результатами.  
  

![](https://habrastorage.org/r/w1560/webt/nx/gq/9s/nxgq9sfndmqi3c9-luvqe9ohqsm.png)

  
По умолчанию папка с результатами будет создана там, откуда вы запускали Auto PY to EXE. Я открывал Auto PY to EXE с рабочего стола, поэтому папка создана на нём. В папке находится множество файлов и папок. Но нам важен файл с расширением `.exe`. В моём случае это `main.exe`. При двойном нажатии будет запускаться программа.  
  
Готово! Наш проект на Python теперь преобразован в исполняемый файл. Его можно запускать на других компьютерах без необходимости установки Python.  
  

### Ресурсы

- [https://pypi.org/project/auto-py-to-exe/](https://pypi.org/project/auto-py-to-exe/)
- [https://github.com/brentvollebregt/auto-py-to-exe](https://github.com/brentvollebregt/auto-py-to-exe)