import os
from typing import List, Tuple
from utils.load_config import LoadConfig
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter
from sqlalchemy import create_engine
import langchain
langchain.debug = False

APPCFG = LoadConfig()


class ChatBot:
    """
    A ChatBot class capable of responding to messages using different modes of operation.
    It can interact with SQL databases, leverage language chain agents for Q&A,
    """
    @staticmethod
    def respond(chatbot: List, message: str, app_functionality: str) -> Tuple:
        """
        Respond to a message based on the given chat and application functionality types.

        Args:
            chatbot (List): A list representing the chatbot's conversation history.
            message (str): The user's input message to the chatbot.
            app_functionality (str): Identifies the functionality for which the chatbot is being used (e.g., 'Chat').

        Returns:
            Tuple[str, List, Optional[Any]]: A tuple containing an empty string, the updated chatbot conversation list,
                                             and an optional 'None' value. The empty string and 'None' are placeholder
                                             values to match the required return type and may be updated for further functionality.
                                             Currently, the function primarily updates the chatbot conversation list.
        """
        if os.path.exists(APPCFG.uploaded_files_sqldb_directory):
                engine = create_engine(
                    f"sqlite:///{APPCFG.uploaded_files_sqldb_directory}")
                db = SQLDatabase(engine=engine)
                #print(db.dialect)
        else:
            chatbot.append(
                (message, f"SQL DB from the uploaded csv/xlsx files does not exist. Please first upload the csv files from the chatbot."))
            return "", chatbot, None
        
        if app_functionality == "Chat":                

            query_prompt =  PromptTemplate(
                        input_variables=[ 'input',  'table_info'], template=APPCFG.write_query_prompt, validate_template=False    
            )
        
            write_query = create_sql_query_chain(APPCFG.langchain_llm, db, prompt = query_prompt)
                        
            execute_query = QuerySQLDataBaseTool(db=db)

            answer_prompt = PromptTemplate.from_template(APPCFG.answer_prompt)
    
            answer = answer_prompt | APPCFG.langchain_llm | StrOutputParser()
            chain = (
                RunnablePassthrough.assign(query=write_query).assign(
                    result=itemgetter("query") | execute_query
                )
                | answer
            )
            response = chain.invoke({"question": message})

            chatbot.append(
                (message, response))
            return "", chatbot
            
        elif app_functionality == "Process files":
            chatbot.append(
                    (message, "Please select correct app functionality,i.e. Chat and try again.."))
            return "", chatbot
        
        elif app_functionality == "Run SQL":
            
            response = db.run(message)

            chatbot.append(
                (message, response))
            return "", chatbot
            

        else:
            pass    