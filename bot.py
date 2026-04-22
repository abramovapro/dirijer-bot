"""
Бот «Дирижёр» — приём заявок от экспертов
Юлия Абрамова | продюсер онлайн-запусков
aiogram 2.x
"""

import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# ═══════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════
BOT_TOKEN     = "8720204374:AAF_VjXBdq1pBYfbJFo-4UuyVcth2pr2bRI"
ADMIN_CHAT_ID = 346125335
ADMIN_USERNAME = "@abramova_juli"
# ═══════════════════════════════════════

logging.basicConfig(level=logging.INFO)

bot     = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp      = Dispatcher(bot, storage=storage)


# ─────────────────────────────────────────
# FSM — шаги анкеты
# ─────────────────────────────────────────
class Form(StatesGroup):
    q1_name        = State()
    q2_profession  = State()
    q3_income      = State()
    q4_goal        = State()
    q5_strengths   = State()
    q6_teach       = State()
    q7_segment     = State()
    q7_segment_det = State()
    q8_social      = State()
    q9_online      = State()
    q9_online_det  = State()
    q10_time       = State()
    q11_budget     = State()
    q12_why        = State()
    q13_priority   = State()


# ─────────────────────────────────────────
# Вспомогательная функция: клавиатура
# ─────────────────────────────────────────
def kb(*buttons):
    markup = InlineKeyboardMarkup(row_width=1)
    for text, data in buttons:
        markup.add(InlineKeyboardButton(text=text, callback_data=data))
    return markup


# ═══════════════════════════════════════
# БЛОК 0 — СТАРТ
# ═══════════════════════════════════════
@dp.message_handler(commands=["start"], state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "Привет! 👋\n\n"
        "Я — бот Юлии Абрамовой, продюсера онлайн-запусков.\n\n"
        "Юлия — Дирижёр. Она не исполнитель — она выстраивает систему вокруг эксперта, "
        "чтобы бизнес рос без выгорания.\n\n"
        "Если ты эксперт и думаешь о масштабировании в онлайн — ты попал(а) по адресу.\n\n"
        "Сейчас я задам тебе несколько вопросов. Это займёт 7–10 минут. "
        "На основе твоих ответов Юлия сделает первичный анализ и свяжется с тобой.\n\n"
        "Готов(а) начать?",
        reply_markup=kb(
            ("✅ Да, начинаем", "start_yes"),
            ("❓ Расскажи подробнее о работе с Юлией", "start_info"),
        )
    )


@dp.callback_query_handler(lambda c: c.data == "start_info", state="*")
async def cb_start_info(cq: types.CallbackQuery):
    await cq.message.edit_text(
        "Юлия работает с экспертами из мягких ниш — красота, здоровье, творчество, "
        "образование, психология, коучинг.\n\n"
        "Она берёт в работу действующих мастеров, у которых уже есть опыт и клиенты — "
        "но рост застрял.\n\n"
        "Что Юлия делает:\n"
        "→ Распаковывает твою экспертность и находит точку отличия\n"
        "→ Выстраивает продуктовую линейку под твои цели\n"
        "→ Составляет финансовую модель и план запуска\n"
        "→ Ведёт проект от стратегии до первых продаж\n\n"
        "Формат: проектная работа. Без хаоса, без выгорания.\n\n"
        "Готов(а) оставить заявку?",
        reply_markup=kb(
            ("✅ Да, поехали", "start_yes"),
            ("🔙 Назад", "start_back"),
        )
    )
    await cq.answer()


@dp.callback_query_handler(lambda c: c.data == "start_back", state="*")
async def cb_start_back(cq: types.CallbackQuery):
    await cq.message.edit_text(
        "Привет! 👋\n\n"
        "Я — бот Юлии Абрамовой, продюсера онлайн-запусков.\n\n"
        "Юлия — Дирижёр. Она не исполнитель — она выстраивает систему вокруг эксперта, "
        "чтобы бизнес рос без выгорания.\n\n"
        "Готов(а) начать?",
        reply_markup=kb(
            ("✅ Да, начинаем", "start_yes"),
            ("❓ Расскажи подробнее о работе с Юлией", "start_info"),
        )
    )
    await cq.answer()


@dp.callback_query_handler(lambda c: c.data == "start_yes", state="*")
async def cb_start_yes(cq: types.CallbackQuery):
    await Form.q1_name.set()
    await cq.message.edit_text(
        "Блок 1 из 5 — Базовая информация\n\n"
        "Вопрос 1 / 13\n\n"
        "Как тебя зовут? (имя и фамилия)"
    )
    await cq.answer()


