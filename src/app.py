import gradio as gr
from utils.file_upload import UploadFile
from utils.chatbot import ChatBot


with gr.Blocks() as csvchat:
    with gr.Tabs():
        with gr.TabItem("Query CSV/XLSX Using OpenSource LLMs"):
            ##############
            # First ROW:
            ##############
            with gr.Row() as row_one:
                chatbot = gr.Chatbot(
                    [],
                    elem_id="chatbot",
                    bubble_full_width=False,
                    height=500,
                    avatar_images=(
                        ("./images/user.png"), "./images/ai.png")
                )

            ##############
            # SECOND ROW:
            ##############
            with gr.Row():
                input_txt = gr.Textbox(
                    lines=4,
                    scale=8,
                    placeholder="Ask your question here..",
                    container=False,
                )
            ##############
            # Third ROW:
            ##############
            with gr.Row() as row_two:
                text_submit_btn = gr.Button(value="Submit text")
                upload_btn = gr.UploadButton(
                    "📁 Upload CSV or XLSX files", file_types=['.csv', '.xlsx'], file_count="multiple")
                app_functionality = gr.Dropdown(
                    label="App functionality", choices=["Chat", "Process files", "Run SQL"], value="Chat")

                clear_button = gr.ClearButton([input_txt, chatbot])
                clear_data_button = gr.Button(value="Clear Data")
            

            ##############
            # Process:
            ##############
            file_msg = upload_btn.upload(fn=UploadFile.run_pipeline, inputs=[
                upload_btn, chatbot, app_functionality], outputs=[input_txt, chatbot], queue=False)

            clear_data_msg = clear_data_button.click(fn=UploadFile.remove_directory, inputs=[clear_data_button], outputs=[input_txt, chatbot], queue=False)
            
            txt_msg = input_txt.submit(fn=ChatBot.respond,
                                       inputs=[chatbot, input_txt,
                                                app_functionality],
                                       outputs=[input_txt,
                                                chatbot],
                                       queue=False).then(lambda: gr.Textbox(interactive=True),
                                                         None, [input_txt], queue=False)

            txt_msg = text_submit_btn.click(fn=ChatBot.respond,
                                            inputs=[chatbot, input_txt,
                                                     app_functionality],
                                            outputs=[input_txt,
                                                     chatbot],
                                            queue=False).then(lambda: gr.Textbox(interactive=True),
                                                              None, [input_txt], queue=False)


if __name__ == "__main__":
    csvchat.launch(allowed_paths=['./'])