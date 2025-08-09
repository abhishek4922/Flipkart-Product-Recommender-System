from langchain_groq import ChatGroq
# IT will be used to chat with llm 
from langchain.chains import create_history_aware_retriever,create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
#  will be used to combine multiple documents stuff strategy when we have
#  multple doc forming one answer 
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
#  it will be used include the conversational history
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from flipkart.config import Config


class RAG_CHAIN_BUILDER:
    def __init__(self,vector_store):
        self.vector_store=vector_store
        self.model = ChatGroq(model=Config.RAG_MODEL,temperature=0.5)
        #  TEMPERATURE MEANS CREATIVENESS OF THE LARGE LANGUAGE MODEL
        self.history_store={}
        # all the session history stored here in this

    def _get_history(self,session_id:str)-> BaseChatMessageHistory:
        # retrieve the chat for particular session 
        if session_id not in self.history_store:
            self.history_store[session_id]=ChatMessageHistory()

        return self.history_store[session_id]
    def build_chain(self):
        retriever = self.vector_store.as_retriever(search_kwargs={"k":3})
        
        # this can convert any vector store into retriever

        context_prompt = ChatPromptTemplate.from_messages([
            ("system", "Given the chat history and user question, rewrite it as a standalone question."),
            MessagesPlaceholder(variable_name="chat_history"), 
            ("human", "{input}")  
        ])

        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", """You're an e-commerce bot answering product-related queries using reviews and titles.
                          Stick to context. Be concise and helpful.\n\nCONTEXT:\n{context}\n\nQUESTION: {input}"""),
            MessagesPlaceholder(variable_name="chat_history"), 
            ("human", "{input}")  
        ])

        history_aware_retriever = create_history_aware_retriever(
            self.model , retriever , context_prompt
        )
#  to create better understanding of the context
#  help llm to understand the context better 
        question_answer_chain = create_stuff_documents_chain(
            self.model , qa_prompt
        )

#  when dealing with qa chain the qa prompt to be given

        rag_chain = create_retrieval_chain(
            history_aware_retriever,question_answer_chain
        )

        return RunnableWithMessageHistory(
            rag_chain,
            self._get_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )
    