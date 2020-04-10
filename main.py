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

#verifica o pokemon
def isPokemon(update, context):
    message = 'Digite o nome ou o código do pokémon:'
    update.message.reply_text(
        message, reply_markup=ReplyKeyboardMarkup([], one_time_keyboard=True))
    return STATE1

#busca na api, verifica se tem e dá os dados
def searchPokemon(update, context):
    pokemon = update.message.text
    data = requests.get(path + pokemon)
    if data.status_code != 200:
        message = """Dado inválido
                        \nDigite o nome ou o código do pokémon:"""
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=message)
    else:
        dataJson = data.json()
        types = []
        abilities = []
        id = dataJson["id"]
        name = dataJson["name"]
        type = dataJson["types"]
        for t in type:
            types.append(t["type"]["name"])
        abilitie = dataJson["abilities"]
        for a in abilitie:
            abilities.append(a["ability"]["name"])
        weight = dataJson["weight"]
        height = dataJson["height"]
        message = "Código: {0} \nNome: {1} \nTipo: {2} \nHabilidades: {3} \nPeso: {4} \nAltura: {5} \n/close para fechar conversa".format(id, name, types, abilities, weight, height)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
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
