# This is a minimal script to generate an image with metadata that can be reuturned with !fetch in the invokeai CLI
# validate the metadata by passing the output to InvokeAI/scripts/sd-metadata.py
import os
from ldm.generate import Generate
from ldm.invoke.globals import Globals
from ldm.invoke.args import Args, metadata_dumps
from ldm.invoke.pngwriter import PngWriter

# returns filename and prompt formatted for CLI, reduced from invoke.py
def prepare_image_metadata(opt, prefix, seed):
    wildcards = dict(opt.__dict__)
    wildcards['prefix'] = prefix
    wildcards['seed'] = seed
    try:
        filename = opt.fnformat.format(**wildcards)
    except KeyError as e:
        print(f'** The filename format contains an unknown key \'{e.args[0]}\'. Will use \'{{prefix}}.{{seed}}.png\' instead')
        filename = f'{prefix}.{seed}.png'
    except IndexError as e:
        print(f'** The filename format is broken or complete. Will use \'{{prefix}}.{{seed}}.png\' instead')
        filename = f'{prefix}.{seed}.png'
    # This formats a prompt as would be used in the CLI
    formatted_dream_prompt = opt.dream_prompt_str(seed=seed)
    return filename, formatted_dream_prompt

# Register with image_callback in prompt2image, see invoke.py for how to handle variations etc.
def image_writer(image, seed, first_seed=None, use_prefix=None, attention_maps_image=None):
    filename, dreamprompt = prepare_image_metadata(opt, prefix, seed)
    path = file_writer.save_image_and_prompt_to_png(
        image = image, 
        dream_prompt = dreamprompt, 
        metadata = metadata_dumps(
            opt, 
            seeds = [seed],
            model_hash = gen.model_hash), 
        name=filename)
    print('\n Generated:', path)

# Setup the opt object, not typed, look to ldm/generate for options corresponding to the cli
opt = Args()

# Specify full paths in the InvokeAI configs/models.yaml to use from other directories
# Specify the path to the models.yaml file in opt.conf if you are not using the defaults settings above
# you may need to specify additional opt.conf options if you are not using the defaults
# For example, opt.sampler_name, opt.steps, etc.
# opt.conf = '../InvokeAI/configs/models.yaml' 
# This will load the default .invokeai settings
args = opt.parse_args()
Globals.root = os.path.expanduser(args.root_dir or os.environ.get('INVOKEAI_ROOT') or os.path.abspath('.'))
Globals.try_patchmatch = args.patchmatch
if not os.path.isabs(opt.conf):
    opt.conf = os.path.normpath(os.path.join(Globals.root,opt.conf))
print(f'>> InvokeAI runtime directory is "{Globals.root}"')
# normalize the config directory relative to root
if not os.path.isabs(opt.conf):
    opt.conf = os.path.normpath(os.path.join(Globals.root,opt.conf))

import transformers
transformers.logging.set_verbosity_error()

# Model is stored in the metadata but not retrieved by !fetch
opt.model = 'stable-diffusion-1.5'

# Channging these options means you will need to create a new generate object
gen = Generate(
    conf = opt.conf, 
    model = opt.model,
    sampler_name = opt.sampler_name)
gen.load_model()

# Use the default width/heigh from the loaded model
opt.width = gen.width
opt.height = gen.height

# These need to be set for !fetch to work from the invokeai cli
opt.cfg_scale = 7.5 # default value

# Set the prompt and output directory
opt.prompt = 'shiba inu on a wanted poster'

opt.output_dir = './outputs'
if not os.path.exists(opt.output_dir):
    os.makedirs(opt.output_dir)

# Get a unique prefix for the output files
file_writer = PngWriter(opt.output_dir)
prefix = file_writer.unique_prefix()

# Generate the image, iterations is optional, default is 1
gen.prompt2image(image_callback=image_writer, prompt=opt.prompt, iterations = 3)