# ═══════════════════════════════════════
# БЛОК 1 — БАЗОВАЯ ИНФОРМАЦИЯ
# ═══════════════════════════════════════
@dp.message_handler(state=Form.q1_name)
async def q1_handler(message: types.Message, state: FSMContext):
    name = message.text.strip()
    await state.update_data(name=name)
    await Form.q2_profession.set()
    await message.answer(
        f"Отлично, {name}! 👍\n\n"
        f"Вопрос 2 / 13\n\n"
        f"Чем ты занимаешься и сколько лет ты в этой профессии?\n\n"
        f"Расскажи в свободной форме — как есть."
    )


@dp.message_handler(state=Form.q2_profession)
async def q2_handler(message: types.Message, state: FSMContext):
    await state.update_data(profession=message.text.strip())
    await Form.q3_income.set()
    await message.answer(
        "Вопрос 3 / 13\n\n"
        "Какой у тебя сейчас примерный доход в месяц?",
        reply_markup=kb(
            ("до 50 000 ₽", "inc_1"),
            ("50 000 – 100 000 ₽", "inc_2"),
            ("100 000 – 200 000 ₽", "inc_3"),
            ("200 000 – 400 000 ₽", "inc_4"),
            ("от 400 000 ₽", "inc_5"),
        )
    )


@dp.callback_query_handler(lambda c: c.data.startswith("inc_"), state=Form.q3_income)
async def q3_handler(cq: types.CallbackQuery, state: FSMContext):
    labels = {
        "inc_1": "до 50 000 ₽",
        "inc_2": "50 000 – 100 000 ₽",
        "inc_3": "100 000 – 200 000 ₽",
        "inc_4": "200 000 – 400 000 ₽",
        "inc_5": "от 400 000 ₽",
    }
    await state.update_data(income=labels[cq.data])
    await Form.q4_goal.set()
    await cq.message.edit_text(
        "Вопрос 4 / 13\n\n"
        "А к какому доходу хочешь прийти — и за какой срок?\n\n"
        "Напиши цифру и период. Например: «300 000 за 6 месяцев»."
    )
    await cq.answer()


@dp.message_handler(state=Form.q4_goal)
async def q4_handler(message: types.Message, state: FSMContext):
    await state.update_data(goal=message.text.strip())
    await Form.q5_strengths.set()
    await message.answer(
        "Блок 2 из 5 — Экспертиза\n\n"
        "Вопрос 5 / 13\n\n"
        "В чём ты сильнее большинства коллег? "
        "Что у тебя получается лучше всего — и что клиенты ценят больше всего?"
    )


# ═══════════════════════════════════════
# БЛОК 2 — ЭКСПЕРТИЗА
# ═══════════════════════════════════════
@dp.message_handler(state=Form.q5_strengths)
async def q5_handler(message: types.Message, state: FSMContext):
    await state.update_data(strengths=message.text.strip())
    await Form.q6_teach.set()
    await message.answer(
        "Вопрос 6 / 13\n\n"
        "Говорили ли тебе, что тебе стоит учить других или что ты хорошо объясняешь?",
        reply_markup=kb(
            ("Да, часто слышу это", "teach_1"),
            ("Иногда говорят", "teach_2"),
            ("Нет, пока не слышал(а)", "teach_3"),
            ("Уже обучаю учеников", "teach_4"),
        )
    )


@dp.callback_query_handler(lambda c: c.data.startswith("teach_"), state=Form.q6_teach)
async def q6_handler(cq: types.CallbackQuery, state: FSMContext):
    labels = {
        "teach_1": "Да, часто слышу это",
        "teach_2": "Иногда говорят",
        "teach_3": "Нет, пока не слышал(а)",
        "teach_4": "Уже обучаю учеников",
    }
    await state.update_data(teach=labels[cq.data])
    await Form.q7_segment.set()
    await cq.message.edit_text(
        "Вопрос 7 / 13\n\n"
        "Есть ли у тебя особый сегмент клиентов — "
        "например, vip-аудитория, корпоративные, узкая специализация?",
        reply_markup=kb(
            ("Да, работаю с vip / премиум", "seg_vip"),
            ("Да, есть узкая специализация", "seg_narrow"),
            ("Нет, работаю с широкой аудиторией", "seg_wide"),
            ("Пока не определился(ась)", "seg_none"),
        )
    )
    await cq.answer()


@dp.callback_query_handler(lambda c: c.data.startswith("seg_"), state=Form.q7_segment)
async def q7_handler(cq: types.CallbackQuery, state: FSMContext):
    labels = {
        "seg_vip":    "Да, работаю с vip / премиум",
        "seg_narrow": "Да, есть узкая специализация",
        "seg_wide":   "Нет, работаю с широкой аудиторией",
        "seg_none":   "Пока не определился(ась)",
    }
    choice = labels[cq.data]
    await state.update_data(segment=choice)

    if cq.data in ("seg_vip", "seg_narrow"):
        await Form.q7_segment_det.set()
        await cq.message.edit_text(
            "Расскажи подробнее — кто эти клиенты и "
            "чем твоя работа с ними отличается?"
        )
    else:
        await state.update_data(segment_detail="—")
        await Form.q8_social.set()
        await cq.message.edit_text(
            "Блок 3 из 5 — Онлайн и соцсети\n\n"
            "Вопрос 8 / 13\n\n"
            "Какие соцсети ты ведёшь и сколько там подписчиков?\n\n"
            "Напиши в свободной форме. Например: «Телеграм — 500, Инстаграм — 1200»."
        )
    await cq.answer()


