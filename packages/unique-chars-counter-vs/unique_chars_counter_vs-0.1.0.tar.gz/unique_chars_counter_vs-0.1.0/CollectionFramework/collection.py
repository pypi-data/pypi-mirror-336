from collections import Counter
import functools
import argparse

@functools.lru_cache(maxsize=None)
def unique_char_count(s: str) -> int:
    count = Counter(s)
    return sum(1 for char in count if count[char] == 1)

def process_input() -> str:
    parser = argparse.ArgumentParser(description='Count unique characters in string or file')
    parser.add_argument('--string', type=str, help='Input string')
    parser.add_argument('--file', type=str, help='Input file path')
    
    args = parser.parse_args()
    
    if args.file:
        try:
            with open(args.file, 'r') as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {args.file}")
        except Exception as e:
            raise Exception(f"Error reading file: {e}")
    elif args.string:
        return args.string
    else:
        raise ValueError("No input provided. Use --string or --file")

def main():
    try:
        input_text = process_input()
        result = unique_char_count(input_text)
        print(f"Number of unique characters: {result}")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0

if __name__ == "__main__":
    main()