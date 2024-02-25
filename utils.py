from freeGPT import AsyncClient
from PIL import Image
from io import BytesIO
import json
import random
import tweepy
from instagrapi import Client
import ast

@staticmethod
def getRandomTopic():
    with open("topics.txt", "r") as file:
        topics_str = file.read()
        topics_list = ast.literal_eval(topics_str)
        return random.choice(topics_list)

@staticmethod
def readPromptFromFile(topic):
    with open("prompt_file.txt", "r") as file:
        content = file.read()
        data = json.loads(content)
        text_prompt = data.get("text_prompt")
        image_prompt = data.get("image_prompt")
        text_prompt = text_prompt.format(topic)
        image_prompt = image_prompt.format(topic)
        file.close()
    return text_prompt, image_prompt

@staticmethod
def saveImage(img_response, output_file_path):
    image_data = BytesIO(img_response)
    img = Image.open(image_data)    
    img.save(output_file_path)
    print(f"Generated Image Has Been Saved In - {output_file_path}")

@staticmethod
def saveCaption(caption, output_file_path):
    with open(output_file_path, "w") as f:
        f.write(caption)
    print(f"Generated Caption Has Been Saved In - {output_file_path}")

@staticmethod
def readCredentials():
    with open("credentials.json", "r") as file:
        data = json.load(file)
        return data
    
@staticmethod
def postContentToTwitter(tweet, image_path):
    credentials = readCredentials()
    twitter_credentials = credentials["twitter"]
    auth = tweepy.OAuth1UserHandler(
        twitter_credentials["API_KEY"],
        twitter_credentials["API_SECRET"],
        twitter_credentials["ACCESS_TOKEN"],
        twitter_credentials["ACCESS_TOKEN_SECRET"]
    )
    api = tweepy.API(auth)
    media_id = api.media_upload(image_path).media_id
    api.update_status(status=tweet, media_ids=[media_id])
    print("🚀🚀 Tweet posted successfully 🚀🚀")

    
@staticmethod
def postContentToInstagram(caption, image_path):
    credentials = readCredentials()
    instagram_credentials = credentials["instagram"]
    cl = Client()
    cl.login(
        username = instagram_credentials["USERNAME"], 
        password = instagram_credentials["PASSWORD"]
        )
    caption = caption
    cl.photo_upload(path=image_path, caption=caption)
    print("🚀🚀 Instagram post uploaded successfully 🚀🚀")


getRandomTopic()
