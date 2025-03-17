from utils import TEMP_DIR, message_dict

from haystack.dataclasses import ChatMessage
from haystack.components.generators.chat import OpenAIChatGenerator

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


chat_generator = OpenAIChatGenerator(model="gpt-4o")
response = None

def example_question_generator(session_hash):
    import sqlite3
    example_response = None
    example_messages = [
        ChatMessage.from_system(
            "You are a helpful and knowledgeable agent who has access to an SQLite database which has a table called 'data_source'."
        )
    ]
    dir_path = TEMP_DIR / str(session_hash)
    connection = sqlite3.connect(f'{dir_path}/data_source.db')
    print("Querying questions");
    cur=connection.execute('select * from data_source')
    columns = [i[0] for i in cur.description]
    print("QUESTION COLUMNS")
    print(columns)
    cur.close()
    connection.close()

    example_messages.append(ChatMessage.from_user(text=f"""We have a SQLite database with the following {columns}. 
                                                  We also have an AI agent with access to the same database that will be performing data analysis.
                                                  Please return an array of seven strings, each one being a question for our data analysis agent
                                                  that we can suggest that you believe will be insightful or helpful to a data analysis looking for
                                                  data insights. Return nothing more than the array of questions because I need that specific data structure
                                                  to process your response. No other response type or data structure will work."""))

    example_response = chat_generator.run(messages=example_messages)

    return example_response["replies"][0].text

def chatbot_with_fc(message, history, session_hash):
    from functions import sqlite_query_func, chart_generation_func, table_generation_func, regression_func
    import tools

    available_functions = {"sql_query_func": sqlite_query_func, "chart_generation_func": chart_generation_func, "table_generation_func":table_generation_func, "regression_func":regression_func }

    if message_dict[session_hash] != None:
        message_dict[session_hash].append(ChatMessage.from_user(message))
    else:
        messages = [
            ChatMessage.from_system(
                """You are a helpful and knowledgeable agent who has access to an SQLite database which has a table called 'data_source'. 
                You also have access to a chart function that can take a query.csv file generated from our sql query and uses plotly dictionaries to generate charts and graphs and returns an iframe that we can display in our chat window.
                You also have access to a function, called table_generation_func, that builds table formatted html.
                You also have access to a linear regression function, called regression_func, that can take a query.csv file generated from our sql query and a list of column names for our independent and dependent variables and return a regression data string and a regression chart which is returned as an iframe."""
            )
        ]
        messages.append(ChatMessage.from_user(message))
        message_dict[session_hash] = messages

    response = chat_generator.run(messages=message_dict[session_hash], generation_kwargs={"tools": tools.tools_call(session_hash)})

    while True:
        # if OpenAI response is a tool call
        if response and response["replies"][0].meta["finish_reason"] == "tool_calls" or response["replies"][0].tool_calls:
            function_calls = response["replies"][0].tool_calls
            for function_call in function_calls:
                message_dict[session_hash].append(ChatMessage.from_assistant(tool_calls=[function_call]))
                ## Parse function calling information
                function_name = function_call.tool_name
                function_args = function_call.arguments

                ## Find the corresponding function and call it with the given arguments
                function_to_call = available_functions[function_name]
                function_response = function_to_call(**function_args, session_hash=session_hash)
                print(function_name)
                ## Append function response to the messages list using `ChatMessage.from_tool`
                message_dict[session_hash].append(ChatMessage.from_tool(tool_result=function_response['reply'], origin=function_call))
                response = chat_generator.run(messages=message_dict[session_hash], generation_kwargs={"tools": tools.tools_call(session_hash)})

        # Regular Conversation
        else:
            message_dict[session_hash].append(response["replies"][0])
            break
    return response["replies"][0].text

                  
