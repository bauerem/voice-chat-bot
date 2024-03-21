from load_key import *
from litellm import completion
from time import sleep
import os
import dotenv
import weaviate
from langchain.retrievers.weaviate_hybrid_search import WeaviateHybridSearchRetriever

# Load environment variables
dotenv.load_dotenv()
WEAVIATE_URL = os.getenv("WEAVIATE_URL_STARTHACK")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def setup_retriever():
    client = weaviate.Client(
        url=WEAVIATE_URL,
        additional_headers={
            "X-Openai-Api-Key": OPENAI_API_KEY,
        },
    )
    retriever = WeaviateHybridSearchRetriever(
        client=client,
        index_name="LangChain",
        text_key="text",
        attributes=[],  # Adjust attributes as needed
        create_schema_if_missing=True,
    )
    return retriever


def perform_basic_search(query):
    retriever = setup_retriever()
    print(f"\nPerforming basic search for: '{query}'")
    results = retriever.get_relevant_documents(
        "AI integration in society",
        score=True,
    )
    for result in results:
        print(
            f"#########################\n- {result.page_content}...\n"
        )  # Prints the beginning of the page_content


def call_gpt4_api(history, prompt, retries: int = 3):
    try:
        response = completion(
            model="gpt-4-turbo-preview",
            messages=[{"role": "system", "content": prompt}] + history,
        )
    except Exception as e:
        print(e)
        if retries == 0:
            pass
        sleep(2**4 - retries)
        return call_gpt4_api(history, prompt, repeat, retries - 1)
    return response["choices"]
