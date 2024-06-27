
import os
from dotenv import load_dotenv
import yaml
from pyprojroot import here
import shutil
from langchain_community.llms import Ollama


class LoadConfig:
    def __init__(self) -> None:
        with open(("./configs/app_config.yml")) as cfg:
            app_config = yaml.load(cfg, Loader=yaml.FullLoader)

        self.load_directories(app_config=app_config)
        self.load_llm_configs(app_config=app_config)
        self.load_llm_model()

        # Un comment the code below if you want to clean up the upload csv SQL DB on every fresh run of the chatbot. (if it exists)
        #self.remove_directory(self.data_directory)

    def load_directories(self, app_config):
        self.uploaded_files_sqldb_directory = str(here(
            app_config["directories"]["uploaded_files_sqldb_directory"]))
        self.data_directory = str(here(
            app_config["directories"]["data_directory"]))

    def load_llm_configs(self, app_config):
        self.model_name = app_config["llm_config"]["model_name"]
        self.local_model_base_url = app_config["llm_config"]["local_model_base_url"]
        self.write_query_prompt = app_config["llm_config"]["write_query_prompt"]
        self.answer_prompt = app_config["llm_config"]["answer_prompt"]
        self.temperature = app_config["llm_config"]["temperature"]
        self.embedding_model_name = os.getenv("embed_deployment_name")

    def load_llm_model(self):
        self.langchain_llm  = Ollama(model=self.model_name, base_url=self.local_model_base_url, temperature = self.temperature)
        

    