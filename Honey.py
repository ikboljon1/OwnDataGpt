import telebot
import PyPDF2
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from API.config import TOKEN,OPENAI_API_KEY

bot = telebot.TeleBot(TOKEN)
openai_api_key = OPENAI_API_KEY
pdf_path = "Data/HoneyMoon.pdf"
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

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    query = message.text
    docs = docsearch.similarity_search(query)
    result = chain.run(input_documents=docs, question=query)
    bot.send_message(message.chat.id, result)

bot.polling()
