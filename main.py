import requests
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, RegexHandler, ConversationHandler)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

path = 'https://pokeapi.co/api/v2/'
STATE1 = 1

# mensagem de inicio
def start(update, context):
    message = """Olá, treinador! 
                        \nDigite /pokemon para buscar"""
    update.message.reply_text(
        message, reply_markup=ReplyKeyboardMarkup([], one_time_keyboard=True))


def searchPokemon(update, context):
    message = 'Digite o nome ou o código do pokémon:'
    update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup([], one_time_keyboard=True))
    pokemon = update.message.text
    print(pokemon)
    data = requests.get(path + pokemon)
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
            CommandHandler('pokemon', searchPokemon),
            CommandHandler('close', close)
        ],
        states={

        },
        fallbacks=[CommandHandler('close', close)])

    # iniciando
    updater.dispatcher.add_handler(conversation_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
