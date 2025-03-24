# OctoLingo

OctoLingo is a powerful and versatile Python package designed to simplify text translation and language processing tasks. Built with developers in mind, OctoLingo provides a seamless interface for translating text, detecting languages, and handling large-scale translation tasks efficiently. Whether you're building a multilingual application, analyzing global content, or automating translation workflows, OctoLingo has you covered.

## Key Features

### 🌍 **Multi-Language Support**
- Translate text between **100+ languages** with high accuracy.
- Automatically detect the language of input text.

### 🚀 **Efficient Large-Text Handling**
- Split large texts into manageable chunks to overcome API limitations.
- Translate large documents or datasets without hassle.
- Batch translation for large-scale projects.

### ⚡ **Asynchronous Translation**
- Perform non-blocking translations using async/await for improved performance.

### 📚 **Custom Glossaries**
- Define custom terms and their translations for domain-specific use cases.
- Ensure consistent translations for specialized vocabulary.

### 📂 **Bulk File Translation**
- Translate entire text files (e.g., `.txt`, `.csv`) with a single command.

### 📜 **Translation History**
- Log and retrieve translation history for auditing and analysis.

### 🛠️ **Developer-Friendly**
- Easy-to-use API with comprehensive documentation.
- Modular design for seamless integration into existing projects.

## Installation

Install OctoLingo via pip:

```bash
pip install octolingo
```

## Usage

### Language Validation
```python
from OctoLingo.translator import OctoLingo

translator = OctoLingo()
print(translator.validate_language('es'))  # Should return True
try:
    print(translator.validate_language('xx'))  # Should raise TranslationError
except Exception as e:
    print(e)
```

### Translating Text

```python
from OctoLingo.translator import OctoLingo

translator = OctoLingo()
translated_text, confidence = translator.translate("Hello, world!", 'es')
print(f"Translated Text: {translated_text}, Confidence: {confidence}")
```

### Batch Translation
```python
from OctoLingo.translator import OctoLingo

translator = OctoLingo()
texts = ["Hello", "Goodbye"]
results = translator.translate_batch(texts, 'es')
for translated_text, confidence in results:
    print(f"Translated Text: {translated_text}, Confidence: {confidence}")
```

### Asynchronous Translation
```python
import asyncio
from OctoLingo.translator import OctoLingo

async def translate_async():
    translator = OctoLingo()
    translated_text, confidence = await translator.translate_async("Hello, world!", 'es')
    print(translated_text)  # Output: "¡Hola, mundo!"

# Check if there's an existing event loop before running it
if __name__ == "__main__":
    try:
        # Get the current event loop
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # In a running loop (like Jupyter), directly await the function
            await translate_async()
        else:
            # If no loop is running, use asyncio.run to start the event loop
            asyncio.run(translate_async())
    except RuntimeError as e:
        print("Error: ", e)

```

### Detecting Language

```python
from OctoLingo.translator import OctoLingo

translator = OctoLingo()
lang, confidence = translator.detect_language("Hola, cómo estás?")
print(f"Detected Language: {lang}, Confidence: {confidence}")
```

### Custom Glossaries

```python
from OctoLingo.glossary import Glossary

glossary = Glossary()
glossary.add_term("Hello", "Hola")
result = glossary.apply_glossary("Hello, world!")
print(result)  # Should print "Hola, world!"
```

### Bulk File Translation

```python
from OctoLingo.translator import OctoLingo
from OctoLingo.file_handler import FileHandler

# Write test content to a file
FileHandler.write_file('input.txt', "Hello, world!")

# Translate the file content
translator = OctoLingo()
text = FileHandler.read_file('input.txt')
translated_text, _ = translator.translate(text, 'es')
FileHandler.write_file('output.txt', translated_text)

# Read and print the translated content
print(FileHandler.read_file('output.txt'))  # Should print the translated text
```

### Translation History

```python
from OctoLingo.history import TranslationHistory

history = TranslationHistory()
history.log_translation("Hello", "Hola", "en", "es")
print(history.get_history())  # Should print the logged translation
```

## Contributing
- OctoLingo is an open-source project, and contributions are welcome! If you'd like to contribute, please check out my GitHub repository for guidelines.