@dp.message_handler(state=Form.q7_segment_det)
async def q7_det_handler(message: types.Message, state: FSMContext):
    await state.update_data(segment_detail=message.text.strip())
    await Form.q8_social.set()
    await message.answer(
        "Блок 3 из 5 — Онлайн и соцсети\n\n"
        "Вопрос 8 / 13\n\n"
        "Какие соцсети ты ведёшь и сколько там подписчиков?\n\n"
        "Напиши в свободной форме. Например: «Телеграм — 500, Инстаграм — 1200»."
    )


# ═══════════════════════════════════════
# БЛОК 3 — ОНЛАЙН И СОЦСЕТИ
# ═══════════════════════════════════════
@dp.message_handler(state=Form.q8_social)
async def q8_handler(message: types.Message, state: FSMContext):
    await state.update_data(social=message.text.strip())
    await Form.q9_online.set()
    await message.answer(
        "Вопрос 9 / 13\n\n"
        "Был ли у тебя опыт онлайн-продаж — курсы, консультации, мастер-классы?",
        reply_markup=kb(
            ("Да, продавал(а) онлайн — есть опыт", "online_yes"),
            ("Пробовал(а), но не пошло", "online_fail"),
            ("Нет, это будет первый раз", "online_no"),
            ("Сейчас продаю онлайн, хочу масштаб", "online_scale"),
        )
    )


@dp.callback_query_handler(lambda c: c.data.startswith("online_"), state=Form.q9_online)
async def q9_handler(cq: types.CallbackQuery, state: FSMContext):
    labels = {
        "online_yes":   "Да, продавал(а) онлайн — есть опыт",
        "online_fail":  "Пробовал(а), но не пошло",
        "online_no":    "Нет, это будет первый раз",
        "online_scale": "Сейчас продаю онлайн, хочу масштаб",
    }
    choice = labels[cq.data]
    await state.update_data(online_exp=choice)

    if cq.data in ("online_yes", "online_fail"):
        await Form.q9_online_det.set()
        await cq.message.edit_text(
            "Что продавал(а) и что сработало / не сработало? Расскажи коротко."
        )
    else:
        await state.update_data(online_detail="—")
        await Form.q10_time.set()
        await cq.message.edit_text(
            "Блок 4 из 5 — Ресурсы\n\n"
            "Вопрос 10 / 13\n\n"
            "Сколько часов в неделю ты готов(а) выделять на развитие "
            "онлайн-направления помимо основной работы?",
            reply_markup=kb(
                ("До 3 часов в неделю", "time_1"),
                ("3–7 часов в неделю", "time_2"),
                ("7–15 часов в неделю", "time_3"),
                ("Готов(а) погружаться полностью", "time_4"),
            )
        )
    await cq.answer()


@dp.message_handler(state=Form.q9_online_det)
async def q9_det_handler(message: types.Message, state: FSMContext):
    await state.update_data(online_detail=message.text.strip())
    await Form.q10_time.set()
    await message.answer(
        "Блок 4 из 5 — Ресурсы\n\n"
        "Вопрос 10 / 13\n\n"
        "Сколько часов в неделю ты готов(а) выделять на развитие "
        "онлайн-направления помимо основной работы?",
        reply_markup=kb(
            ("До 3 часов в неделю", "time_1"),
            ("3–7 часов в неделю", "time_2"),
            ("7–15 часов в неделю", "time_3"),
            ("Готов(а) погружаться полностью", "time_4"),
        )
    )


# ═══════════════════════════════════════
# БЛОК 4 — РЕСУРСЫ
# ═══════════════════════════════════════
@dp.callback_query_handler(lambda c: c.data.startswith("time_"), state=Form.q10_time)
async def q10_handler(cq: types.CallbackQuery, state: FSMContext):
    labels = {
        "time_1": "До 3 часов в неделю",
        "time_2": "3–7 часов в неделю",
        "time_3": "7–15 часов в неделю",
        "time_4": "Готов(а) погружаться полностью",
    }
    await state.update_data(time_per_week=labels[cq.data])
    await Form.q11_budget.set()
    await cq.message.edit_text(
        "Вопрос 11 / 13\n\n"
        "Есть ли стартовый бюджет на развитие проекта?",
        reply_markup=kb(
            ("Пока без вложений", "bud_0"),
            ("До 30 000 ₽", "bud_1"),
            ("30 000 – 100 000 ₽", "bud_2"),
            ("От 100 000 ₽", "bud_3"),
        )
    )
    await cq.answer()


