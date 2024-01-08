import telebot
import os
import openai

from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

from API.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

bot = telebot.TeleBot("6853169439:AAHZdBoHQwWroofKKqNPD3j9VVRsEZSgTfE")

BOT_ROLE = "HoneyMoon махсулоти хакида малумот берувчи чатбот"
user_contexts = {}
chat_log = []
CHAT_LOG_DIR = "chat_logs"
file = 'Data/data.csv'
loader = TextLoader(file)
# Vectorstore index
index = VectorstoreIndexCreator().from_loaders([loader])

@bot.message_handler(func=lambda msg: True)
def handle_message(msg):

  user_id = msg.from_user.id
  user_name = msg.from_user.first_name

  query = msg.text

  if user_id not in user_contexts:
    user_contexts[user_id] = []

  context = user_contexts[user_id]

  if len(context) > 5:
    context = context[-5:]

  user_file = os.path.join(CHAT_LOG_DIR, f"{user_name}_{user_id}.txt")

  if not os.path.exists(CHAT_LOG_DIR):
    os.mkdir(CHAT_LOG_DIR)
  prompt = f"Bot role: {BOT_ROLE}\\n\\nUser query: {query}\\nPrevious context:\\n{context}\\n\\nBot response:"
  print(prompt)


  chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model='gpt-4'),
    retriever=index.vectorstore.as_retriever(search_kwargs={'k': 1})
  )

  result = chain({'question': prompt, 'chat_history': chat_log})
  bot.send_message(msg.chat.id, result['answer'])

  with open(user_file, "a") as f:
    f.write(f"{user_name}: {query}\n\n")

    f.write(f"{ 'BOT' }: {result['answer']}\n\n")

  chat_log.append((query, result['answer']))

  context.append(result['answer'])
  user_contexts[user_id] = context

bot.polling()


import json

# Function to save user contexts to a file
def save_contexts(contexts, file_path):
    with open(file_path, 'w') as file:
        json.dump(contexts, file)

# Function to load user contexts from a file
def load_contexts(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file does not exist

# Example usage
# user_contexts = load_contexts('user_contexts.json')
# ... update user_contexts during the bot operation ...
# save_contexts(user_contexts, 'user_contexts.json')
