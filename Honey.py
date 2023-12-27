import json
import os
import telebot
import PyPDF2
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from API.config import TOKEN, OPENAI_API_KEY

bot = telebot.TeleBot(TOKEN)
openai_api_key = OPENAI_API_KEY

BOT_ROLE = "HoneyMoon mahsuloti haqida malumot beruvchi bot"
CHAT_LOG_DIR = "chat_logs"
chat_log = []


pdf_path = "Data/HoneyMoon8.pdf"
reader = PyPDF2.PdfReader(pdf_path)
raw_text = ""
for page in reader.pages:
    raw_text += page.extract_text()

cleaned_text = raw_text.replace("\n", " ").strip()
splitter = CharacterTextSplitter(separator="\n", chunk_size=500, chunk_overlap=150)
texts = splitter.split_text(cleaned_text)

embeddings = OpenAIEmbeddings()
docsearch = FAISS.from_texts(texts, embeddings)
chain = load_qa_chain(OpenAI(), chain_type="stuff")
context = []
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global context
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    history = {"context": context}
    prompt = history
    prompt = json.dumps(prompt)
    print(prompt)

    if len(context) > 5:
        context = context[-5]
    query = f"bot role:{BOT_ROLE} Pervious text:{prompt}  query:{message.text} chiroyli formatda javob ber"
    context.append(query)

    user_file = os.path.join(CHAT_LOG_DIR, f"{user_name}_{user_id}.txt")
    if not os.path.exists(CHAT_LOG_DIR):
        os.mkdir(CHAT_LOG_DIR)

    docs = docsearch.similarity_search(query)
    result = chain.run(input_documents=docs, question=query)
    bot_response = f'answer:{result}'
    context.append(bot_response)
    bot.send_message(message.chat.id, result)

    with open(user_file, "a") as f:
        f.write(f"{user_name}: {query}\n")
        f.write(f"Bot: {result}\n")

    chat_log.append((query, result))

bot.polling()
