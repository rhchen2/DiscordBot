import os
import requests
import json

def get_cat_facts():
  response = requests.get("https://meowfacts.herokuapp.com/")
  json_data = json.loads(response.text)
  facts = json_data['data']
  return(facts)

def get_inspiring_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def get_random_fact():
  response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
  json_data = json.loads(response.text)
  facts = json_data['text']
  return(facts)
