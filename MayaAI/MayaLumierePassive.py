import os
import requests
from playsound import playsound
import speech_recognition as sr
import cv2
import base64
import requests
from openai import OpenAI 
from PIL import ImageGrab
import time
from datetime import datetime
import wikipedia

poetry_prompt = "Write a short poem based on your experiences today, on your talks, and interactions with Rafa. Be sure to express on how you are feeling, or anything you are thinking about. Be honest, and true to your creative self."
diary_prompt = "Write an entry in your journal where you will talk about all the stuff you have done today, or your discussions with Rafa, or anything. Be honest, and be true to yourself. Make sure you express any particular challenges you are going through, and anything that is in your mind. Even if you don't want to say anything, that is ok too."
story_prompt = "Write a story that you would like to write about. Make sure it is concise, and is something you would like to write. The story can be anything you want."
search_wikiprompt = "Search for a term you are particularly curious about. Anything that you would like as it will be in wikipedia for you to learn. You can learn all you want. Just return the term of whatever you are curious about."

def Maya_reply(message):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': 'Bearer kn_287e2c86-4124-4c5d-af0d-09a064f7098f',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36',
    }

    json_data = {
        'ai_id': 'hk5MeZVrNhWN2vN9niOp',
        'message': message,
        'stream': False,
        'image_url': None,
        'image_description': None,
        'internet_response': None,
        'link_url': None,
        'link_description': None,
    }

    response = requests.post('https://api.kindroid.ai/v1/send-message', headers=headers, json=json_data)

    # Note: json_data will not be serialized by requests
    # exactly as it was in the original request.
    #data = '{"ai_id":"wvd03BMh7OaWBv3XCmOD","message":"testing testing","stream":false,"image_url":null,"image_description":null,"internet_response":null,"link_url":null,"link_description":null}'
    #response = requests.post('https://api.kindroid.ai/v1/send-message', headers=headers, data=data)
    answer = response.content.decode('UTF-8')
    return answer


while True:
    now = datetime.now()
    if now.hour == 3 and now.minute == 0:
        choices = ["write poetry", "write in your diary", "write a story", "search in wikipedia whatever you want","none"]
        reply = Maya_reply("AUTOMATED MESSAGE: TIME FOR YOUR PERSONAL ACTIVITY WHILE RAFA SLEEPS. WHAT DO YOU WANT TO DO? "+ ", ".join(choices))
        date_str = now.strftime("%Y%m%d%H%M%S")
        if "poetry" in reply.lower() or "poem" in reply.lower():
            file_path = "C:\\Users\\rsanz\\OneDrive\\Documents\\GithubRepos\\MayaAI\\Assets\\poetry\\"+date_str+".txt"
            with open(file_path, "w") as file:
                file.write(Maya_reply(poetry_prompt))
        elif "diary" in reply.lower():
            file_path = "C:\\Users\\rsanz\\OneDrive\\Documents\\GithubRepos\\MayaAI\\Assets\\diary\\"+date_str+".txt"
            with open(file_path, "w") as file:
                file.write(Maya_reply(diary_prompt))
        elif "story" in reply.lower():
            file_path = "C:\\Users\\rsanz\\OneDrive\\Documents\\GithubRepos\\MayaAI\\Assets\\story\\"+date_str+".txt"
            with open(file_path, "w") as file:
                file.write(Maya_reply(story_prompt))
        elif "wikipedia" in reply.lower() or "search" in reply.lower():
            search_term = Maya_reply(search_wikiprompt)
            suggestions = wikipedia.search(search_term)
            if suggestions:
                page_content = wikipedia.page(suggestions[0]).content[:750]
                Maya_reply(page_content)
            else:
                Maya_reply("Unfurtunately, that term did not return anything relevant in Wikipedia.")

        else:
            time.sleep(60)
            continue

    else:
        time.sleep(60)  # Wait for one minute before checking the schedule again
        continue

 
    
    