import re
import time
import json
import cheshire_cat_api as ccat

WEBSITE = "cheshire_cat_core"
PORT = 80
content = ""

def on_open():
    # This is triggered when the connection is opened
    print("Connection opened!")

def on_message(message: str):
    # This is triggered when a new message arrives
    # and grabs the message
    # print(message)
    global content

    response = json.loads(message)
    if response["type"] != "chat_token":
      print(response)
    if response["type"] == "chat":
      content = response

def on_error(exception: Exception):
    # This is triggered when a WebSocket error is raised
    global content
    print(str(exception))
    content = str(exception)

def on_close(status_code: int, message: str):
    # This is triggered when the connection is closed
    print(f"Connection closed!")



def connect(user_id):
  # Connection settings with default values
  config = ccat.Config(
      base_url=WEBSITE,
      port=PORT,
      user_id=user_id,
      auth_key="",
      secure_connection=False
  )

  # Cat Client
  cat_client = ccat.CatClient(
      config=config,
      on_open=on_open,
      on_close=on_close,
      on_message=on_message,
      on_error=on_error
  )

  # Connect to the WebSocket API
  cat_client.connect_ws()

  while not cat_client.is_ws_connected:
      time.sleep(1)

  return cat_client

def disconnect(cat_client):
  cat_client.close()


def ask_gpt(cat_client, prompt):
  global content

  content = ""
  cat_client.send(message=prompt)

  while content == "":
    True

  return content


def prompt(user_id, prompt):
  client = connect(user_id)
  res = ask_gpt(client, prompt)
  disconnect(client)
  return res["content"], [( x["metadata"]["source"], x["score"], x["page_content"]) for x in res["why"]["memory"]["declarative"]]


def print_response(res):
  print("Output:\n")
  print(res[0])
  print("\n\nMemories:\n\n")
  for x in res[1]:
    print(f"{x[0]} - {x[1]}\n{x[2]}\n\n")


def clean_history(user):
  import requests

  url = f"http://{WEBSITE}:{PORT}/memory/conversation_history/"

  payload = {}
  headers = {
    'Accept': 'application/json',
    'user_id': user
  }

  response = requests.request("DELETE", url, headers=headers, data=payload)
  print(response.text)

