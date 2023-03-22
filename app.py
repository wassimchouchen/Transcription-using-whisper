from flask import Flask, request, jsonify

# from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
# from pyannote.audio import Audio
# from pyannote.core import Segment
# import wave
# import contextlib
# from sklearn.cluster import AgglomerativeClustering
# import numpy as np
from api.functions import process_audio_file

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():

    num_speakers=2
    path="records\record.mp3"
    model_size="large"
    transcript=process_audio_file(path,model_size,num_speakers)
    print(transcript)

    return jsonify({'transcript': transcript})



if __name__ == "__main__":
    app.run(debug=True)

















    #     with contextlib.closing(wave.open("temp_audio.wav", 'r')) as f:
    #     frames = f.getnframes()
    #     rate = f.getframerate()
    #     duration = frames / float(rate)

    # audio = Audio()
    # embedding_model = PretrainedSpeakerEmbedding(
    #     "speechbrain/spkrec-ecapa-voxceleb",
    #     device=torch.device("cuda"))

    # segments = cluster_speakers("temp_audio.wav", result, 2, audio, embedding_model, duration)

    # transcript = ""
    # for (i, segment) in enumerate(segments):
    #     if i == 0 or segments[i - 1]["speaker"] != segment["speaker"]:
    #         transcript += "\n" + segment["speaker"] + ' ' + str(datetime.timedelta(seconds=round(segment["start"]))) + '\n'
    #     transcript += segment["text"][1:] + ' '