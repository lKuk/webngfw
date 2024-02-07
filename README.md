## Установка и запуск webngfw

### Установка:

1. Выполнить установку  Python 3.9+

2. Скопировать репозиторий проекта
   ```sh
   git clone http://.../webngfw
   ```
   
3. Перейти в каталог с проектом webngfw
   ```sh
   cd webngfw
   ```

4. Создать виртуальное окружение и активировать его
   ```sh
   python -m venv env 
   ```
   ```sh
   "env/Scripts/activate.bat"
   ```
5. Обновить пакетный менеджер pip и выполнить установку пакетов
   ```sh
   python -m pip install --upgrade pip
   ```
   ```sh
   python -m pip install -r requirements.txt
   ```

### Запуск:

1. Выполнить команду
   ```sh
   python manage.py runserver 8000
   ```
2. Перейти в браузере по url http://127.0.0.1:8000/

### Запуск https:
1. Выполнить команды по очереди:
   ```sh
   pip install django-sslserver
   choco install mkcert
   mkcert -install  
   mkdir cert
   mkcert -cert-file cert/cert.pem -key-file cert/key.pem localhost 127.0.0.1
   python manage.py runsslserver --certificate cert/cert.pem --key cert/key.pem
   ```
   
