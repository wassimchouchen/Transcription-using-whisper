# import whisper
# import datetime

# import subprocess
# import pickle
# import torch
# import pyannote.audio
# from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
# embedding_model = PretrainedSpeakerEmbedding( "speechbrain/spkrec-ecapa-voxceleb",device=torch.device("cuda"))

# from pyannote.audio import Audio
# from pyannote.core import Segment

# import wave
# import contextlib

# from sklearn.cluster import AgglomerativeClustering
# import numpy as np


# def transcription(path,model_size):

#         if path[-3:] != 'wav':
#                 subprocess.call(['ffmpeg', '-i', path, 'audio.wav', '-y'])
#                 path = 'audio.wav'


#         model = whisper.load_model(model_size)

#         result = model.transcribe(path)

#         return result

#         segments = result["segments"]

#         with contextlib.closing(wave.open(path,'r')) as f:
#             frames = f.getnframes()
#             rate = f.getframerate()
#             duration = frames / float(rate)

#         audio = Audio()

#         def segment_embedding(segment):
#                 start = segment["start"]
#                 # Whisper overshoots the end timestamp in the last segment
#                 end = min(duration, segment["end"])
#                 clip = Segment(start, end)
#                 waveform, sample_rate = audio.crop(path, clip)
#                 return embedding_model(waveform[None])


#         embeddings = np.zeros(shape=(len(segments), 192))
#         for i, segment in enumerate(segments):
#             embeddings[i] = segment_embedding(segment)

#         embeddings = np.nan_to_num(embeddings)

#         clustering = AgglomerativeClustering(num_speakers).fit(embeddings)
#         labels = clustering.labels_
#         for i in range(len(segments)):
#             segments[i]["speaker"] = 'SPEAKER ' + str(labels[i] + 1)



#         def time(secs):
#             return datetime.timedelta(seconds=round(secs))

#         f = open("transcript.txt", "w")

#         for (i, segment) in enumerate(segments):
#                 if i == 0 or segments[i - 1]["speaker"] != segment["speaker"]:
#                     f.write("\n" + segment["speaker"] + ' ' + str(time(segment["start"])) + '\n')
#                 f.write(segment["text"][1:] + ' ')
#         f.close()

#         print(open('transcript.txt','rb').load())

#         return f
