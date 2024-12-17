# MorphicAI Client

## Overview
MorphicAI Client is a Python-based SDK designed to interact with the MorphicAI API. It provides a structured and user-friendly interface to send queries, receive responses, and handle streaming data efficiently. This implementation follows modern software design principles, including the use of custom exceptions and abstract base classes.

## Features
- **Easy API Interaction**: Send queries to the MorphicAI API and receive responses effortlessly.
- **Streaming Support**: Stream responses in real-time with optional console output.
- **Error Handling**: Robust custom error classes to manage various failure scenarios, including network issues and API limits.
- **Extensibility**: Built with object-oriented principles, making it easy to extend and customize.

## Installation
Ensure you have Python 3.7 or higher installed. Install the required dependencies using:

```bash
pip install requests
```

## Usage
### Example
```python
from morphic_ai import MorphicAI, MorphicAIError

client = MorphicAI()

try:
    response = client.query('What is the current AQI in New Delhi?')

    print('\n' + '=' * 60)
    if response.results:
        for i, result in enumerate(response.results, start=1):
            print(f"Result {i}: {result}\n")

    print('=' * 60)
    print("Streaming Response:", response.streaming_response)

    print('=' * 60)
    if response.related_queries:
        for i, query in enumerate(response.related_queries, start=1):
            print(f"Related Query {i}: {query['query']}\n")
except MorphicAIError as e:
    print(f"Error: {e}")
```

### Output
Upon running the example, the client streams the response to the console in real-time. Once completed, it displays any related results and queries.

## API Reference
### Classes
#### `MorphicAI`
- **Methods**:
  - `query(query: str, stream: bool = True) -> MorphicAIResponse`
    - Sends a query to the MorphicAI API.
    - **Parameters**:
      - `query`: The input question or command.
      - `stream`: Whether to stream the response in real-time (default: `True`).
    - **Returns**: `MorphicAIResponse` object containing the streaming response, results, and related queries.

#### `MorphicAIError`
- Base class for all custom errors.

#### `RequestError`
- Raised for HTTP-related issues.

#### `LimitReachedError`
- Raised when the daily API limit for guest users is reached.

### Data Classes
#### `MorphicAIResponse`
- **Attributes**:
  - `streaming_response`: The real-time response from the API.
  - `results`: Parsed results from the API response.
  - `related_queries`: Suggested related queries.

## Acknowledgments
- [MorphicAI](https://www.morphic.sh/) for providing the API.

## Disclaimer ⚠️

**IMPORTANT: EDUCATIONAL PURPOSE ONLY**

This library interfaces with the MorphicAI search API for educational purposes only. It is not intended to harm or exploit the https://www.morphic.sh/ website in any way.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact
For questions or support, please open an issue or reach out to the maintainer.

## Contributing

Contributions are welcome! Please submit pull requests or open issues on the project repository.
