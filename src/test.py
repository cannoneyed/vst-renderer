# Notes: there's an issue with inconsistent versions of python being linked to by the
# RenderMan build process and conda used by jupyter notebooks. For now, I've opted
# to run this script with /usr/include/python2.7, which is the linked version

import os
import librenderman as rm
import numpy as np
import librosa

sampleRate = 44100
bufferSize = 512
renderLength = 10.0

engine = rm.RenderEngine(sampleRate, bufferSize)
sylenth_path = '/Library/Audio/Plug-Ins/VST/Sylenth1.vst'

def load_plugin():
    if engine.load_plugin(sylenth_path):
        print('loaded plugin succesfully')


def load_preset(preset_path):
    if not engine.load_preset(preset_path):
        print('error loading preset...')


def load_midi(midi_path):
    if not engine.load_midi(midi_path):
        print('error loading midi...')

entries = []
def isvalid(filename):
    return os.path.isfile(filename) and '.fxp' in filename

def makePresetEntry(dirpath, patch_name):
    path_name = os.path.join(dirpath, patch_name)
    patch_name = patch_name.replace(".fxp", "")
    patch_name = patch_name.replace(" ", "_")
    group = dirpath.replace("sylenth_patches/", "")
    entry =(path_name, patch_name, group)
    return entry

for (dirpath, dirnames, filenames) in os.walk('sylenth_patches'):
    for f in filenames:
        if not isvalid(os.path.join(dirpath, f)): continue
        entry = makePresetEntry(dirpath, f)
        entries.append(entry)

def render_audio(filename):
    def render(output_filename):
        engine.render_midi(renderLength)
        audio = engine.get_audio_frames()
        audio = np.array(audio, np.float)

        librosa.output.write_wav(output_filename, audio, sampleRate)
    render(filename)

def make_output_filename(patch_name, modifier, group):
    patch_name = patch_name.replace('&', 'and')
    patch_name = patch_name.replace("'", '')
    directory = 'output/' + group + "/" + patch_name
    if not os.path.exists(directory):
        os.makedirs(directory)
    output_filename = directory + "/" + patch_name + modifier + '.wav'
    return output_filename

def render_preset(path, patch, group):
    # render preset basic
    load_preset(path)
    output_filename = make_output_filename(patch, "__base", group)

    render_audio(output_filename)

load_plugin()
load_midi("test.mid")
(path, patch, group) = entries[0]
render_preset(path, patch, group)
