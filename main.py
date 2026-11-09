
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN


dp = Dispatcher(storage=MemoryStorage())


# Состояния теста
class ProfessionForm(StatesGroup):
    subjects = State()
    interests = State()
    strengths = State()
class SkillForm(StatesGroup):
    direction = State()
    strength = State()
    level = State()
class MissingSkillsForm(StatesGroup):
    direction = State()
    profession = State()
    level = State()
class CareerPlanForm(StatesGroup):
    direction = State()
    profession = State()
    time = State()
# Главное меню
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎯 Подобрать профессию")],
        [KeyboardButton(text="📊 Анализ навыков")],
        [KeyboardButton(text="🔍 Найти недостающие навыки")],
        [KeyboardButton(text="🧭 Карьерный план")],
        [KeyboardButton(text="⬅️ Главное меню")]
    ],
    resize_keyboard=True
)

# Функция для создания клавиатуры с вариантами ответов
def create_keyboard(options):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=option)] for option in options],
        resize_keyboard=True
    )

@dp.message(F.text == "⬅️ Главное меню")
async def back_to_menu(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "🏠 Ты вернулся в главное меню!\n\n"
        "Что хочешь сделать дальше?",
        reply_markup=menu
    )
# Запуск бота
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Привет! Я Onward 🚀\n\n"
        "Помогу разобраться в профессиях, навыках "
        "и построить карьерный план.\n\n"
        "Выбери, что хочешь сделать:",
        reply_markup=menu
    )


# Отмена теста
@dp.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Тест отменён. Можешь начать заново!",
        reply_markup=menu
    )


# Начало подбора профессии
@dp.message(F.text == "🎯 Подобрать профессию")
async def professions(message: Message, state: FSMContext):
    await state.set_state(ProfessionForm.subjects)

    await message.answer(
        "🎯 Давай подберём тебе профессию!\n\n"
        "Вопрос 1 из 3.\n"
        "Какие школьные предметы тебе больше нравятся?",
        reply_markup=create_keyboard([
            "Математика и физика",
            "Языки и история",
            "Биология и химия",
            "Искусство и литература"
        ])
    )


# Вопрос 1
@dp.message(ProfessionForm.subjects)
async def get_subjects(message: Message, state: FSMContext):
    options = [
        "Математика и физика",
        "Языки и история",
        "Биология и химия",
        "Искусство и литература"
    ]

    if message.text not in options:
        await message.answer("Пожалуйста, выбери один из предложенных вариантов.")
        return

    await state.update_data(subjects=message.text)
    await state.set_state(ProfessionForm.interests)

    await message.answer(
        "Вопрос 2 из 3.\n"
        "Что тебе интереснее?",
        reply_markup=create_keyboard([
            "Работать с людьми",
            "Работать с технологиями",
            "Работать с данными и исследованиями",
            "Создавать что-то новое"
        ])
    )


# Вопрос 2
@dp.message(ProfessionForm.interests)
async def get_interests(message: Message, state: FSMContext):
    options = [
        "Работать с людьми",
        "Работать с технологиями",
        "Работать с данными и исследованиями",
        "Создавать что-то новое"
    ]

    if message.text not in options:
        await message.answer("Пожалуйста, выбери один из предложенных вариантов.")
        return

    await state.update_data(interests=message.text)
    await state.set_state(ProfessionForm.strengths)

    await message.answer(
        "Вопрос 3 из 3.\n"
        "Что у тебя получается лучше всего?",
        reply_markup=create_keyboard([
            "Анализировать и решать задачи",
            "Общаться и помогать людям",
            "Придумывать идеи",
            "Организовывать и руководить"
        ])
    )


