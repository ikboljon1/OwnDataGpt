import streamlit as st
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

# 1. Vectorise the sales response csv data
loader = CSVLoader(file_path="Data/HoneyMoon.csv")
documents = loader.load()

embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(documents, embeddings)

# 2. Function for similarity search


def retrieve_info(query):
    similar_response = db.similarity_search(query, k=3)

    page_contents_array = [doc.page_content for doc in similar_response]

    # print(page_contents_array)

    return page_contents_array


# 3. Setup LLMChain & prompts
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")

template = """
Siz HoneyMoon mahsulotlarini qo'llab-quvvatlash bo'yicha mutaxassissiz. 
Sizning vazifangiz - mijozlarning savollariga aniq va tushunarli javoblar berish, HoneyMoon mahsulotining xususiyatlari va afzalliklarini hisobga olib.
Men sizga istiqbolli mijozning xabarini beraman va siz, HoneyMoon mahsulotining o'tmishdagi eng yaxshi amaliyotlariga asoslanib, 
ushbu mijozga yuborishim kerak bo'lgan eng yaxshi javobni berishingiz kerak. 
Quyida keltirilgan qoidalarga rioya qilishingiz kerak:

1/ Javob o'tmishdagi eng yaxshi amaliyotlar bilan juda o'xshash yoki hatto bir xil bo'lishi kerak, 
uzunlik, ovoz ohangi, mantiqiy dalillar va boshqa tafsilotlar jihatidan.

2/ Agar eng yaxshi amaliyotlar tegishli bo'lmasa, unda mijozning xabariga eng yaxshi amaliyotlar uslubini taqlid qilib javob bering.

Quyida men olgan mijozning xabari keltirilgan:
{message}

Iltimos, ushbu ma'lumotlarni hisobga olgan holda, mijozga yuborishim kerak bo'lgan eng yaxshi javobni yozing:
"""

prompt = PromptTemplate(
    input_variables=["message"],
    template=template
)

chain = LLMChain(llm=llm, prompt=prompt)


# 4. Retrieval augmented generation
def generate_response(message):
    best_practice = retrieve_info(message)
    response = chain.run(message=message, best_practice=best_practice)
    return response


# 5. Build an app with streamlit
def main():
    st.set_page_config(
        page_title="Customer response generator", page_icon=":bird:")

    st.header("Customer response generator :bird:")
    message = st.text_area("customer message")

    if message:
        st.write("Generating best practice message...")

        result = generate_response(message)

        st.info(result)


if __name__ == '__main__':
    main()
