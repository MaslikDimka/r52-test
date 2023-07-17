'''Для создания системы мониторинга базы данных сервера воспользовался Python и PostgreSQL,использовал следующий алгоритм:
1. Создание базы данных для хранения данных мониторинга и уведомлений.
2. Написание скрипта на Python для сбора и записи в базу данных, данных мониторинга базы данных сервера.
3. Написание скрипта на Python для проверки данных мониторинга на наличие проблем и отправка уведомлений.'''
#Создание базы данных
'''
CREATE DATABASE monitoring_db;
CREATE TABLE monitoring (
    id SERIAL PRIMARY KEY,
    server_name TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    cpu_load FLOAT NOT NULL,
    memory_usage FLOAT NOT NULL,
    disk_usage FLOAT NOT NULL,
    network_traffic FLOAT NOT NULL
);'''
#Подключение к базе данных
conn = psycopg2.connect(
    host="localhost",
    database="monitoring_db",
    user='postgres',
    password="*******"
)
# Получение данных мониторинга
cpu_load = psutil.cpu_percent()
memory_usage = psutil.virtual_memory().percent
disk_usage = psutil.disk_usage('/').percent
network_traffic = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
# Сохранение данных в базу данных
cursor = conn.cursor()
cursor.execute("INSERT INTO monitoring (server_name, timestamp, cpu_load, memory_usage, disk_usage, network_traffic) VALUES (%s, %s, %s, %s, %s, %s)", ("myserver", datetime.now(pytz.utc), cpu_load, memory_usage, disk_usage, network_traffic))
conn.commit()
cursor.close()
conn.close()
# Проверка наличия проблем и отправка уведомлений о проблеме на почтовый ящик
if cpu_load > 90 or memory_usage > 90 or disk_usage > 90 or network_traffic > 100000000:
    smtp_server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    smtp_server.login(user='*********', password='******')
    from_email = '*********'
    to_email = '******'
    subject = 'Attention!Problem'
    message = 'A problem was found on this server when monitoring data'
    smtp_server.sendmail(from_email, to_email, message)
    print("Problem on the server:", f"CPU load: {cpu_load}%, Memory usage: {memory_usage}%, Disk usage: {disk_usage}%, Network traffic: {network_traffic} bytes")
    smtp_server.quit()
else:
    print("The server is working fine")