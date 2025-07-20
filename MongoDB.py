from pymongo import MongoClient # Ou AsyncMongoClient para bots assíncronos
from dotenv import load_dotenv
import os

load_dotenv() # Carrega variáveis do arquivo.env

# Opção 1: Conexão básica (host e porta padrão)
# client = MongoClient() # Conecta a localhost:27017 por padrão [7]

# Opção 2: Especificando host e porta explicitamente
# client = MongoClient("localhost", 27017) [7]

# Opção 3: Usando URI de conexão (recomendado para flexibilidade e autenticação)
# A URI deve ser definida como uma variável de ambiente por segurança
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI) # Use AsyncMongoClient(MONGO_URI) para assíncrono [7, 8]

db = client.telegram_bot_db