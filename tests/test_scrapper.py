import unittest
from unittest.mock import patch, mock_open, MagicMock

from src.scrapper.Scrapper import ScrapperBOC

class TestScrapperBOC(unittest.TestCase):

    def setUp(self):
        self.url = "http://example.com/boc/"
        self.procesos = 5
        self.carpeta = "test_boc"
        self.start = 1
        self.end = 5
        self.paciencia = 3
        self.scrapper = ScrapperBOC(self.url, self.procesos, self.carpeta, self.start, self.end, self.paciencia)

    @patch('scrapper_boc.requests.head')
    def test_check_url_valid(self, mock_head):
        mock_head.return_value.status_code = 200
        result = self.scrapper._check_url("http://example.com/valid")
        self.assertTrue(result)

    @patch('scrapper_boc.requests.head')
    def test_check_url_invalid(self, mock_head):
        mock_head.return_value.status_code = 404
        result = self.scrapper._check_url("http://example.com/invalid")
        self.assertFalse(result)

    @patch('scrapper_boc.requests.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_download_document(self, mock_open, mock_get):
        mock_get.return_value.content = b'Test content'
        self.scrapper._download_document("http://example.com/test.pdf", "test_boc/test.pdf")
        mock_open.assert_called_with("test_boc/test.pdf", 'wb')
        mock_open().write.assert_called_once_with(b'Test content')

    @patch('scrapper_boc.ScrapperBOC._download_document')
    @patch('scrapper_boc.ScrapperBOC._check_url')
    def test_process_url_valid(self, mock_check_url, mock_download_document):
        mock_check_url.return_value = True
        self.scrapper._process_url(1)
        mock_download_document.assert_called_once_with(self.url + "1", f"{self.carpeta}/boc_1.pdf")

    @patch('scrapper_boc.ScrapperBOC._download_document')
    @patch('scrapper_boc.ScrapperBOC._check_url')
    def test_process_url_invalid(self, mock_check_url, mock_download_document):
        mock_check_url.return_value = False
        self.scrapper._process_url(1)
        self.assertIn(self.url, self.scrapper.get_error_descarga())
        mock_download_document.assert_not_called()

    @patch('scrapper_boc.os.makedirs')
    @patch('scrapper_boc.os.path.exists')
    @patch('scrapper_boc.ThreadPoolExecutor')
    @patch('scrapper_boc.tqdm')
    @patch('scrapper_boc.time.time', side_effect=[1, 61])
    def test_run(self, mock_time, mock_tqdm, mock_executor, mock_exists, mock_makedirs):
        mock_exists.return_value = False
        self.scrapper.run()
        mock_makedirs.assert_called_once_with(self.carpeta)
        mock_executor.return_value.__enter__.return_value.map.assert_called_once()

    @patch('scrapper_boc.os.listdir', return_value=['boc_1.pdf', 'boc_2.pdf'])
    def test_last_download(self, mock_listdir):
        last_download = self.scrapper.last_download()
        self.assertEqual(last_download, 2)

    def test_tiempo_de_descargar(self):
        self.scrapper._tiempo_total = 3600  # 1 hour
        tiempo, unidad = self.scrapper.tiempo_de_descargar()
        self.assertEqual(tiempo, 1.0)
        self.assertEqual(unidad, 'horas')

    def test_get_error_descarga(self):
        self.scrapper._error_descarga = ["http://example.com/invalid"]
        errors = self.scrapper.get_error_descarga()
        self.assertEqual(errors, ["http://example.com/invalid"])

    @patch('scrapper_boc.ScrapperBOC.last_download', return_value=2)
    @patch('scrapper_boc.ScrapperBOC.run')
    def test_continua_download(self, mock_run, mock_last_download):
        self.scrapper.continua_download(5)
        self.assertEqual(self.scrapper._boc_start, 3)
        self.assertEqual(self.scrapper._boc_end, 8)
        mock_run.assert_called_once()

if __name__ == '__main__':
    unittest.main()
