from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

path = 'https://pokeapi.co/api/v2/'

#mensagem de inicio
def start(update, context):
    message = """Olá, treinador! 
                        \nDitige o nome ou o cógido do pokémon: """
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


#cancelando bot e dando tchau
def close(update, context):
    message = "Tchau, treinador!"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    return ConversationHandler.END

#main
def main():
    #config
    updater = Updater(token=myToken, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    #opções de conversas
    conversation_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CommandHandler('close', close)
        ],
        fallbacks=[CommandHandler('close', close)])

    #iniciando
    updater.dispatcher.add_handler(conversation_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()