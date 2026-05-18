"""
Скрипт для заполнения базы данных тестовыми данными.
Запуск: python manage.py shell < populate_db.py
или: python populate_db.py (из папки проекта)
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from store.models import Category, Author, Book

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
    ('Лев', 'Толстой', 'Великий русский писатель, автор "Войны и мира" и "Анны Карениной".'),
    ('Фёдор', 'Достоевский', 'Классик русской литературы, автор "Преступления и наказания".'),
    ('Агата', 'Кристи', 'Знаменитая английская писательница детективного жанра.'),
    ('Стивен', 'Кинг', 'Американский мастер хоррора и триллера.'),
    ('Джоан', 'Роулинг', 'Автор серии книг о Гарри Поттере.'),
    ('Михаил', 'Булгаков', 'Русский писатель, автор "Мастера и Маргариты".'),
    ('Чингиз', 'Айтматов', 'Выдающийся кыргызский и советский писатель.'),
    ('Эрих', 'Мария Ремарк', 'Немецкий писатель, автор "На Западном фронте без перемен".'),
]

authors = []
for first, last, bio in authors_data:
    author, created = Author.objects.get_or_create(
        first_name=first, last_name=last,
        defaults={'bio': bio}
    )
    authors.append(author)
    print(f"  {'Создан' if created else 'Уже есть'}: {first} {last}")

print("\nСоздаём книги...")
books_data = [
    {
        'title': 'Война и мир',
        'slug': 'voyna-i-mir',
        'author': authors[0],
        'category': categories['klassicheskaya-literatura'],
        'description': 'Эпический роман-эпопея Льва Толстого, описывающий русское общество в эпоху войн с Наполеоном. Одно из величайших произведений мировой литературы.',
        'price': 850,
        'stock': 15,
        'pages': 1225,
        'year_published': 1869,
        'publisher': 'Эксмо',
        'language': 'Русский',
        'isbn': '978-5-04-089473-6',
        'featured': True,
    },
    {
        'title': 'Преступление и наказание',
        'slug': 'prestuplenie-i-nakazanie',
        'author': authors[1],
        'category': categories['klassicheskaya-literatura'],
        'description': 'Философский роман о студенте Раскольникове, решившемся на убийство. Одно из самых известных произведений Достоевского.',
        'price': 650,
        'stock': 20,
        'pages': 672,
        'year_published': 1866,
        'publisher': 'АСТ',
        'language': 'Русский',
        'isbn': '978-5-17-090823-4',
        'featured': True,
    },
    {
        'title': 'Убийство в Восточном экспрессе',
        'slug': 'ubiystvo-v-vostochnom-ekspresse',
        'author': authors[2],
        'category': categories['detektivy'],
        'description': 'Классический детектив с Эркюлем Пуаро. В поезде, застрявшем в снегах, найден убитый. Кто преступник среди двенадцати подозреваемых?',
        'price': 480,
        'stock': 25,
        'pages': 288,
        'year_published': 1934,
        'publisher': 'Эксмо',
        'language': 'Русский',
        'isbn': '978-5-04-106843-2',
        'featured': True,
    },
    {
        'title': 'Сияние',
        'slug': 'siyanie',
        'author': authors[3],
        'category': categories['fantastika'],
        'description': 'Роман ужасов о смотрителе отеля Overlook, изолированного в горах Колорадо зимой. Психологический триллер о безумии и сверхъестественном.',
        'price': 720,
        'stock': 10,
        'pages': 688,
        'year_published': 1977,
        'publisher': 'АСТ',
        'language': 'Русский',
        'isbn': '978-5-17-119743-1',
        'featured': False,
    },
    {
        'title': 'Гарри Поттер и философский камень',
        'slug': 'garri-potter-filosofsky-kamen',
        'author': authors[4],
        'category': categories['detskaya-literatura'],
        'description': 'Первая книга серии о молодом волшебнике Гарри Поттере. История о дружбе, магии и борьбе добра со злом.',
        'price': 590,
        'stock': 30,
        'pages': 432,
        'year_published': 1997,
        'publisher': 'РОСМЭН',
        'language': 'Русский',
        'isbn': '978-5-353-01435-6',
        'featured': True,
    },
    {
        'title': 'Мастер и Маргарита',
        'slug': 'master-i-margarita',
        'author': authors[5],
        'category': categories['klassicheskaya-literatura'],
        'description': 'Мистический роман о визите Воланда (дьявола) в советскую Москву. Одно из самых загадочных и глубоких произведений русской литературы XX века.',
        'price': 530,
        'stock': 18,
        'pages': 480,
        'year_published': 1967,
        'publisher': 'Эксмо',
        'language': 'Русский',
        'isbn': '978-5-04-099876-3',
        'featured': True,
    },
    {
        'title': 'Белый пароход',
        'slug': 'belyy-parohod',
        'author': authors[6],
        'category': categories['klassicheskaya-literatura'],
        'description': 'Повесть выдающегося кыргызского писателя Чингиза Айтматова о мальчике, живущем в горном урочище, и его мечтах.',
        'price': 350,
        'stock': 12,
        'pages': 184,
        'year_published': 1970,
        'publisher': 'Кыргызстан',
        'language': 'Русский',
        'isbn': '978-5-000-00001-0',
        'featured': False,
    },
    {
        'title': 'На Западном фронте без перемен',
        'slug': 'na-zapadnom-fronte-bez-peremen',
        'author': authors[7],
        'category': categories['klassicheskaya-literatura'],
        'description': 'Антивоенный роман о немецких солдатах Первой мировой войны. Одно из самых пронзительных произведений о войне.',
        'price': 420,
        'stock': 14,
        'pages': 304,
        'year_published': 1929,
        'publisher': 'АСТ',
        'language': 'Русский',
        'isbn': '978-5-17-088034-2',
        'featured': False,
    },
    {
        'title': 'Анна Каренина',
        'slug': 'anna-karenina',
        'author': authors[0],
        'category': categories['klassicheskaya-literatura'],
        'description': 'Роман о трагической судьбе женщины в высшем свете, разрывающейся между долгом и любовью. Вечная история страсти и нравственного выбора.',
        'price': 750,
        'stock': 8,
        'pages': 864,
        'year_published': 1878,
        'publisher': 'Эксмо',
        'language': 'Русский',
        'isbn': '978-5-04-099877-0',
        'featured': False,
    },
    {
        'title': 'Идиот',
        'slug': 'idiot-dostoevsky',
        'author': authors[1],
        'category': categories['klassicheskaya-literatura'],
        'description': 'Роман о добром и наивном князе Мышкине, оказавшемся в жестоком мире петербургского общества. Размышления о природе добра и красоты.',
        'price': 580,
        'stock': 9,
        'pages': 640,
        'year_published': 1869,
        'publisher': 'АСТ',
        'language': 'Русский',
        'isbn': '978-5-17-099123-7',
        'featured': False,
    },
    {
        'title': 'Десять негритят',
        'slug': 'desyat-negrityat',
        'author': authors[2],
        'category': categories['detektivy'],
        'description': 'Самый известный детектив Агаты Кристи. Десять человек приглашены на уединённый остров, и один за другим начинают погибать.',
        'price': 440,
        'stock': 20,
        'pages': 256,
        'year_published': 1939,
        'publisher': 'Эксмо',
        'language': 'Русский',
        'isbn': '978-5-04-107234-7',
        'featured': False,
    },
    {
        'title': 'Оно',
        'slug': 'ono-stiven-king',
        'author': authors[3],
        'category': categories['fantastika'],
        'description': 'Культовый роман ужасов о группе детей из города Дерри, столкнувшихся с древним злом в образе клоуна Пеннивайза.',
        'price': 890,
        'stock': 7,
        'pages': 1376,
        'year_published': 1986,
        'publisher': 'АСТ',
        'language': 'Русский',
        'isbn': '978-5-17-119744-8',
        'featured': True,
    },
]

for data in books_data:
    book, created = Book.objects.get_or_create(slug=data['slug'], defaults=data)
    print(f"  {'Создана' if created else 'Уже есть'}: {data['title']}")

print("\n" + "="*50)
print("База данных успешно заполнена!")
print("="*50)
print(f"\nКатегорий: {Category.objects.count()}")
print(f"Авторов:   {Author.objects.count()}")
print(f"Книг:      {Book.objects.count()}")
print(f"\nАдмин-панель: http://127.0.0.1:8000/admin/")
print(f"Логин: admin | Пароль: admin123")
print(f"\nЗапуск: python manage.py runserver")
