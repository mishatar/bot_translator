# Python Bot Translator

Телеграмм Бот, осуществляющий перевод текста с английского на русский язык с использованием библиотеки на python.
Также реализована возможность просмотра истории переведенных текстов отдельно взятого пользователя.

### Технологии 
- Python
- Aiogram
- SQLlite3
- Poetry
- Docker

### Описание запуска бота:
- Склонируйте репозиторий:
```commandline
git clone https://github.com/mishatar/bot_translator.git
cd translator
```

- Зарегестрируйте нового бота:
```commandline
Напишите @BotFather в телеграмме -> выберите /newbot -> введите имя бота
Далее скопируйте токен бота и вставьте его в config.py
```

- Создать и запустить контейнеры Docker, выполнить команду:
```commandline
docker-compose up -d --build
```

### Готово! Можно использовать бота:
 - /start - запуск бота
 - /history - история переведенных текстов отдельно взятого пользователя
