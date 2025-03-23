import os
from transformers import pipeline
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector

# reading in transcript
transcript_path = os.path.join("components", "transcript.txt")
transcript_open = open(transcript_path, "r")
transcript = transcript_open.read()

# Summarize key points from transcript
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
summary = summarizer(transcript, max_length=150, min_length=40)

print(summary)

# video_manager = VideoManager(['input_video.mp4'])
# scene_manager = SceneManager()
# scene_manager.add_detector(ContentDetector())

# video_manager.start()
# scene_manager.detect_scenes(frame_source=video_manager)
# scene_list = scene_manager.get_scene_list()