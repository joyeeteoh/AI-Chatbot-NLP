import chromadb
import pandas as pd
import json

   
from  chromadb import Documents, EmbeddingFunction, Embeddings
from langchain_ollama.embeddings import OllamaEmbeddings

class vector_db:
    def __init__(self, vdb_name: str):
        self.vdb_name = vdb_name
        self.client = chromadb.HttpClient(host="localhost", port=8899)
        self.vdb = self.get_vector_db()

    def query(self, query_texts, n_results):
        if not self.vdb:
            print("Vector database not found. Please create it first.")
            return None
        
        results = self.vdb.query(query_texts=query_texts, n_results=n_results)
        return results
    
    def create_vector_db(self):
        # os.system('chroma run --path ~/temp/chroma --port 8899')    
        vdb = self.client.create_collection(name=self.vdb_name, 
                                              metadata={"hnsw:space":"cosine"},
                                              embedding_function=BgeM3EmbeddingFunction())
        return vdb

    def get_vector_db(self):
        try:
            vdb = self.client.get_collection(name=self.vdb_name, embedding_function=BgeM3EmbeddingFunction())
            return vdb
        except Exception as e:
            print(f"Error retrieving vector database: {e}")
            return None
        
    def delete_vector_db(self, vdb_name: str):
        try:
            if self.client.get_collection(name=vdb_name):
                self.client.delete_collection(name=vdb_name)
        except Exception as e:
            print(e)

    def add_vdb(self, vdb, question, answer):
        cate_info = {"Question": question, "Answer":answer}
        print(f"Adding {vdb.count()} to vector db: {cate_info}")
        vdb.add(documents=[json.dumps(cate_info, ensure_ascii=False)], 
                ids=[f'cate_id: {vdb.count()}'])
    

    def load_file(self, file_path):
        if file_path.endswith('.csv'):
            return self._load_csv(file_path)
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            return self._load_excel(file_path)

    def _load_excel(self, file_path):
        return pd.read_excel(file_path)

    def _load_csv(self, file_path):
        return pd.read_csv(file_path)

class BgeM3EmbeddingFunction(EmbeddingFunction):
    
    def __init__(self):
        self._embedding_function = OllamaEmbeddings(model="bge-m3")

    def __call__(self, input: Documents) -> Embeddings:
        embedding = self._embedding_function.embed_documents(input)
        # print(f"Original Text:\n{input}\n\nEmbedding:\n{embedding}")
        return embedding

    
if __name__ == "__main__":

    vdb_name = "cate_vdb_4"
    vdb = vector_db(vdb_name)

    file_path = "knowledge_base/data/en_faq.xlsx"
    df = vdb.load_file(file_path)
    print(df.head())

    
    vdb.delete_vector_db(vdb_name)
    vdb_created = vdb.create_vector_db()

    df.apply(lambda x: vdb.add_vdb(vdb_created, x['Title'], x['Content']), axis=1)
