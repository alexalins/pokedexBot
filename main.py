import requests
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, RegexHandler, ConversationHandler)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

path = 'https://pokeapi.co/api/v2/pokemon/'
STATE1 = 1

# mensagem de inicio


def start(update, context):
    message = """Olá, treinador!
                        \nDigite /pokemon para buscar"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def isPokemon(update, context):
    message = 'Digite o nome ou o código do pokémon:'
    update.message.reply_text(
        message, reply_markup=ReplyKeyboardMarkup([], one_time_keyboard=True))
    return STATE1


def searchPokemon(update, context):
    pokemon = update.message.text
    data = requests.get(path + pokemon)
    if data.status_code != 200:
        message = """Dado inválido
                        \nDigite o nome ou o código do pokémon:"""
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    else:
        dataJson = data.json()

        id = dataJson["id"]
        name = dataJson["name"]
        type = dataJson["types""type"]
        weight = dataJson["weight"]
        height = dataJson["height"]
        print(type)
        #message =  'Id: ' + id + '\nNome: ' + name +'\nTipo: ' + type +'\nPeso: ' + weight +'\nAltura: ' + height +'\n'
        #context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        return ConversationHandler.END

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
            CommandHandler('pokemon', isPokemon),
            CommandHandler('close', close)
        ],
        states={
            STATE1: [MessageHandler(Filters.text, searchPokemon)],
        },
        fallbacks=[CommandHandler('close', close)])

    # iniciando
    updater.dispatcher.add_handler(conversation_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
