import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from app.catalog.models import Category, Product, Tag, Sales
from app.core.models import Image
from app.orders.models import DeliverySettings


class Command(BaseCommand):
    help = "Create admin user and initial catalog data"

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        # ---------- Admin ----------
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            self.stdout.write(self.style.SUCCESS("Admin user created"))
        else:
            self.stdout.write("Admin user already exists")

        # ---------- Images Category ----------
        tv_image = Image.objects.create(
            src="media/category/tv.png",
            alt="media/category/tv.png"
        )
        device_image = Image.objects.create(
            src="media/category/devices.png",
            alt="media/category/devices.png"
        )
        computer_image = Image.objects.create(
            src="media/category/computer.png",
            alt="media/category/computer.png"
        )
        mouse_image = Image.objects.create(
            src="media/category/mouse.png",
            alt="media/category/mouse.png"
        )
        monitor_image = Image.objects.create(
            src="media/category/monitor.png",
            alt="media/category/monitor.png"
        )
        laptop_image = Image.objects.create(
            src="media/category/laptop.png",
            alt="media/category/laptop.png"
        )
        keyboard_image = Image.objects.create(
            src="media/category/keyboard.png",
            alt="media/category/keyboard.png"
        )
        tablet_image = Image.objects.create(
            src="media/category/tablet.png",
            alt="media/category/tablet.png"
        )
        smartphone_image = Image.objects.create(
            src="media/category/smartphone.png",
            alt="media/category/smartphone.png"
        )
        phone_image = Image.objects.create(
            src="media/category/phone.png",
            alt="media/category/phone.png"
        )
        headphone_image = Image.objects.create(
            src="media/category/headphone.png",
            alt="media/category/headphone.png"
        )

        # ---------- Images Products ----------
        chuwi_image_1 = Image.objects.create(
            src="media/products/chuwi/CoreBook_1.jpeg",
            alt="media/products/chuwi/CoreBook_1.jpeg"
        )
        chuwi_image_2 = Image.objects.create(
            src="media/products/chuwi/CoreBook_2.jpeg",
            alt="media/products/chuwi/CoreBook_3.jpeg"
        )
        chuwi_image_3 = Image.objects.create(
            src="media/products/chuwi/CoreBook_3.jpeg",
            alt="media/products/chuwi/CoreBook_3.jpeg"
        )
        apex_pro_tkl_1 = Image.objects.create(
            src="media/products/steelseries/Apex_Pro_TKL_1.jpg",
            alt="media/products/steelseries/Apex_Pro_TKL_1.jpg"
        )
        apex_pro_tkl_2 = Image.objects.create(
            src="media/products/steelseries/Apex_Pro_TKL_2.jpg",
            alt="media/products/steelseries/Apex_Pro_TKL_2.jpg"
        )
        mx_anywhere = Image.objects.create(
            src="media/products/logitech/MX_Anywhere_3S.jpeg",
            alt="media/products/logitech/MX_Anywhere_3S.jpeg"
        )
        xiaomi = Image.objects.create(
            src="media/products/xiaomi/monitor.jpeg",
            alt="media/products/xiaomi/monitor.jpeg"
        )
        blackview = Image.objects.create(
            src="media/products/blackview/tablet.jpeg",
            alt="media/products/blackview/tablet.jpeg"
        )
        lg = Image.objects.create(
            src="media/products/lg/tv.jpeg",
            alt="media/products/lg/tv.jpeg"
        )
        jbl = Image.objects.create(
            src="media/products/jbl/headphone.jpeg",
            alt="media/products/jbl/headphone.jpeg"
        )
        infinix = Image.objects.create(
            src="media/products/infinix/smartphone.jpeg",
            alt="media/products/infinix/smartphone.jpeg"
        )
        nokia = Image.objects.create(
            src="media/products/nokia/phone.jpeg",
            alt="media/products/nokia/phone.jpeg"
        )

        # ---------- Categories ----------
        tv, _ = Category.objects.get_or_create(
            title="TV",
            image=tv_image
        )
        device, _ = Category.objects.get_or_create(
            title="Device",
            image=device_image
        )
        computer, _ = Category.objects.get_or_create(
            title="Computer",
            image=computer_image
        )
        mouse, _ = Category.objects.get_or_create(
            title="Mouse",
            image=mouse_image,
            parent=computer
        )
        monitor, _ = Category.objects.get_or_create(
            title="Monitor",
            image=monitor_image,
            parent=computer
        )
        laptop, _ = Category.objects.get_or_create(
            title="Laptop",
            image=laptop_image,
            parent=computer
        )
        keyboard, _ = Category.objects.get_or_create(
            title="Keyboard",
            image=keyboard_image,
            parent=computer
        )
        tablet, _ = Category.objects.get_or_create(
            title="Tablet",
            image=tablet_image,
            parent=device
        )
        smartphone, _ = Category.objects.get_or_create(
            title="Smartphone",
            image=smartphone_image,
            parent=device
        )
        phone, _ = Category.objects.get_or_create(
            title="Phone",
            image=phone_image,
            parent=device
        )
        headphone, _ = Category.objects.get_or_create(
            title="Headphone",
            image=headphone_image,
            parent=device
        )

        # ---------- Tags ----------
        gaming, _ = Tag.objects.get_or_create(name="gaming")
        office, _ = Tag.objects.get_or_create(name="office")
        call, _ = Tag.objects.get_or_create(name="call")

        # ---------- Products ----------
        chuwi, created = Product.objects.get_or_create(
            title="Chuwi CoreBook X CWI570-12450H16G512",
            defaults={
                "category": laptop,
                "price": 600,
                "count": 10,
                "description": "14.0' 2160 x 1440, IPS, 60 Гц, Intel Core i5 12450H, "
                               "16 ГБ DDR4, SSD 512 ГБ, видеокарта встроенная, "
                               "Windows 11 Home, цвет крышки темно-серый, аккумулятор 46.2 Вт·ч",
                "fullDescription": "✅ Ноутбук Chuwi CoreBook X 2024 — это идеальный выбор для тех, "
                                   "кто нуждается в мощном и компактном устройстве для работы и учебы. "
                                   "Он сочетает стильный дизайн с высокой производительностью, "
                                   "что делает его отличным вариантом для офисных задач и повседневного "
                                   "использования."
                                   "✅ С эргономичным корпусом и легким весом, этот ноутбук удобно переносить, "
                                   "что оценят студенты и профессионалы, постоянно находящиеся в движении. "
                                   "Внутри установлен мощный процессор Intel i3-1220P, который обеспечивает "
                                   "быструю обработку данных и готов к любым задачам. ✅ Объем оперативной "
                                   "памяти в 16 ГБ позволяет открывать множество приложений и вкладок "
                                   "одновременно без потери скорости. Накопитель на 512 ГБ предоставляет "
                                   "достаточно места для хранения файлов, документов и медиа-контента, "
                                   "что делает работу более комфортной и продуктивной. ✅ Этот ноутбук "
                                   "также подходит для легкой мультимедийной работы, обеспечивая хорошее "
                                   "качество изображения и звука. Он станет отличным помощником для дизайнеров, "
                                   "студентов и всех, кто нуждается в надежной технике для выполнения различных задач. "
                                   "Chuwi CoreBook X 2024 — это не просто офисный ноутбук, а высококачественное "
                                   "устройство, способное справиться с любыми вызовами повседневной жизни. "
                                   "Если вы ищете компактный ноутбук с отличными характеристиками, дизайном "
                                   "и практичностью, эта модель станет вашим идеальным выбором.",
                "freeDelivery": True,
            },
        )
        if created:
            chuwi.tags.set([office])
            chuwi.images.set([chuwi_image_1, chuwi_image_2, chuwi_image_3])

        steelseries, created = Product.objects.get_or_create(
            title="SteelSeries Apex Pro TKL",
            defaults={
                "category": keyboard,
                "price": 220,
                "count": 10,
                "description": "игровая для ПК, магнитная, Steelseries OmniPoint, полностью металлическая, "
                               "интерфейс подключения - USB-A, подсветка, кириллица: да, USB-хаб, цвет черный",
                "fullDescription": "Данная игровая клавиатура снабжена дисплеем OLED Smart, "
                                   "благодаря которому можно управлять настройками клавиатуры без "
                                   "необходимости переключаться между окнами на компьютере. Также "
                                   "присутствует функция оповещений Discord, Tidal и Spotify в режиме "
                                   "реального времени и возможность сохранения до 5 настраиваемых макросов.",
                "freeDelivery": False,
                "limited": True,
            },
        )
        if created:
            steelseries.tags.set([gaming])
            steelseries.images.set([apex_pro_tkl_1, apex_pro_tkl_2])

        logitech, created = Product.objects.get_or_create(
            title="Logitech MX Anywhere 3S",
            defaults={
                "category": mouse,
                "price": 85,
                "count": 12,
                "description": "ноутбучная мышь, беспроводная Bluetooth/беспроводная радио, "
                               "сенсор лазерный 8000 dpi, 7 кнопок, колесо с нажатием, цвет темно-серый",
                "fullDescription": "Опыт максимальной универсальности с выдающейся производительностью. "
                                   "Это продвинутая компактная мышь, которая позволяет вам работать где угодно. "
                                   "Теперь с уровнем точности и отзывчивости на следующем уровне благодаря 8K DPI "
                                   "отслеживанию на любой поверхности и тихим щелчкам.✅ Отслеживает везде, "
                                   "идет везде. Работайте на любой поверхности - даже на стекле (минимальная "
                                   "толщина стекла 74 мм) с MX Anywhere 3S - теперь с сенсором 8K DPI, чтобы "
                                   "вы могли охватить большую площадь с незаметными движениями.",
                "freeDelivery": False,
                "limited": True,
            },
        )
        if created:
            logitech.tags.set([office])
            logitech.images.set([mx_anywhere])

        xiaomi_monitor, created = Product.objects.get_or_create(
            title="Xiaomi Gaming Monitor G27i 2026 P27FDA-RGGL",
            defaults={
                "category": monitor,
                "price": 180,
                "count": 15,
                "description": "27', 1920x1080, 16:9, IPS, 200 Гц, глубина 8 бит, HDMI+DisplayPort",
                "fullDescription": "Xiaomi Gaming Monitor G27i 2026 - это 27-дюймовый игровой монитор "
                                   "с IPS-матрицей, который отлично подойдет для геймеров, ценящих "
                                   "плавность изображения и точную цветопередачу. Экран с разрешением "
                                   "1920x1080 пикселей обеспечивает четкое и насыщенное изображение, "
                                   "а высокая частота обновления 200 Гц и время отклика 1 мс GtG позволяют "
                                   "мгновенно реагировать на происходящее в играх. ✅ Монитор отличается "
                                   "поддержкой HDR (DisplayHDR 400), что обеспечивает более глубокие тени "
                                   "и яркие светлые участки, а также расширенный цветовой охват:100% sRGB "
                                   "и 95% DCI-P3. Благодаря технологии AMD FreeSync Premium и совместимости "
                                   "с NVIDIA G-Sync, устраняется разрыв и дергание кадров, что важно для "
                                   "динамичных сцен.",
                "freeDelivery": True,
            },
        )
        if created:
            xiaomi_monitor.images.set([xiaomi])

        blackview_tablet, created = Product.objects.get_or_create(
            title="Blackview Tab 16 Pro 8GB/256GB",
            defaults={
                "category": tablet,
                "price": 200,
                "count": 5,
                "description": "11.0' IPS, 60 Гц (1920x1200), Android, UniSoC Tiger T616, 8 ГБ / 256 ГБ, "
                               "Wi-Fi + сотовая связь (nanoSIM + nanoSIM), аккумулятор 7700 мАч",
                "fullDescription": "✅ Стильный, тонкий и легкий как воздух весом 503 г и толщиной 7,45 мм, "
                                   "его изысканный дизайн и легкая конструкция переопределяют ваше представление "
                                   "о планшете, делая его идеальным партнером как для работы в кафе, так и для "
                                   "отдыха на диване. ✅ Четкое и яркое изображение, выбирайте потрясающий вид. "
                                   "Насладитесь обширным 11-дюймовым дисплеем Full HD. Его живые цвета, четкий "
                                   "контраст и щедрые углы обзора оживляют каждую сцену, полностью погружая "
                                   "вас в увлекательные сюжеты игр и фильмов.",
                "freeDelivery": False,
                "limited": False,
            },
        )
        if created:
            blackview_tablet.tags.set([call])
            blackview_tablet.images.set([blackview])

        lg_tv, created = Product.objects.get_or_create(
            title="LG NanoCell AI NANO81 55NANO81A6A",
            defaults={
                "category": tv,
                "price": 650,
                "count": 10,
                "description": "55' 3840x2160 (4K UHD), частота матрицы 60 Гц, Smart TV (LG webOS), "
                               "HDR10, HLG, AirPlay, Wi-Fi, смарт пульт",
                "fullDescription": "✅ Мощный ИИ-процессор α7 Gen8: новый уровень визуального восприятия."
                                   "Процессор α7 Gen8 с искусственным интеллектом обеспечивает обработку "
                                   "изображений в разрешении 4K с высокой чёткостью и глубиной. Построенный "
                                   "на базе усовершенствованных технологий, он работает быстрее и эффективнее, "
                                   "чем предыдущие поколения. Яркое жёлтое свечение и разноцветные вспышки "
                                   "подчеркивают его технологическую мощь. Сравнение произведено с α5 Gen6 "
                                   "по внутренним техническим характеристикам.",
                "freeDelivery": True,
                "limited": True,
            },
        )
        if created:
            lg_tv.images.set([lg])

        jbl_headphone, created = Product.objects.get_or_create(
            title="JBL Tune Flex 2 Ghost",
            defaults={
                "category": headphone,
                "price": 95,
                "count": 25,
                "description": "беспроводные наушники с микрофоном, вставные, портативные, "
                               "полностью беспроводные (TWS), Bluetooth 5.3, 20-20000 Гц, "
                               "быстрая зарядка, время работы 12 ч, с кейсом 48 ч, активное шумоподавление",
                "fullDescription": "✅ JBL Pure Bass Sound с пространственным звучанием. "
                                   "Наушники JBL Tune Flex 2 оснащены динамическими драйверами диаметром "
                                   "12 мм, которые обеспечивают мощный звук JBL Pure Bass. И независимо от "
                                   "того, слушаете ли вы свой любимый плейлист, смотрите фильм или играете "
                                   "в игру, JBL Spatial Sound преобразует стереозвук из любого источника или "
                                   "устройства в более захватывающий звуковой опыт.",
                "freeDelivery": False,
                "limited": False,
            },
        )
        if created:
            jbl_headphone.images.set([jbl])

        infinix_smartphone, created = Product.objects.get_or_create(
            title="Infinix Hot 60i X6728 4GB/128GB",
            defaults={
                "category": smartphone,
                "price": 105,
                "count": 9,
                "description": "смартфон, Android, экран 6.7' IPS (720x1600) 120 Гц, Mediatek "
                               "Helio G81 Ultimate, ОЗУ 4 ГБ, память 128 ГБ, поддержка карт памяти, "
                               "камера 50 Мп, аккумулятор 5160 мАч, моноблок, влагозащита IP64",
                "fullDescription": "✅ Infinix HOT 60i сочетает ультратонкий дизайн и современные "
                                   "технологии, предлагая 7,7-мм корпус весом всего 188 г в эффектной "
                                   "Color-Pop палитре. При компактных габаритах смартфон оснащён мощной "
                                   "батареей на 5160 мА·ч с энергоёмкостью 810 Вт·ч/л и поддержкой 45 Вт "
                                   "FastCharge, позволяющей зарядить до 50 % всего за 24 минуты. "
                                   "Ресурс аккумулятора рассчитан на 5 лет работы (до 1800 циклов зарядки), "
                                   "а защита от перегрева при ночной зарядке повышает долговечность. ✅ За "
                                   "производительность отвечает MediaTek Helio G81 Ultimate с восьмиядерным"
                                   " CPU и графикой для плавного гейминга и многозадачности. Игровые функции "
                                   "дополняет GyroPro — аппаратный гироскоп для точной навигации в "
                                   "GPS-«слепых зонах» и высокой чувствительности в играх. Объём памяти "
                                   "достигает 256 ГБ ПЗУ и 16 ГБ ОЗУ (8 ГБ + 8 ГБ виртуального расширения).",
                "freeDelivery": False,
            },
        )
        if created:
            infinix_smartphone.tags.set([call])
            infinix_smartphone.images.set([infinix])

        nokia_phone, created = Product.objects.get_or_create(
            title="Nokia 3210 4G (2024) Dual SIM TA-1618",
            defaults={
                "category": phone,
                "price":90,
                "count": 5,
                "description": "кнопочный телефон, экран 2.4' TFT (240x240), UniSoC Tiger T107, ОЗУ 64 Мб, "
                               "память 128 Мб, поддержка карт памяти, камера 2 Мп, аккумулятор 1450 мАч, моноблок",
                "fullDescription": "✅ Оригинальный телефон Nokia 3210 был выпущен в далеком 1999 году, "
                                   "а теперь его обновленная версия возвращается.✅ Кнопочный телефон с "
                                   "поддержкой LTE, который подходит не только для голосовых вызовов. "
                                   "✅ Пользователи могут смотреть погоду, новости и даже видео благодаря "
                                   "специальному программному обеспечению (не на базе Android).",
                "freeDelivery": False,
                "limited": True,
            },
        )
        if created:
            nokia_phone.tags.set([call])
            nokia_phone.images.set([nokia])

        delivery_cost, create = DeliverySettings.objects.get_or_create(
            free_delivery_threshold=500,
            delivery_price=10,
            express_delivery_price=20,
        )

        self.stdout.write(self.style.SUCCESS("Initial data created"))