@dp.callback_query_handler(lambda c: c.data.startswith("bud_"), state=Form.q11_budget)
async def q11_handler(cq: types.CallbackQuery, state: FSMContext):
    labels = {
        "bud_0": "Пока без вложений",
        "bud_1": "До 30 000 ₽",
        "bud_2": "30 000 – 100 000 ₽",
        "bud_3": "От 100 000 ₽",
    }
    await state.update_data(budget=labels[cq.data])
    await Form.q12_why.set()
    await cq.message.edit_text(
        "Блок 5 из 5 — Мотивация\n\n"
        "Вопрос 12 / 13\n\n"
        "Почему ты хочешь масштабироваться именно сейчас? Что подтолкнуло?"
    )
    await cq.answer()


# ═══════════════════════════════════════
# БЛОК 5 — МОТИВАЦИЯ
# ═══════════════════════════════════════
@dp.message_handler(state=Form.q12_why)
async def q12_handler(message: types.Message, state: FSMContext):
    await state.update_data(why_now=message.text.strip())
    await Form.q13_priority.set()
    await message.answer(
        "Вопрос 13 / 13 — последний! 🎉\n\n"
        "И последнее — что для тебя самое важное в этом проекте?",
        reply_markup=kb(
            ("💰 Больше денег", "pri_money"),
            ("🕊 Свобода и гибкий график", "pri_freedom"),
            ("📣 Влияние и аудитория", "pri_influence"),
            ("🏆 Признание в профессии", "pri_fame"),
            ("✨ Всё вместе", "pri_all"),
        )
    )


@dp.callback_query_handler(lambda c: c.data.startswith("pri_"), state=Form.q13_priority)
async def q13_handler(cq: types.CallbackQuery, state: FSMContext):
    labels = {
        "pri_money":     "Больше денег",
        "pri_freedom":   "Свобода и гибкий график",
        "pri_influence": "Влияние и аудитория",
        "pri_fame":      "Признание в профессии",
        "pri_all":       "Всё вместе",
    }
    await state.update_data(priority=labels[cq.data])
    data = await state.get_data()
    name = data.get("name", "Эксперт")

    # ─── Финальное сообщение пользователю ───────────────────────
    await cq.message.edit_text(
        f"{name}, спасибо! 🎼\n\n"
        f"Твои ответы отправлены Юлии.\n\n"
        f"Она изучит их и свяжется с тобой в течение 1–2 рабочих дней.\n\n"
        f"Если хочешь — можешь написать ей напрямую:\n"
        f"👉 {ADMIN_USERNAME}\n\n"
        f"До скорого! 🤝"
    )

    # ─── Уведомление Юлии ───────────────────────────────────────
    user = cq.from_user
    user_link = f'<a href="tg://user?id={user.id}">{user.full_name}</a>'

    summary = (
        f"🎼 <b>Новая заявка от эксперта</b>\n\n"
        f"<b>Имя:</b> {data.get('name', '—')}\n"
        f"<b>Профессия и опыт:</b> {data.get('profession', '—')}\n"
        f"<b>Текущий доход:</b> {data.get('income', '—')}\n"
        f"<b>Цель:</b> {data.get('goal', '—')}\n"
        f"<b>Сильные стороны:</b> {data.get('strengths', '—')}\n"
        f"<b>Обучение:</b> {data.get('teach', '—')}\n"
        f"<b>Сегмент:</b> {data.get('segment', '—')}\n"
        f"<b>Детали сегмента:</b> {data.get('segment_detail', '—')}\n"
        f"<b>Соцсети:</b> {data.get('social', '—')}\n"
        f"<b>Опыт онлайн:</b> {data.get('online_exp', '—')}\n"
        f"<b>Детали онлайн:</b> {data.get('online_detail', '—')}\n"
        f"<b>Время в неделю:</b> {data.get('time_per_week', '—')}\n"
        f"<b>Бюджет:</b> {data.get('budget', '—')}\n"
        f"<b>Мотивация:</b> {data.get('why_now', '—')}\n"
        f"<b>Приоритет:</b> {data.get('priority', '—')}\n\n"
        f"→ В Telegram: {user_link}\n"
        f"→ @{user.username or '—'}"
    )

    try:
        await bot.send_message(ADMIN_CHAT_ID, summary)
    except Exception as e:
        logging.error(f"Ошибка отправки уведомления: {e}")

    await state.finish()
    await cq.answer()


# ─────────────────────────────────────────
# Запуск
# ─────────────────────────────────────────
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
