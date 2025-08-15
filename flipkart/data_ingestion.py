from langchain_astradb import AstraDBVectorStore
from langchain_openai import OpenAIEmbeddings
from flipkart.data_converter import DataConverter
from flipkart.config import Config


class DataIngestion:
    def __init__(self) -> None:
        self.embedding = OpenAIEmbeddings(model=Config.EMBEDDING_MODEL)
        self.vstore = AstraDBVectorStore(
            embedding=self.embedding,
            collection_name="flipkart_database",
            api_endpoint=Config.ASTRA_DB_API_ENDPOINT,
            token=Config.ASTRA_DB_APPLICATION_TOKEN,
            namespace=Config.ASTRA_DB_KEYSPACE
        )

    def ingest(self, load_existing: bool=True):
        if load_existing:
            return self.vstore

        docs = DataConverter(
            file_path="data/flipkart_product_review.csv"
        ).convert()

        self.vstore.add_documents(documents=docs)

        return self.vstore

if __name__ == '__main__':
    ingestor = DataIngestion()
    ingestor.ingest(load_existing=False)


