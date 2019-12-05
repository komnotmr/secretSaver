# SecretSaver
### Установка
Для работы сервера необходимы [Python3](https://www.python.org/) и [Flask](https://www.palletsprojects.com/p/flask/):
**Пример установки пакета с помощью pip**
```sh
$ pip install flask 
```
или
```sh
$ sudo pip install flask 
```
После установки всего необходимого нужно клонировать репозиторий ([git](https://git-scm.com/downloads))
```
$ git clone https://github.com/komnotmr/secretSaver
```
### Запуск
Перейдите в каталог с файлом server.py
```
$ cd ...
$ ls
$ server.py modules static templates ...
$ ./server.py или python3 server.py
```
При удачном запуске в консоль будут выведены следующие сообщения
```
* Serving Flask app "server" (lazy loading)
* Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```
После запуска в папке с сервером будет создан файл **test.db**. В нём хранятся данные пользователей.

### Использование
Доступ к порталу осуществлется через порт **5000**. С компьютера, на котором запущен сервер адрес для доступа к порталу будет следующим: **http://localhost:5000/**
На портале два поля для ввода:
- Текстовое поле для ввода сообщения или секретного кода
- Поле для ввода даты, до которой сообщение будет доступно.

> Ключ для получения секретного сообщения имеет вид:  xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

### Тестирование
Для имитации запросов в папке test есть скрипт **requests.sh** и несколько сообщений находящихся в файле words. **requests.sh** принимает на вход 3 обязательных параметра, таких как:
<имя файла с сообщениями> <кол-во итераций отправки> <задержка между запросами>
Пример использования (Отправить все сообщения из файла words один раз с задержкой в 2 секунды).
```sh
$ ./requests.sh words 1 2
```
>   Каждое сообщение отправляется дважды с постфиксом **Старое** или **Новое**. Для каждого постфикса генерируется своё "время жизни" сообщения. Таким образом после очередного запуска метода *removeOldRecords* класса *Saver* все сообщения с постфиксом **Старое** должны быть удалены.

