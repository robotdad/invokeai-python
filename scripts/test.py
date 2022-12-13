# shortest script to drive InvokeAI, just to test if it works
# will not save metadata in the generated file as of 2.2.4
from ldm.generate import Generate

# Make sure you have the INVOKEAI_ROOT environment variable set per the readme
gr = Generate(conf = 'e:/invokeai/configs/models.yaml')
gr.load_model()
gr.prompt2png(prompt     = "a squirrel eating ice cream",
              outdir     = "./outputs",
              iterations = 1)