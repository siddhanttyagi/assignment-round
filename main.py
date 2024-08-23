from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

api_key = os.getenv('api_key')

genai.configure(api_key= api_key)

model = genai.GenerativeModel('gemini-1.5-flash',
                              # Set the `response_mime_type` to output JSON
                              generation_config={"response_mime_type": "application/json"})

prompt = """
  List 5 popular cookie recipes.
  Using this JSON schema:
    Recipe = {"recipe_name": str}
  Return a `list[Recipe]`
  """

response = model.generate_content(prompt)
print(response.text)