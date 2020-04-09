import requests
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, RegexHandler, ConversationHandler)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

path = 'https://pokeapi.co/api/v2/'
STATE1 = 1
STATE2 = 2
pokemon = ''

# mensagem de inicio


def start(update, context):
    try:
        message = """Olá, treinador! 
                            \nDitige o nome ou o cógido do pokémon: """
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        update.message.reply_text(
            message, reply_markup=ReplyKeyboardMarkup([], one_time_keyboard=True))
        return STATE1
    except Exception as e:
        print(str(e))


def isPokemon(update, context):
    data = update.message.text
    print(data)
    if len(data) < 1:
        message = """Dado inválido. Por favor, ditige o nome ou o cógido do pokémon: """
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=message)
        return STATE1
    else:
        pokemon = data
        return STATE2


def searchPokemon(update, context):
    data = requests.get(path+ pokemon)
    print(data)

# cancelando bot e dando tchau
def close(update, context):
    message = "Tchau, treinador!"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    return ConversationHandler.END

# main
def main():
   
    myToken = ''
    # config
    updater = Updater(token=myToken, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    # opções de conversas
    conversation_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CommandHandler('close', close)
        ],
        states={
            STATE1: [MessageHandler(Filters.text, isPokemon)],
            STATE2: [MessageHandler(Filters.text, searchPokemon)],
        },
        fallbacks=[CommandHandler('close', close)])

    # iniciando
    updater.dispatcher.add_handler(conversation_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