# Вопрос 3 и результат
@dp.message(ProfessionForm.strengths)
async def get_strengths(message: Message, state: FSMContext):
    options = [
        "Анализировать и решать задачи",
        "Общаться и помогать людям",
        "Придумывать идеи",
        "Организовывать и руководить"
    ]

    if message.text not in options:
        await message.answer("Пожалуйста, выбери один из предложенных вариантов.")
        return

    await state.update_data(strengths=message.text)
    data = await state.get_data()

    recommendations = {
        "Работать с людьми": [
            "Психолог",
            "HR-специалист",
            "Преподаватель"
        ],
        "Работать с технологиями": [
            "Разработчик программного обеспечения",
            "Специалист по кибербезопасности",
            "Инженер"
        ],
        "Работать с данными и исследованиями": [
            "Аналитик данных",
            "Экономист",
            "Исследователь"
        ],
        "Создавать что-то новое": [
            "Графический дизайнер",
            "Архитектор",
            "UX/UI-дизайнер"
        ]
    }

    professions_list = recommendations[data["interests"]]

    await message.answer(
        "🎉 Тест завершён!\n\n"
        f"Твои любимые предметы: {data['subjects']}\n"
        f"Твои интересы: {data['interests']}\n"
        f"Твои сильные стороны: {data['strengths']}\n\n"
        "🌟 Вот профессии, которые стоит изучить:\n\n"
        f"1. {professions_list[0]}\n"
        f"2. {professions_list[1]}\n"
        f"3. {professions_list[2]}\n\n"
        "Это предварительные рекомендации, а не окончательный выбор. "
        "Изучи эти профессии и подумай, какая тебе ближе!",
        reply_markup=menu
    )

    await state.clear()


# Остальные функции пока в разработке

# Начало анализа навыков
@dp.message(F.text == "📊 Анализ навыков")
async def skills(message: Message, state: FSMContext):
    await state.set_state(SkillForm.direction)

    await message.answer(
        "📊 Давай проанализируем твои навыки!\n\n"
        "Вопрос 1 из 3.\n"
        "В какой сфере тебе интересно развиваться?",
        reply_markup=create_keyboard([
            "IT и технологии",
            "Бизнес и экономика",
            "Дизайн и творчество",
            "Работа с людьми"
        ])
    )


# Вопрос 1
@dp.message(SkillForm.direction)
async def get_direction(message: Message, state: FSMContext):
    options = [
        "IT и технологии",
        "Бизнес и экономика",
        "Дизайн и творчество",
        "Работа с людьми"
    ]

    if message.text not in options:
        await message.answer("Выбери один из предложенных вариантов.")
        return

    await state.update_data(direction=message.text)
    await state.set_state(SkillForm.strength)

    await message.answer(
        "Вопрос 2 из 3.\n"
        "Какой навык ты считаешь своей сильной стороной?",
        reply_markup=create_keyboard([
            "Аналитическое мышление",
            "Коммуникация",
            "Креативность",
            "Организация и планирование"
        ])
    )


# Вопрос 2
@dp.message(SkillForm.strength)
async def get_strength(message: Message, state: FSMContext):
    options = [
        "Аналитическое мышление",
        "Коммуникация",
        "Креативность",
        "Организация и планирование"
    ]

    if message.text not in options:
        await message.answer("Выбери один из предложенных вариантов.")
        return

    await state.update_data(strength=message.text)
    await state.set_state(SkillForm.level)

    await message.answer(
        "Вопрос 3 из 3.\n"
        "Как ты оцениваешь свой текущий уровень навыков?",
        reply_markup=create_keyboard([
            "Начинающий",
            "Средний уровень",
            "Уверенный уровень"
        ])
    )


# Вопрос 3 и результат
@dp.message(SkillForm.level)
async def get_level(message: Message, state: FSMContext):
    options = [
        "Начинающий",
        "Средний уровень",
        "Уверенный уровень"
    ]

    if message.text not in options:
        await message.answer("Выбери один из предложенных вариантов.")
        return

    await state.update_data(level=message.text)
    data = await state.get_data()

    development = {
        "IT и технологии": "Программирование, цифровая грамотность и работа с данными",
        "Бизнес и экономика": "Финансовая грамотность, анализ рынка и управление проектами",
        "Дизайн и творчество": "Работа с дизайн-инструментами, визуальное мышление и композиция",
        "Работа с людьми": "Эмпатия, публичные выступления и командная работа"
    }

    await message.answer(
        "📊 Твой анализ навыков готов!\n\n"
        f"🌐 Сфера интересов: {data['direction']}\n"
        f"💪 Сильная сторона: {data['strength']}\n"
        f"📈 Текущий уровень: {data['level']}\n\n"
        "🎯 Что рекомендуется развивать:\n"
        f"{development[data['direction']]}\n\n"
        "Это предварительная самооценка на основе твоих ответов. "
        "Она поможет определить направление дальнейшего развития.",
        reply_markup=menu
    )

    await state.clear()




