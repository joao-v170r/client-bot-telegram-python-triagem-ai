# Triagem Inteligente SUS com IA

## Visão Geral
Este serviço opera um bot do Telegram desenvolvido em Python para realizar triagem de usuários, integrando-se a uma API do Telegram e outra API de triagem em Spring Boot e armazenando dados em um banco MongoDB. O bot recebe mensagens dos usuários, envia para a API de triagem, recebe uma resposta desta API e a encaminha de volta para o usuário, e armazena dados relevantes das conversas para associar uma conversa a um atendimento na API de triagem. 

A API de triagem pode ser consultada em: `https://github.com/joao-v170r/client-bot-telegram-python-triagem-ai`.

## Estrutura do Projeto
- `Application.py`: Ponto de entrada do bot. Configura comandos, handlers e inicializa o bot Telegram.
- `UseCase.py`: Contém a lógica dos handlers, integração com a API externa e persistência no MongoDB.
- `MongoDB.py`: Gerencia a conexão com o banco de dados MongoDB.
- `__pycache__/`: Arquivos compilados do Python.

## Principais Funcionalidades
- **/start**: Inicia a conversa e orienta o usuário.
- **/help**: Lista comandos disponíveis.
- **Atendimento**: Recebe mensagens, envia para a API de triagem e responde ao usuário.
- **Persistência**: Salva histórico de mensagens e dados do chat no MongoDB.

## Configuração
1. **Variáveis de Ambiente**:
   - `MONGO_URI`: URI de conexão com o MongoDB (padrão: `mongodb://localhost:27017/`).
   - Token do bot Telegram deve ser definido em `Application.py`.
2. **Dependências**:
   - `python-telegram-bot`
   - `pymongo`
   - `httpx`
   - `python-dotenv`

Instale as dependências com:
```bash
pip install python-telegram-bot pymongo httpx python-dotenv
```

## Execução
1. Certifique-se de que o MongoDB está em execução.
2. Certifique-se de substituir o token em `Application.py` por um token válido.
3. Execute o serviço:
```bash
python Application.py
```

## Integrações com APIs externas
- O serviço utiliza API do Telegram para receber as mensagens de uma conversa com o bot e enviar como resposta as mensagens da API de triagem.
- O serviço envia mensagens para a API de triagem no endpoint `/realizar-atendimento`.
- Espera-se que a API retorne uma resposta com os campos `mensagem` e `idAtendimento`.

## Estrutura dos Dados no MongoDB
- Cada chat é salvo com:
  - `user_id`, `first_name`, `chat_id`, `last_interaction`, `messages`, `api_id_chat`
- Cada mensagem contém:
  - `message_id`, `timestamp`, `raw_data`, `text`, `message_type`
