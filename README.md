<div align="left">
  <img src="about/cover.png" width="300">
  <h1>🐱 Cat Clicker</h1>

  ![Python Version](https://img.shields.io/badge/Python-3.12-blue)
  ![License](https://img.shields.io/badge/License-MIT-green)
  ![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
</div>

> [!IMPORTANT]
> **Запуск готового `.exe` файла (для игроков)**
> 1. Перейдите в раздел **Releases** (Релизы) справа на странице репозитория
> 2. Скачайте последний ZIP-архив и распакуйте его в любую удобную папку
> 3. Запустите файл **`Cat Clicker.exe`**
> 
> **Запуск через исходный код `main.py` (для разработчиков)**
> ```bash
> git clone https://github.com/krisstianeF/cat-clicker-game.git
> ```
> ```bash
> cd cat-clicker-game
> ```
> ```bash
> pip install -r requirements.txt
> ```
> ```bash
> python main.py
> ```

# About

Cat Clicker - это милая и уютная игра-кликер, в которой вам предстоит кликать, зарабатывать очки, повышать уровень и наблюдать, как ваш питомец становится счастливее! 

В игре есть три уровня сложности (состояния): стартовое окно, процесс игры и экран победы. Достигните 40 очков, чтобы выиграть!

| Стартовое окно | Главное окно (Игра) | Финальное окно (Победа) |
| :---: | :---: | :---: |
| ![Старт](about/first_wnd.png) | ![Игра](about/main_wnd.png) | ![Победа](about/win_wnd.png) |

## Technology & Structure

*   **Язык:** Python 3.12
*   **Интерфейс:** Tkinter (встроенная библиотека)
*   **Звуки:** Pygame (микшер)
*   **Сборка:** PyInstaller

```text
cat-clicker-game/
│
├── main.py                # Главный исполняемый файл (исходный код)
├── requirements.txt       # Список библиотек для установки
├── README.md              # Этот файл с описанием
│
├── assets/                # Все ресурсы игры
│   ├── images/            # Картинки (фоны, котики, кнопки)
│   └── sounds/            # Звуковые эффекты и музыка
│
└── about/                 # Документация (дизайн, скриншоты, описание)
    └── Cat Clicker.md     # Подробный отчет о создании игры
```

## Design

Вся графика для игры была нарисована в Figma. Подробный процесс создания, код и объяснение логики описаны в файле **[about/how_was_made.md](about/how_was_made.md)**.

---
*Сделано с любовью к котикам :3*

*Графические ассеты (картинки) и звуки являются собственностью автора и не могут быть использованы в коммерческих целях без разрешения*
