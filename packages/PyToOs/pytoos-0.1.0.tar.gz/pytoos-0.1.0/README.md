PyToOs - библиотека, которая позволяет управлять .py файлами 
С ней можно делать скрипты для создания, редактирования, удаления .py файлов
Примеры использования:
Создание .py файла:
from pytoos import create_py_file

# Создаём файл с кодом (если файл существует - перезаписываем)
success = create_py_file(
    "hello.py", 
    content="print('Привет от PyToOs!')", 
    overwrite=True
)

if success:
    print("Файл создан!")
Редактирование .py файла:
from pytoos import edit_py_file

# Добавляем код в конец файла
edit_py_file("hello.py", "print('Новая строка')", mode="append")

# Вставляем код на 2-ю строку
edit_py_file("hello.py", "x = 42", line=2, mode="insert")

# Полная замена содержимого
edit_py_file("hello.py", "def foo():\n    return 'bar'", mode="replace")
Удаление .py файла:
from pytoos import remove_py_file

# Без подтверждения (удаляет сразу)
remove_py_file("hello.py") 

# С подтверждением (запросит ввод в консоли)
remove_py_file("hello.py", confirm=True)