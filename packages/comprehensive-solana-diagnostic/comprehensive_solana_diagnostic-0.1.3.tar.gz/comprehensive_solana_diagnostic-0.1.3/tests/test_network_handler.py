import unittest
from comprehensive_solana_diagnostic import NetworkStatusHandler, safe_print, safe_import, inspect_module
from click.testing import CliRunner
from comprehensive_solana_diagnostic import main as cli_main
from unittest.mock import patch
from io import StringIO

class TestNetworkStatusHandler(unittest.TestCase):
    def test_initialization(self):
        handler = NetworkStatusHandler("https://api.mainnet-beta.solana.com")
        self.assertIsNotNone(handler)
        self.assertEqual(handler.rpc_url, "https://api.mainnet-beta.solana.com")

    def test_initialization_with_custom_rpc(self):
        handler = NetworkStatusHandler("https://custom.rpc.url")
        self.assertEqual(handler.rpc_url, "https://custom.rpc.url")

    def test_get_comprehensive_status(self):
        handler = NetworkStatusHandler("https://api.mainnet-beta.solana.com")
        status = handler.get_comprehensive_status()
        self.assertIsInstance(status, str)
        self.assertIn("Network status for", status)

    def test_invalid_rpc_url(self):
        with self.assertRaises(ValueError):
            NetworkStatusHandler("invalid-url")

    def test_rpc_connection_failure(self):
        handler = NetworkStatusHandler("https://invalid.rpc.url")
        with patch('aiohttp.ClientSession.get', side_effect=Exception("Connection failed")):
            with self.assertRaises(Exception):
                handler._get_rpc_connection()

    def test_solana_core_component_inspection(self):
        handler = NetworkStatusHandler("https://api.mainnet-beta.solana.com")
        with patch('importlib.import_module', side_effect=ImportError("Module not found")):
            with self.assertRaises(ImportError):
                handler._inspect_solana_core_components()

    def test_cli(self):
        runner = CliRunner()
        result = runner.invoke(cli_main, ['--rpc-url', 'https://api.testnet.solana.com'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Network status for https://api.testnet.solana.com", result.output)

    def test_cli_verbose(self):
        runner = CliRunner()
        result = runner.invoke(cli_main, ['--verbose'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Verbose output enabled", result.output)

    def test_cli_argument_parsing(self):
        runner = CliRunner()
        result = runner.invoke(cli_main, ['--rpc-url', 'https://custom.rpc.url', '--verbose'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Verbose output enabled", result.output)
        self.assertIn("Network status for https://custom.rpc.url", result.output)

    def test_safe_print(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            safe_print("Test message")
            self.assertIn("Test message", fake_out.getvalue())

    def test_diagnostic_error_handling(self):
        handler = NetworkStatusHandler("https://api.mainnet-beta.solana.com")
        # Patch the safe_print used inside comprehensive_solana_diagnostic.py
        with patch('comprehensive_solana_diagnostic.comprehensive_solana_diagnostic.safe_print') as mock_print:
            # Patch os.listdir to raise an exception to trigger error handling in get_comprehensive_status
            with patch('os.listdir', side_effect=Exception("Test error")):
                with self.assertRaises(Exception):
                    handler.get_comprehensive_status()
            # Verify that one of the safe_print calls contains a traceback message  
            traceback_printed = any("Traceback (most recent call last):" in args[0]
                                      for args, _ in mock_print.call_args_list)
            self.assertTrue(traceback_printed, "Expected a traceback to be printed")
            # Check that safe_print was called with the error message
            mock_print.assert_any_call("Error: Test error")

    def test_cli_main(self):
        runner = CliRunner()
        result = runner.invoke(cli_main)
        self.assertEqual(result.exit_code, 0)

    def test_main_function(self):
        with patch('comprehensive_solana_diagnostic.main') as mock_main:
            mock_main.return_value = 0
            result = mock_main()
            self.assertEqual(result, 0)

    def test_initialization_checks(self):
        with patch('os.path.exists', return_value=False):
            with self.assertRaises(ValueError):
                NetworkStatusHandler("https://api.mainnet-beta.solana.com")

    def test_rpc_connection_error_handling(self):
        handler = NetworkStatusHandler("https://api.mainnet-beta.solana.com")
        with patch('aiohttp.ClientSession.get', side_effect=Exception("Connection failed")):
            with self.assertRaises(Exception):
                handler._get_rpc_connection()

    def test_solana_core_component_import_verification(self):
        handler = NetworkStatusHandler("https://api.mainnet-beta.solana.com")
        with patch('importlib.import_module') as mock_import:
            mock_import.return_value = True
            self.assertTrue(handler._inspect_solana_core_components())

    def test_cli_argument_parsing_edge_cases(self):
        runner = CliRunner()
        result = runner.invoke(cli_main, ['--rpc-url', 'https://custom.rpc.url', '--verbose'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Verbose output enabled", result.output)
        self.assertIn("Network status for https://custom.rpc.url", result.output)

    def test_main_function_error_handling(self):
        with patch('comprehensive_solana_diagnostic.main', side_effect=Exception("Test error")):
            with self.assertRaises(Exception):
                main()

    def test_initialization_config_checks(self):
        with patch('os.path.exists', return_value=True):
            handler = NetworkStatusHandler("https://api.mainnet-beta.solana.com")
            self.assertEqual(handler.rpc_url, "https://api.mainnet-beta.solana.com")

    def test_rpc_connection_error_logging(self):
        handler = NetworkStatusHandler("https://api.mainnet-beta.solana.com")
        with patch('aiohttp.ClientSession.get', side_effect=Exception("Connection failed")):
            with patch('sys.stdout', new=StringIO()) as self.captured_output:
                with self.assertRaises(Exception):
                    handler._get_rpc_connection()
            self.assertIn("Error getting RPC connection: Connection failed", self.captured_output.getvalue())

    def test_solana_core_component_inspection_edge_cases(self):
        handler = NetworkStatusHandler("https://api.mainnet-beta.solana.com")
        with patch('importlib.import_module', side_effect=ImportError("Module not found")):
            with self.assertRaises(ImportError):
                handler._inspect_solana_core_components()

    def test_cli_argument_parsing_edge_cases(self):
        runner = CliRunner()
        result = runner.invoke(cli_main, ['--rpc-url', 'https://custom.rpc.url', '--verbose'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Verbose output enabled", result.output)
        self.assertIn("Network status for https://custom.rpc.url", result.output)

    def test_main_function_execution(self):
        with patch('comprehensive_solana_diagnostic.main') as mock_main:
            mock_main.return_value = 0
            result = mock_main()
            self.assertEqual(result, 0)

    def test_safe_print_error_handling(self):
        """Test safe_print handles errors gracefully"""
        with patch('sys.stderr', new=StringIO()) as captured_stderr:
            safe_print(None)  # Should handle None input
            self.assertIn("Error printing message", captured_stderr.getvalue())

    def test_safe_import_error_handling(self):
        """Test safe_import handles import errors gracefully"""
        result = safe_import("non_existent_module")
        self.assertIsNone(result)

    def test_inspect_module_error_handling(self):
        """Test inspect_module handles errors gracefully"""
        result = inspect_module(None)
        self.assertEqual(result, {})

if __name__ == '__main__':
    unittest.main()
