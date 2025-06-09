from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
import random

FLASHCARD_GAME, FLASHCARD_REPLY = range(2)

mensagens_acerto = [
    "🎉 Parabéns! Você acertou em cheio! 🚀",
    "🔥 Uau! Você mandou muito bem! 🎯",
    "👏 Isso aí! Você está no caminho certo! 🌟",
    "🎯 Acertou na mosca! Excelente trabalho! 🏆",
    "💡 Brilhante! Você está arrebentando! 🤩",
    "🚀 Boom! Você detonou nessa! 🎇",
    "🏅 Medalha de ouro para você! Muito bom! 🥇",
    "🎊 Sim! Você está cada vez melhor! 💪",
    "🧠 Mente afiada! Você acertou de novo! 🔥",
    "🌟 Genial! Continue assim! O sucesso te espera! 🚀"
]

mensagens_erro = [
    "😬 Opa! Quase lá! Tente mais uma vez! 🔄",
    "❌ Errado, mas não desista! Você está aprendendo! 📚",
    "🤔 Hmmm... Não foi dessa vez! Bora tentar de novo? 🔄",
    "😅 Perto! Continue tentando, você consegue! 💪",
    "🚧 Erros fazem parte do caminho! Vamos lá! 🏗️",
    "🔄 Não foi dessa vez, mas cada erro te deixa mais forte! 💡",
    "💭 Opa, pense mais um pouco! Você chega lá! 🎯",
    "⚠️ Errar faz parte do aprendizado! Tente de novo! 📈",
    "🤖 Erros? Só mais um passo para o acerto! Bora! 🚀",
    "🔥 Você está quase lá! Um pouco mais de esforço e acerta! 🏆"
]


application = Application.builder().token("TOKEN DO BOT").build()

resp_certa = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username
    await update.message.reply_text(f"Hello World {user}!")


async def flashcard_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global resp_certa
    resp_certa = None
    imagens = {'Ferro.webp':'iron', 'Maça.webp':'apple', 'Ouro.webp':'gold', 'Ovo.webp':'egg'}
    lista_imgs = ['Ferro.webp', 'Maça.webp', 'Ouro.webp', 'Ovo.webp']
    sorteio_img = random.randint(0, len(lista_imgs))
    img = lista_imgs[sorteio_img]
    resp_certa = imagens[img].lower()
    context.user_data['item'] = resp_certa
    await update.message.reply_photo(
        photo=open(f'/home/nathanael-bueno/Área de trabalho/Study/cursos - ferias FAP/mini curso python/images/{img}', 'rb'),
        caption='o que é isso? descreva o objeto em inglês.'
    )
    return FLASHCARD_REPLY

async def sair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bye!")
    await update.message.reply_text(f"Acertos: {context.user_data.get('acertos', 0)}\nErros: {context.user_data.get('erros', 0)}")
    context.user_data['acertos'] = 0
    context.user_data['erros'] = 0
    return ConversationHandler.END

async def flashcard_reply(update:Update, context: ContextTypes.DEFAULT_TYPE):
    global resp_certa
    reply = update.message.text
    resp_certa = context.user_data.get('item', '')
    if reply.lower() == str(resp_certa).lower():
        context.user_data['acertos'] = context.user_data.get('acertos', 0) + 1
        await update.message.reply_text(random.choice(mensagens_acerto))
    else:
        context.user_data['erros'] = context.user_data.get('erros', 0) + 1
        await update.message.reply_text(random.choice(mensagens_erro))
    
    reply_keyboard = [["/continuar", "/sair"]]
    
    await update.message.reply_text("Deseja continuar?\n",
                                    reply_markup=ReplyKeyboardMarkup(
                                        reply_keyboard, one_time_keyboard=True,
                                        input_field_placeholder='Continuar?'
                                    ))
    
    return FLASHCARD_GAME

application.add_handler(CommandHandler("start", start))
application.add_handler(ConversationHandler(
    entry_points =[
        CommandHandler("flashcard", flashcard_game),],
    
    states={
        FLASHCARD_REPLY: [
            MessageHandler(filters.TEXT, flashcard_reply)
        ],
        FLASHCARD_GAME: [
            CommandHandler('continuar', flashcard_game)
        ]
    },
    
    fallbacks=[
        CommandHandler("sair", sair)

    ]
))



application.run_polling(allowed_updates=Update.ALL_TYPES)
