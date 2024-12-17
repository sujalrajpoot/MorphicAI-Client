import requests
import json
import random
import string
from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass

class MorphicAIError(Exception):
    """Base class for all MorphicAI-related errors."""
    pass

class RequestError(MorphicAIError):
    """Raised when an error occurs during the HTTP request."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code

class LimitReachedError(MorphicAIError):
    """Raised when the daily limit for guest users is reached."""
    pass

@dataclass
class MorphicAIResponse:
    streaming_response: str
    results: Optional[List[Dict[str, Any]]] = None
    related_queries: Optional[List[Dict[str, Any]]] = None

class MorphicAIClient(ABC):
    @abstractmethod
    def query(self, query: str, stream: bool = True) -> MorphicAIResponse:
        pass

class MorphicAI(MorphicAIClient):
    BASE_URL = 'https://www.morphic.sh/api/chat-stream'
    HEADERS = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://www.morphic.sh',
        'priority': 'u=1, i',
        'referer': 'https://www.morphic.sh/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    @staticmethod
    def _generate_message_id() -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    def query(self, query: str, stream: bool = True) -> MorphicAIResponse:
        payload = {
            'messages': [
                {
                    'role': 'user',
                    'content': query.strip(),
                    'type': 'input',
                    'id': self._generate_message_id(),
                    'status': 'done',
                },
            ],
            'include_images': True,
        }

        try:
            with requests.Session() as session:
                response = session.post(self.BASE_URL, headers=self.HEADERS, json=payload, stream=True)
                response.raise_for_status()

                streaming_response = ""
                results = []
                related_queries = []

                for line in response.iter_lines(decode_unicode=True):
                    if line:
                        try:
                            data = json.loads(line)
                            if 'GUEST_LIMIT_REACHED' in line:
                                raise LimitReachedError("Daily limit reached for guest users.")

                            if data['type'] == 'tool':
                                results = data.get('toolInvocation', {}).get('result', {}).get('results', [])
                            elif data['type'] == 'answer':
                                content = data.get('content', "")
                                streaming_response += content
                                if stream:
                                    print(content, end='', flush=True)
                            elif data['type'] == 'related':
                                related_queries = data.get('data', {}).get('items', [])
                        except:continue

                return MorphicAIResponse(
                    streaming_response=streaming_response,
                    results=results,
                    related_queries=related_queries,
                )
        except requests.exceptions.RequestException as e:
            raise RequestError(f"HTTP request failed: {str(e)}", status_code=e.response.status_code if e.response else None)

if __name__ == "__main__":
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
