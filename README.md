# Глобальный поиск документов

![Иллюстрация к проекту](https://user-images.githubusercontent.com/47356327/119249566-2bde0a00-bba2-11eb-840f-648cca499d09.png)

Данный програмный проект реализован используя API бага вк, который позволяет получать документы которые когда либо были отпрвлены как сообщения пользователями данной социальной сети. Это позволяет получать ссылки на большинство:
 * книг 
 * документов на различные тематики
 * iptv плэйлисты...
 
 Для коректной роботы нужно указать следующие параметры в файле setting.txt:
  * version => актуальную версию api documents
  * token => токен на vk api который можно свободно получить на данном сайте в настройках приложения 
  * proxy => прокси сервера позволяющего заходить на ранее упомянутый сайт
 
 Для запуска программы нужно открыть один из двух файлов:
 * console_version.py - версия которая работает в терминале
 * web_version.py - версия которая работает в браузере
 
 Команда для запуска программы python3 <название файла>
