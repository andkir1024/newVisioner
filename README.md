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

параметры запуска с командной строкой
1. источник файлов png для обработки
--dirSrc=../popular/
2. включение оконного режима иначи консоль отрабатывает всю заданную директорию dirSrc
--wnd
3. коэффициэнт перемасштабирования для  создания svg (9.066)
--svg=9.066
4. директория для результата
--dirDst=../popular/

пример запуска
main.exe --dirSrc=../graphs/ --svg=9.977 --dirDst=../outGraphs/  --pngDir=../outGraphs/ --thre=500 --badDir=../outBadGraphs/

./main --dirSrc=./srcDemo --svg=9.977 --dirDst=./outSvg --thre=500 --badDir=../bad
./main --dirSrc=../src/ --svg=9.907 --dirDst=../outSvgFed1/ --pngDir=../outSvgFed1/ --thre=500 --badDir=../bad

./AJPMax_validator -f outSvgDemo

параметры преобразования svg
dx=100_dy=100_sx=1.01_sy=1.02_cx=100_cy=100_a=45
где dx dy смещение
    sx sy масштабирование
    cx cy центр поворота  
    a угол поворота по часовой стрелке в градусах