JulianPR telegram bot
====================
____________________

Бот, создаваемый в ходе видеокурса по телеграм ботам с помощью aiogram версии 3.x на
канале [Masson](https://www.youtube.com/channel/UClpHXG4_b0WZxxNPkGPiRug).

## О боте

В настоящий момент бот находится в разработке, процесс разработки частично показан в самих видео, а частично скрыт. Тем
не менее все изменения зафикисированы здесь - на гитхабе.

Чтобы разрабатывать бота вместе со мной, сделайте следующие действия:

1) `` git pull``

---

2) Создайте .env файл со следующим содержанием:

> token=(токен вашего бота)  
db_user=(имя пользователя базы данных)   
db_name=(название базы данных)   
db_port=5432   
SQLALCHEMY_WARN_20=1
---

3) Настройте ссылку в alembic.ini по этому примеру:

> sqlalchemy.url = postgresql+asyncpg://MassonNn@localhost/julianpr

---

4) ``make migrate``

---

5) Cледите за обновлениями в моем [телеграм канале](https://t.me/massonnn_yt)

---

6) Смотрите новые ролики