import re
from warnings import filterwarnings

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ContextTypes, ConversationHandler, MessageHandler,
                          filters)
from telegram.warnings import PTBUserWarning

import answers
from logger import logger
from service import convert, unknown

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

CURRENT_FROM, CURRENT_TO, VALUE = range(3)

async def start_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"user {update.effective_user.id} - /start")
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=answers.START_ANSWER
    )

async def help_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"user {update.effective_user.id} - /help")
    
    buttons = [
        [InlineKeyboardButton("Начать диалог", callback_data="start")],
        [InlineKeyboardButton("Cписок команд", callback_data="help")],
        [InlineKeyboardButton("Конвертировать валюту", callback_data="convert")],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=answers.HELP_ANSWER, reply_markup=reply_markup
    )

async def button_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    command = query.data
    if command == "start":
        await start_handle(update, context)
    elif command == "help":
        await help_handle(update, context)
    elif command == "convert":
        await start_convert_handle(update, context)
        return CURRENT_FROM

async def start_convert_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"user {update.effective_user.id} - start conversation /convert")

    if update.effective_message:
        await update.effective_message.reply_text(answers.START_CONVERT_ANSWER)
    elif update.callback_query and update.callback_query.message:
        await update.callback_query.message.reply_text(answers.START_CONVERT_ANSWER)
    return CURRENT_FROM

async def get_currency_from(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return ConversationHandler.END
    
    context.user_data['currency_from'] = update.message.text.upper()
    await update.message.reply_text(answers.CURRENCY_FROM_ANSWER)
    return CURRENT_TO

async def get_currency_to(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return ConversationHandler.END
    
    context.user_data['currency_to'] = [
        currency.strip().upper() 
        for currency in update.message.text.replace(",", " ").replace("  ", " ").strip().split()
    ]
    
    await update.message.reply_text(answers.CURRENCY_TO_ANSWER)
    return VALUE

async def get_value(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    if not update.message or not update.message.text:
        return ConversationHandler.END
    
    logger.info(f"user {update.effective_user.id} - conversion /convert {update.message.text, context.user_data['currency_from'], context.user_data['currency_to']}")
    
    try:
        context.user_data['value'] = float(update.message.text)
        answer = await convert(context.user_data['value'], context.user_data['currency_from'], context.user_data['currency_to'])
        await update.message.reply_text(answer)
    except Exception:
        await update.message.reply_text("Некорректное значение суммы.")
    finally:
        return ConversationHandler.END

async def cancel_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return ConversationHandler.END

async def convert_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"user {update.effective_user.id} - /convert {" ".join(context.args) if context.args else ""}")
    try:
        value = float(context.args[0])
    except Exception:
        logger.info(f"user {update.effective_user.id} - error value type - {context.args}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=answers.ERROR_INPUT_FORMAT_ANSWER
        )
        return

    if context.args[2].lower() != "to":
        logger.info(f"user {update.effective_user.id} - error input format - {context.args}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=answers.ERROR_INPUT_FORMAT_ANSWER
        )
        return

    base = context.args[1].upper()
    targets = [
        word.upper()
        for currency in context.args[3:]
        for word in currency.replace(",", " ").replace("  ", " ").strip().split()
    ]

    answer = await convert(value, base, targets)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)

async def unknown_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = await unknown(update.message.text.lower())

    if answer == answers.GREETINGS_ANSWER:
        logger.info(f"user {update.effective_user.id} - Greetings")
    elif answer == answers.GOODBYE_ANSWER:
        logger.info(f"user {update.effective_user.id} - Goodbye")
    else:
        logger.info(f"user {update.effective_user.id} - Unknown command")
        
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=answer
    )

def add_handlers(application: Application):
    application.add_handler(CommandHandler("start", start_handle))
    application.add_handler(CommandHandler("help", help_handle))
    
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("convert", start_convert_handle, has_args=False), CallbackQueryHandler(button_handle, pattern=re.compile(r'^convert$'))],
        states={
            CURRENT_FROM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_currency_from)],
            CURRENT_TO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_currency_to)],
            VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_value)],
        },
        fallbacks=[CommandHandler('cancel', cancel_handle)],
    )

    application.add_handler(conversation_handler)
    application.add_handler(CallbackQueryHandler(button_handle, pattern=re.compile(r'^(?!convert$).*$')))
    application.add_handler(CommandHandler("convert", convert_handle))
    application.add_handler(MessageHandler(filters.ALL, unknown_handle))
