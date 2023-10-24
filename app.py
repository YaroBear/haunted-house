from vlc import MediaPlayer
import json
import numpy
from pathlib import Path
from flask import Flask
import threading
from logging import getLogger, StreamHandler, DEBUG
from scipy.signal import find_peaks

app = Flask(__name__)

logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel(DEBUG)

THUNDER_CLAP_PEAK_TIME_SERIES = None
SAMPLE_RATE = 10000

THUNDER_PATH = Path("./thunder.mp3")
BACH_PATH = Path("./bach.mp3")

def play_thunder(seconds):
    logger.debug(f"Playing thunder for {seconds} seconds")
    process = MediaPlayer(THUNDER_PATH)
    process.play()

    threading.Timer(seconds, process.stop).start()

def play_bach(seconds):
    logger.debug(f"Playing bach for {seconds} seconds")
    process = MediaPlayer(BACH_PATH)
    process.play()

    threading.Timer(seconds, process.stop).start()

# def filter_level(nd_arr, level=0.3):

def clap():
    print("clap\r")

# def naive_find_peaks(nd_array, level=0.5, sample_rate=SAMPLE_RATE):
#     idx = numpy.argwhere(nd_array >= 0.5).ravel()
#     to_seconds = numpy.vectorize(lambda v: v / sample_rate)
#     seconds = to_seconds(idx)
#     print(seconds)
#     print(len(seconds))

def queue_claps(nd_array):
    peaks, _ = find_peaks(nd_array, height=0.5, distance=1000)
    to_seconds = numpy.vectorize(lambda v: v / SAMPLE_RATE)
    time_series_second_markers = to_seconds(peaks)

    logger.debug(f"Peaks: {peaks}")
    logger.debug(f"Peak time series second markers: {time_series_second_markers}")

    for time in time_series_second_markers:
        threading.Timer(time, clap).start()

def analyze_thunder_claps():
    fp_time_series = Path("output.json")

    global THUNDER_CLAP_PEAK_TIME_SERIES

    if fp_time_series.is_file():
        with open(fp_time_series, 'r') as filehandle:
            j = json.load(filehandle)
            THUNDER_CLAP_PEAK_TIME_SERIES = numpy.array(j).ravel()
        # return
    
    # y_data, _ = librosa.load(THUNDER_PATH, sr=SAMPLE_RATE)

    # THUNDER_CLAP_PEAK_TIME_SERIES = y_data.ravel()

    # with open(fp_time_series, 'w') as filehandle:
    #     json.dump(y_data.tolist(), filehandle)
        

def startup():
    analyze_thunder_claps()

startup()

@app.route("/")
def haunted_house():
    queue_claps(THUNDER_CLAP_PEAK_TIME_SERIES)
    play_thunder(22)
    play_bach(16)

    return "done"