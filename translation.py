from googletrans import Translator
from gtts import gTTS
import os
import subprocess
import json
import ffmpeg
# Function to translate text


def translate_text(input_text, target_language):
    translator = Translator()
    translated = translator.translate(
        input_text, src="en", dest=target_language)
    return translated.text

input_file_path = "./texts.json"
output_file_path = "./texts_translated.json"

def translateData():
    print("flag")
    # Input and output file paths
    # input_file_path = r"C:\Users\Sumit\OneDrive\Desktop\input.txt"
    # output_file_path = r"C:\Users\Sumit\OneDrive\Desktop\output.txt"

    # Desired target language (e.g., 'fr' for French)
    # target_language = input("Enter the desired language code: ")
    target_languages = ["hi", "ur","gu", "mr",
                        "te", "kn", "ml", "ta", "or", "bn"]

    result = dict()

    input_file = open(input_file_path, "r")
    press_releases_list = json.load(input_file)
    input_file.close()
    # print(type(press_releases_list[0]))

    for lang in target_languages:
        # print(lang)
        result[lang] = []
        for press_release in press_releases_list:
            # print(len(press_release))
            translated_press_release = translate_text(press_release, lang)
            result[lang].append(translated_press_release)

    # txt = translate_text(press_releases_list[0],target_languages[7])
    # with open("fml.txt","w",encoding="utf-8") as f:
    #     f.write(txt)
    # print(result)


    translated_obj = json.dumps(result)

    with open(output_file_path, "w") as output_file:
        output_file.write(translated_obj)


# translateData()

# # Read text from the input file
# with open(input_file_path, 'r', encoding='utf-8') as input_file:
#     input_text = input_file.read()

# # Translate the text
# translated_text = translate_text(input_text, target_language)

# # Save the translated text to the output file
# with open(output_file_path, 'w', encoding='utf-8') as output_file:
#     output_file.write(translated_text)

def convertTextToSpeech():
    input_file = open(output_file_path,"r")
    translated_releases = json.load(input_file)
    for lang in translated_releases:
        releases = translated_releases[lang]
        count = 1
        for release in releases:
            speech = gTTS(text=release,lang=lang,slow=False)  
            speech.save(f"./speech/{lang}-rel{count}.mp3")  
            count += 1

# convertTextToSpeech()

# Text to Speech
# with open(output_file_path,"r",encoding='utf-8') as file:
#     text = file.read()
# speech=gTTS(text=text, lang= target_language, slow=False)
# speech.save("text.mp3")

# #Speech to Video
# image_file = r"C:\Users\Sumit\OneDrive\Desktop\Sumithra\download.jpeg"
# audio_file = "text.mp3"
# output_file = r"C:\Users\Sumit\OneDrive\Desktop\Sumithra\output.mp4"

def merge_images_and_audio(image_path, audio_path, output_path):
    # Define the input streams for the images and audio
    input_images = ffmpeg.input(image_path, pattern_type='glob', framerate=30, executable='E:\Projects\sih_hackathon\ffmpeg-2023-09-07-git-9c9f48e7f2-full_build\ffmpeg-2023-09-07-git-9c9f48e7f2-full_build\bin')

    input_audio = ffmpeg.input(audio_path)

    # Use the concat filter to combine the images into a single video stream
    video = input_images.filter('concat', v=1)

    # Combine the video and audio streams into a single output stream
    output = ffmpeg.output(video, input_audio, output_path)

    # Run the ffmpeg command to generate the output video file
    ffmpeg.run(output)

def convertSpeechToVideo():
    # subprocess.call(['ffmpeg', '-loop', '1', '-i', image_file, '-i', audio_file, '-c:v', 'libx264', '-tune', 'stillimage', '-c:a', 'aac', '-b:a', '192k', '-pix_fmt', 'yuv420p', '-shortest', output_file])
    input_file = open(output_file_path,"r")
    translated_releases = json.load(input_file)
    for lang in translated_releases:
        releases = translated_releases[lang]
        count = 1
        for release in releases:
            merge_images_and_audio("./Untitled_video",f"./speech/{lang}-rel{count}.mp3",f"./videos/{lang}-rel{count}.mp4")
            count += 1

# print('Video created successfully!')
convertSpeechToVideo()