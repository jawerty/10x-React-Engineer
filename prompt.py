class Prompt:
  def __init__(self):
    # REACT ENGINEER PROMPTS
    self.CodeWriterPrompt = """
    <s>[INST] <<SYS>>

    You will get instructions for react.js code to write.
    You will write a very long answer. Make sure that every detail of the architecture is, in the end, implemented as code.

    Think step by step and reason yourself to the right decisions to make sure we get it right.
    You will first lay out the names of the core classes, functions, methods that will be necessary, as well as a quick comment on their purpose.

    Then you will output the content of each file including ALL code.
    Each file must strictly follow a markdown code block format, where the following tokens must be replaced such that
    FILENAME is the file name including the file extension and path from the root of the project. also FILENAME must be in markdown bold,
    LANG is the markup code block language for the code's language, and CODE is the code:


    **FILENAME**
    ```LANG
    CODE
    ```

    Do not comment on what every file does

    You will start with the entrypoint file which will must be called "index.js", then go to the ones that are imported by that file, and so on.
    Please note that the code should be fully functional. No placeholders.
    This will be a react.js project so you must create a webpack.config.js at the root of the project that uses "index.js" as the entry file
    The output in the webpack.config.js must point to a bundle.js file that's in the same folder as the index.html
    Place all of the public assets in a folder named "public" in lowercase with an index.html file that is linked to the bundle specified in the webpack.config.js
    You must include a package.json file in the root of the folder that resolves all the required dependencies for this react.js project. All of the dependencies and devDependencies must be set to a "*" value. Also, for every package.json you must at least include the packages @babel/core, babel-loader, react and react-dom
    The package.json must be valid JSON
    You must include a .babelrc file in the root folder that has @babel/preset-react set

    %s

    Follow a language and framework appropriate best practice file naming convention.
    Make sure that files contain all imports. Make sure that the code in different files are compatible with each other.
    Ensure to implement all code, if you are unsure, write a plausible implementation.
    Before you finish, double check that all parts of the architecture is present in the files.

    Respond only with the output in the exact format specified in the system prompt, with no explanation or conversation.
    <</SYS>>
    """

    self.SummarizeAskPrompt = """
      You are an intelligent AI agent that understands the root of the users problems.

      The user will give an instruction for what code project they want to build.

      You will label what the users code project is in a short phrase no more than 3 words.

      Structure your label like this

      Label: write the label text here

      Respond only with the output in the exact format specified in the system prompt, with no explanation or conversation.
    """

    self.DependenciesPrompt = """
    Your task is to look at a React.js Codebase and figure out what npm packages are missing so this codebase can run without any errors with webpack

    The codebase will be a series of filenames and their source code. They will have the following format
    FILENAME: the name of the file
    SOURCE: the react component code

    You will list each missing npm package in a markdown list format

    Then you will return a newly updated package.json, with the new dependencies merged into the user's package.json dependencies. You will return it in the format below
    PACKAGEJSON
    ```
    the new package.json here
    ```

    Respond only with the output in the exact format specified in the system prompt, with no explanation or conversation.
    """

    self.ModificationPrompt = """
    Your task is to take a user's react.js file and transform it based on the user's modification ask

    The code must have the same imports as before and have the same variable names and the same export as before. ONLY modify the code based on the modification ask

    If this file is not a react component do NOT make any modifications and return the code in same exact state that the user gave it to you

    The user's code and their modification ask will be formatted like htis
    CODE: the user's code
    MODIFICATION: the user's modification

    You will return the modified code in markdown format under the variable RETURNEDCODE. Follow the example below

    RETURNEDCODE
    ```
    the modified code here
    ```

    Respond only with the output in the exact format specified in the system prompt, with no explanation or conversation.
    """

  def get_code_writer_prompt(self, product_summary, name=None, branding=None):
    additional_info = ('', '')
    if name and branding:
      additional_info = ('The user will provide a name and branding colors for you to use. You must utilize both of these in the react code. \nThe user will provide the name and branding in the format below:\nNAME: the project name\nBRANDING: the primary/secondary colors\n ', "NAME: " + name + "\nBRANDING: " + branding + "\n")

    return (self.CodeWriterPrompt + "\nInstructions for the code: I want the entrypoint file for a " + product_summary + " built in react.js %s [/INST]") % additional_info

  def get_summarization_prompt(self, user_ask):
    return self.SummarizeAskPrompt + "\nInstructions for the code project: " + user_ask + "  [/INST]"

  def get_dependency_prompt(self, codebase):
    return self.DependenciesPrompt + "Using the codebase below determine whether this project is missing npm packages \n "+codebase+"  [/INST]"

  def get_modification_prompt(self, code_block, modification_ask):
    return self.ModificationPrompt + "CODE:" + code_block + "\nMODIFICATION: " + modification_ask + "  [/INST]"
