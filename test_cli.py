import unittest
from unittest.mock import Mock, patch, mock_open
import json
import sys
import os
import requests

# add the parent dit to the path so we can import cli
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cli
import config

class TestClaudeCLI(unittest.TestCase):
    """test cases for the ClaudeCLI class."""

    def setUp(self):
        """setup test fixtures"""
        self.api_key = "test_api_key"
        self.claude_cli = cli.ClaudeCLI(self.api_key)

    def test_init_with_api_key(self):
        """test ClaudeCLI init with API key"""
        self.assertEqual(self.claude_cli.api_key, self.api_key)
        self.assertEqual(self.claude_cli.base_url, config.API_BASE_URL)
        self.assertEqual(self.claude_cli.conversation_history, [])

    def test_init_without_api_key(self):
        """test without api key raises valueError"""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError) as context:
                cli.ClaudeCLI()
            self.assertIn("API key required", str(context.exception))

    @patch.dict(os.environ, {config.API_KEY_ENV_VAR: "env_api_key"})
    def test_init_with_env_api_key(self):
        """test CC intialization with env. var. API Key"""
        claude_cli = cli.ClaudeCLI()
        self.assertEqual(claude_cli.api_key, "env_api_key")

    def test_clear_conversation(self):
        """test conversation clearing func"""
        # add some conversation history
        self.claude_cli.conversation_history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there"}
        ]

        # clear and verify
        self.claude_cli.clear_conversation()
        self.assertEqual(self.claude_cli.conversation_history, [])

    def test_save_conversation(self):
        test_conversation = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there"}
        ]
        self.claude_cli.conversation_history= test_conversation

        # mock file writing
        with patch('builtins.open', mock_open()) as mock_file:
            result = self.claude_cli.save_conversation("test.json")

            #verify the function returns true
            self.assertTrue(result)

            # verify the file opened correctly, and verify json was written 
            mock_file.assert_called_once_with("test.json", 'w', encodings='utf-8')
            mock_file().write.assert_called()

    def test_load_conversation(self):
        """test conversation loading functionality"""
        test_conversation = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there"}
        ]
        self.claude_cli.conversation_history = test_conversation

        # mock file reading
        with patch('builtins.open', mock_open(read_data=json.dumps(test_conversation))):
            result = self.claude_cli.load_conversation("test.json")

            # verify the func returns True, and the convo was loaded
            self.assertTrue(result)
            self.assertEqual(self.claude_cli.conversation_history, test_conversation)

    @patch('requests.post')
    def test_send_message_success(self, mock_post):
        """test successfil message sending"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "content": [{"text": "Hello! How can I help you?"}],
            "usage": {"input_tokens": 10, "output_tokens": 15},
            "model": "claude-3-sonnet-20240229"
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        # test message sending
        result = self.claude_cli.send_message("Hello")

        # verify result
        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Hello! How can I help you?")
        self.assertEqual(len(self.claude_cli.conversation_history), 2)


    @patch('request.post')
    def test_send_message_api_error(self, mock_post):
        """test API error handling"""
        mock_post.side_effect = requests.exceptions.RequestException("Connection error")

        # test message sending
        result = self.claude_cli.send_message("Hello")
        
        # verify the error handling
        self.assertFalse(result["success"])
        self.assertIn("API request failed", result["error"])
        self.assertIsNone(result["message"])

class TestConfig(unittest.TestCase):
    """Test cases for the config module"""

    def test_api_headers(self):
        """test api headers generation"""
        api_key = "test_key"
        headers = config.get_api_headers(api_key)

        self.assertEqual(headers["x-api-key"], api_key) 
        self.assertEqual(headers["anthropic-version"], config.API_VERSION) 
        self.assertEqual(headers["content-type"], "application/json") 

    def test_constants(self):
        """test config constants"""
        self.assertIsInstance(config.DEFAULT_MODEL, str)
        self.assertIsInstance(config.DEFAULT_MAX_TOKENS, int)
        self.assertIsInstance(config.API_BASE_URL, str)
        self.assertIsInstance(config.CLI_NAME, str)
        self.assertIsInstance(config.ERROR_MESSAGES, dict)
        self.assertIsInstance(config.SUCCESS_MESSAGES, dict)

if __name__ == '__main__':
    # run the tests
    unittest.main(verbosity=2)