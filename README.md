# VST Renderer POC

Simple demonstration of rendering audio from a VST plugin programatically. Built
with [RenderMan](https://github.com/fedden/RenderMan) and
[JUCE](https://juce.com/).

### Setup
We'll be using the RenderMan library to open VST plugins to create synthesized
audio clips. RenderMan uses JUCE to host the VST plugins and render the audio,
and in order to use it from Python we wrap the C++ code using Boost.

The following outlines the steps to build and use on MacOS:

- Set up a new conda Python 2.7 environment: `conda create --name <conda_env>`
- Clone the cannoneyed fork of the RenderMane library
  [here](https://github.com/cannoneyed/RenderMan.git). This fork contains a
  number of modifications to allow controlling specific plugin parameters and
  loading presets.
- Change the python header search path from `/usr/include/python2.7` to  `/anaconda/envs/<conda_env>/lib/python`
2.7 in the `RenderMan.jucer` file in order to link to the conda version of python.
- Install [JUCE](https://juce.com/), then open the `RenderMan.jucer` to
  regenerate the XCode project with the correct python library linked.
- Build the library using XCode.
- Per the installation instructions, rename the built library mv
  librenderman.so.dylib librenderman.so, and move it to this library's `/src` folder to use
  it.
- use otool -L librenderman.so to validate that we've linke to the correct
  version of python.
