import whisper
import datetime
import subprocess
import torch
import pyannote.audio
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
from pyannote.audio import Audio
from pyannote.core import Segment
import wave
import contextlib
from sklearn.cluster import AgglomerativeClustering
import numpy as np


def segment_embedding(audio, embedding_model, path, segment,duration):
    start = segment["start"]
    end = min(duration, segment["end"])
    clip = Segment(start, end)
    waveform, sample_rate = audio.crop(path, clip)
    return embedding_model(waveform[None])


def transcribe(path, model_size):
    if path[-3:] != 'wav':
        subprocess.call(['ffmpeg', '-i', path, 'audio.wav', '-y'])
        path = 'audio.wav'

    model = whisper.load_model(model_size)
    result = model.transcribe(path)
    return result


def cluster_speakers(path, result, num_speakers, audio, embedding_model, duration):
    segments = result["segments"]
    embeddings = np.zeros(shape=(len(segments), 192))
    for i, segment in enumerate(segments):
        embeddings[i] = segment_embedding(audio, embedding_model, path, segment)

    embeddings = np.nan_to_num(embeddings)

    clustering = AgglomerativeClustering(num_speakers).fit(embeddings)
    labels = clustering.labels_
    for i in range(len(segments)):
        segments[i]["speaker"] = 'SPEAKER ' + str(labels[i] + 1)

    return segments


def create_transcript(segments):
    def time(secs):
        return datetime.timedelta(seconds=round(secs))

    with open("transcript.txt", "w") as f:
        for (i, segment) in enumerate(segments):
            if i == 0 or segments[i - 1]["speaker"] != segment["speaker"]:
                f.write("\n" + segment["speaker"] + ' ' + str(time(segment["start"])) + '\n')
            f.write(segment["text"][1:] + ' ')



def process_audio_file(path, model_size, num_speakers):
    result = transcribe(path, model_size)

    with contextlib.closing(wave.open(path, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)

    audio = Audio()
    embedding_model = PretrainedSpeakerEmbedding(
        "speechbrain/spkrec-ecapa-voxceleb",
        device=torch.device("cuda"))

    segments = cluster_speakers(path, result, num_speakers, audio, embedding_model, duration)

    create_transcript(segments)

    with open('transcript.txt', 'r') as f:
        transcript = f.read()

    return transcript




# This code is a Python script that processes an audio file and generates a transcript of the spoken content, with speakers labeled and separated by newlines. It uses the Whisper speech-to-text library for transcription, Pyannote Audio for speaker clustering, and sklearn for agglomerative clustering.

# The segment_embedding() function takes an audio waveform, an embedding model, the path to the audio file, and a segment of the audio file as input. It returns the embedding of the segment using the embedding model.

# The transcribe() function takes the path to an audio file and a model size as input. It checks if the file is a WAV file, and if not, uses FFmpeg to convert it to a WAV file. It then loads the specified Whisper model and transcribes the audio file, returning the transcription result.

# The cluster_speakers() function takes the path to an audio file, a transcription result, the number of speakers to cluster, an Audio object, an embedding model, and the duration of the audio file as input. It extracts the segments from the transcription result, computes the embedding of each segment using segment_embedding(), clusters the embeddings using agglomerative clustering, and assigns speaker labels to the segments based on the clustering result. It returns the labeled segments.

# The create_transcript() function takes a list of labeled segments as input, and generates a transcript file with the speaker labels and the spoken text, separated by newlines.

# The process_audio_file() function takes the path to an audio file, a model size, and the number of speakers to cluster as input. It transcribes the audio file using transcribe(), extracts the duration of the audio file, creates an Audio object and an embedding model, clusters the speakers using cluster_speakers(), creates a transcript using create_transcript(), and returns the transcript as a string.
# # if __name__ == "__main__":
# #     # Replace 'path/to/audio.wav' with the path to your audio file
#     path = 'path/to/audio.wav'
#     model_size = 'large'
#     num_speakers = 2
#     process_audio_file(path, model_size, num_speakers)
