
# Accepte un fichier et retourne le dB du son (médiane, excluant les vides)
#
# Dépendances Python à installer :
#   pip install pydub numpy
#
# Dépendance système requise :
#   FFmpeg
#
# Installation FFmpeg :
#   Windows : installer FFmpeg et l'ajouter au PATH
#   Linux Ubuntu/Debian : sudo apt install ffmpeg
#   Linux Fedora : sudo dnf install ffmpeg
#   Linux Arch : sudo pacman -S ffmpeg
#
# Remarque :
#   pydub utilise FFmpeg pour lire les fichiers mp4/mp3.

from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import numpy as np


def load_audio(file_path):
    return AudioSegment.from_file(file_path)


def get_nonsilent_audio(audio, silence_thresh=-10, min_silence_len=100):
    nonsilent_ranges = detect_nonsilent(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh
    )

    if not nonsilent_ranges:
        raise ValueError("Aucun segment non silencieux trouvé.")

    result = AudioSegment.empty()

    for start_ms, end_ms in nonsilent_ranges:
        result += audio[start_ms:end_ms]

    return result


def median_dbfs(audio, chunk_ms=50):
    values = []

    for start in range(0, len(audio), chunk_ms):
        chunk = audio[start:start + chunk_ms]

        if len(chunk) == 0:
            continue

        if chunk.rms == 0:
            continue

        values.append(chunk.dBFS)

    if not values:
        raise ValueError("Aucune valeur de dBFS exploitable trouvée.")

    return float(np.median(values))


def median_db_excluding_silence(
    file_path,
    silence_thresh=-10,
    min_silence_len=100,
    chunk_ms=50
):
    audio = load_audio(file_path)
    cleaned_audio = get_nonsilent_audio(
        audio,
        silence_thresh=silence_thresh,
        min_silence_len=min_silence_len
    )
    return median_dbfs(cleaned_audio, chunk_ms=chunk_ms)