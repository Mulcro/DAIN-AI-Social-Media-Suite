import os
import moviepy as mp
import speech_recognition as sr
from pydub import AudioSegment

######### generates transcript based on video input #########
def get_transcript(input_video_path):
    # input_video_path = os.path.join("components", "input_video3.mp4")
    extracted_audio_path = os.path.join("components", "extracted_audio.wav")
    transcript_path = os.path.join("components", "transcript.txt")

    if os.path.exists(input_video_path):
        video_clip = mp.VideoFileClip(input_video_path) # reading in video
        video_clip.audio.write_audiofile(extracted_audio_path) # creating audio file from video
    else:
        print("Video file path does not exist")

    if os.path.exists(extracted_audio_path):
        audio = AudioSegment.from_wav(extracted_audio_path)
        fh = open(transcript_path, "w+")
        n = 30*1000 # 30 second chunks
        chunks = [audio[i:i+n] for i in range(0, len(audio), n)]
        try:
            os.mkdir("audio_chunks")
        except(FileExistsError):
            pass

        os.chdir("audio_chunks")
        
        # looping through the chunks
        i=0 # counter for naming the audio chunks
        for chunk in chunks:
            # export audio chunk and save it in  
            # the current directory. 
            print("saving chunk{0}.wav".format(i)) 
            # specify the bitrate to be 192 k 
            chunk.export("./chunk{0}.wav".format(i), bitrate ='192k', format ="wav") 
    
            # the name of the newly created chunk 
            filename = 'chunk'+str(i)+'.wav'
            print("Processing chunk "+str(i))
    
            file = filename # getting the name of the newly created chunk 
    
            r = sr.Recognizer() # creating a speech recognition object 
            # recognize the chunk 
            with sr.AudioFile(file) as source: 
                # remove this if it is not working correctly. 
                # r.adjust_for_ambient_noise(source) 
                # audio_listened = r.listen(source) 
                try: 
                    # try converting it to text
                    chunk_audio = r.record(source)
                    rec = r.recognize_google(chunk_audio)
                    # write the output to the file. 
                    fh.write(rec+" ") 
        
                # catch any errors. 
                except sr.UnknownValueError: 
                    print("Could not understand audio") 
        
                except sr.RequestError as e: 
                    print("Could not request results. check your internet connection")
            os.remove(filename) # removing each audio chunk 
        
            i += 1   
        os.chdir('..') 

    else:
        print("can't find audio")

    os.rmdir("audio_chunks")
    return