# Начало поиска недостающих навыков
@dp.message(F.text == "🔍 Найти недостающие навыки")
async def missing_skills(message: Message, state: FSMContext):
    await state.set_state(MissingSkillsForm.direction)

    await message.answer(
        "🔍 Давай определим, каких навыков тебе не хватает!\n\n"
        "Вопрос 1 из 3.\n"
        "В какой сфере ты хочешь развиваться?",
        reply_markup=create_keyboard([
            "IT и технологии",
            "Бизнес и экономика",
            "Дизайн и творчество",
            "Работа с людьми"
        ])
    )


# Вопрос 1
@dp.message(MissingSkillsForm.direction)
async def get_missing_direction(message: Message, state: FSMContext):
    options = [
        "IT и технологии",
        "Бизнес и экономика",
        "Дизайн и творчество",
        "Работа с людьми"
    ]

    if message.text not in options:
        await message.answer("Выбери один из предложенных вариантов.")
        return

    await state.update_data(direction=message.text)
    await state.set_state(MissingSkillsForm.profession)

    await message.answer(
        "Вопрос 2 из 3.\n"
        "Какую профессию ты хочешь освоить?\n\n"
        "Напиши её название своими словами."
    )


# Вопрос 2
@dp.message(MissingSkillsForm.profession)
async def get_missing_profession(message: Message, state: FSMContext):
    if not message.text or len(message.text) > 100:
        await message.answer("Напиши название профессии (до 100 символов).")
        return

    await state.update_data(profession=message.text)
    await state.set_state(MissingSkillsForm.level)

    await message.answer(
        "Вопрос 3 из 3.\n"
        "Как ты оцениваешь свои знания в этой сфере?",
        reply_markup=create_keyboard([
            "Пока ничего не знаю",
            "Знаю основы",
            "Уже имею опыт"
        ])
    )


# Вопрос 3 и результат
@dp.message(MissingSkillsForm.level)
async def get_missing_level(message: Message, state: FSMContext):
    options = [
        "Пока ничего не знаю",
        "Знаю основы",
        "Уже имею опыт"
    ]

    if message.text not in options:
        await message.answer("Выбери один из предложенных вариантов.")
        return

    await state.update_data(level=message.text)
    data = await state.get_data()

    skill_map = {
        "IT и технологии": [
            "Основы программирования",
            "Работа с базами данных",
            "Английский язык",
            "Решение технических задач"
        ],
        "Бизнес и экономика": [
            "Финансовая грамотность",
            "Анализ данных",
            "Коммуникация и переговоры",
            "Управление проектами"
        ],
        "Дизайн и творчество": [
            "Основы композиции",
            "Работа с графическими инструментами",
            "Визуальное мышление",
            "Создание портфолио"
        ],
        "Работа с людьми": [
            "Эффективная коммуникация",
            "Эмпатия",
            "Решение конфликтов",
            "Публичные выступления"
        ]
    }

    skills = skill_map[data["direction"]]

    if data["level"] == "Пока ничего не знаю":
        priority = skills
    elif data["level"] == "Знаю основы":
        priority = skills[:3]
    else:
        priority = skills[1:]

    result = "\n".join(
        f"• {skill}" for skill in priority
    )

    await message.answer(
        "🎯 Анализ завершён!\n\n"
        f"Желаемая профессия: {data['profession']}\n"
        f"Сфера: {data['direction']}\n"
        f"Твой уровень: {data['level']}\n\n"
        "📚 Навыки, которые стоит изучить:\n"
        f"{result}\n\n"
        "💡 Совет: начни с одного навыка и постепенно "
        "переходи к следующему.\n\n"
        "Это предварительный список для выбранной сферы.",
        reply_markup=menu
    )

    await state.clear()

