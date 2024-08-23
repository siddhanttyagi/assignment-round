from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

api_key = os.getenv('api_key')

genai.configure(api_key= api_key)

