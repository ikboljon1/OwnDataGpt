# Kerakli kutubxonalarni import qilish
import PyPDF2
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from API.config import OPENAI_API_KEY
# OpenAI kalitini o'rnatish

openai_api_key = OPENAI_API_KEY
# PDF fayl manzili
pdf_path = "Data/HoneyMoonfull.pdf"

# PDF o'qish va matn ajratib olish
reader = PyPDF2.PdfReader(pdf_path)
raw_text = ""
for page in reader.pages:
    raw_text += page.extract_text()

# Matnni tozalash
cleaned_text = raw_text.replace("\n", " ").strip()

# Matnni bo'laklarga ajratish
splitter = CharacterTextSplitter(separator="\n", chunk_size=500, chunk_overlap=150)
texts = splitter.split_text(cleaned_text)

# Vektirlarni saqlash uchun FAISS qidiruv tizimini yaratish
embeddings = OpenAIEmbeddings()
docsearch = FAISS.from_texts(texts, embeddings)

# Savol-javob zanjirini yuklash
chain = load_qa_chain(OpenAI(), chain_type="stuff")

# Foydalanuvchidan savol olish
query = input("Savolingizni kiriting: ")

# Eng o'xshash hujjatlarni topish
docs = docsearch.similarity_search(query)

# Savol-javob zanjiridan natija olish
result = chain.run(input_documents=docs, question=query)

# Natijani chiqarish
print(result)
