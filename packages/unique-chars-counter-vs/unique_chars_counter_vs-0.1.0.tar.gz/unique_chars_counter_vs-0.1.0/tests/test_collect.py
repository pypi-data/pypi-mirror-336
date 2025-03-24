import os
import pytest
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from CollectionFramework.collection import unique_char_count, process_input
from unittest.mock import mock_open, patch

@pytest.mark.parametrize("test_input,expected", [
    ("testXixiknaXaxa", 4),
    ("aaaa", 0),
    ("xaxaxa", 0),
    ("", 0),
    ("abcdef", 6),
])
def test_unique_char_count(test_input, expected):
    assert unique_char_count(test_input) == expected
    
def test_cache_info():
    unique_char_count.cache_clear()
    initial_info = unique_char_count.cache_info()
    assert initial_info.hits == 0
    assert initial_info.misses == 0
    assert initial_info.currsize == 0
    
    result1 = unique_char_count("test")
    first_call_info = unique_char_count.cache_info()
    assert first_call_info.hits == 0
    assert first_call_info.misses == 1
    assert first_call_info.currsize == 1

    result2 = unique_char_count("test")
    second_call_info = unique_char_count.cache_info()
    assert second_call_info.hits == 1
    assert second_call_info.misses == 1
    assert second_call_info.currsize == 1

class TestCLI:
    @patch('argparse.ArgumentParser.parse_args')
    def test_process_string_input(self, mock_args):
        mock_args.return_value.string = "test"
        mock_args.return_value.file = None
        
        result = process_input()
        assert result == "test"

    @patch('builtins.open', new_callable=mock_open, read_data="test data")
    @patch('argparse.ArgumentParser.parse_args')
    def test_process_file_input(self, mock_args, mock_file):
        mock_args.return_value.file = "test.txt"
        mock_args.return_value.string = None
        
        result = process_input()
        assert result == "test data"
        mock_file.assert_called_once_with("test.txt", "r")

    @patch('builtins.open', new_callable=mock_open, read_data="file data")
    @patch('argparse.ArgumentParser.parse_args')
    def test_file_priority(self, mock_args, mock_file):
        mock_args.return_value.string = "string data"
        mock_args.return_value.file = "test.txt"
        
        result = process_input()
        assert result == "file data"
        mock_file.assert_called_once_with("test.txt", "r")