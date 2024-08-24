from dotenv import load_dotenv
import google.generativeai as genai
import os
import json
import time

load_dotenv()

api_key = os.getenv('api_key')

genai.configure(api_key= api_key)

model = genai.GenerativeModel('gemini-1.5-flash',
                              # Set the `response_mime_type` to output JSON
                              generation_config={"response_mime_type": "application/json"})

with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    
res_list = []
cnt=0
for item in data:
  cnt+=1
  if cnt==14:
    print("Waiting for 1.5 minutes...")
    #this wait is because the google gemini LLM api plan that i am using has limit of 15 request per minute.
    time.sleep(90)
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
  Note- Don't generate the response exactly same the ideal_response. try to make it better. use the json data for it.
  also, answer the query in the same style as query written in i.e if it in english answer it in english and same goes for Hindi, hinglish or any other language.
  in the output i want a json object which look like this:{"generated_response": "your_response"}
  also Note that: your_response is a string. please make Your_response small and to the point.

  """
  prompt = prompt + f"{item}"

  response = model.generate_content(prompt)
  print(response.text)
  response_dict = json.loads(response.text)
  temp_dict={}
  temp_dict['ticket_id'] = item['chat_context']['ticket_id']
  temp_dict['latest_query'] = item['latest_query']
  temp_dict['generated_response'] = response_dict['generated_response']
  temp_dict['ideal_response'] = item['ideal_response']
  
  res_list.append(temp_dict)

print('----------------------------------------------------------------')

output_file = 'output.json'

# Write the list to the JSON file
with open(output_file, 'w') as file:
    json.dump(res_list, file, indent=4)

print(f"Data has been written to {output_file}")
print(len(res_list))
