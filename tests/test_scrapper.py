import unittest
from unittest.mock import patch, MagicMock, mock_open
import requests
import os, sys

# Agrega el directorio src al sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from scrapper.scrappers.Scrapper import ScrapperBOC

class TestScrapperBOC(unittest.TestCase):

    def setUp(self):
        self.url = "https://boc.cantabria.es/boces/verAnuncioAction.do?idAnuBlob="
        self.scrapper = ScrapperBOC(self.url, procesos=5, carpeta='test_boc', start=1, end=5, paciencia=5)
        
    @patch('requests.head')
    def test_check_url(self, mock_head):
        mock_head.return_value.status_code = 200
        self.assertTrue(self.scrapper._check_url(self.url + "1"))

        mock_head.return_value.status_code = 404
        self.assertFalse(self.scrapper._check_url(self.url + "2"))

    @patch('requests.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_download_document(self, mock_open, mock_get):
        mock_get.return_value.content = b'%PDF'
        self.assertTrue(self.scrapper._download_document(self.url + "1", "test_boc/boc_1.pdf"))

        mock_get.return_value.content = b'Not a PDF'
        self.assertFalse(self.scrapper._download_document(self.url + "2", "test_boc/boc_2.pdf"))

    @patch.object(ScrapperBOC, '_check_url', return_value=True)
    @patch.object(ScrapperBOC, '_download_document', return_value=True)
    def test_process_url_success(self, mock_download_document, mock_check_url):
        self.scrapper._process_url(1)
        self.assertEqual(len(self.scrapper._error_descarga), 0)

    @patch.object(ScrapperBOC, '_check_url', return_value=False)
    def test_process_url_failure(self, mock_check_url):
        self.scrapper._process_url(1)
        self.assertEqual(len(self.scrapper._error_descarga), 1)

    @patch('os.makedirs')
    @patch('scrapper.Scrapper.tqdm', return_value=range(1, 5))
    @patch.object(ScrapperBOC, '_process_url')
    def test_run(self, mock_process_url, mock_tqdm, mock_makedirs):
        self.scrapper.run()
        self.assertEqual(mock_process_url.call_count, 4)

    def test_tiempo_de_descargar(self):
        self.scrapper._tiempo_total = 59
        tiempo, unidad = self.scrapper.tiempo_de_descargar()
        self.assertEqual((tiempo, unidad), (59, 'seg'))

        self.scrapper._tiempo_total = 3600
        tiempo, unidad = self.scrapper.tiempo_de_descargar()
        self.assertEqual((tiempo, unidad), (1.0, 'horas'))

    def test_get_error_descarga(self):
        self.scrapper._error_descarga = [self.url + "1", self.url + "2"]
        self.assertEqual(self.scrapper.get_error_descarga(), [self.url + "1", self.url + "2"])

    @patch('os.listdir', return_value=['boc_1.pdf', 'boc_2.pdf'])
    def test_last_download(self, mock_listdir):
        self.assertEqual(self.scrapper.last_download(), 2)

    @patch('os.listdir', return_value=['boc_1.pdf', 'boc_2.pdf', 'boc_3.pdf'])
    def test_last_download_with_gaps(self, mock_listdir):
        self.assertEqual(self.scrapper.last_download(), 3)

if __name__ == '__main__':
    unittest.main()
