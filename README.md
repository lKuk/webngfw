### Установка и запуск(требуется установленный Python 3.9+)

1. Скопировать репозиторий
   ```sh
   git clone https://github.com/lKuk/webngfw
   ```
2. Перейти в каталог с проектом
3. Созадть виртуальное окружение и активировать его
   ```sh
   python -m venv ngfwEnv
   ```
      ```sh
   ngfwEnv\Scripts\activate.bat
   ```
4. Перейтив в скопированный проект и выполнить комманду
   ```sh
   python -m pip install requirments.txt
5. Перейтив в скопированный проект и выполнить комманду
   ```sh
   python manage.py runserver 8000
6. Зайти в браузере на http://127.0.0.1:8000/
