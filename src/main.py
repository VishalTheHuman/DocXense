from markdowns import * 
from process import *
from extractcontent import ExtractContent
import streamlit as st

def handleUserQuery(query):
    context = st.session_state.vector_store.similarity_search(query)
    context = "\n".join([x.page_content for x in context])
    print(context)
    response = st.session_state.conversation.invoke({"question":query, "context":context if len(context) < 30000 else context[:30000]})
    return response["text"]
    
def clearChat():
    st.session_state.messages = []

def clearAll():
    clearChat()
    if "conversation" in st.session_state:
        del st.session_state.conversation
    if "vector_store" in st.session_state:
        del st.session_state.vector_store
    if "content" in st.session_state:
        del st.session_state.content
             
def main():
    # Title 
    st.set_page_config(page_title = "DocXense", page_icon="📚")
    st.title(":blue[Doc]:orange[X]:red[ense] 💻📚", anchor=False)

    HOME = ASK = TEST = None

    # File Upload
    with st.spinner("Processing"):
        FILE = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"], accept_multiple_files=False)
    
    if not FILE:
        clearAll()
    
    if FILE:
        valid_extensions = ["pdf", "docx", "txt"]
        file_extension = FILE.name.split(".")[-1]
                
        if file_extension in valid_extensions:
            with open(f"storage/file.{file_extension}", "wb") as f:
                f.write(FILE.getvalue())
            if "content" not in st.session_state:
                st.session_state.content = getChunks(ExtractContent.readPdf(f"storage/file.{file_extension}")[0])
            if "vector_store" not in st.session_state:
                st.session_state.vector_store = getVectorStore(st.session_state.content)
            if "conversation" not in st.session_state:
                st.session_state.conversation = createConversationChain(st.session_state.vector_store)

            HOME, ASK, TEST = st.tabs(["**Home🏡**", "**Ask It 🤔**", "**Test Yourself 🤓**"])

            with HOME:
                st.markdown(HOME_MARKDOWN, unsafe_allow_html=False)
            
            with ASK:
                messages = st.container(height=350)
                if "messages" not in st.session_state:
                    st.session_state.messages = []
                if prompt := st.chat_input("What's Up ?"):
                    st.session_state.messages.append({"role":"user", "content":prompt})
                    response = handleUserQuery(prompt)
                    st.session_state.messages.append({"role":"assistant", "content":response})
                if st.session_state.messages:
                    for message in st.session_state.messages:
                        with messages.chat_message(message["role"]):
                            st.markdown(message["content"])
                st.button('Clear Chat', on_click=clearChat)
                
            with TEST:
                st.button("Test Yourself")
        
        else:
            st.error("Invalid file format. Please upload a PDF, DOCX, or TXT file.")

    else:
        HOME = st.tabs(["**Home🏡**"])[0]
        with HOME:
            st.markdown(HOME_MARKDOWN, unsafe_allow_html=False)

if __name__ == "__main__":
    main()