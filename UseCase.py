import logging
import httpx # Importar httpx para futuras integrações reais
from telegram import Update
from datetime import datetime
from telegram.ext import ContextTypes
from telegram.ext import MessageHandler, filters
from MongoDB import db

SPRING_BOOT_API_BASE_URL = "http://localhost:8080"

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler para o comando /help.
    Envia uma mensagem de ajuda com os comandos disponíveis.
    """
    help_text = (
        "Aqui estão os comandos que você pode usar:\n"
        "/start - Inicia a conversa com o bot.\n"
        "/help - Mostra esta mensagem de ajuda.\n"
        "/echo <texto> - Repete o texto que você enviar.\n"
        "/processar <id_produto> - Processa o texto usando uma API externa (mockada)."
    )
    await update.message.reply_text(help_text)
    logging.info(f"Usuário {update.effective_user.first_name} solicitou ajuda.")

async def atendimento(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # logging.info("Este são os dados do update: %s", update)

    timestamp = datetime.now()
    endpoint = f"{SPRING_BOOT_API_BASE_URL}/realizar-atendimento"

    message = update.message
    chatCollection = db.chat

    chatCurrent = chatCollection.find_one({'chat_id': message.chat_id})
    logging.info("Este são os dados do chatCurrent: %s", chatCurrent)
    if not chatCurrent:
        logging.info("Novo Chat iniciado")
        chatCurrent = {
            'user_id': message.from_user.id,
            'first_name': message.from_user.first_name,
            'chat_id': message.chat_id,
            'last_interaction': timestamp,
            'messages': [],
            'api_id_chat': ''
        }

    messageCurrent = {
            'message_id': message.message_id,
            'timestamp': timestamp,
            'raw_data': message.to_dict()
    }
    
    if message.text:
        messageCurrent['text'] = message.text
        messageCurrent['message_type'] = 'text'
    else:
        messageCurrent['message_type'] = 'unknown' # Lidar com outros tipos ou ignorar
    
    if messageCurrent['message_type'] == 'text':  
        requestPayLoad = {
            "id": chatCurrent['api_id_chat'],
            "mensagem": messageCurrent['text']
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(endpoint, json=requestPayLoad, timeout=10.0)
                response.raise_for_status()  # Lança uma exceção para códigos de status HTTP 4xx/5xx
                logging.info("Resposta da API recebida")
                data = response.json()
                mensagem_api = data.get("mensagem", "Resposta da API não contém mensagem.")
                chatCurrent['api_id_chat'] = data.get("idAtendimento", "Resposta de API não contem o id do atendidmento")
                await update.message.reply_text(mensagem_api)
        except httpx.RequestError as e:
            logging.warning(f"Erro ao conectar com a API Spring Boot: {e}")
            await update.message.reply_text(f"Erro ao conectar com a API Spring Boot: {e}")
        except httpx.HTTPStatusError as e:
            logging.warning(f"Erro na API call({requestPayLoad}) (status {e.response.status_code}): {e.response.text}") # Removed data from here
            await update.message.reply_text(f"Erro na API (status {e.response.status_code}): {e.response.text}")
        except Exception as e:
            logging.warning(f"Erro ao conectar com a API Spring Boot: {e}")
            await update.message.reply_text(f"Ocorreu um erro inesperado: {e}")
    else: 
        logging.error("Não consegui processar a messagem")
        await update.message.reply_text("Não consegui entender essa mensagem.")
    
    chatCurrent["messages"].append(messageCurrent)

    chatCollection.update_one(
        {'user_id': chatCurrent["user_id"], 'chat_id': chatCurrent["chat_id"]},
        {'$set': chatCurrent},
        upsert=True
    )
    logging.info("Usuario salvo com sucesso")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler para mensagens de texto que não são comandos.
    Simplesmente ecoa o texto recebido de volta ao usuário.
    """
    if update.message and update.message.text:
        logging.info(f"Mensagem de texto recebida de {update.effective_user.first_name}: {update.message.text}")
        await update.message.reply_text(update.message.text)
