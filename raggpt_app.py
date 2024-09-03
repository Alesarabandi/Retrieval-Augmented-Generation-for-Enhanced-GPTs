"""
This module uses Gradio to create an interactive chatbot web app with three main parts:

Top Row: This section features the chatbot where you can have a conversation. It also includes a hidden bar with extra info that you can toggle on or off with a button. You can provide feedback to the chatbot using like or dislike icons.

Middle Row: This area has a box where you can type messages or upload files such as PDFs or documents.

The app responds to your interactions in several ways:

When you upload files, it reads them and updates the chat and input area.
When you send a message, the chatbot replies based on your input, the document type you selected, and the current settings.
The response appears in the chat and input area, and the extra info bar may update as well.
To use the app, simply run the script. The comments in the code provide more details on how everything works.
"""
import gradio as gr
import openai
from utils.upload_file import UploadFile
from utils.chatbot import ChatBot
from utils.ui_settings import UISettings

openai.api_key = "API KEY"


with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.TabItem("CYBERSEC-GPT 🤖"):
            ##############
            # First ROW:
            ##############
            with gr.Row() as row_one:
           
                
                with gr.Column(visible=False) as reference_bar:
                
                    ref_output = gr.Markdown()
                    

                with gr.Column() as chatbot_output:
                    chatbot = gr.Chatbot(
                        [],
                        elem_id="chatbot",
                        bubble_full_width=False,
                        height=500,
                        avatar_images=(
                            ("Directory of the image"),

                    )
                    # **Adding like/dislike icons
                    chatbot.like(UISettings.feedback, None, None)
            ##############
            # SECOND ROW:
            ##############
            with gr.Row():
                input_txt = gr.Textbox(
                    lines=4,
                    scale=8,
                    placeholder="Enter text and press enter, or upload PDF files",
                    container=False,
                )

            ##############
            # Third ROW:
            ##############
            with gr.Row() as row_two:
                text_submit_btn = gr.Button(value="Submit text")
                sidebar_state = gr.State(False)
                btn_toggle_sidebar = gr.Button(
                    value="References")
                btn_toggle_sidebar.click(UISettings.toggle_sidebar, [sidebar_state], [
                    reference_bar, sidebar_state])
                upload_btn = gr.UploadButton(
                    "📁 Upload PDF or file", file_types=[
                        '.pdf',
                        '.doc'
                    ],
                    file_count="multiple")
                temperature_bar = gr.Slider(minimum=0, maximum=1, value=0, step=0.1,
                                            label="Temperature", info="Choose between 0 and 1")
                rag_with_dropdown = gr.Dropdown(
                    label="RAG with", choices=["Preprocessed doc", "Upload doc: Process for RAG"], value="Preprocessed doc")
                clear_button = gr.ClearButton([input_txt, chatbot])
            ##############
            # Process:
            ##############
            file_msg = upload_btn.upload(fn=UploadFile.process_uploaded_files, inputs=[
                upload_btn, chatbot, rag_with_dropdown], outputs=[input_txt, chatbot], queue=False)

            txt_msg = input_txt.submit(fn=ChatBot.respond,
                                       inputs=[chatbot, input_txt,
                                               rag_with_dropdown, temperature_bar],
                                       outputs=[input_txt,
                                                chatbot, ref_output],
                                       queue=False).then(lambda: gr.Textbox(interactive=True),
                                                         None, [input_txt], queue=False)

            txt_msg = text_submit_btn.click(fn=ChatBot.respond,
                                            inputs=[chatbot, input_txt,
                                                    rag_with_dropdown, temperature_bar],
                                            outputs=[input_txt,
                                                     chatbot, ref_output],
                                            queue=False).then(lambda: gr.Textbox(interactive=True),
                                                              None, [input_txt], queue=False)


if __name__ == "__main__":
    demo.launch()
