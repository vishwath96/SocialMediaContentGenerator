from freeGPT import AsyncClient
import argparse
from utils import *
import asyncio
import time
import os


async def generateImage(input_topic):
    run_model = True
    while run_model:
        try:
            resp = await AsyncClient.create_generation("prodia", input_topic)
            print(f"🤖: Image has been generated")
            output = resp
        except Exception as e:
            print(f"🤖: Unable to generate image due to exception:- {e}")
            output = None
        run_model = False
    return output

async def generateCaption(prompt):
    run_model = True
    while run_model:
        try:
            resp = await AsyncClient.create_completion("gpt4", prompt)
            print(f"🤖: Caption has been generated")
            output = resp.encode('utf-16', 'surrogatepass').decode('utf-16')
        except Exception as e:
            print(f"🤖: Unable to generate image due to exception:- {e}")
            output = None
        run_model=False
    return output


if __name__ == "__main__":
    print("🚀🚀🚀🚀 Running social media content generator 🚀🚀🚀🚀")
    parser = argparse.ArgumentParser(description="Generate & Post Content on Social Media")
    parser.add_argument("-topic", "--topic", type=str, default="", help="Topic for generating content")
    parser.add_argument("-dir", "--directory", type=str, default="", help="Folder to save the generated content")
    parser.add_argument("-tweet", "--tweet", type=bool, default=False, help="Flag to tweet on Twitter")
    parser.add_argument("-post", "--post", type=bool, default=False, help="Flag to post on Instagram")

    input_args = vars(parser.parse_args())    
    epoch = int(time.time())

    input_topic = input_args["topic"]
    if input_topic == "":
        input_topic = getRandomTopic()

    text_prompt, image_prompt = readPromptFromFile(input_topic)
    output_directory = input_args["directory"]

    if output_directory == "":
        output_directory = "."
    output_directory = output_directory + "/" + f"{input_topic}_{epoch}"

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    image = asyncio.run(generateImage(image_prompt))
    caption = asyncio.run(generateCaption(text_prompt))

    image_path = output_directory + "/image.png"
    caption_path = output_directory + "/caption.txt"

    if image and caption:
        saveImage(image, image_path)
        saveCaption(caption, caption_path) 
        
        if input_args["tweet"]:
            postContentToTwitter(caption, image_path)
        if input_args["post"]:
            postContentToInstagram(caption, image_path)

    else:
        print(f"🤖: Could not generate image or caption.")
