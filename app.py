import gradio as gr
from flask import Flask, render_template_string
import threading
import os

# --- Gradio UI定義 ---
def greet(name):
    return f"こんにちは、{name}さん。ご質問があれば選択肢からどうぞ。"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")

# --- Gradio を別スレッドで起動 ---
def run_gradio():
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False, prevent_thread_lock=True)

# --- Flask アプリ定義 ---
app = Flask(__name__)

# --- ルートアクセスで iframe を返すシンプルHTML ---
@app.route("/")
def main():
    html = """
    <!DOCTYPE html>
    <html><head><title>チャットBot</title></head>
    <body style="margin:0;padding:0;">
      <iframe src="http://127.0.0.1:7860/" width="100%" height="100%" style="border:none;"></iframe>
    </body></html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    # Gradio 起動
    threading.Thread(target=run_gradio, daemon=True).start()

    # Flask 起動
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
