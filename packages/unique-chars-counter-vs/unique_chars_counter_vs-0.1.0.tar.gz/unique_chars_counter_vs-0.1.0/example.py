#!/usr/bin/env python3
"""
Example script demonstrating the usage of the unique character counter.
This script provides sample usage scenarios for both string and file inputs.
"""

import os
from CollectionFramework.collection import count_unique_chars

def demonstrate_string_examples():
    """Demonstrate counting unique characters in strings."""
    print("\n=== String Input Examples ===")
    
    examples = [
        "hello world",
        "aabbcde",
        "AaBbCc123",
        "11223344",
        "Python Programming!",
        "",  # Empty string test
        " ",  # Space only test
        "!@#$%^&*()"  # Special characters test
    ]
    
    for text in examples:
        try:
            result = count_unique_chars(text)
            print(f'\nInput: "{text}"')
            print(f"Unique characters count: {result}")
        except Exception as e:
            print(f'Error processing "{text}": {e}')

def demonstrate_file_example():
    """Demonstrate counting unique characters from a file."""
    print("\n=== File Input Example ===")
    
    sample_file = "sample.txt"
    sample_text = "This is a sample text file.\nIt contains multiple lines!\n123321"
    
    try:
        # Write sample content to file
        with open(sample_file, "w", encoding="utf-8") as f:
            f.write(sample_text)
        
        # Read and process the file
        with open(sample_file, "r", encoding="utf-8") as f:
            content = f.read()
            result = count_unique_chars(content)
            print('\nFile content:')
            print(sample_text)
            print(f"\nUnique characters count: {result}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up the sample file
        if os.path.exists(sample_file):
            try:
                os.remove(sample_file)
            except Exception as e:
                print(f"Warning: Could not remove sample file: {e}")

def main():
    """Main function to run all examples."""
    print("=== Unique Character Counter Examples ===")
    
    try:
        demonstrate_string_examples()
        demonstrate_file_example()
    except KeyboardInterrupt:
        print("\nExample demonstration interrupted by user")
    except Exception as e:
        print(f"\nUnexpected error occurred: {e}")

if __name__ == "__main__":
    main() 