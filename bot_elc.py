# -*- coding: utf-8 -*-
import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Получаем токен из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("Токен бота не найден в переменных окружения!")

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Создаем постоянную клавиатуру меню
def get_main_keyboard():
    keyboard = [
        [KeyboardButton("Билеты/пожертвования")],
        [KeyboardButton("Посещение концертов")],
        [KeyboardButton("Дата и время концертов")],
        [KeyboardButton("Приём в церковный хор")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        'Добро пожаловать! Я бот Евангелическо-лютеранской церкви св. Екатерины (г. Казань).\n'
        'Используйте кнопки меню ниже для получения информации:'
    )
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_keyboard()
    )

# Обработчик нажатий на кнопки меню
async def handle_menu_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    if user_text == "Посещение концертов":
        response_text = "<b>Регистрации на наши концерты нет.</b>\nКак правило, все наши концерты длятся час с небольшим. Двери в зал открываются за 30-40 минут до начала концерта. \nСтрогого дресс-кода у нас нет, мы лишь просим мужчин при входе в церковь снимать головные уборы, женщины могут быть как в юбке, так и в брюках, им головной убор необязателен. \nФото- и видео-съёмку мы разрешаем. \n\nПомните, это действующая церковь, нам важно сохранить приятную и спокойную атмосферу. \n\nПроведение концертов — многовековая традиция, открывающая всем желающим, вне зависимости от убеждений и взглядов, возможность познакомиться с живой музыкальной культурой, активно развивающейся и сохраняющейся."
        # Отправляем с HTML разметкой
        await update.message.reply_text(
            response_text,
            parse_mode='HTML',
            reply_markup=get_main_keyboard()
        )   

    elif user_text == "Дата и время концертов":
        response_text = "Концерты в нашей церкви проводятся регулярно каждую <b>субботу и воскресенье в 18:00.</b> Афиша на месяц публикуется в последнюю неделю предыдущего месяца. \n\n<b>С более подробным расписанием концертов вы можете ознакомиться в наших группах:</b> \nТелеграм — https://t.me/organ_kazan\nВКонтакте — https://vk.ru/organkazan"
        # Отправляем с HTML разметкой
        await update.message.reply_text(
            response_text,
            parse_mode='HTML',
            reply_markup=get_main_keyboard()
        )   

    elif user_text == "Билеты/пожертвования":
        response_text = "<b>Регистрации на наши концерты нет.</b>\n\nБилеты мы не продаём, но у нас принимаются пожертвования. Вы можете внести пожертвования за концерт наличными средствами или переводом непосредственно на входе перед началом концерта. На входе Вас сориентируют.\n\nРекомендуемый размер пожертвований: \nВходной - 600 рублей.\nЛьготный (школьники, студенты, пенсионеры, инвалиды) - 400 рублей. \n\nВаши пожертвования будут направлены на уставную деятельность общины и поддержку музыкального служения."
        # Отправляем с HTML разметкой
        await update.message.reply_text(
            response_text,
            parse_mode='HTML',
            reply_markup=get_main_keyboard()
        )    

    elif user_text == "Приём в церковный хор":
        response_text = "По вопросам приёма в хор пишите кантору церкви Н. Кошелю в телеграме: @Katharinenkirche."
        await update.message.reply_text(
            response_text,
            reply_markup=get_main_keyboard()
        )

    else:
        # Если получен любой другой текст
        response_text = "Пожалуйста, используйте кнопки меню ниже для получения информации."
        await update.message.reply_text(
            response_text,
            reply_markup=get_main_keyboard()
        )
    

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/help - Получить справку\n\n"
        "Бот предоставляет информацию о:\n"
        "• Дате и времени концертов\n"
        "• Правилах посещения концертов\n"
        "• Билетах и пожертвованиях\n"
        "• Наборе в церковный хор"
    )
    await update.message.reply_text(
        help_text,
        reply_markup=get_main_keyboard()
    )

# Обработчик для любых текстовых сообщений
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Если это не команда и не кнопка меню, показываем меню
    if update.message.text:
        response_text = "Пожалуйста, используйте кнопки меню ниже для получения информации."
        await update.message.reply_text(
            response_text,
            reply_markup=get_main_keyboard()
        )

# Основная функция
def main():
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Регистрируем обработчики команд
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    
    # Регистрируем обработчик для кнопок меню (точное соответствие тексту кнопок)
    application.add_handler(MessageHandler(
        filters.TEXT & filters.Regex(r'^(Билеты/пожертвования|Посещение концертов|Дата и время концертов|Приём в церковный хор)$'),
        handle_menu_buttons
    ))
    
    # Регистрируем обработчик для всех остальных текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # Запускаем бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
