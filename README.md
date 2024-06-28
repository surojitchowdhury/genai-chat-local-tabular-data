# genai-chat-local-tabular-data
Project to use Open Source LLM to chat securely with your local tabular data without any cost!

To start using:
- Download ollama from https://ollama.com/download
- Pull Open Source model `codellama` by running following commands from Terminal.
    `ollama pull codellama`
- Clone the git repo and install all python dependencies using:
    `pip install -r requirements.txt`
- Run the application using:
    `python app.py`

Application will be hosted securely on your local at:
http://127.0.0.1:7860

App Functionality:
- Process Files: To upload CSV or XLSX files
- Chat: To chat with your loaded data in simple english
- Run SQL: In case LLM returns with an SQL without giving proper result, just run the SQL in this mode. You can also run your custom SQL on the Data if you are familiar with SQL. Tables names are same as your files names in alphanumeric (i.e. without any special characters in file name)

Live Demo: https://www.youtube.com/watch?v=29f-oViiI_s

The application doesn't need any internet connection, any API Keys to run. So effectively IT IS FREE to RUN!!!

