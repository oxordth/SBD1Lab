import motor.motor_asyncio
import random

client = motor.motor_asyncio.AsyncIOMotorClient("localhost", 27017)
db = client.collector

surname_male = ["Иванов", "Петров","Сидоров","Каменев","Попов","Тимашенко"]
surname_female = ['Иванова', 'Петрова','Сидорова','Каменева','Попова','Кубикова','Петренко' ]
name_male = ["Алексей", "Сергей","Андрей","Олег","Игорь","Петр","Тимофей"]
name_female = ["Арина", "Марина","Карина","Полина","Ирина","Мальвина","Малина"]
cities = ["Волгоград", "Москва", "Санкт-Петербург", "Казань"]
manufacturer = ["Cold Steel", "Spyderco", "Noks", "Victorinox", "Kershaw"]
grip_material = ["Cedar", "G10", "Plastic", "Oak"]
steel = ["SK5", "80CrV2", "L6", "V-Toku2"]
form_fact = ["Fixed", "Automatic", "Folding"]
available = ["Да", "Нет"]
address = ["г. Волгоград, ул. Республиканская, д. 22", "г. Псков, ул. Садовая, д. 17", "г. Кострома, Калинина ул., д. 3", "г. Сыктывкар, Дзержинского ул., д. 14", "г. Химки, Речной пер., д. 9"]


async def do_insert_many_users(surname_male, surname_female, name_male, name_female, cities):
    collection = db.users
    n = await collection.count_documents({})
    for i in range(n, 2000):
        if i % 2 == 0:
            result = await collection.insert_many([{"i": i, "Name": random.choice(name_male), "Surname":
            random.choice(surname_male), "City": random.choice(cities)}])
        else:
            result = await collection.insert_many([{"i": i, "Name": random.choice(name_female), "Surname":
            random.choice(surname_female), "City": random.choice(cities)}])
async def do_insert_many_knives(manufacturer, grip_material, steel, form_fact):
    collection = db.knives
    n = await collection.count_documents({})
    for i in range(n, 2000):
        result = await collection.insert_many([{"i": i, "Manufacturer": random.choice(manufacturer), "Grip":
        random.choice(grip_material), "Steel": random.choice(steel), "Form": random.choice(form_fact)}])
async def do_insert_many_avaliable(available, address):
    collection = db.availability
    n = await collection.count_documents({})
    for i in range(n, 2000):
        result = await collection.insert_many([{"i": i, "id_product": random.randint(0, n), "address":
        random.choice(address), "available": random.choice(available)}])

loop = client.get_io_loop()
loop.run_until_complete(do_insert_many_users(surname_male, surname_female, name_male, name_female, cities))
loop = client.get_io_loop()
loop.run_until_complete(do_insert_many_knives(manufacturer, grip_material, steel, form_fact))
loop = client.get_io_loop()
loop.run_until_complete(do_insert_many_avaliable(available, address))
