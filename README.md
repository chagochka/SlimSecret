# SlimSecret
 ## Краткая характеристика
* Наименование программы: **SlimSecret** - программа для вашего питания.
* Назначение программы: программа предназначена для **учета колорий** съеденной за день пищи.
* Конечные пользователи: люди **желающие похудеть** или **набрать массу**.

## Техническое задание
Людям желающим похудеть или набрать массу нужно рассчитывать количество употребленных калорий в сутки. Делать это самому очень неудобно. 

Программа **SlimSecret** расчитывает Рекомендуемое Суточное Количество(РСК) по формуле Миффлина-Сан Жеора(Расчет РСК основан на уникальных факторах, включая возраст, вес, рост, пол и уровень активности.), чтобы дать пользователю представление об ежедневном количестве калорий, нужном для достижении цели пользователя.

Формула Миффлина-Сан Жеора:

 + для **мужчин**: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) + 5) x A;
 + для **женщин**: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) – 161) x A.

**A** – это уровень активности человека, его различают обычно по пяти степеням физических нагрузок в сутки:

 + **1,2** – минимальная активность, сидячая работа, не требующая значительных физических нагрузок;
 + **1,375** – слабый уровень активности: интенсивные упражнения не менее 20 минут один-три раза в неделю. Это может быть езда на велосипеде, бег трусцой, баскетбол, плавание, катание на коньках и т. д. Если вы не тренируетесь регулярно, но сохраняете занятый стиль жизни, который требует частой ходьбы в течение длительного времени, то выберите этот коэффициент;
 + **1,55** – умеренный уровень активности: интенсивная тренировка не менее 30-60 мин три-четыре раза в неделю (любой из перечисленных выше видов спорта);
 + **1,7** – тяжелая или трудоемкая активность: интенсивные упражнения и занятия спортом 5-7 дней в неделю. Трудоемкие занятия также подходят для этого уровня, они включают строительные работы (кирпичная кладка, столярное дело и т. д.), занятость в сельском хозяйстве и т. п.;
 + **1,9** – экстремальный уровень: включает чрезвычайно активные и/или очень энергозатратные виды деятельности: занятия спортом с почти ежедневным графиком и несколькими тренировками в течение дня; очень трудоемкая работа, например, сгребание угля или длительный рабочий день на сборочной линии. Зачастую этого уровня активности очень трудно достичь.

Стоит отметить, что данная формула актуальна только для лиц в возрасте от **13** до **80** лет.

Как только **РСК** пользователя установлено, он сможет отслеживать количество употребленных калорий в программе.

## Сборка и запуск
Разработка и тестирование программы было осуществлено в операционной системе **Microsoft Windows 10 1809**. Для успешного запуска и нормальной работы должно быть установлено следующее программное обеспечение:

+ язык **Python 3.7**
+ библиотека **PyQt 5.15.4**
+ библиотека **googletrans 4.0.0**
+ библиотека **PyQtChart 5.15.6**

## Функциональные возможности
Программа **SlimSecret** позволяет просто и удобно расчитывать РСК и отслеживтье съеденные в день калорий.

При помощи **SlimSecret** можно легко рассчитывать РСК и следить за калориями, благодаря базе данных пользователь может найти калорийность и нутрициенты нужного продукта. Если продукта не оказалось в базе данных пользователь сам вносит данные о продукте.
# Интерфейс программы
## Окно регистрации
Если пользователь ещё не зарегистрирован открывется **окно регистрации**

![reg](./pic/reg.png 'Окно регистрации')

Здесь пользователь заполняет поля для регистрации и регистрируется.
## Главное окно
Уже зарегистрированный пользователь попадает в **главное окно**

![main](./pic/main.png 'Главное окно')
## Окно добавления каллорий
При нажатии соответствующей кнопки на главном окне пользователь попадает в **Окно добавления каллорий**

![add](./pic/add.png 'Окно добавления каллорий')

Здесь введя в строке поиска необходимый продукт пользователь может выбрать нужный ему вариант из списка, в списке представлены название на русском и оригиальное(как в БД). Если такого не оказалось пользователь может сам ввести информацию о продукте(все поля открыты для редактирования).
Так же пользователь увидит круговую диаграмму нутрициентов продукта(доступно только для существующих в базе продуктов).
## Окно профиля
При нажатии соответствующей кнопки на главном окне пользователь попадает в **Окно профиля**

![profile](./pic/profile.png 'Окно профиля')

Здесь он может удалить свой профил или изменить данные(расчет РСК пройдет заново).
