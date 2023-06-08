from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
from langchain.memory import ConversationBufferWindowMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from django.shortcuts import redirect
from django.http import JsonResponse
from django.shortcuts import render
import os


template = """Assistant is a large language model trained by Gregory.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.


{history}
Human: {human_input}
Assistant:"""

chatgpt_chain = LLMChain(
    llm=ChatOpenAI(temperature=0, model='gpt-3.5-turbo'),
    prompt=PromptTemplate.from_template(template),
    verbose=True,
    memory=ConversationBufferWindowMemory(),
)

messages = []
embedding = OpenAIEmbeddings()
vectordb = Chroma(embedding_function=embedding, persist_directory='db')


def index(request):
    if not messages:
        load_data_from_db()
    print(chatgpt_chain.memory)
    return render(request, 'main/index.html', {'messages': messages})


def api(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = chatgpt_chain.predict(human_input=message)
        messages.append({'role': 'human', 'content': message})
        messages.append({'role': 'ai', 'content': response})
        vectordb.add_texts(texts=[message, response], metadatas=[
                           {"role": "human"}, {"role": "ai"}])
        vectordb.persist()
        return redirect('/')
    else:
        return JsonResponse({'error': 'Invalid request method'})


def delete_conversation(request):
    if request.method == 'POST':
        vectordb._collection.delete()
        messages.clear()
        chatgpt_chain.memory.clear()
        return redirect('/')
    else:
        return JsonResponse({'error': 'Invalid request method'})


def load_data_from_db():
    docs = vectordb.get()['documents']
    roles = vectordb.get()['metadatas']
    chathistory = ChatMessageHistory()
    for i in range(len(docs)):
        messages.append({'role': roles[i].get('role'), 'content': docs[i]})
        if roles[i].get('role') == 'human':
            chathistory.add_user_message(docs[i])
        else:
            chathistory.add_ai_message(docs[i])
    chatgpt_chain.memory = ConversationBufferWindowMemory(
        chat_memory=chathistory)
