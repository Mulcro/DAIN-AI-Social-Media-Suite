import os
import moviepy as mp
from moviepy import TextClip, CompositeVideoClip
import speech_recognition as sr
from pydub import AudioSegment

def editHighlights():
    # initiating folder paths
    path = os.getcwd()
    parent = os.path.abspath(os.path.join(path, os.pardir))
    highlights = os.path.join(parent, "constants", "highlights")
    edited = os.path.join(parent, "constants", "edited")

    # cropping each highlight
    for filename in os.listdir(highlights):
        file_path = os.path.join(highlights, filename)
        if os.path.isfile(file_path):
            print(f"Processing file: {file_path}")

            video_clip = mp.VideoFileClip(file_path) # reading in video

            clip_size = video_clip.size
            x1= clip_size[0]/2 - clip_size[1]/4
            y1= 0
            x2 = clip_size[0]/2 + clip_size[1]/4
            y2 = clip_size[1]
            vertical=video_clip.cropped(x1=x1, y1=y1, x2=x2, y2=y2)
            vertical.write_videofile(os.path.join(edited, filename))

if __name__ == "__main__":
    try:
        editHighlights()
    except Exception as e:
        print(f"An error occurred: {e}")