import gradio as gr
from flask import Flask, Response
import os

# --- GradioのUI関数（シンプルな例：必要に応じて置き換え） ---
def greet(name):
    return f"こんにちは、{name}さん。ご質問があれば選択肢からどうぞ。"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")

# --- Flaskアプリ定義 ---
app = Flask(__name__)

# --- ルートアクセスでGradioを返す ---
@app.route("/")
def main():
    return Response(demo.launch(share=False, inline=True, prevent_thread_lock=True), mimetype='text/html')

# --- ポート指定：Render用 ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
