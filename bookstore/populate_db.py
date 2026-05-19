"""
Скрипт для заполнения базы данных тестовыми данными.
Запуск: python populate_db.py (из папки bookstore)
"""

import os
import sys
import django
import requests
from io import BytesIO
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from store.models import Category, Author, Book


def download_image(url, timeout=10):
    """Скачивает картинку и возвращает ContentFile или None."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, timeout=timeout, headers=headers)
        if response.status_code == 200 and len(response.content) > 1000:
            return ContentFile(response.content)
    except Exception as e:
        print(f"    Ошибка загрузки {url}: {e}")
    return None


print("Создаём суперпользователя...")
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("  Суперпользователь создан: admin / admin123")
else:
    print("  Суперпользователь уже существует.")

print("\nСоздаём категории...")
categories_data = [
    ('Классическая литература', 'klassicheskaya-literatura', 'Произведения великих писателей прошлого'),
    ('Современная проза', 'sovremennaya-proza', 'Лучшие романы современных авторов'),
    ('Детективы', 'detektivy', 'Захватывающие детективные истории'),
    ('Фантастика', 'fantastika', 'Научная фантастика и фэнтези'),
    ('Детская литература', 'detskaya-literatura', 'Книги для детей и подростков'),
    ('Учебники', 'uchebniki', 'Образовательная литература'),
    ('Психология', 'psihologiya', 'Книги по психологии и саморазвитию'),
    ('История', 'istoriya', 'Исторические произведения и документалистика'),
]

categories = {}
for name, slug, desc in categories_data:
    cat, created = Category.objects.get_or_create(slug=slug, defaults={'name': name, 'description': desc})
    categories[slug] = cat
    print(f"  {'Создана' if created else 'Уже есть'}: {name}")

print("\nСоздаём авторов...")
authors_data = [
    {
        'first_name': 'Лев', 'last_name': 'Толстой',
        'bio': 'Великий русский писатель (1828–1910), автор "Войны и мира" и "Анны Карениной". Один из величайших романистов в истории мировой литературы.',
        'photo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/L.N.Tolstoy_Prokudin-Gorsky.jpg/440px-L.N.Tolstoy_Prokudin-Gorsky.jpg',
        'photo_name': 'tolstoy.jpg',
    },
    {
        'first_name': 'Фёдор', 'last_name': 'Достоевский',
        'bio': 'Русский писатель (1821–1881), мастер психологической прозы. Автор "Преступления и наказания", "Идиота", "Братьев Карамазовых".',
        'photo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Vasily_Perov_-_%D0%9F%D0%BE%D1%80%D1%82%D1%80%D0%B5%D1%82_%D0%A4.%D0%9C.%D0%94%D0%BE%D1%81%D1%82%D0%BE%D0%B5%D0%B2%D1%81%D0%BA%D0%BE%D0%B3%D0%BE_-_Google_Art_Project.jpg/440px-Vasily_Perov_-_%D0%9F%D0%BE%D1%80%D1%82%D1%80%D0%B5%D1%82_%D0%A4.%D0%9C.%D0%94%D0%BE%D1%81%D1%82%D0%BE%D0%B5%D0%B2%D1%81%D0%BA%D0%BE%D0%B3%D0%BE_-_Google_Art_Project.jpg',
        'photo_name': 'dostoevsky.jpg',
    },
    {
        'first_name': 'Агата', 'last_name': 'Кристи',
        'bio': 'Знаменитая английская писательница (1890–1976), королева детективного жанра. Автор более 80 романов о Эркюле Пуаро и мисс Марпл.',
        'photo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Agatha_Christie.png/440px-Agatha_Christie.png',
        'photo_name': 'christie.jpg',
    },
    {
        'first_name': 'Стивен', 'last_name': 'Кинг',
        'bio': 'Американский мастер ужасов и триллеров (род. 1947). Автор более 60 романов — "Оно", "Сияние", "Мизери". Продал свыше 350 миллионов книг.',
        'photo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Stephen_King%2C_Comicon.jpg/440px-Stephen_King%2C_Comicon.jpg',
        'photo_name': 'king.jpg',
    },
    {
        'first_name': 'Джоан', 'last_name': 'Роулинг',
        'bio': 'Британская писательница (род. 1965), автор серии о Гарри Поттере — одной из самых продаваемых книжных серий в истории.',
        'photo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/J_K_Rowling_2010.jpg/440px-J_K_Rowling_2010.jpg',
        'photo_name': 'rowling.jpg',
    },
    {
        'first_name': 'Михаил', 'last_name': 'Булгаков',
        'bio': 'Русский писатель и драматург (1891–1940), автор "Мастера и Маргариты" — одного из самых читаемых романов XX века.',
        'photo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Bulgakov.jpg/440px-Bulgakov.jpg',
        'photo_name': 'bulgakov.jpg',
    },
    {
        'first_name': 'Чингиз', 'last_name': 'Айтматов',
        'bio': 'Выдающийся кыргызский и советский писатель (1928–2008). Автор "Джамили", "Белого парохода", "Плахи". Национальный символ Кыргызстана.',
        'photo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Chingiz_Aitmatov.jpg/440px-Chingiz_Aitmatov.jpg',
        'photo_name': 'aitmatov.jpg',
    },
    {
        'first_name': 'Эрих Мария', 'last_name': 'Ремарк',
        'bio': 'Немецкий писатель (1898–1970), автор "На Западном фронте без перемен" и "Трёх товарищей". Его книги были сожжены нацистами в 1933 году.',
        'photo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Erich_Maria_Remarque_1929.jpg/440px-Erich_Maria_Remarque_1929.jpg',
        'photo_name': 'remarque.jpg',
    },
    {
        'first_name': 'Антон', 'last_name': 'Чехов',
        'bio': 'Русский писатель и драматург (1860–1904), мастер короткого рассказа. Автор пьес "Вишнёвый сад", "Три сестры", "Чайка".',
        'photo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Chekhov_1903.jpg/440px-Chekhov_1903.jpg',
        'photo_name': 'chekhov.jpg',
    },
    {
        'first_name': 'Александр', 'last_name': 'Пушкин',
        'bio': 'Основоположник современного русского литературного языка (1799–1837). Автор "Евгения Онегина", "Капитанской дочки". Погиб на дуэли в 37 лет.',
        'photo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Pushkin_by_Kiprensky.jpg/440px-Pushkin_by_Kiprensky.jpg',
        'photo_name': 'pushkin.jpg',
    },
    {
        'first_name': 'Джордж', 'last_name': 'Оруэлл',
        'bio': 'Британский писатель и публицист (1903–1950). Автор антиутопий "1984" и "Скотный двор". Критиковал тоталитаризм и политическую ложь.',
        'photo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/George_Orwell_press_photo.jpg/440px-George_Orwell_press_photo.jpg',
        'photo_name': 'orwell.jpg',
    },
    {
        'first_name': 'Борис', 'last_name': 'Акунин',
        'bio': 'Российский писатель (род. 1956), настоящее имя — Григорий Чхартишвили. Автор детективной серии о сыщике Эрасте Фандорине.',
        'photo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Boris_Akunin_-_2012.jpg/440px-Boris_Akunin_-_2012.jpg',
        'photo_name': 'akunin.jpg',
    },
    {
        'first_name': 'Эрнест', 'last_name': 'Хемингуэй',
        'bio': 'Американский писатель (1899–1961), лауреат Нобелевской премии 1954 года. Автор "Старика и моря", "По ком звонит колокол".',
        'photo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/ErnestHemingway.jpg/440px-ErnestHemingway.jpg',
        'photo_name': 'hemingway.jpg',
    },
    {
        'first_name': 'Франц', 'last_name': 'Кафка',
        'bio': 'Австрийский писатель (1883–1924). Автор "Превращения" и "Процесса". Его произведения полны абсурда и экзистенциального страха.',
        'photo_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Kafka_portrait.jpg/440px-Kafka_portrait.jpg',
        'photo_name': 'kafka.jpg',
    },
]

authors = {}
for data in authors_data:
    photo_url = data.pop('photo_url')
    photo_name = data.pop('photo_name')
    author, created = Author.objects.get_or_create(
        first_name=data['first_name'], last_name=data['last_name'],
        defaults={'bio': data['bio']}
    )
    if created or not author.photo:
        print(f"  {'Создан' if created else 'Обновляю'}: {data['first_name']} {data['last_name']} — загружаю фото...")
        img = download_image(photo_url)
        if img:
            author.photo.save(photo_name, img, save=True)
            print(f"    Фото загружено!")
        else:
            print(f"    Фото не удалось загрузить.")
    else:
        print(f"  Уже есть: {data['first_name']} {data['last_name']}")
    authors[f"{data['first_name']} {data['last_name']}"] = author

print("\nСоздаём книги...")
books_data = [
    {'title': 'Война и мир', 'slug': 'voyna-i-mir', 'author': authors['Лев Толстой'], 'category': categories['klassicheskaya-literatura'], 'description': 'Эпический роман-эпопея Льва Толстого, описывающий русское общество в эпоху войн с Наполеоном.', 'price': 850, 'stock': 15, 'pages': 1225, 'year_published': 1869, 'publisher': 'Эксмо', 'language': 'Русский', 'isbn': '978-5-04-089473-6', 'featured': True, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9785040894736-L.jpg', 'cover_name': 'voyna-i-mir.jpg'},
    {'title': 'Анна Каренина', 'slug': 'anna-karenina', 'author': authors['Лев Толстой'], 'category': categories['klassicheskaya-literatura'], 'description': 'Роман о трагической судьбе женщины в высшем свете, разрывающейся между долгом и любовью.', 'price': 750, 'stock': 8, 'pages': 864, 'year_published': 1878, 'publisher': 'Эксмо', 'language': 'Русский', 'isbn': '978-5-04-099877-0', 'featured': False, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9780199536061-L.jpg', 'cover_name': 'anna-karenina.jpg'},
    {'title': 'Преступление и наказание', 'slug': 'prestuplenie-i-nakazanie', 'author': authors['Фёдор Достоевский'], 'category': categories['klassicheskaya-literatura'], 'description': 'Философский роман о студенте Раскольникове, решившемся на убийство.', 'price': 650, 'stock': 20, 'pages': 672, 'year_published': 1866, 'publisher': 'АСТ', 'language': 'Русский', 'isbn': '978-5-17-090823-4', 'featured': True, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9780140449136-L.jpg', 'cover_name': 'prestuplenie.jpg'},
    {'title': 'Идиот', 'slug': 'idiot-dostoevsky', 'author': authors['Фёдор Достоевский'], 'category': categories['klassicheskaya-literatura'], 'description': 'Роман о добром и наивном князе Мышкине, оказавшемся в жестоком мире петербургского общества.', 'price': 580, 'stock': 9, 'pages': 640, 'year_published': 1869, 'publisher': 'АСТ', 'language': 'Русский', 'isbn': '978-5-17-099123-7', 'featured': False, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9780140447927-L.jpg', 'cover_name': 'idiot.jpg'},
    {'title': 'Братья Карамазовы', 'slug': 'bratya-karamazovy', 'author': authors['Фёдор Достоевский'], 'category': categories['klassicheskaya-literatura'], 'description': 'Последний роман Достоевского — глубокое философское исследование веры, сомнения и морали.', 'price': 700, 'stock': 11, 'pages': 896, 'year_published': 1880, 'publisher': 'АСТ', 'language': 'Русский', 'isbn': '978-5-17-099124-4', 'featured': False, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9780374528379-L.jpg', 'cover_name': 'karamazovy.jpg'},
    {'title': 'Убийство в Восточном экспрессе', 'slug': 'ubiystvo-v-vostochnom-ekspresse', 'author': authors['Агата Кристи'], 'category': categories['detektivy'], 'description': 'Классический детектив с Эркюлем Пуаро. В поезде найден убитый — кто преступник среди двенадцати подозреваемых?', 'price': 480, 'stock': 25, 'pages': 288, 'year_published': 1934, 'publisher': 'Эксмо', 'language': 'Русский', 'isbn': '978-5-04-106843-2', 'featured': True, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9780007119318-L.jpg', 'cover_name': 'vostochny-express.jpg'},
    {'title': 'Десять негритят', 'slug': 'desyat-negrityat', 'author': authors['Агата Кристи'], 'category': categories['detektivy'], 'description': 'Самый известный детектив Агаты Кристи. Десять человек на уединённом острове начинают погибать один за другим.', 'price': 440, 'stock': 20, 'pages': 256, 'year_published': 1939, 'publisher': 'Эксмо', 'language': 'Русский', 'isbn': '978-5-04-107234-7', 'featured': False, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9780312330873-L.jpg', 'cover_name': 'desyat-negrityat.jpg'},
    {'title': 'Сияние', 'slug': 'siyanie', 'author': authors['Стивен Кинг'], 'category': categories['fantastika'], 'description': 'Роман ужасов о смотрителе отеля Overlook, изолированного зимой. Психологический триллер о безумии и сверхъестественном.', 'price': 720, 'stock': 10, 'pages': 688, 'year_published': 1977, 'publisher': 'АСТ', 'language': 'Русский', 'isbn': '978-5-17-119743-1', 'featured': False, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9780385121675-L.jpg', 'cover_name': 'siyanie.jpg'},
    {'title': 'Оно', 'slug': 'ono-stiven-king', 'author': authors['Стивен Кинг'], 'category': categories['fantastika'], 'description': 'Культовый роман ужасов о группе детей, столкнувшихся с древним злом в образе клоуна Пеннивайза.', 'price': 890, 'stock': 7, 'pages': 1376, 'year_published': 1986, 'publisher': 'АСТ', 'language': 'Русский', 'isbn': '978-5-17-119744-8', 'featured': True, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9781501142970-L.jpg', 'cover_name': 'ono.jpg'},
    {'title': 'Мизери', 'slug': 'mizeri-king', 'author': authors['Стивен Кинг'], 'category': categories['fantastika'], 'description': 'Психологический триллер о писателе, попавшем в плен к своей одержимой поклоннице.', 'price': 560, 'stock': 13, 'pages': 448, 'year_published': 1987, 'publisher': 'АСТ', 'language': 'Русский', 'isbn': '978-5-17-119745-5', 'featured': False, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9780450417399-L.jpg', 'cover_name': 'mizeri.jpg'},
    {'title': 'Гарри Поттер и философский камень', 'slug': 'garri-potter-filosofsky-kamen', 'author': authors['Джоан Роулинг'], 'category': categories['detskaya-literatura'], 'description': 'Первая книга серии о молодом волшебнике Гарри Поттере. История о дружбе, магии и борьбе добра со злом.', 'price': 590, 'stock': 30, 'pages': 432, 'year_published': 1997, 'publisher': 'РОСМЭН', 'language': 'Русский', 'isbn': '978-5-353-01435-6', 'featured': True, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9780439708180-L.jpg', 'cover_name': 'hp1.jpg'},
    {'title': 'Гарри Поттер и тайная комната', 'slug': 'garri-potter-taynaya-komnata', 'author': authors['Джоан Роулинг'], 'category': categories['detskaya-literatura'], 'description': 'Вторая книга серии. Гарри возвращается в Хогвартс, где начинают происходить загадочные нападения на учеников.', 'price': 590, 'stock': 25, 'pages': 384, 'year_published': 1998, 'publisher': 'РОСМЭН', 'language': 'Русский', 'isbn': '978-5-353-01436-3', 'featured': False, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9780439064873-L.jpg', 'cover_name': 'hp2.jpg'},
    {'title': 'Мастер и Маргарита', 'slug': 'master-i-margarita', 'author': authors['Михаил Булгаков'], 'category': categories['klassicheskaya-literatura'], 'description': 'Мистический роман о визите Воланда в советскую Москву. Одно из самых загадочных произведений русской литературы XX века.', 'price': 530, 'stock': 18, 'pages': 480, 'year_published': 1967, 'publisher': 'Эксмо', 'language': 'Русский', 'isbn': '978-5-04-099876-3', 'featured': True, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9785040998760-L.jpg', 'cover_name': 'master-margarita.jpg'},
    {'title': 'Собачье сердце', 'slug': 'sobache-serdce', 'author': authors['Михаил Булгаков'], 'category': categories['klassicheskaya-literatura'], 'description': 'Сатирическая повесть о профессоре, пересадившем человеческий гипофиз бездомной собаке. Острая критика советского общества.', 'price': 380, 'stock': 16, 'pages': 224, 'year_published': 1925, 'publisher': 'Эксмо', 'language': 'Русский', 'isbn': '978-5-04-099878-7', 'featured': False, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9780802150592-L.jpg', 'cover_name': 'sobache-serdce.jpg'},
    {'title': 'Белый пароход', 'slug': 'belyy-parohod', 'author': authors['Чингиз Айтматов'], 'category': categories['klassicheskaya-literatura'], 'description': 'Повесть о мальчике, живущем в горном урочище, и его мечтах. Глубокое размышление о добре и жестокости мира.', 'price': 350, 'stock': 12, 'pages': 184, 'year_published': 1970, 'publisher': 'Кыргызстан', 'language': 'Русский', 'isbn': '978-5-000-00001-0', 'featured': True, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9785840100419-L.jpg', 'cover_name': 'belyy-parohod.jpg'},
    {'title': 'Джамиля', 'slug': 'dzhamilya', 'author': authors['Чингиз Айтматов'], 'category': categories['klassicheskaya-literatura'], 'description': 'Повесть о любви молодой кыргызской женщины. Луи Арагон назвал её "самой прекрасной повестью о любви в мировой литературе".', 'price': 300, 'stock': 14, 'pages': 96, 'year_published': 1958, 'publisher': 'Кыргызстан', 'language': 'Русский', 'isbn': '978-5-000-00002-7', 'featured': False, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9785840100426-L.jpg', 'cover_name': 'dzhamilya.jpg'},
    {'title': 'Плаха', 'slug': 'plaha', 'author': authors['Чингиз Айтматов'], 'category': categories['klassicheskaya-literatura'], 'description': 'Роман о нравственном выборе человека на фоне советского общества. Один из самых острых романов Айтматова.', 'price': 420, 'stock': 10, 'pages': 304, 'year_published': 1986, 'publisher': 'Кыргызстан', 'language': 'Русский', 'isbn': '978-5-000-00003-4', 'featured': False, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9785840100433-L.jpg', 'cover_name': 'plaha.jpg'},
    {'title': 'На Западном фронте без перемен', 'slug': 'na-zapadnom-fronte-bez-peremen', 'author': authors['Эрих Мария Ремарк'], 'category': categories['klassicheskaya-literatura'], 'description': 'Антивоенный роман о немецких солдатах Первой мировой войны. Одно из самых пронзительных произведений о войне.', 'price': 420, 'stock': 14, 'pages': 304, 'year_published': 1929, 'publisher': 'АСТ', 'language': 'Русский', 'isbn': '978-5-17-088034-2', 'featured': False, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9780449213940-L.jpg', 'cover_name': 'zapadny-front.jpg'},
    {'title': 'Три товарища', 'slug': 'tri-tovarischa', 'author': authors['Эрих Мария Ремарк'], 'category': categories['klassicheskaya-literatura'], 'description': 'Роман о дружбе трёх ветеранов Первой мировой и любви на фоне Германии 1920-х годов.', 'price': 450, 'stock': 12, 'pages': 384, 'year_published': 1936, 'publisher': 'АСТ', 'language': 'Русский', 'isbn': '978-5-17-088035-9', 'featured': True, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9780449208397-L.jpg', 'cover_name': 'tri-tovarischa.jpg'},
    {'title': 'Вишнёвый сад', 'slug': 'vishnyovy-sad', 'author': authors['Антон Чехов'], 'category': categories['klassicheskaya-literatura'], 'description': 'Последняя пьеса Чехова — лирическая комедия об уходящей эпохе дворянства и неизбежных переменах.', 'price': 320, 'stock': 17, 'pages': 112, 'year_published': 1904, 'publisher': 'Эксмо', 'language': 'Русский', 'isbn': '978-5-04-099879-4', 'featured': False, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9780140447521-L.jpg', 'cover_name': 'vishnyovy-sad.jpg'},
    {'title': 'Палата №6 и другие рассказы', 'slug': 'palata-nomer-6', 'author': authors['Антон Чехов'], 'category': categories['klassicheskaya-literatura'], 'description': 'Сборник рассказов Чехова, включая "Палату №6" — историю о враче, оказавшемся в психиатрической больнице.', 'price': 360, 'stock': 15, 'pages': 320, 'year_published': 1892, 'publisher': 'Эксмо', 'language': 'Русский', 'isbn': '978-5-04-099880-0', 'featured': False, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9780140449921-L.jpg', 'cover_name': 'palata-6.jpg'},
    {'title': 'Евгений Онегин', 'slug': 'evgeniy-onegin', 'author': authors['Александр Пушкин'], 'category': categories['klassicheskaya-literatura'], 'description': 'Роман в стихах — энциклопедия русской жизни XIX века. История холодного петербургского франта и влюблённой в него девушки.', 'price': 380, 'stock': 20, 'pages': 240, 'year_published': 1833, 'publisher': 'Эксмо', 'language': 'Русский', 'isbn': '978-5-04-099881-7', 'featured': True, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9780140447804-L.jpg', 'cover_name': 'onegin.jpg'},
    {'title': 'Капитанская дочка', 'slug': 'kapitanskaya-dochka', 'author': authors['Александр Пушкин'], 'category': categories['klassicheskaya-literatura'], 'description': 'Исторический роман о временах пугачёвского восстания. История любви и чести на фоне кровавых событий XVIII века.', 'price': 290, 'stock': 18, 'pages': 176, 'year_published': 1836, 'publisher': 'АСТ', 'language': 'Русский', 'isbn': '978-5-17-099125-1', 'featured': False, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9785170991251-L.jpg', 'cover_name': 'kapitanskaya-dochka.jpg'},
    {'title': '1984', 'slug': '1984-orwell', 'author': authors['Джордж Оруэлл'], 'category': categories['fantastika'], 'description': 'Культовая антиутопия о тоталитарном обществе, где Большой Брат следит за каждым. Одна из самых влиятельных книг XX века.', 'price': 490, 'stock': 22, 'pages': 320, 'year_published': 1949, 'publisher': 'АСТ', 'language': 'Русский', 'isbn': '978-5-17-099126-8', 'featured': True, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9780451524935-L.jpg', 'cover_name': '1984.jpg'},
    {'title': 'Скотный двор', 'slug': 'skotny-dvor', 'author': authors['Джордж Оруэлл'], 'category': categories['fantastika'], 'description': 'Политическая сатира-притча о животных, свергнувших хозяина фермы. Острая аллегория на советский тоталитаризм.', 'price': 320, 'stock': 19, 'pages': 128, 'year_published': 1945, 'publisher': 'АСТ', 'language': 'Русский', 'isbn': '978-5-17-099127-5', 'featured': False, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9780451526342-L.jpg', 'cover_name': 'skotny-dvor.jpg'},
    {'title': 'Азазель', 'slug': 'azazel-akunin', 'author': authors['Борис Акунин'], 'category': categories['detektivy'], 'description': 'Первый роман о сыщике Эрасте Фандорине. Молодой чиновник расследует загадочные самоубийства в Москве 1876 года.', 'price': 410, 'stock': 16, 'pages': 256, 'year_published': 1998, 'publisher': 'Захаров', 'language': 'Русский', 'isbn': '978-5-8159-0001-2', 'featured': False, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9785815900012-L.jpg', 'cover_name': 'azazel.jpg'},
    {'title': 'Старик и море', 'slug': 'starik-i-more', 'author': authors['Эрнест Хемингуэй'], 'category': categories['klassicheskaya-literatura'], 'description': 'Повесть о старом кубинском рыбаке и его схватке с огромным марлином. За неё Хемингуэй получил Нобелевскую премию.', 'price': 360, 'stock': 20, 'pages': 128, 'year_published': 1952, 'publisher': 'АСТ', 'language': 'Русский', 'isbn': '978-5-17-099128-2', 'featured': True, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9780684801223-L.jpg', 'cover_name': 'starik-more.jpg'},
    {'title': 'По ком звонит колокол', 'slug': 'po-kom-zvonit-kolokol', 'author': authors['Эрнест Хемингуэй'], 'category': categories['klassicheskaya-literatura'], 'description': 'Роман об американском добровольце в Испании. История любви и самопожертвования на фоне гражданской войны.', 'price': 520, 'stock': 11, 'pages': 480, 'year_published': 1940, 'publisher': 'АСТ', 'language': 'Русский', 'isbn': '978-5-17-099129-9', 'featured': False, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9780684803357-L.jpg', 'cover_name': 'kolokol.jpg'},
    {'title': 'Превращение', 'slug': 'prevraschenie-kafka', 'author': authors['Франц Кафка'], 'category': categories['klassicheskaya-literatura'], 'description': 'Знаменитая повесть о коммивояжёре, проснувшемся однажды утром огромным насекомым. Символ отчуждения человека.', 'price': 310, 'stock': 15, 'pages': 96, 'year_published': 1915, 'publisher': 'АСТ', 'language': 'Русский', 'isbn': '978-5-17-099130-5', 'featured': False, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9780553213690-L.jpg', 'cover_name': 'prevraschenie.jpg'},
    {'title': 'Процесс', 'slug': 'process-kafka', 'author': authors['Франц Кафка'], 'category': categories['klassicheskaya-literatura'], 'description': 'Роман о банковском служащем, арестованном без объяснения причин. Абсурдный судебный процесс как метафора бюрократии.', 'price': 380, 'stock': 12, 'pages': 272, 'year_published': 1925, 'publisher': 'АСТ', 'language': 'Русский', 'isbn': '978-5-17-099131-2', 'featured': False, 'cover_url': 'https://covers.openlibrary.org/b/isbn/9780805209990-L.jpg', 'cover_name': 'process.jpg'},
]

for data in books_data:
    cover_url = data.pop('cover_url')
    cover_name = data.pop('cover_name')
    book, created = Book.objects.get_or_create(slug=data['slug'], defaults=data)
    if created or not book.cover:
        print(f"  {'Создана' if created else 'Обновляю'}: {data['title']} — загружаю обложку...")
        img = download_image(cover_url)
        if img:
            book.cover.save(cover_name, img, save=True)
            print(f"    Обложка загружена!")
        else:
            print(f"    Обложка не найдена, пропускаем.")
    else:
        print(f"  Уже есть: {data['title']}")

print("\n" + "="*50)
print("База данных успешно заполнена!")
print("="*50)
print(f"\nКатегорий: {Category.objects.count()}")
print(f"Авторов:   {Author.objects.count()}")
print(f"Книг:      {Book.objects.count()}")
print(f"\nЛогин: admin | Пароль: admin123")