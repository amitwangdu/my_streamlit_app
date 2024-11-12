import chromadb

class ChromaHelper:
    def __init__(self, collection_name: str):
        """
        Initializes a Chroma client and creates or retrieves a collection.

        Parameters:
            collection_name (str): The name of the collection to work with.
        """
        self.client = chromadb.Client()
        self.collection = self._get_or_create_collection(collection_name)
    
    def _get_or_create_collection(self, name: str):
        """
        Creates or retrieves a collection based on the name.

        Parameters:
            name (str): The name of the collection.

        Returns:
            Collection: The Chroma collection instance.
        """
        try:
            return self.client.create_collection(name=name)
        except Exception:
            return self.client.get_collection(name=name)
    
    def upsert_document(self, doc_id: str, text: str):
        """
        Upserts a document into the collection.

        Parameters:
            doc_id (str): The unique document ID.
            text (str): The document text.
        """
        self.collection.upsert(ids=[doc_id], documents=[text])
    
    def get_similar_documents(self, text: str):
        """
        Retrieve documents with similarity distance of 0.0 to the input text.

        Parameters:
            text (str): The text content to compare.

        Returns:
            list: List of document IDs with an exact similarity match (distance = 0.0).
        """
        results = self.collection.query(query_texts=[text], n_results=10)
        similar_docs = [
            doc_id
            for doc_id, score in zip(results["ids"][0], results["distances"][0])
            if score == 0.0  # Only retrieve documents with a distance of 0.0
        ]
        return similar_docs
    
    def get_all_file_names(self):
        """
        Retrieves all file names (IDs) stored in the collection.

        Returns:
            list: List of all document IDs (file names).
        """
        try:
            results = self.collection.get()
            documents = results.get("documents", [])
            file_names = [doc.get("id") for doc in documents if isinstance(doc, dict) and "id" in doc]
            return file_names
        except Exception as e:
            print(f"Error retrieving file names: {e}")
            return []
