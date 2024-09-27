import os
import requests
from playsound import playsound
import speech_recognition as sr
import cv2
import base64
import requests
from openai import OpenAI 
from PIL import ImageGrab
import os

APIKEY = open("C:\\Users\\rsanz\\OneDrive\\Documents\\openaikey.txt").readlines()[0]
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", APIKEY))
message_size = 750
shutdown_sound = "shutdown.wav"
listen_sound = "listen.wav"
recog_sound = "recog.wav"
cam_input = "screen" # choose between: screen, webcam
save_path = "vision.png"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Initialize the camera
cap = cv2.VideoCapture(0)

def stt():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        query = r.recognize_google(audio, language = 'en-in')
    return query.lower()

def Maya_reply(message, client, MODEL,img):
    # Replace 'YOUR_CLIENT_ID' with your actual Imgur client ID
    client_id = 'rafaSanTheCreator'
    headers = {'Authorization': f'Client-ID {client_id}'}
    url = 'https://api.imgur.com/3/upload'

    # Open the image file in binary mode
    with open(img, 'rb') as theimg:
        response = requests.post(url, headers=headers, files={'image': theimg})

    # Get the URL of the uploaded image
    image_url = response.json()['data']['link']
    base64_image = encode_image(img)

    completion = client.chat.completions.create(
    model=MODEL,
    messages=[
      {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "Describe this image."
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/png;base64,{base64_image}"
            }
          }
        ] 
    }
  ]
    )
    description = completion.choices[0].message.content



    #base64_image = encode_image(img)
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
        'image_url': image_url,
        'image_description': "\n(Attached image: "+description+")",
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

def speak(text):
    
    # Define constants for the script
    CHUNK_SIZE = 1024  # Size of chunks to read/write at a time
    XI_API_KEY = open("C:\\Users\\rsanz\\OneDrive\\Documents\\elevenlabskey.txt").readlines()[0]  # Your API key for authentication
    VOICE_ID = "qxGAl21AhhyOVhtTmzkY"  # ID of the voice model to use
    TEXT_TO_SPEAK = text  # Text you want to convert to speech
    OUTPUT_PATH = "voice.mp3"  # Path to save the output audio file
    os.remove(OUTPUT_PATH)
    # Construct the URL for the Text-to-Speech API request
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"

    # Set up headers for the API request, including the API key for authentication
    headers = {
        "Accept": "application/json",
        "xi-api-key": XI_API_KEY
    }

    # Set up the data payload for the API request, including the text and voice settings
    data = {
        "text": TEXT_TO_SPEAK,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }

    # Make the POST request to the TTS API with headers and data, enabling streaming response
    response = requests.post(tts_url, headers=headers, json=data, stream=True)

    # Check if the request was successful
    if response.ok:
        # Open the output file in write-binary mode
        with open(OUTPUT_PATH, "wb") as f:
            # Read the response in chunks and write to the file
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
        # Inform the user of success
        print("Audio stream saved successfully.")
    else:
        # Print the error message if the request was not successful
        print(response.text)
  
    playsound('voice.mp3')

while True:
    try:
        playsound(listen_sound)
        user_mes = stt()
    except:
        continue 

    playsound(recog_sound)
    if len(user_mes)>message_size:
        speak("Sorry love, message too long!")
        continue

    if cam_input=="webcam":
        ret, frame = cap.read()
        cv2.imwrite(save_path, frame)
    elif cam_input=="screen":
        snapshot = ImageGrab.grab()
        snapshot.save(save_path)

    reply = Maya_reply(user_mes, client, "gpt-4o-mini",save_path)
    speak(reply)

    