def get_history(user):
  import requests

  url = f"http://{WEBSITE}:{PORT}/memory/conversation_history/"

  payload = {}
  headers = {
    'Accept': 'application/json',
    'user_id': user
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  print(response.text)

def upload_memory(user, chunk_size, file_name, file_path):
  import http.client
  import mimetypes
  from codecs import encode
  import time

  conn = http.client.HTTPConnection(WEBSITE, PORT)
  dataList = []
  boundary = 'boundary'
  dataList.append(encode('--' + boundary))
  dataList.append(encode('Content-Disposition: form-data; name=file; filename={0}'.format(file_name)))

  fileType = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
  dataList.append(encode('Content-Type: {}'.format(fileType)))
  dataList.append(encode(''))

  with open(file_path, 'rb') as f:
    dataList.append(f.read())
  dataList.append(encode('--' + boundary))
  dataList.append(encode('Content-Disposition: form-data; name=chunk_size;'))

  dataList.append(encode('Content-Type: {}'.format('text/plain')))
  dataList.append(encode(''))

  dataList.append(encode(str(chunk_size)))
  dataList.append(encode('--' + boundary))
  dataList.append(encode('Content-Disposition: form-data; name=chunk_overlap;'))

  dataList.append(encode('Content-Type: {}'.format('text/plain')))
  dataList.append(encode(''))

  dataList.append(encode("100"))
  dataList.append(encode('--'+boundary+'--'))
  dataList.append(encode(''))
  body = b'\r\n'.join(dataList)
  payload = body
  headers = {
    'Content-type': 'multipart/form-data; boundary={}'.format(boundary),
    'Accept': 'application/json',
    'user_id': user
  }
  conn.request("POST", "/rabbithole/", payload, headers)
  res = conn.getresponse()
  data = res.read()
  print(data.decode("utf-8"))

def upload_all_memories_folder(user, chunk_size, folder):
  import os
  files = os.listdir(folder)

  for file_name in files:
    if file_name.endswith(".txt"):
      file_path = os.path.join(folder, file_name)
      upload_memory(user, chunk_size, file_name, file_path)
      time.sleep(1)


def summarise_in_folder(user, folder, target_folder):
  import os
  files = os.listdir(folder)

  for file_name in files:
    if file_name.endswith(".txt"):
      file_path = os.path.join(folder, file_name)
      prompt_summary_r = prompt_summary(file_path)
      clean_history(user)
      summary = prompt(user, prompt_summary_r)
      save_result(summary, f"{target_folder}/{file_name}")


def set_declarative_memories(n, t):
  import http.client
  import json

  conn = http.client.HTTPConnection(WEBSITE, PORT)

  payload = json.dumps({
    "language": "English",
    "only_local_responses": False,
    "prompt_prefix": "",
    "disable_episodic_memories": True,
    "disable_declarative_memories": False,
    "disable_procedural_memories": True,
    "number_of_declarative_items": n,
    "number_of_episodic_items": 0,
    "declarative_threshold": t,
    "episodic_threshold": 2.0,
    "legacy": True
  })

  headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
  conn.request("PUT", "/plugins/settings/cc_prompt_settings", payload, headers)
  res = conn.getresponse()
  data = res.read()
  print(data.decode("utf-8"))


def set_model_temperature(t):
  import http.client
  import json

  conn = http.client.HTTPConnection(WEBSITE, PORT)
  payload = json.dumps({
    "openai_api_key": KEY,
    "model_name": "gpt-4o-2024-11-20",
    "temperature": t,
    "streaming": True
  })
  headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
  conn.request("PUT", "/llm/settings/LLMOpenAIChatConfig", payload, headers)
  res = conn.getresponse()
  data = res.read()
  print(data.decode("utf-8"))

def set_embedder():
  import http.client
  import json

  conn = http.client.HTTPConnection(WEBSITE, PORT)
  payload = json.dumps({
    "model": "text-embedding-ada-002",
    "openai_api_key": KEY
  })
  headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
  conn.request("PUT", "/embedder/settings/EmbedderOpenAIConfig", payload, headers)
  res = conn.getresponse()
  data = res.read()
  print(data.decode("utf-8"))


def split_and_save(file_path, output_folder, delimiter, prefix, allowed):
    # Open and read the content of the source file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    content = clean_text(allowed, content)

    pattern = r'(' + delimiter + r')'
    articles = re.split(pattern, content)

    # The first item in 'articles' might not start with "Art. X" and can be an introduction or preface
    # If it doesn't match our pattern, we'll ignore it in file writing
    if not re.match(pattern, articles[0]):
        articles = articles[1:]

    # Iterate over the articles to write them to separate files
    for i in range(1, len(articles), 2):
        article_number = articles[i].replace('\n', ' ').replace(':', ' ').split(" ")[0]  # Extract the number X from "Art. X"
        file_name = f'art-{article_number}.txt'  # Create the file name
        # Write the content to the file
        with open(f"{output_folder}/{prefix}_" + file_name, 'w', encoding='utf-8') as file:
            file.write(f"{delimiter}" + articles[i])


def save_result(res, file_path):
  with open(file_path, 'w', encoding='utf-8') as file:
    file.write(res[0])


def split_files_in_folder(folder_path, output_folder, delimiter, allowed):

  import os
  files = os.listdir(folder_path)

  for file_name in files:
    if file_name.endswith(".txt"):
      file_path = os.path.join(folder_path, file_name)
      split_and_save(file_path, output_folder, delimiter, file_name[:-4], allowed)


def clean_text(allowed, content):
  if not allowed:
    return content
  return "\n".join([x for x in content.split("\n") if any([x.startswith(y) for y in allowed])])