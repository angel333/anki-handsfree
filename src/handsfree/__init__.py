# -*- coding: utf-8 -*-

# Handsfree addon for Anki
# Author: Ondrej Simek
# License: MIT
# Details: https://github.com/angel333/anki-handsfree

import os
import platform
import json
import re
import subprocess
import sys

from aqt import mw
from aqt.utils import (showInfo, getOnlyText, askUser)
from aqt.qt import *

# pydub
sys.path.append(os.path.join(os.path.dirname(__file__), "vendor/pydub"))
os.environ["PATH"] += os.pathsep + os.path.dirname(__file__) # dirty hack, see bellow
from pydub import AudioSegment
from pydub.generators import (Sine, WhiteNoise)
# A hack to prevent ffmpeg from showing a window, see https://stackoverflow.com/a/49111811
if subprocess.mswindows:
      subprocess.STARTUPINFO.dwFlags |= subprocess.STARTF_USESHOWWINDOW
# Setting converter path will still raise an excpetion because pydub checks the converter upon the import.
# - I've solved this by adding ffmpeg to PATH (see above)
# AudioSegment.converter = os.path.join(
#     os.path.dirname(__file__),
#     "ffmpeg" + (".exe" if platform.system() == "Windows" else ""))

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

def text_extract_audio(text):
    """
    Extracts audio files in the [sound:...] tags from a text.
    """
    def get_file_path(file_name):
        return os.path.abspath(os.path.join(mw.col.media.dir(), file_name))
    file_names = re.findall(r'\[sound:(.+?)\]', text)
    paths = list(map(get_file_path, file_names))
    print(paths)
    return paths

def process_cards(card_ids):
    """
    Return a list of tuples (question, answer) with lists of audio files.
    """
    def card_extract_audio(card_id):
        card = mw.col.getCard(card_id)
        q_files = text_extract_audio(card.q())
        a_files = text_extract_audio(card.a())
        return q_files, a_files
    def audio_present(lists):
        return len(lists[0]) > 0 and len(lists[1]) > 0
    all = map(card_extract_audio, card_ids)
    relevant = filter(audio_present, all)
    return relevant

def create_countdown_segment():
    track = AudioSegment.empty()
    for i in range(0, 3):
        track += Sine(2000 + (i * 100)).to_audio_segment(duration=200, volume=-30)
        track += AudioSegment.silent(duration=800)
    return track

def create_card_segment(audio_files, qa_delay=0, aq_delay=0, countdown=False, repeat=False):
    # Question
    seg_q = AudioSegment.empty()
    for f in audio_files[0]:
        seg_q += AudioSegment.from_file(f)
    # Answer
    seg_a = AudioSegment.empty()
    for f in audio_files[1]:
        seg_a += AudioSegment.from_file(f)
    seg_pre_q_beep = Sine(2000).to_audio_segment(duration=500, volume=-30)
    seg_qa_delay = AudioSegment.silent(qa_delay)
    seg_aq_delay = AudioSegment.silent(aq_delay)
    seg_countdown = create_countdown_segment()

    track = seg_pre_q_beep + seg_q + seg_qa_delay
    if countdown:
        track += seg_countdown
    track += seg_a
    if (repeat):
        pause_500 = AudioSegment.silent(500)
        track += pause_500 + seg_q + pause_500 + seg_a + pause_500
    track += seg_aq_delay
    return track

def run():
    with open(CONFIG_PATH) as raw_json:
        config = json.load(raw_json)

    query = getOnlyText("Query:", default=config["query"])
    if query == "":
        return
    all_cards = mw.col.findCards(query)
    relevant_cards = process_cards(all_cards)

    output_dir = getOnlyText(
        str(len(all_cards)) + " cards found, " + str(len(relevant_cards)) + " are relevant. Please specify output path:",
        default=os.path.expanduser(config["output_directory"]))
    if output_dir == "":
        return

    i = 0
    track = AudioSegment.empty()
    for audio_files in relevant_cards:
        i += 1
        track += create_card_segment(audio_files,
            qa_delay=config["qa_delay"],
            aq_delay=config["aq_delay"],
            countdown=config["countdown"],
            repeat=config["repeat"])
        if config["output_individual"]:
            output_path = os.path.abspath(os.path.join(output_dir, config["output_individual_filename_pattern"].format(i)))
            track.export(output_path, format=config["output_format"], tags=config["audio_tags"], bitrate=config["output_bitrate"])
            track = AudioSegment.empty()
    if not config["output_individual"]:
        output_path = os.path.abspath(os.path.join(output_dir, config["output_filename"]))
        track.export(output_path, format=config["output_format"], tags=config["audio_tags"], bitrate=config["output_bitrate"])

    showInfo(str(len(relevant_cards)) + " cards exported.")

export_action = QAction("Handsfree export", mw)
export_action.triggered.connect(run)
mw.form.menuTools.addAction(export_action)
