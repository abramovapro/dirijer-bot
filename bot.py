"""
Бот «Дирижёр» — приём заявок от экспертов
Юлия Абрамова | продюсер онлайн-запусков
python-telegram-bot 20.x
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ConversationHandler, ContextTypes
)

# ═══════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════
BOT_TOKEN      = "8720204374:AAF_VjXBdq1pBYfbJFo-4UuyVcth2pr2bRI"
ADMIN_CHAT_ID  = 346125335
ADMIN_USERNAME = "@abramova_juli"
# ═══════════════════════════════════════

logging.basicConfig(level=logging.INFO)

# ─── Состояния диалога ───────────────────────────────────────────
(WAITING_START, Q1_NAME, Q2_PROFESSION, Q3_INCOME, Q4_GOAL,
 Q5_STRENGTHS, Q6_TEACH, Q7_SEGMENT, Q7_SEG_DET, Q8_SOCIAL,
 Q9_ONLINE, Q9_ONLINE_DET, Q10_TIME, Q11_BUDGET, Q12_WHY,
 Q13_PRIORITY) = range(16)


def kb(*rows):
    return InlineKeyboardMarkup([[InlineKeyboardButton(t, callback_data=d)] for t, d in rows])


# ═══════════════════════════════════════
# СЕРВИСНЫЕ КОМАНДЫ
# ═══════════════════════════════════════
async def get_my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Твой ID: {update.effective_chat.id}")


# ═══════════════════════════════════════
# БЛОК 0 — СТАРТ
# ═══════════════════════════════════════
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
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
    return WAITING_START


async def cb_start_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(
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
    return WAITING_START


async def cb_start_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(
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
    return WAITING_START


async def cb_start_yes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(
        "Блок 1 из 5 — Базовая информация\n\n"
        "Вопрос 1 / 13\n\n"
        "Как тебя зовут? (имя и фамилия)"
    )
    return Q1_NAME


# ═══════════════════════════════════════
# БЛОК 1 — БАЗОВАЯ ИНФОРМАЦИЯ
# ═══════════════════════════════════════
async def q1_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    context.user_data["name"] = name
    await update.message.reply_text(
        f"Отлично, {name}! 👍\n\n"
        f"Вопрос 2 / 13\n\n"
        f"Чем ты занимаешься и сколько лет ты в этой профессии?\n\n"
        f"Расскажи в свободной форме — как есть."
    )
    return Q2_PROFESSION


async def q2_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["profession"] = update.message.text.strip()
    await update.message.reply_text(
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
    return Q3_INCOME


async def q3_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    labels = {"inc_1": "до 50 000 ₽", "inc_2": "50 000 – 100 000 ₽",
              "inc_3": "100 000 – 200 000 ₽", "inc_4": "200 000 – 400 000 ₽",
              "inc_5": "от 400 000 ₽"}
    context.user_data["income"] = labels[q.data]
    await q.edit_message_text(
        "Вопрос 4 / 13\n\n"
        "А к какому доходу хочешь прийти — и за какой срок?\n\n"
        "Напиши цифру и период. Например: «300 000 за 6 месяцев»."
    )
    return Q4_GOAL


async def q4_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["goal"] = update.message.text.strip()
    await update.message.reply_text(
        "Блок 2 из 5 — Экспертиза\n\n"
        "Вопрос 5 / 13\n\n"
        "В чём ты сильнее большинства коллег? "
        "Что у тебя получается лучше всего — и что клиенты ценят больше всего?"
    )
    return Q5_STRENGTHS


# ═══════════════════════════════════════
# БЛОК 2 — ЭКСПЕРТИЗА
# ═══════════════════════════════════════
async def q5_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["strengths"] = update.message.text.strip()
    await update.message.reply_text(
        "Вопрос 6 / 13\n\n"
        "Говорили ли тебе, что тебе стоит учить других или что ты хорошо объясняешь?",
        reply_markup=kb(
            ("Да, часто слышу это", "teach_1"),
            ("Иногда говорят", "teach_2"),
            ("Нет, пока не слышал(а)", "teach_3"),
            ("Уже обучаю учеников", "teach_4"),
        )
    )
    return Q6_TEACH


async def q6_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    labels = {"teach_1": "Да, часто слышу это", "teach_2": "Иногда говорят",
              "teach_3": "Нет, пока не слышал(а)", "teach_4": "Уже обучаю учеников"}
    context.user_data["teach"] = labels[q.data]
    await q.edit_message_text(
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
    return Q7_SEGMENT


async def q7_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    labels = {"seg_vip": "Да, работаю с vip / премиум",
              "seg_narrow": "Да, есть узкая специализация",
              "seg_wide": "Нет, работаю с широкой аудиторией",
              "seg_none": "Пока не определился(ась)"}
    context.user_data["segment"] = labels[q.data]
    if q.data in ("seg_vip", "seg_narrow"):
        await q.edit_message_text(
            "Расскажи подробнее — кто эти клиенты и чем твоя работа с ними отличается?"
        )
        return Q7_SEG_DET
    else:
        context.user_data["segment_detail"] = "—"
        await q.edit_message_text(
            "Блок 3 из 5 — Онлайн и соцсети\n\n"
            "Вопрос 8 / 13\n\n"
            "Какие соцсети ты ведёшь и сколько там подписчиков?\n\n"
            "Напиши в свободной форме. Например: «Телеграм — 500, Инстаграм — 1200»."
        )
        return Q8_SOCIAL


async def q7_det_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["segment_detail"] = update.message.text.strip()
    await update.message.reply_text(
        "Блок 3 из 5 — Онлайн и соцсети\n\n"
        "Вопрос 8 / 13\n\n"
        "Какие соцсети ты ведёшь и сколько там подписчиков?\n\n"
        "Напиши в свободной форме. Например: «Телеграм — 500, Инстаграм — 1200»."
    )
    return Q8_SOCIAL


# ═══════════════════════════════════════
# БЛОК 3 — ОНЛАЙН И СОЦСЕТИ
# ═══════════════════════════════════════
async def q8_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["social"] = update.message.text.strip()
    await update.message.reply_text(
        "Вопрос 9 / 13\n\n"
        "Был ли у тебя опыт онлайн-продаж — курсы, консультации, мастер-классы?",
        reply_markup=kb(
            ("Да, продавал(а) онлайн — есть опыт", "online_yes"),
            ("Пробовал(а), но не пошло", "online_fail"),
            ("Нет, это будет первый раз", "online_no"),
            ("Сейчас продаю онлайн, хочу масштаб", "online_scale"),
        )
    )
    return Q9_ONLINE


async def q9_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    labels = {"online_yes": "Да, продавал(а) онлайн — есть опыт",
              "online_fail": "Пробовал(а), но не пошло",
              "online_no": "Нет, это будет первый раз",
              "online_scale": "Сейчас продаю онлайн, хочу масштаб"}
    context.user_data["online_exp"] = labels[q.data]
    if q.data in ("online_yes", "online_fail"):
        await q.edit_message_text(
            "Что продавал(а) и что сработало / не сработало? Расскажи коротко."
        )
        return Q9_ONLINE_DET
    else:
        context.user_data["online_detail"] = "—"
        await q.edit_message_text(
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
        return Q10_TIME


async def q9_det_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["online_detail"] = update.message.text.strip()
    await update.message.reply_text(
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
    return Q10_TIME


# ═══════════════════════════════════════
# БЛОК 4 — РЕСУРСЫ
# ═══════════════════════════════════════
async def q10_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    labels = {"time_1": "До 3 часов в неделю", "time_2": "3–7 часов в неделю",
              "time_3": "7–15 часов в неделю", "time_4": "Готов(а) погружаться полностью"}
    context.user_data["time_per_week"] = labels[q.data]
    await q.edit_message_text(
        "Вопрос 11 / 13\n\n"
        "Есть ли стартовый бюджет на развитие проекта?",
        reply_markup=kb(
            ("Пока без вложений", "bud_0"),
            ("До 30 000 ₽", "bud_1"),
            ("30 000 – 100 000 ₽", "bud_2"),
            ("От 100 000 ₽", "bud_3"),
        )
    )
    return Q11_BUDGET


async def q11_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    labels = {"bud_0": "Пока без вложений", "bud_1": "До 30 000 ₽",
              "bud_2": "30 000 – 100 000 ₽", "bud_3": "От 100 000 ₽"}
    context.user_data["budget"] = labels[q.data]
    await q.edit_message_text(
        "Блок 5 из 5 — Мотивация\n\n"
        "Вопрос 12 / 13\n\n"
        "Почему ты хочешь масштабироваться именно сейчас? Что подтолкнуло?"
    )
    return Q12_WHY


# ═══════════════════════════════════════
# БЛОК 5 — МОТИВАЦИЯ
# ═══════════════════════════════════════
async def q12_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["why_now"] = update.message.text.strip()
    await update.message.reply_text(
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
    return Q13_PRIORITY


async def q13_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    labels = {"pri_money": "Больше денег", "pri_freedom": "Свобода и гибкий график",
              "pri_influence": "Влияние и аудитория", "pri_fame": "Признание в профессии",
              "pri_all": "Всё вместе"}
    context.user_data["priority"] = labels[q.data]
    d = context.user_data
    name = d.get("name", "Эксперт")

    # ─── Финальное сообщение пользователю ───────────────────────
    await q.edit_message_text(
        f"{name}, спасибо! 🎼\n\n"
        f"Твои ответы отправлены Юлии.\n\n"
        f"Она изучит их и свяжется с тобой в течение 1–2 рабочих дней.\n\n"
        f"Если хочешь — можешь написать ей напрямую:\n"
        f"👉 {ADMIN_USERNAME}\n\n"
        f"До скорого! 🤝"
    )

    # ─── Уведомление Юлии ───────────────────────────────────────
    user = q.from_user
    summary = (
        f"🎼 НОВАЯ ЗАЯВКА ОТ ЭКСПЕРТА\n\n"
        f"Имя: {d.get('name', '—')}\n"
        f"Профессия и опыт: {d.get('profession', '—')}\n"
        f"Текущий доход: {d.get('income', '—')}\n"
        f"Цель: {d.get('goal', '—')}\n"
        f"Сильные стороны: {d.get('strengths', '—')}\n"
        f"Обучение: {d.get('teach', '—')}\n"
        f"Сегмент: {d.get('segment', '—')}\n"
        f"Детали сегмента: {d.get('segment_detail', '—')}\n"
        f"Соцсети: {d.get('social', '—')}\n"
        f"Опыт онлайн: {d.get('online_exp', '—')}\n"
        f"Детали онлайн: {d.get('online_detail', '—')}\n"
        f"Время в неделю: {d.get('time_per_week', '—')}\n"
        f"Бюджет: {d.get('budget', '—')}\n"
        f"Мотивация: {d.get('why_now', '—')}\n"
        f"Приоритет: {d.get('priority', '—')}\n\n"
        f"→ @{user.username or '—'} | {user.full_name}"
    )
    try:
        await context.bot.send_message(ADMIN_CHAT_ID, summary)
    except Exception as e:
        logging.error(f"Ошибка отправки уведомления: {e}")

    return ConversationHandler.END


# ═══════════════════════════════════════
# ЗАПУСК
# ═══════════════════════════════════════
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WAITING_START: [
                CallbackQueryHandler(cb_start_info, pattern="^start_info$"),
                CallbackQueryHandler(cb_start_back, pattern="^start_back$"),
                CallbackQueryHandler(cb_start_yes,  pattern="^start_yes$"),
            ],
            Q1_NAME:       [MessageHandler(filters.TEXT & ~filters.COMMAND, q1_handler)],
            Q2_PROFESSION: [MessageHandler(filters.TEXT & ~filters.COMMAND, q2_handler)],
            Q3_INCOME:     [CallbackQueryHandler(q3_handler, pattern="^inc_")],
            Q4_GOAL:       [MessageHandler(filters.TEXT & ~filters.COMMAND, q4_handler)],
            Q5_STRENGTHS:  [MessageHandler(filters.TEXT & ~filters.COMMAND, q5_handler)],
            Q6_TEACH:      [CallbackQueryHandler(q6_handler, pattern="^teach_")],
            Q7_SEGMENT:    [CallbackQueryHandler(q7_handler, pattern="^seg_")],
            Q7_SEG_DET:    [MessageHandler(filters.TEXT & ~filters.COMMAND, q7_det_handler)],
            Q8_SOCIAL:     [MessageHandler(filters.TEXT & ~filters.COMMAND, q8_handler)],
            Q9_ONLINE:     [CallbackQueryHandler(q9_handler, pattern="^online_")],
            Q9_ONLINE_DET: [MessageHandler(filters.TEXT & ~filters.COMMAND, q9_det_handler)],
            Q10_TIME:      [CallbackQueryHandler(q10_handler, pattern="^time_")],
            Q11_BUDGET:    [CallbackQueryHandler(q11_handler, pattern="^bud_")],
            Q12_WHY:       [MessageHandler(filters.TEXT & ~filters.COMMAND, q12_handler)],
            Q13_PRIORITY:  [CallbackQueryHandler(q13_handler, pattern="^pri_")],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    app.add_handler(CommandHandler("id", get_my_id))
    app.add_handler(conv)
    app.run_polling()


if __name__ == "__main__":
    main()
