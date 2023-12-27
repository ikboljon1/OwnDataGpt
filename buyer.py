import click
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
import openai
from API.config import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY



@click.command()
@click.option('--query','-q', required=True)
def retrieve_openai(query):
    file = 'Datachat_logs/._5541917762.txt'
    loader = TextLoader(file)
    index = VectorstoreIndexCreator().from_loaders([loader])
    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model='gpt-3.5-turbo'),
        retriever=index.vectorstore.as_retriever(
            search_kwargs={'k': 1}
        )
    )
    chat_log = []
    result = chain({'question': query, 'chat_history': chat_log})
    click.echo(result['answer'])
    chat_log.append((query, result['answer']))

if __name__ == '__main__':
    retrieve_openai()
