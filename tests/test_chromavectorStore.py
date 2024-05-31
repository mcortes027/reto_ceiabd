import unittest
from unittest.mock import patch, MagicMock
import os, sys

# Agrega el directorio src al sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from scrapper.storage.ChromaVectorStore import ChromaVectorStore 
import chromadb

class TestChromaVectorStore(unittest.TestCase):

    @patch('your_module.chromadb.HttpClient')
    @patch('your_module.OllamaEmbeddings')
    @patch('your_module.CharacterTextSplitter')
    @patch('your_module.logging')
    def setUp(self, mock_logging, mock_text_splitter, mock_embeddings, mock_http_client):
        # Setup mocks
        self.mock_client = mock_http_client.return_value
        self.mock_embeddings = mock_embeddings.return_value
        self.mock_text_splitter = mock_text_splitter.return_value

        self.mock_text_splitter.split_documents.return_value = ['chunk1', 'chunk2']

        # Instantiate the class
        self.store = ChromaVectorStore()

    def test_initialization(self):
        # Test if the vector store is initialized correctly
        self.assertEqual(self.store.host, "localhost")
        self.assertEqual(self.store.port, 8000)
        self.assertEqual(self.store.collection_name, "ChatBOC_BD_Vector")

    @patch('your_module.Chroma')
    def test_initialize_vectorstore(self, mock_chroma):
        self.store._initialize_vectorstore()
        mock_chroma.assert_called_once_with(client=self.mock_client, embedding_function=self.mock_embeddings, collection_name="ChatBOC_BD_Vector")

    @patch('your_module.Chroma')
    def test_add_documento(self, mock_chroma):
        documento = MagicMock()
        self.store.add_documento(documento)
        self.store.text_splitter.split_documents.assert_called_once_with(documento)
        mock_chroma.from_documents.assert_called_once_with(documents=['chunk1', 'chunk2'], embedding=self.mock_embeddings, client=self.mock_client, collection_name="ChatBOC_BD_Vector")

    @patch('your_module.Chroma')
    def test_add_list_documentos(self, mock_chroma):
        documentos = [MagicMock(), MagicMock()]
        self.store.add_list_documentos(documentos)
        self.assertEqual(self.store.text_splitter.split_documents.call_count, 2)
        self.assertEqual(mock_chroma.from_documents.call_count, 2)

    def test_combine_docs(self):
        docs = [MagicMock(page_content="content1"), MagicMock(page_content="content2")]
        combined = self.store._combine_docs(docs)
        self.assertEqual(combined, "content1\ncontent2")

    @patch('your_module.Chroma')
    def test_get_documents(self, mock_chroma):
        mock_retriever = MagicMock()
        mock_retriever.invoke.return_value = [MagicMock(page_content="content1"), MagicMock(page_content="content2")]
        self.store.vectorstore = MagicMock(as_retriever=MagicMock(return_value=mock_retriever))

        result = self.store.get_documents("query")
        self.assertEqual(result, "content1\ncontent2")

    @patch('your_module.os')
    @patch('your_module.logging')
    def test_inicia_logs(self, mock_logging, mock_os):
        mock_os.path.exists.return_value = False
        mock_os.makedirs.return_value = None

        self.store._inicia_logs()
        mock_os.makedirs.assert_called_once_with("Log_System")
        mock_logging.basicConfig.assert_called_once()


if __name__ == '__main__':
    unittest.main()
