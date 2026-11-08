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