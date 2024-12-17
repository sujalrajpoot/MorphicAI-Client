from morphic_ai import MorphicAI, MorphicAIError

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
