# %%
import json
from pathlib import Path

import openai
import pandas as pd

# User input -------------------------------------------------------------
openai_secret_file_path = "M:\secrets\OpenAI\openai_secret.json"
message_contents = [
    "API keyを保存するjsonファイルの例を教えてください",
    '\n\n{\n "API_KEY": "your_api_key_here"\n}',
    "そのjsonファイルからAPI KEYを取り出すコードをpythonで書いてください。"
]
#  ------------------------------------------------------------------------

def set_api_key_from_file(file_path):
    with open(file_path, "r") as f:
        openai_secret = json.load(f)
    openai.api_key = openai_secret["API_KEY"]

def save_chat_history(file_path, message_content):
    if file_path.is_file():
        chat_history = pd.read_csv(file_path, index_col="id")
    else:
        chat_history = pd.DataFrame(
            index=pd.Index([], name="id"),
            columns=["query","response"]
        )
    print(len(chat_history))
    chat_history.loc[len(chat_history)] = [message_contents[-1], message_content]
    chat_history.to_csv(file_path)

def chat(message_contents, model="gpt-3.5-turbo"):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    for i, content in enumerate(message_contents):
        role = "user" if i % 2 == 0 else "assistant"
        messages.append({"role": role, "content": content})
    return openai.ChatCompletion.create(model=model, messages=messages)

def run():
    set_api_key_from_file(openai_secret_file_path)
    response = chat(message_contents, "gpt-3.5-turbo")
    message_content = response["choices"][0]["message"]["content"]
    print(message_content)
    save_chat_history(Path("chat_history.csv"), message_content)

if __name__ == "__main__":
    run()
# %%

