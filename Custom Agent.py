import json
import os
import telebot
import PyPDF2
from langchain.chains import LLMChain

from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import CSVLoader

from API.config import TOKEN, OPENAI_API_KEY

bot = telebot.TeleBot(TOKEN)
openai_api_key = OPENAI_API_KEY
language = "Uzbek tilida"
BOT_ROLE = "HoneyMoon.txt mahsuloti operatori"
CHAT_LOG_DIR = "chat_logs"
chat_log = []

pdf_path = "Data/HoneyMoon.pdf"
reader = PyPDF2.PdfReader(pdf_path)
raw_text = ""
for page in reader.pages:
    raw_text += page.extract_text()

cleaned_text = raw_text.replace("\\n", " ").strip()
splitter = CharacterTextSplitter(separator="\\n", chunk_size=1000, chunk_overlap=200)
texts = splitter.split_text(cleaned_text)

# (Your existing bot functionalities and code)

# New message handling with your provided code snippet
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global context
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    history = {"context": context}
    prompt = history
    prompt = json.dumps(prompt)

    if len(context) > 2:
        context = context[-2:]
    query = f"bot role:{BOT_ROLE}language: {language} history:{prompt} Customer query:{message.text}"
    context.append(query)
    print(len(context))

    user_file = os.path.join(CHAT_LOG_DIR, f"{user_name}_{user_id}.txt")
    if not os.path.exists(CHAT_LOG_DIR):
        os.mkdir(CHAT_LOG_DIR)

    # Assuming docsearch and chain are defined elsewhere in your code
    docs = docsearch.similarity_search(query, k=1)
    result = chain.run(input_documents=docs, question=query)
    bot_response = f'answer:{result}'
    context.append(bot_response)
    bot.send_message(message.chat.id, result)

    with open(user_file, "a") as f:
        f.write(f"{user_name}: {query}\n")
        f.write(f"Bot: {result}\n")

    chat_log.append((query, result))

 # Template for response
    template = """Quyidagi savollarga eng yaxshi javob bering, HoneyMoon.txt mahsuloti haqida ma'lumotlardan foydalanib. Quyidagi vositalarga kirishingiz bor:

    {tools}

    Foydalanish uchun quyidagi formatdan foydalaning:

    Savol: javob berishingiz kerak bo'lgan savol
    O'ylash: javobingizda HoneyMoonning afzalliklari va tarkibiy qismlarini hisobga oling
    Harakat: qilinishi kerak bo'lgan harakat, [{tool_names}] ro'yxatidagi biri bo'lishi kerak
    Harakat Kirishi: harakat uchun kirish ma'lumoti
    Kuzatish: harakat natijasi
    ... (bu O'ylash/Harakat/Harakat Kirishi/Kuzatish N marta takrorlanishi mumkin)
    O'ylash: Endi yakuniy javobni bilaman
    Yakuniy Javob: asl savolga yakuniy javob

    Boshlang! Yakuniy javobingizni berayotganda HoneyMoon.txt mahsulotining afzalliklari va tarkibiy qismlariga asoslanib javob bering.

    Savol: {input}
    {agent_scratchpad}"""

    # Placeholder for the response generation logic
    response = "This is a placeholder response. Implement response generation logic here."

    # Sending the response back to the user
    bot.send_message(message.chat.id, response)
# Botni ishga tushirish
bot.polling()
