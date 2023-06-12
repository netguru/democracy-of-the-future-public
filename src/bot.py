import os
import pickle

from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.vectorstores.faiss import FAISS

class QnABot:
    def __init__(
        self,
        directory: str,
        index: str | None = None,
        model: str | None = None,
        temperature=0,
    ):
        self._engine = "ng-gpt4-32k"
        self._chain_type = "stuff"

        # Initialize the QnABot by selecting a model, creating a loader, and loading or creating an index
        self._llm = self.select_model(model, temperature)
        self._loader = self.create_loader(directory)
        self._search_index = self.load_or_create_index(index)

        # Load the question-answering chain for the selected model
        self._chain = load_qa_with_sources_chain(self._llm, chain_type=self._chain_type)


    def select_model(self, model: str | None, temperature: float):
        # Select and set the appropriate model based on the provided input
        if model is None or model == "ngchat":
            print("Using model: ngchat")
            return ChatOpenAI(temperature=temperature, engine=self._engine)

    def create_loader(self, directory: str):
        return DirectoryLoader(directory, recursive=True)

    def load_or_create_index(self, index_path: str | None):
        # Load an existing index from disk or create a new one if not available
        if index_path is not None and os.path.exists(index_path):
            print("Loading path from disk...")
            with open(index_path, "rb") as f:
                 search_index = pickle.load(f)
        else:
            print("Creating index...")
            search_index = FAISS.from_documents(
                self._loader.load_and_split(), OpenAIEmbeddings(
                    document_model_name="ngembedding", chunk_size=1)
            )
        return search_index

    def save_index(self, index_path: str):
        # Save the index to the specified path
        with open(index_path, "wb") as f:
            pickle.dump(self._search_index, f)

    def get_answer(self, question, k=3):
        print(question)
        # Retrieve the answer to the given question and return it
        input_documents = self._search_index.similarity_search(question, k=k)
        return self._chain(
            {
                "input_documents": input_documents,
                "question": question,
            },
            return_only_outputs=True,
        )["output_text"]