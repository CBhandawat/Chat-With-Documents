import openai
from openai import ChatCompletion
from openai.error import AuthenticationError, InvalidRequestError
import streamlit as st
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma
import os

def load_document(file):
  import os
  name, extension = os.path.splitext(file)

  if extension == '.pdf':
    from langchain_community.document_loaders import PyPDFLoader
    print(f'Loading {file}')
    loader = PyPDFLoader(file)

  elif extension == '.docx':
    from langchain.document_loaders import Docx2txtLoader
    print(f'Loading {file}')
    loader = Docx2txtLoader(file)

  elif extension == '.txt':
    from langchain.document_loaders import TextLoader
    loader = TextLoader(file)

  else:
    print('Document format not supported!')
    return None


  data = loader.load()
  return data


def chunk_data(data, chunk_size=256, chunk_overlap=20):
  from langchain.text_splitter import RecursiveCharacterTextSplitter
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  chunks = text_splitter.split_documents(data)
  return chunks


def create_embeddings(chunks):
  embeddings = OpenAIEmbeddings()
  vector_store=Chroma.from_documents(chunks, embeddings)
  return vector_store

def ask_and_get_answer(vector_store,q,k=3):
  from langchain.chains import RetrievalQA
  from langchain.chat_models import ChatOpenAI

  llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=1)

  retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k':k})

  chain = RetrievalQA.from_chain_type(llm=llm, chain_type='stuff',retriever=retriever)

  answer = chain.run(q)
  return answer


def calculate_embedding_cost(texts):
  import tiktoken
  enc = tiktoken.encoding_for_model('text-embedding-ada-002')
  total_tokens = sum([len(enc.encode(page.page_content)) for page in texts])
  # print(f'Total Tokens: {total_tokens}')
  # print(f'Embedding cost in USD: {total_tokens/1000 * 0.0004:.6f}')
  return total_tokens, total_tokens/1000 * 0.0004


def clear_history():
  if 'history' in st.session_state:
    del st.session_state['history']


def check_api_key(api_key):
    try:
        openai.api_key = api_key
        response = ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "test"}],  # Minimal prompt
            max_tokens=1,  # Limit response length
        )
        st.success('Valid API Key!')  # API key is valid
        return True
    except AuthenticationError as e:
        if e.http_status == 401:
            st.error('Invalid API Key! Please check and try again.')
            return False
        else:
            st.error(f"Authentication error: {e}")
            return False
    except InvalidRequestError as e:
        st.error(f"Invalid request: {e}")
        return False
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return False


if __name__ == "__main__":
  import os
  from dotenv import load_dotenv, find_dotenv
  load_dotenv(find_dotenv(), override=True)

  
  st.subheader('LLM Question-Answering Application')

  with st.sidebar:
    api_key = st.text_input('OPEN_AI_API_KEY:',type='password')
    response = False
    if api_key:
      os.environ['OPENAI_API_KEY'] = api_key
      response = check_api_key(api_key)

    uploaded_file = st.file_uploader('Upload a file',type=['pdf','docx','txt'], disabled=not response)
    chunk_size = st.number_input('Chunk Size:',min_value=100, max_value=2048,value=512, disabled=not response)
    k=st.number_input('k', min_value=1, max_value=20, value=3, disabled=not response)
    add_data = st.button('Add data', disabled=not response)

    if uploaded_file and add_data:
      with st.spinner("Reading, Chunking and Embedding Data..."):
        bytes_data=uploaded_file.read()
        file_name = os.path.join('./',uploaded_file.name)
        with open(file_name, 'wb') as f:
          f.write(bytes_data)

        data = load_document(file_name)
        chunks = chunk_data(data, chunk_size=chunk_size)
        st.write(f'Chunk Size: {chunk_size}, Chunks: {len(chunks)}')

        tokens, embedding_cost = calculate_embedding_cost(chunks)
        st.write(f'Embedding Cost: ${embedding_cost:.4f}')

        vector_store = create_embeddings(chunks)

        st.session_state.vs = vector_store
        st.success('File Uploaded, Chunked and Embedded Successfully.')


  q = st.text_input('Ask a question about the context of your file:')
  
  if q:
    if 'vs' in st.session_state:
      vector_store = st.session_state.vs
      st.write(f'k= {k}')
      answer = ask_and_get_answer(vector_store,q,k)
      st.text_area('LLM Answer: ', value=answer)


      st.divider()
      if 'history' not in st.session_state:
        st.session_state.history = ''
      value = f'Q: {q} \nA: {answer}'
      st.session_state.history = f'{value} \n {"-" * 100} \n {st.session_state.history}'
      h = st.session_state.history
      st.text_area(label='Chat History',value=h,key='history',height=400)
    
