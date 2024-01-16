import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
class_names = json.load(open('app/class_indices.json'))

def fetchAICompletion (prompt):
  OpenAiApi = 'https://api.openai.com/v1/chat/completions'
  OpenAiModel = "gpt-3.5-turbo-1106"
  OpenAiKey = os.getenv('OPENAI_API_KEY')
  data ={
        "model": OpenAiModel,
        "response_format": { "type": "json_object" },
        "messages": [
          {
            "role": "system",
            "content": "You are a helpful assistant designed to output JSON.",
          },
          {
            "role":"user",
            "content": prompt
          }
        ]
  }
  headers={
          'Content-Type': 'application/json',
          "Authorization": f'Bearer {OpenAiKey}',
  }
  try:
    result = requests.post(OpenAiApi,headers=headers, json=data).json()
    return result['choices'][0]['message']['content']
  except Exception as error:
    print(error)

def class_format(name):
  arr = name.split('-') 
  if arr[0] in arr[1]:
    return arr[1].replace(arr[0],"")
  return arr[1]

def save_json(data, pathname="app/class_indices.json"):
  json_object = json.dumps(data, indent=4)
  with open(pathname, "w") as outfile:
      outfile.write(json_object)

def search_class_treatment(lang="pt-BR"):
  class_names_obj = []
  # class_format = lambda name: name.split('-')[1]
  for class_name in class_names:
    obj = {class_name:{}}
    if not ("healthy" in class_name):
      disease = class_format(class_name)
      prompt = f'Translate the plant disease name {disease} to ${lang} and return a descritive text how to treat in {lang} within a json with the keys disease and treatment '
      treatment = json.loads(fetchAICompletion(prompt))
      # print(treatment)
      obj[class_name]= {
        'disease':   treatment['disease'],
        'treatment': treatment['treatment']
      }
    class_names_obj.append(obj)
    # break
  save_json(class_names_obj)
search_class_treatment()



