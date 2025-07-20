import logging
from UseCase import *
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Configurar logging para ver as mensagens do bot no console
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Seu token da API do Bot Telegram (substitua pelo seu token real)
TOKEN = "7606592501:AAGTBFv9-V0v0A64SUVWAzFEfd2Uw82nRrA"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler para o comando /start.
    Envia uma mensagem de boas-vindas ao usuário.
    """
    user = update.effective_user
    # reply_html permite usar formatação HTML na mensagem
    await update.message.reply_html(
        f"Olá, {user.mention_html()}! Eu vou iniciar seu processo de triagem. O que você esta sentido ??",
        # do_quote=True # Opcional: para citar a mensagem original do usuário
    )

def main() -> None:
    """
    Função principal para configurar e iniciar o bot.
    """
    # Constrói a aplicação do bot com o token
    application = ApplicationBuilder().token(TOKEN).build()

    # Adiciona o handler para o comando /start
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), atendimento))  # Lida com mensagens de texto que não são comandos

    # Inicia o bot usando long polling.
    # allowed_updates=Update.ALL_TYPES garante que o bot receba todos os tipos de atualizações.
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()