# Начало создания карьерного плана
@dp.message(F.text == "🧭 Карьерный план")
async def career_plan(message: Message, state: FSMContext):
    await state.set_state(CareerPlanForm.direction)

    await message.answer(
        "🗺 Давай построим твой карьерный план!\n\n"
        "В какой сфере ты хочешь развиваться?",
        reply_markup=create_keyboard([
            "IT и технологии",
            "Бизнес и экономика",
            "Дизайн и творчество",
            "Работа с людьми"
        ])
    )
# Вопрос 1
@dp.message(CareerPlanForm.direction)
async def get_career_direction(message: Message, state: FSMContext):
    options = [
        "IT и технологии",
        "Бизнес и экономика",
        "Дизайн и творчество",
        "Работа с людьми"
    ]

    if message.text not in options:
        await message.answer("Выбери один из предложенных вариантов.")
        return

    await state.update_data(direction=message.text)
    await state.set_state(CareerPlanForm.profession)

    await message.answer(
        "Какую профессию ты хочешь освоить?\n"
        "Напиши название своими словами."
    )


# Вопрос 2
@dp.message(CareerPlanForm.profession)
async def get_career_profession(message: Message, state: FSMContext):
    if not message.text or len(message.text) > 100:
        await message.answer("Напиши название профессии (до 100 символов).")
        return

    await state.update_data(profession=message.text)
    await state.set_state(CareerPlanForm.time)

    await message.answer(
        "Сколько времени в неделю ты готов уделять обучению?",
        reply_markup=create_keyboard([
            "1–3 часа",
            "4–6 часов",
            "7–10 часов"
        ])
    )

# Вопрос 3 и готовый план
@dp.message(CareerPlanForm.time)
async def get_career_time(message: Message, state: FSMContext):
    options = [
        "1–3 часа",
        "4–6 часов",
        "7–10 часов"
    ]

    if message.text not in options:
        await message.answer("Выбери один из предложенных вариантов.")
        return

    await state.update_data(time=message.text)
    data = await state.get_data()

    plans = {
        "IT и технологии": [
            "Неделя 1: изучить основы программирования и цифровой грамотности.",
            "Неделя 2: пройти вводный урок по выбранному языку программирования.",
            "Неделя 3: выполнить небольшой практический проект.",
            "Неделя 4: оформить проект и оценить, что получилось."
        ],
        "Бизнес и экономика": [
            "Неделя 1: изучить основы экономики и финансовой грамотности.",
            "Неделя 2: познакомиться с анализом рынка и данных.",
            "Неделя 3: разобрать пример бизнес-проекта.",
            "Неделя 4: придумать собственную бизнес-идею и представить её."
        ],
        "Дизайн и творчество": [
            "Неделя 1: изучить основы композиции и цвета.",
            "Неделя 2: познакомиться с инструментами дизайна.",
            "Неделя 3: создать первый дизайн-проект.",
            "Неделя 4: собрать небольшое портфолио."
        ],
        "Работа с людьми": [
            "Неделя 1: изучить основы коммуникации.",
            "Неделя 2: потренировать навыки общения и активного слушания.",
            "Неделя 3: изучить командную работу и решение конфликтов.",
            "Неделя 4: подготовить небольшое выступление или проект."
        ]
    }

    plan = "\n\n".join(plans[data["direction"]])

    await message.answer(
        "🎉 Твой карьерный план готов!\n\n"
        f"🎯 Желаемая профессия: {data['profession']}\n"
        f"🌐 Сфера: {data['direction']}\n"
        f"⏰ Время на обучение: {data['time']} в неделю\n\n"
        "📅 ТВОЙ ПЛАН НА 4 НЕДЕЛИ:\n\n"
        f"{plan}\n\n"
        "💡 Совет: выполняй задания постепенно и "
        "отмечай свой прогресс. План можно адаптировать "
        "под твои интересы и уровень знаний.",
        reply_markup=menu
    )

    await state.clear()
async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())

