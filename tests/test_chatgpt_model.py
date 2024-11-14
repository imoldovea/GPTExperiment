# File: test_chatgpt_model.py

import unittest
from unittest.mock import patch, Mock

from chatgpt_model import ChatGPTModel


class TestChatGPTModel(unittest.TestCase):

    @patch('chatgpt_model.openai.ChatCompletion.create')
    def test_generate_response_with_history(self, mock_openai_create):
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Test response"))]
        mock_openai_create.return_value = mock_response

        model = ChatGPTModel(model='gpt-3.5-turbo', role='user')
        model.history = []
        model.max_tokens = 150
        model.temperature = 0.7

        prompt = "Hello, how are you?"
        response = model.generate_response(prompt, use_history=True)

        self.assertEqual(response, "Test response")
        self.assertEqual(len(model.history), 2)
        self.assertEqual(model.history[0]['content'], prompt)
        self.assertEqual(model.history[1]['content'], "Test response")

    @patch('chatgpt_model.openai.ChatCompletion.create')
    def test_generate_response_without_history(self, mock_openai_create):
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Test response"))]
        mock_openai_create.return_value = mock_response

        model = ChatGPTModel(model='gpt-3.5-turbo', role='user')
        model.history = []
        model.max_tokens = 150
        model.temperature = 0.7

        prompt = "Hello, how are you?"
        response = model.generate_response(prompt, use_history=False)

        self.assertEqual(response, "Test response")
        self.assertEqual(len(model.history), 0)

    @patch('chatgpt_model.openai.ChatCompletion.create', side_effect=Exception("API error"))
    def test_generate_response_error_handling(self, mock_openai_create):
        model = ChatGPTModel(model='gpt-3.5-turbo', role='user')
        model.history = []
        model.max_tokens = 150
        model.temperature = 0.7

        prompt = "Hello, how are you?"
        response = model.generate_response(prompt, use_history=True)

        self.assertIn("A model error occurred: API error", response)
        self.assertEqual(len(model.history), 1)
        self.assertEqual(model.history[0]['content'], prompt)


if __name__ == '__main__':
    unittest.main()