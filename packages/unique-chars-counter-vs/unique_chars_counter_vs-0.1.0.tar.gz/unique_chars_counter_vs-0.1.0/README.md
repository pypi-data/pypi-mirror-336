# 🖥️ Task 4 CLI Character Counter

> A command-line interface application developed as part of the Foxminded course.
> This code provides a convenient command-line tool for counting unique characters in strings or files, with error handling and performance optimization through memoization.

## 📋 Requirements
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Pytest](https://img.shields.io/badge/pytest-latest-brightgreen.svg)](https://docs.pytest.org/)
[![Coverage](https://img.shields.io/badge/coverage-pytest--cov-yellowgreen.svg)](https://pytest-cov.readthedocs.io/)

## 🚀 Installation
```bash
git clone https://git.foxminded.ua/foxstudent106775/task_4_cli.git
```

## 💻 Usage

### How to Run

1. **Open your Terminal/Command Prompt:**
   Navigate to the directory containing unique_chars.py using the `cd` command.

2. **Run the Application:**

   #### Using a String Input:
   ```bash
   python unique_chars.py --string "your string here"
   ```
   **Examples:**
   ```bash
   python unique_chars.py --string "hello world"
   python unique_chars.py --string "AaBbCc123"
   ```

   #### Using a File Input:
   ```bash
   python unique_chars.py --file "your_file.txt"
   ```
   **Examples:**
   ```bash
   # Local file
   python unique_chars.py --file "my_text.txt"
   
   # Absolute path (Unix/Linux)
   python unique_chars.py --file "/path/to/your/file/data.txt"
   
   # Absolute path (Windows)
   python unique_chars.py --file "C:\folder\file.txt"
   ```

### 🎯 Available Options

| Option | Description |
|--------|-------------|
| `--string "string"` | Specifies the input string to be analyzed (must be in double quotes) |
| `--file "file_path"` | Specifies the path to the text file to be analyzed (must be in double quotes) |

### 📝 Expected Outputs

#### ✅ Successful Execution
```bash
Number of unique characters: [number]
```
> Where `[number]` is the count of characters that appear only once in the input.

#### ❌ Error Outputs

| Error Type | Message | Description |
|------------|---------|-------------|
| ValueError | `No input provided. Use --string or --file` | No input option provided |
| FileNotFoundError | `File not found: [file_path]` | Specified file doesn't exist |
| IOError | `Error reading file: [error_message]` | File reading problems |
| Exception | `Error: [error_message]` | Other unexpected errors |

### 📊 Example Scenarios

1. **Counting unique characters in a string:**
   ```bash
   $ python unique_chars.py --string "aabbcde"
   Number of unique characters: 3  # (c, d, and e appear once)
   ```

2. **Counting unique characters in a file:**
   ```bash
   $ python unique_chars.py --file "data.txt"  # data.txt contains "122345"
   Number of unique characters: 3  # (1, 3, and 5 appear once)
   ```

## 📁 Project Structure

```
task_4_cli/
├── CollectionFramework/
│   ├── collection.py
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   └── test_collect.py
```

## 🧪 Testing

Run tests using pytest with coverage:

```bash
pytest --cov=CollectionFramework tests/
```

## 👨‍💻 Author

**Volodymyr Savchenko**

## 📄 License

[![MIT License](https://https://git.foxminded.ua/foxstudent106775/task_4_cli.git)]

---
*Made in Python*
