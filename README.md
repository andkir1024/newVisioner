 (Ctrl+Shift+P) Python: Create Environment
инициализхация виртуального окружения
python -m venv .venv

установка необходимых зависимостей
pip install -r Requirements.txt

сохранение необходимых зависимостей
pip freeze > Requirements.txt

git config --global user.email "andkir@mail.ru"
git config --global user.name "andkir1024"

pip install PyInstaller

создание выполняемого файла
pyinstaller --onefile main.py

параметры преобразования svg
dx=100_dy=100_sx=1.01_sy=1.02_cx=100_cy=100_a=45_m=0
где dx dy смещение
    sx sy масштабирование
    cx cy центр поворота  
    a угол поворота по часовой стрелке в градусах
    m модификация лекакла
        0 переместить угол в вверх и слева
        1 отступ сверху и по бокам на 1 mm