import google.generativeai as genai
import os
from google.api_core.exceptions import InvalidArgument
import gradio as gr
import time

initial_prompt = "Você é um consultor de desenvolvimento de projetos."

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=initial_prompt)
chat = model.start_chat()

def gradio_wrapper(message, _history):
    text = message["text"]
    uploaded_files = []
    for files_info in message["files"]:
      file_path = files_info["path"]
      uploaded_file_info = genai.upload_file(file_path)
      while uploaded_file_info.state.name == "PROCESSING":
        time.sleep(3)
        uploaded_file_info = genai.get_file(uploaded_file_info.name)
    prompt = [text]
    prompt.extend(uploaded_files)
    
    try:
        response = chat.send_message(prompt)
    except InvalidArgument as e:
          response = chat.send_message(
              f"O usuário te enviou um arquivo para você ler e obteve o erro: {e}. "
              "Pode explicar o que houve e dizer quais tipos de arquivos você "
              "dá suporte? Assuma que a pessoa não sabe programação e "
              "não quer ver o erro original. Explique de forma simples e concisa."
          )
    return response.text

chat_interface = gr.ChatInterface(
fn=gradio_wrapper,
title="Chatbot",
multimodal=True
)

chat_interface.launch()