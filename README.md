# Chat-With-Documents

# Summary
As the name suggests Chat With Document enables you to chat with your personal documents(PDF, TXT, DOCX) using Large Language Models like GPT. While OpenAI has recently launched a fine-tuning API for GPT models, it doesn't enable the base pretrained models to learn new data, and the responses can be prone to factual hallucinations. So we have used the approach to use model inputs with embedded-based search.

# 1. Prepare the Document (once per document)
a. Load the data into LangChain Documents <br/>
b. Split the documents into chunks <br/>
c. Embed the chunks into numeric vectors <br/>
d. Save the chunks and embeddings into vector database <br/>

# 2. Search (once per query)
a. Embed the user's question <br/>
b. Using the question's embeddings and the chunks embeddings, rank the vectors by similarity to the question's embedding. The nearest vectors represent chunks similar to the question. <br/>

# 3. Ask (once per query)
a. Insert the question and the most relevant chunks into the message to a GPT model <br/>
b. Return GPT's answer. <br/>

# DEMO

[streamlit-chat_with_documents_demo.webm](https://github.com/user-attachments/assets/4cd7ae26-1bd7-456d-9614-f80fe3e9d3ef)

# Getting Started
1. Prerequisites:
  a. 3.11 ≤ Python < 3.12.5 with Conda <br/>
  b. [OpenAI API Key](https://auth.openai.com/authorize?issuer=auth0.openai.com&client_id=DRivsnm2Mu42T3KOpqdtwB3NYviHYzwD&audience=https%3A%2F%2Fapi.openai.com%2Fv1&redirect_uri=https%3A%2F%2Fplatform.openai.com%2Fauth%2Fcallback&device_id=89fec6e2-ceef-4aa9-9a00-c861166971f4&screen_hint=signup&max_age=0&scope=openid+profile+email+offline_access&response_type=code&response_mode=query&state=Q18waFZoY2owbTJ0NUgybnE3MkdUM0NzQW8wTnkyQzYzOGpyYldDZFE3MQ%3D%3D&nonce=VG1sSUNaTU4ydVcxd0c2Vm52c084RmlSbjlVVVRmWEFYMlhFWmN2ajAxQg%3D%3D&code_challenge=7q-RHFsluPgm1sUtF7_sMyoItqfd__7wnDYs6d1n4gY&code_challenge_method=S256&auth0Client=eyJuYW1lIjoiYXV0aDAtc3BhLWpzIiwidmVyc2lvbiI6IjEuMjEuMCJ9&flow=control) <br/>
  c. The documents <br/>

2. Clone the repository
    ```
    git clone https://github.com/CBhandawat/Chat-With-Documents
    cd Chat-With-Documents
    ```

3. Setup
   Create Virtual Environment:
     ```
     python -m venv venv
     ```

   Activate:
     ```
     .\.venv\Scripts\activate
     ```

   Install all requirements:
     ```
     pip install -r requirements.txt
     ```

4. Run
   ```
   streamlit run chat_with_documents.py
   ```
It will open your browser and from there you can enter your OPENAI API KEY and get started.

# Acknowledgement
Special thanks to [LangChain](https://github.com/langchain-ai/langchain), [ChromaDB](https://github.com/chroma-core/chroma), [Streamlit](https://github.com/streamlit/streamlit) for their invaluable contributions to the open source community. 

# LICENSE
[Apache 2.0 License](https://github.com/CBhandawat/Chat-With-Documents/blob/main/LICENSE)




   
   
   
   
