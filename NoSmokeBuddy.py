from datetime import datetime
# Берём инструмент для работы с датой и временем.

from telegram import Update
# Берём объект, через который Telegram передаёт сообщения боту.

from telegram.ext import Application, CommandHandler, ContextTypes

# Берём инструменты для создания бота: запуск, обработка команд, обработка сообщений, фильтры.

TELEGRAM_BOT_TOKEN = "8139998528:AAFka51sXJ6j2uSGCaFYO6obYzD2n6YUQ2o"

START_DATE_STR = "06-12-2025"  # дата, когда ты бросил курить (день-месяц-год)

CIGS_PER_PACK = 20  # сколько сигарет в пачке
CIGS_PER_DAY = 7  # сколько ты раньше курил в день
PACK_COST = 1100  # цена пачки в тенге
CURRENCY = "KZT"  # валюта для вывода

# превращаем строку с датой в настоящий объект datetime
START_DATE = datetime.strptime(START_DATE_STR, "%d-%m-%Y")


def calculate_progress():
    """
    - сколько дней / часов / минут прошло с момента отказа
    - сколько сигарет не выкурено
    - сколько денег сэкономлено
    """

    now = datetime.now()  # текущий момент времени
    delta = now - START_DATE  # разница между сейчас и датой отказа
    total_seconds = int(delta.total_seconds())  # сколько всего секунд прошло

    if total_seconds < 0:  # если дата в будущем
        return None, None, None, None, None  # сигнал: данные некорректны

    days = delta.days  # полные дни
    total_hours = total_seconds // 3600  # полные часы
    minutes = (total_seconds % 3600) // 60  # оставшиеся минуты

    cigs_per_hour = CIGS_PER_DAY / 24  # сигарет в среднем в час
    cigs_saved = round(total_hours * cigs_per_hour)  # не выкуренные сигареты

    price_per_cig = PACK_COST / CIGS_PER_PACK  # цена одной сигареты
    money_saved = round(cigs_saved * price_per_cig, 2)  # сэкономленные деньги

    return days, total_hours, minutes, cigs_saved, money_saved
    # возвращаем: дни, часы, минуты, сигареты, деньги


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Считаем прогресс
    days, hours, minutes, cigs_saved, money_saved = calculate_progress()

    # Если дата стоит в будущем
    if days is None:
        await  update.message.reply_text(
            "Похоже, дата начала стоит в будущем. Проверь START_DATE_STR в коде."
        )
        return

    # Форматируем текст ответа
    text = (
        "Привет! Я No Smoke Buddy. Скажи сигаретам нет.\n\n"
        f"Ты не куришь: {days} дней, {hours % 24} часов, {minutes} минут. \n"
        f"Сигарет НЕ выкурено: {cigs_saved}.\n"
        f"Сэкономлено денег: {money_saved} {CURRENCY}.\n\n"
        f"Хочется курить? Понимаю. Но это пройдет. Будь сильным."
    )

    # Отправляем ответ пользователю
    await  update.message.reply_text(text)


if __name__ == "__main__":
    # создаем приложение бота
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # регистрируем команду /start
    app.add_handler(CommandHandler("start", start))

    print("Бот запущен. Нажми Ctrl+C, чтобы остановить. Но стоит ли :)")
    app.run_polling()
