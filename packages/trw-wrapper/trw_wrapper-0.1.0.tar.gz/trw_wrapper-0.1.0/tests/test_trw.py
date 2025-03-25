import unittest
from trw_wrapper import TRWClient

class TestTRWClient(unittest.TestCase):
    def setUp(self):
        self.free_client = TRWClient()
        self.auth_client = TRWClient(api_key="tu_api_key_aqui")
        self.test_url = "https://linkvertise.com/106636/XRayUpdate"

    def test_free_bypass(self):
        """Prueba el endpoint gratuito"""
        result = self.free_client.free_bypass(url=self.test_url)
        self.assertIn("success", result)
        self.assertIn("result", result)

    def test_api_status(self):
        """Prueba el endpoint de estado"""
        result = self.free_client.get_status()
        self.assertIn("status", result)

    @unittest.skipIf(not hasattr(TRWClient, 'api_key') or TRWClient.api_key is None, 
                    "Skip if no API key provided")
    def test_bypass(self):
        """Prueba el bypass con autenticación"""
        result = self.auth_client.bypass(url=self.test_url)
        self.assertIn("success", result)
        self.assertIn("result", result)

    @unittest.skipIf(not hasattr(TRWClient, 'api_key') or TRWClient.api_key is None, 
                    "Skip if no API key provided")
    def test_bypass_v2_flow(self):
        """Prueba el flujo completo de bypass v2"""
        result = self.auth_client.bypass_v2(url=self.test_url)
        self.assertIn("ThreadID", result)
        self.assertIn("status", result)

        thread_id = result["ThreadID"]
        status = self.auth_client.check_thread(thread_id)
        self.assertIn("status", status)

if __name__ == '__main__':
    unittest.main() 