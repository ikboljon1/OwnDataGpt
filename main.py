# Kerakli kutubxonalarni import qilish
import PyPDF2
import os


from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from API.config import OPENAI_API_KEY
from langchain.vectorstores import Chroma, Pinecone
import pinecone
# OpenAI kalitini o'rnatish

openai_api_key = OPENAI_API_KEY
# PDF fayl manzili
pdf_path = "Data/HoneyMoon8.pdf"

# PDF o'qish va matn ajratib olish
reader = PyPDF2.PdfReader(pdf_path)
raw_text = ""
for page in reader.pages:
    raw_text += page.extract_text()

# Matnni tozalash
cleaned_text = raw_text.replace("\n", " ").strip()

# Matnni bo'laklarga ajratish
splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=0)
texts = splitter.split_text(cleaned_text)

# Vektirlarni saqlash uchun FAISS qidiruv tizimini yaratish
embeddings = OpenAIEmbeddings()
pinecone.init(
    api_key = "a9447164-eb52-479f-b7f8-0b4d77e038e7",
	environment='gcp-starter'
)
index = pinecone.Index('honeymoon')

docsearch = Pinecone.from_texts([t.page_content for t in texts])
# docsearch = FAISS.from_texts(texts, embeddings)

# Savol-javob zanjirini yuklash
chain = load_qa_chain(OpenAI(), chain_type="stuff")

# Foydalanuvchidan savol olish
query = input("Savolingizni kiriting: ")

# Eng o'xshash hujjatlarni topish
docs = docsearch.similarity_search(query, k=1)

# Savol-javob zanjiridan natija olish
result = chain.run(input_documents=docs, question=query)

# Natijani chiqarish
print(result)
