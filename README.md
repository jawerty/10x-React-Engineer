# 10x-React-Engineer
Coding was livestreamed here -> https://youtube.com/live/6_sdnYDmUmo

Update: The prompts work well with Code Llama. Tested output using [The Bloke's Code LLama Instruct](https://huggingface.co/TheBloke/CodeLlama-13B-Instruct-fp16)

# How it works
10x-React-Engineer first uses the [GPT-Engineer](https://github.com/AntonOsika/gpt-engineer) method of taking in the users input and scaffolding the project first starting at the entry point and resolving all the imports recursively (through the prompting).

Then there's a `dev loop` that will first resolve missing dependencies it missed from reading the codebase. Then the loop will ask the user for additonal modifications to make to the react components (like updating the design to bootstrap) 

1) User ask summarization
2) Scaffolding
3) Dev Loop
	- Dependency fixer
	- Code modification feedback


### The AI asks your initial prompt and requests modifications in a feedback loop
![Screen Shot 2023-08-15 at 2 22 06 AM](https://github.com/jawerty/10x-React-Engineer/assets/1999719/93e42a6b-953e-44d1-baff-1d219cb98bea)

### Example generated output
![Screen Shot 2023-08-15 at 2 26 35 AM](https://github.com/jawerty/10x-React-Engineer/assets/1999719/3629b96e-8be6-48c2-a650-99742eb7400e)

After each loop it will write the code in the `react-output` directory

The User ask summarization will eventually be optional as I keep working on the features. I found it to be more so how things work in the real world.

# How to use it
### Build/Run from source
First install the pip packages
```
$ pip3 install -r requirements.txt
```

Then execute the run script
```
$ python3 run.py
```

### Jupyter notebook 
a jupyter notebook with all the code accessible in the end it outputs into a `react-output` folder

This next upcoming week I will revamp the codebase into more than a single file and add more features. I want to keep iterating on this until it's working well enough to generate React projects locally on a finetuned 7b llama 2 model.

### Google Colab (best option)
Here's a Google [Colab](https://colab.research.google.com/drive/1b8zZo0O87plL2icYKs6uxXRHlqqe0Mx_?usp=sharing) with the code for you to play with

# This is an experiment
This was coded in 6 hours on a live stream I did Aug 14th 2023. Have mostly been avoiding autonomous agents until the dust settled but a viewer on my discord suggested I just go for it so here it is. This actually impressed me a lot. Llama 2's reasoning ability with just the 13b parameter model was very impressive. There are still inconsistent issues which you can see near the end of the live stream with resolving webpack.config.js pathnames. However you can update the prompts or use a larger model to try and straighten those out.

It actually works pretty well for only being tested on Llama 2 13b Chat model. Going to push the limits more with the 70b model and show results.

# TODO
- Main thing is to fine tune the 13b chat llama 2 to be better at react
- JSON fixer for package.json post processing
- Add generated codebase as context to modification inferences
- Add option to modify everything vs file by file
- Make ask summarization optional
