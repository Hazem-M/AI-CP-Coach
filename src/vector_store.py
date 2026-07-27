import os
import json
from typing import List, Dict, Any
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

class ProblemVectorStore:
    """Manages the FAISS vector database for Codeforces problems."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", index_path: str = "./knowledge_base/faiss_index"):
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        self.index_path = index_path
        self.vector_store = None
        
        # Load existing index if it exists
        if os.path.exists(os.path.join(self.index_path, "index.faiss")):
            self.load()

    def create_documents_from_problems(self, problems: List[Dict[str, Any]]) -> List[Document]:
        """Convert problem dicts to LangChain Documents."""
        documents = []
        for prob in problems:
            # Create a rich text representation for the embedding model
            tags_str = ", ".join(prob.get("tags", []))
            content = f"Problem Name: {prob.get('name', 'Unknown')}\n"
            content += f"Rating: {prob.get('rating', 'Unrated')}\n"
            content += f"Tags: {tags_str}\n"
            if "statement" in prob:
                content += f"Statement: {prob['statement'][:1000]}..." # Truncate if too long
                
            metadata = {
                "name": prob.get("name"),
                "contestId": prob.get("contestId"),
                "index": prob.get("index"),
                "rating": prob.get("rating"),
                "tags": prob.get("tags", [])
            }
            documents.append(Document(page_content=content, metadata=metadata))
        return documents

    def build_index(self, problems: List[Dict[str, Any]]):
        """Build the FAISS index from a list of problems."""
        print(f"Building index from {len(problems)} problems...")
        documents = self.create_documents_from_problems(problems)
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        print("Index built successfully.")
        
    def save(self):
        """Save the index to disk."""
        if self.vector_store:
            os.makedirs(self.index_path, exist_ok=True)
            self.vector_store.save_local(self.index_path)
            print(f"Index saved to {self.index_path}")
            
    def load(self):
        """Load the index from disk."""
        print(f"Loading index from {self.index_path}...")
        self.vector_store = FAISS.load_local(
            self.index_path, 
            self.embeddings,
            allow_dangerous_deserialization=True # Required for local loading in newer FAISS
        )
        
    def search_similar_problems(self, query: str, k: int = 5) -> List[Document]:
        """Search for similar problems given a query."""
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Build or load an index first.")
        return self.vector_store.similarity_search(query, k=k)

if __name__ == "__main__":
    # Test script for building a dummy index
    print("Testing Vector Store initialization...")
    store = ProblemVectorStore()
    
    # Dummy data
    dummy_problems = [
        {
            "name": "Watermelon", "contestId": 4, "index": "A", "rating": 800, 
            "tags": ["math", "brute force"], 
            "statement": "One hot summer day Pete and his friend Billy decided to buy a watermelon..."
        },
        {
            "name": "Way Too Long Words", "contestId": 71, "index": "A", "rating": 800, 
            "tags": ["strings"], 
            "statement": "Sometimes some words like 'localization' or 'internationalization' are so long..."
        }
    ]
    
    store.build_index(dummy_problems)
    store.save()
    
    print("Searching for 'fruit'...")
    results = store.search_similar_problems("fruit", k=1)
    print(f"Top result: {results[0].metadata['name']}")
