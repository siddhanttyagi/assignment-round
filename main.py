from dotenv import load_dotenv
import google.generativeai as genai
import os
import json

load_dotenv()

api_key = os.getenv('api_key')

genai.configure(api_key= api_key)

model = genai.GenerativeModel('gemini-1.5-flash',
                              # Set the `response_mime_type` to output JSON
                              generation_config={"response_mime_type": "application/json"})

with open('temp.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    

for item in data:
  
  prompt = """
    I have given you the json object whose schema explination is as follow :
  {
    profile_context: {
      patient_profile -> Text data for patient's profile containing medical conditions, food preferences etc.
      program_name -> Careplan they are enrolled into
      diet_chart -> raw json data of the diet chart they have been prescribed
      diet_chart_url -> pdf of the diet chart precribed
    }
      
    latest_query -> Array of latest messages sent by the patient which we need to generate a reply for
    ideal_response -> Ideal expected response for the latest query
    chat_context: {
      ticket_id -> Unique identifier for the patient query
      ticket_created -> timestamp at which the patient asked the query
      chat_history -> historical chat messages with the patient from previous 6hrs
    }
  }
  Note - in chat_history the schema is like this : 
  1. `message` -> Contains the description of picture(LLM generated) along with the caption(if any)
  2. `asset_url` -> Actual asset link sent by the patient
  3. `role` -> Defines the message sender(*User* is patient and *Dt Disha* is our careteam)

  Use the below json data, understand the messages in chat history and reply to the query of the patient. You can see the ideal_response for your reference.
  in the output i want a json object which look like this:{"generated_response": "your_response"}
  also Note that: your_response is a string. please make Your_response small and to the point.

  """
  prompt = prompt + f"{item}"

  response = model.generate_content(prompt)
  print(response.text)