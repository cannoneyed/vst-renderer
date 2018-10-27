# Notes: there's an issue with inconsistent versions of python being linked to by the
# RenderMan build process and conda used by jupyter notebooks. For now, I've opted
# to run this script with /usr/include/python2.7, which is the linked version

import librenderman as rm
import wave
import scipy.io.wavfile
import numpy as np

sampleRate = 44100
bufferSize = 512
fftSize = 512

engine = rm.RenderEngine(sampleRate, bufferSize, fftSize)
sylenth_path = '/Library/Audio/Plug-Ins/VST/Sylenth1.vst'
if engine.load_plugin(sylenth_path):
    print('loaded plugin succesfully')

description = engine.get_plugin_parameters_description()
description = description.split('\n')

# Settings to play a note and extract data from the synth.
midiNote = 40
midiVelocity = 127
noteLength = 0.1
renderLength = 5.0

# # Get the patch and display it!
preset_path = '/Users/andrewcoenen/cannoneyed/synth-embeddings/python/test.fxp'
if engine.load_preset(preset_path):
    print('loaded preset succesfully')

# patch = engine.get_patch()

# for (index, value) in patch:
#     if value != 0.0:
#         print(index, value)

# generator = rm.PatchGenerator(engine)
# new_patch = generator.get_random_patch()
# engine.set_patch(new_patch)

# Render the data.
engine.render_patch(midiNote, midiVelocity, noteLength, renderLength, False)
audio = engine.get_audio_frames()
audio = np.array(audio, np.float32)
# audio = audio.astype(np.int16)

print(max(audio))

scipy.io.wavfile.write('test.wav', sampleRate, audio)
