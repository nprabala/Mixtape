# Server

## Sanic

To use Sanic: pip install sanic and then run python ModelServer.py.


To help with live reloading for development, pip install hupper and run

> hupper -m \<app name\>

so it can track your changes and reload the server.

## ModelServer

To test ModelServer locally, download postman (API tool for sending requests),
insert localhost:8000/chord_progressions as the URL, make it a POST request,
and insert notes as the request body in the following format:

    [{"note":"A", "duration":2},
    {"note":"B", "duration":1},
    {"note":"C", "duration":0.25},
    {"note":"D", "duration":0.5},
    {"note":"A", "duration":1}]

The server will return chords in a similar format (just with 'chords' instead
of notes).

Until the model is finished, the server just sends back some dummy chords.


# Magenta (transcription)

## Setup

In order to run the onsets script, you will need to set up a few things for Google Magenta to work.

### Conda

I recommend downloading conda for (https://conda.io/en/master/) and setting up a conda virtual environment (https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/):

> conda create -n \<env name\> python=3.6

Activate the environment with

> source activate \<env name\>

### Modules

After conda is installed, you will need to pip install magenta, librosa, tensorflow which are needed for the script. In addition, magenta may require a few other libraries that aren't listed such as numpy, but it'll alert you which ones you will need when you try to run the script.

### Magenta Checkpoint

In order to use the checkpoint file that google provides, you will need to download it from here https://storage.googleapis.com/magentadata/models/onsets_frames_transcription/maestro_checkpoint.zip. Once unzipped, the resulting train folder needs to be put into the same directory as the Transcribe.py script.

## Issues

* Bus Error: 10. To handle this, pip uninstall numpy and then conda install numpy instead
* Make sure you are using the correct versions for Python (Python vs Python3)

## More info

More information about Magenta can be found on their gitub: https://github.com/tensorflow/magenta/tree/master/magenta/