import google.generativeai as genai
import os
import gradio as gr

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

initial_prompt = (
    "Você é um assistente que analisa o sentimento de textos fornecidos, "
    "identificando se o sentimento é positivo, negativo ou neutro, e fornecendo um breve feedback."
)

model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=initial_prompt)

chat = model.start_chat()
def gradio_wrapper(message, _history):
    user_text = message["text"]
    files = message.get("files", [])
    file_contents = []
    if files:
        for file_info in files:
            file_path = file_info["path"]
            if file_info["mime_type"] == "text/plain":
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                file_contents.append(content)
            else:
                pass
    combined_text = user_text + "\n\n" + "\n\n".join(file_contents)
    prompt = f"Analise o sentimento do seguinte texto:\n{combined_text}"
    response = chat.send_message(prompt)
    return response.text

chat_interface = gr.ChatInterface(
    fn=gradio_wrapper,
    title="Analisador de Sentimentos 🎭",
    multimodal=True
)
chat_interface.launch()