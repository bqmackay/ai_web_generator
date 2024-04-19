
from langchain_community.tools.shell.tool import ShellTool
from langchain_community.chat_models.ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.document_loaders import DirectoryLoader
from langchain_openai import ChatOpenAI
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain_community.document_loaders import TextLoader
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor
from langchain.tools import BaseTool, StructuredTool, tool
import nltk
import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.data.path.append("/Users/byronmackay/nltk_data")
# nltk.download('punkt')

@tool
def look_at_existing_app():
    """returns all the app's file names"""
    code = DirectoryLoader(f"./app/", silent_errors=True).load()
    return [c.metadata["source"] for c in code]

@tool
def create_new_file(filename: str):
    """Only use this if the file is not created already. 
    If it is, then use the tool get_page_contents. 
    Creates a new file with the given filename. 
    Only use this function when the file doesn't already exist."""
    with open(filename, 'w'):
        pass

@tool
def get_page_contents(files):
    """
    returns the current contents for the given file names. files is a list.
    These contents should be edited and not completely replaced.
    """
    loader = TextLoader(files[0])
    return [f"___{doc.metadata["source"]}___\n{doc.page_content}" for doc in loader.load()]

@tool
def update_file_contents(file_dict):
    """
    Updates existing files in the app. 
    file_dict is a dictionary with the key as the file's path and the value as the content.
    """

    for path, content in file_dict.items():
        update_file(path, content)

    return f"The follow files have been updated: {"\n".join(file_dict.keys())}"

def update_file(file_path, new_content):
    try:
        # Open the file in write mode
        with open(file_path, 'w') as file:
            # Write the new content to the file
            file.write(new_content)
        print("File updated successfully.")
    except Exception as e:
        print("Error:", e)

tools = [ShellTool(ask_human_input=True), update_file_contents, look_at_existing_app, get_page_contents]
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert web developer.",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


llm_with_tools = llm.bind_tools(tools)

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

while(True):
    prompt = input("Prompt: ")
    list(agent_executor.stream({"input": prompt}))

# Add the funcitonality to game.js so the cursor moves from one box to the next when a letter is put in it. Conversly, when a box is empty and the delete key is pressed, the cursor should go to the previous box and the character in that box should be removed
# Add the funcitonlaity to game.js to check the answer to the game. if the inputed word matches the secret word, a message should appear congratulating the user with an emoji at the end.
# When a word is guessed, create a new row of text boxes below the current ones. The old text boxes should become uneditable and the new text boxes are the ones the person is using to enter new letters