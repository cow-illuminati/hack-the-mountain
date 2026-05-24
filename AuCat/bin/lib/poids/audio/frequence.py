# Accepte un fichier vidéo/audio et retourne les 2 fréquences dominantes
# les plus fréquentes dans la voix, entre 80 Hz et 500 Hz.
#
# Idée générale :
#   - charge l'audio du fichier (mp4, mov, mp3, wav, etc.)
#   - analyse l'audio par petites fenêtres temporelles
#   - extrait, pour chaque fenêtre, la fréquence dominante
#   - ignore les fréquences hors de la plage humaine choisie
#   - découpe la plage 80-500 Hz en 16 bins égaux
#   - retourne les 2 fréquences principales (centre des bins)
#
# Utilité :
#   ce fichier ne reconnaît pas une personne avec certitude.
#   Il donne plutôt une signature fréquentielle simple de la voix
#   qui parle dans la vidéo.
#
# Dépendances Python à installer :
#   pip install numpy librosa
#
# Dépendance système souvent requise :
#   FFmpeg
#
# Installation FFmpeg :
#   Windows : installer FFmpeg et l'ajouter au PATH
#   Linux Ubuntu/Debian : sudo apt install ffmpeg
#   Linux Fedora : sudo dnf install ffmpeg
#   Linux Arch : sudo pacman -S ffmpeg
#
# Remarques :
#   - librosa peut charger de nombreux formats audio/vidéo via audioread/FFmpeg
#   - mp4 et mov sont acceptés si FFmpeg peut les lire
#   - le résultat est une fréquence dominante, pas une identité de personne

import numpy as np
import librosa


MIN_FREQ = 80.0
MAX_FREQ = 500.0
NUM_BINS = 16
TOP_K = 2


def load_audio(file_path, sr=None):
    audio, sample_rate = librosa.load(file_path, sr=sr, mono=True)
    return audio, sample_rate


def get_dominant_frequencies(audio, sample_rate, min_freq=MIN_FREQ, max_freq=MAX_FREQ):
    pitches, magnitudes = librosa.piptrack(
        y=audio,
        sr=sample_rate,
        fmin=min_freq,
        fmax=max_freq
    )

    dominant_frequencies = []

    for t in range(pitches.shape[1]):
        frame_magnitudes = magnitudes[:, t]
        frame_pitches = pitches[:, t]

        if frame_magnitudes.size == 0:
            continue

        max_index = np.argmax(frame_magnitudes)
        freq = frame_pitches[max_index]

        if min_freq <= freq <= max_freq:
            dominant_frequencies.append(float(freq))

    return dominant_frequencies


def create_frequency_bins(min_freq=MIN_FREQ, max_freq=MAX_FREQ, num_bins=NUM_BINS):
    return np.linspace(min_freq, max_freq, num_bins + 1)


def get_bin_index(freq, bin_edges):
    idx = np.digitize(freq, bin_edges, right=False) - 1

    if idx < 0:
        return None

    if idx >= len(bin_edges) - 1:
        idx = len(bin_edges) - 2

    return idx


def get_bin_center(bin_index, bin_edges):
    start = float(bin_edges[bin_index])
    end = float(bin_edges[bin_index + 1])
    return float((start + end) / 2.0)


def top_2_frequencies(
    file_path,
    min_freq=MIN_FREQ,
    max_freq=MAX_FREQ,
    num_bins=NUM_BINS,
    top_k=TOP_K
):
    audio, sample_rate = load_audio(file_path)
    dominant_frequencies = get_dominant_frequencies(
        audio,
        sample_rate,
        min_freq=min_freq,
        max_freq=max_freq
    )

    if not dominant_frequencies:
        return [0.0, 0.0]

    bin_edges = create_frequency_bins(
        min_freq=min_freq,
        max_freq=max_freq,
        num_bins=num_bins
    )

    counts = np.zeros(num_bins, dtype=int)

    for freq in dominant_frequencies:
        idx = get_bin_index(freq, bin_edges)
        if idx is not None:
            counts[idx] += 1

    sorted_indices = np.argsort(counts)[::-1]
    top_indices = [idx for idx in sorted_indices if counts[idx] > 0][:top_k]

    frequencies_hz = [get_bin_center(idx, bin_edges) for idx in top_indices]

    while len(frequencies_hz) < top_k:
        frequencies_hz.append(0.0)

    return frequencies_hz