# shortest script to drive InvokeAI, just to test if it works
# will not save metadata in the generated file as of 2.1.3
from ldm.generate import Generate

# Specify full paths in the InvokeAI configs/models.yaml to use from other directories
gr = Generate(conf = '../InvokeAI/configs/models.yaml')
gr.load_model()
gr.prompt2png(prompt     = "an astronaut riding a horse",
              outdir     = "./outputs",
              iterations = 3)