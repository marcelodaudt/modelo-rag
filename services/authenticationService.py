from pinecone.grpc import PineconeGRPC as Pinecone
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def authentication_pinecone():
    pc = Pinecone(api_key=os.getenv("API_KEY_PINECONE"))
    return pc

def authentication_openai():
    clientOpenAI = OpenAI(api_key=os.getenv("API_KEY_OPENAI"))

    return clientOpenAI