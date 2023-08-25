import os
import re

from agent import Agent

class ReactEngineer(Agent):
  def __init__(self, prompt):
    super().__init__()
    self.prompt = prompt

  def parse_summarization_result(self, output):
    label_token = 'Label:'
    output_lines = output.split("\n")
    for i in reversed(range(0, len(output_lines))):
      if label_token in output_lines[i]:
        line = output_lines[i]
        return line[line.index(label_token)+len(label_token):].strip()

  def parse_scaffolding_result(self, output):
    output = output[output.index("[/INST]"):]
    code_blocks = re.findall(r"```(.*?)```", output, re.DOTALL)
    file_names = re.findall(r"\*\*(.*?)\*\*", output, re.DOTALL)
    print(file_names)
    print(code_blocks)
    code_files = []
    print("files length", len(file_names))
    print("codes length", len(code_blocks))

    for i in range(0, len(file_names)):
      if i < len(code_blocks):
        code_files.append({
            "file_name": file_names[i],
            "code_block": code_blocks[i]
        })

    return code_files

  def initiate_code_modification(self, code_files, modification_ask):
    new_code_files = []
    for file_code_pair in code_files:
      mod_prompt = self.prompt.get_modification_prompt("\n".join(file_code_pair["code_block"].split("\n")[1:]), modification_ask)
      modification_result = self.generate(mod_prompt)
      print("MOD_RESULT:", modification_result)
      if "RETURNEDCODE" in modification_result:
        modification_result = modification_result[modification_result.index("[/INST]"):]
        code_block_raw_string = modification_result[modification_result.index("RETURNEDCODE") + len("RETURNEDCODE"):]
        file_code_pair["code_block"] = re.findall(r"```(.*?)```", code_block_raw_string, re.DOTALL)[0]
      new_code_files.append(file_code_pair)
    return new_code_files


  def resolve_missing_dependencies(self, code_files):
    print("Resolving missing dependencies...")
    codebase = "\n".join(
      list(map(lambda x: f"FILENAME: {x['file_name']}\nSOURCE: {x['code_block']}\n", code_files))
    )
    dep_prompt = self.prompt.get_dependency_prompt(codebase)
    dep_result = self.generate(dep_prompt)
    dep_result = dep_result[dep_result.index("[/INST]"):]
    print(dep_result)
    if "PACKAGEJSON" in dep_result:
      package_json_text = re.findall(r"```(.*?)```", dep_result, re.DOTALL)[0]
      return package_json_text
    else:
      return None

  def dev_loop(self, code_files, user_ask, modification_ask=None):
    if modification_ask:
      # update each related code block with a prediction using the modification ask of the user
      code_files = self.initiate_code_modification(code_files, modification_ask)

    # dependency resolving
    new_package_json = self.resolve_missing_dependencies(code_files)
    # set new package.json if it exists
    if new_package_json:
      for code_file in code_files:
        if 'package.json' in code_file["file_name"]:
          code_file["code_block"] = new_package_json

    for file_code_pair in code_files:
      filepath = "react-output/"+file_code_pair["file_name"]
      os.makedirs(os.path.dirname(filepath), exist_ok=True)
      with open(filepath, "w+") as f:
        code_block = file_code_pair["code_block"].split("\n")[1:]
        f.write("\n".join(code_block).encode('ascii', 'ignore').decode('ascii'))

    print("Done! Check out your codebase in react-output/")
    user_input = input("$ Do you wish to make modifications? [y/n]")
    if user_input == "y":
      modification_ask = input("$ What modifications do you want to make?")
      self.dev_loop(code_files, user_ask, modification_ask=modification_ask)
    else:
      print("Congrats on your 10x React project")

  # idea, name, branding are from the autostartup package
  def run(self, idea=None, name=None, branding=None):
    if idea is None:
      print("$ I am your personal 10x React Engineer ask me what you want to build?")
      init_user_ask = input("$ ")
      initial_sum_prompt = self.prompt.get_summarization_prompt(init_user_ask)
      summarization_result = self.generate(initial_sum_prompt)
      # print(summarization_result)
      project_summary = self.parse_summarization_result(summarization_result)
      print("Product Summary:", project_summary)
    else:
      project_summary = idea
    print("\n\nBeginning scaffolding...\n\n")
    scaffolding_output = self.prompt.get_code_writer_prompt(project_summary, name=name, branding=branding)
    scaffolding_result = self.generate(scaffolding_output)
    print(scaffolding_result)
    code_files = self.parse_scaffolding_result(scaffolding_result)

    self.dev_loop(code_files, init_user_ask)
