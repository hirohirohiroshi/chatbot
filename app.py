# import json
# import gradio as gr

# # --- FAQデータ読み込み ---
# with open("faq_data.json", "r", encoding="utf-8") as f:
#     faq_data = json.load(f)

# with open("faq_tree.json", "r", encoding="utf-8") as f:
#     faq_tree = json.load(f)

# # --- 質問から回答を取得 ---
# def get_answer(question):
#     for item in faq_data:
#         if item["question"] == question:
#             return item["answer"]
#     return "申し訳ありません、その質問に対する回答が見つかりませんでした。"

# # --- 質問リスト更新関数（カテゴリ選択時） ---
# def update_questions(category):
#     for group in faq_tree:
#         if group["category"] == category:
#             return gr.update(choices=group["questions"], value=None)
#     return gr.update(choices=[], value=None)

# # --- Gradio UI構築 ---
# with gr.Blocks(title="司法書士FAQ選択型Bot") as demo:
#     gr.Markdown("## 司法書士チャットBot（選択式）")
#     gr.Markdown("ジャンルを選んでから、質問を選択してください。")

#     category_dropdown = gr.Dropdown(
#         choices=[cat["category"] for cat in faq_tree],
#         label="Step 1: ジャンルを選んでください"
#     )

#     question_dropdown = gr.Dropdown(
#         choices=[],
#         label="Step 2: 質問を選んでください"
#     )

#     answer_box = gr.Textbox(label="回答", lines=5)

#     category_dropdown.change(fn=update_questions, inputs=category_dropdown, outputs=question_dropdown)
#     question_dropdown.change(fn=get_answer, inputs=question_dropdown, outputs=answer_box)

# if __name__ == "__main__":
#     demo.launch()


# app.py
import json
import gradio as gr
from flask import Flask, send_from_directory

app = Flask(__name__)

# --- FAQデータ読み込み ---
with open("faq_data.json", "r", encoding="utf-8") as f:
    faq_data = json.load(f)

with open("faq_tree.json", "r", encoding="utf-8") as f:
    faq_tree = json.load(f)

# --- 質問と回答照合 ---
def get_answer(question):
    for item in faq_data:
        if item["question"] == question:
            return item["answer"]
    return "申し訳ありません、その質問に対する回答が見つかりませんでした。"

def update_questions(category):
    for group in faq_tree:
        if group["category"] == category:
            return gr.update(choices=group["questions"], value=None)
    return gr.update(choices=[], value=None)

# --- Gradioインタフェース構築 ---
with gr.Blocks(title="司法書士FAQ選択型Bot") as demo:
    gr.Markdown("## 司法書士チャットBot（選択式）")
    category_dropdown = gr.Dropdown(
        choices=[cat["category"] for cat in faq_tree],
        label="Step 1: ジャンルを選んでください"
    )
    question_dropdown = gr.Dropdown(
        choices=[],
        label="Step 2: 質問を選んでください"
    )
    answer_box = gr.Textbox(label="回答", lines=5)
    category_dropdown.change(fn=update_questions, inputs=category_dropdown, outputs=question_dropdown)
    question_dropdown.change(fn=get_answer, inputs=question_dropdown, outputs=answer_box)

app = gr.mount_gradio_app(app, demo, path="/")

# --- アセット（アイコン等）配布対応（任意）---
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(".", filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
