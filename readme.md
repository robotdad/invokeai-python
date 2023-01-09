# InvokeAI basic Python samples
The purpose of these scripts is to generate images you can later bring back and use with InvokeAI interface. 

The scripts directory has two examples:
* test.py is a minimal example, it does not save metadata in the output image.
* metadata.py will save metadata in the output image.
* startinvokeai.py starts metadata.py in the background.

For the images with metadata in them, you can start the InvokeAI CLI and load a command that will regenerate the image using !fetch path/to/image.

## Paths
Before running the scripts you should have InvokeAI working locally as the scripts depend on the model files. You will most likely want to use set the INVOKEAI_ROOT to the runtime location of InvokeAI where the invokeai.init and the model files live. The scripts themselves have no dependencies on InvokeAI source code being available locally other than as a library from the requirements.txt.

## Setup
InvokeAI currently set to 2.2.5, update requirements.txt to change. This could be reworked to use conda instead, but the instructions here use the virtualenv path.

From within this project directory:
```
virtualenv venv
.\venv\Scripts\activate.ps1
```

Presently there is [an issue](https://github.com/invoke-ai/InvokeAI/issues/1409) with installing torch that is impacting Windows at least. So run this before installing from requirements.txt. Note this pinned version of torch does not have a build for Python 3.11, you need 3.10 or earlier.
```
pip install --extra-index-url https://download.pytorch.org/whl/cu116 --trusted-host https://download.pytorch.org torch==1.12.1 torchvision==0.13.1
```

Now continue as usual.

```
pip install --prefer-binary -r requirements.txt
```
Note that the requirments.txt here was produced by flattening the nested requirements from InvokeAI on Windows. You may need to adjust for your platform. The main addition is the line pointing to the InvokeAI repo. You can specify a specific release tag after the @ symbol there.

