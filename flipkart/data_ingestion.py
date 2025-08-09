from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from flipkart.data_converter import DataConverter
from flipkart.config import Config
#  imported things needed
class DataIngestor:
    def __init__(self):
        self.embedding = HuggingFaceEndpointEmbeddings(model=Config.EMBEDDING_MODEL)
        self.vector_store = AstraDBVectorStore(embedding=self.embedding,
                                               collection_name="flipkartdb",
                                               api_endpoint=Config.ASTRA_DB_API_ENDPOINT,
                                               token=Config.ASTRA_DB_APPLICATION_TOKEN,
                                               namespace=Config.ASTRA_DB_KEYSPACE)
        # initalised hugging embeddings model and vector store in which model to be used, database, api and all other things
    def ingest(self,load_existing=True):
        if load_existing==True:
            return self.vector_store
        
        #   when our vector store is already there we do not need to convert the docs and again run that
        #   when we want to run we can set load_existing to False
        #  set it when there is changes in the data 
        #  when no change default is True

        docs = DataConverter("data/flipkart_product_review.csv").convert()
        self.vector_store.add_documents(docs)
        # store all the docs in the astra db auto convert in embedding and store in astra db
        return self.vector_store
    



if __name__ == "__main__":
    ingestor = DataIngestor()
    ingestor.ingest(load_existing=False)
