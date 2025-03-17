# from typing import List
# from typing import Dict
# import plotly.io as pio
# import plotly.express as px
# import pandas as pd
# from utils import TEMP_DIR
# import os
# import ast
# from dotenv import load_dotenv

# load_dotenv()

# root_url = os.getenv("ROOT_URL")

# def chart_generation_func(data: List[str], x_column: str, y_column: str, graph_type: str, session_hash: str, layout: Dict[str,str]={}, category: str=""):
#     print("CHART GENERATION")
#     print(data)
#     print(graph_type)
#     print(x_column)
#     print(y_column)
#     print(category)
#     print(layout)
#     try:
#         dir_path = TEMP_DIR / str(session_hash)
#         chart_path = f'{dir_path}/chart.html'
#         csv_query_path = f'{dir_path}/query.csv'

#         df = pd.read_csv(csv_query_path)

#         #setting up the plotly express objects 
#         if graph_type == "bar":
#          initial_graph = px.bar(df, x=x_column, y=y_column, barmode="group")
#         elif graph_type == "scatter":
#          if category in df.columns:
#             initial_graph = px.scatter(df, x=x_column, y=y_column, color=category)  
#          else:
#             initial_graph = px.scatter(df, x=x_column, y=y_column)
#         elif graph_type == "line":
#          if category in df.columns:
#             initial_graph = px.line(df, x=x_column, y=y_column, color=category)
#          else:
#             initial_graph = px.line(df, x=x_column, y=y_column)   
#         elif graph_type == "pie":
#          initial_graph = px.pie(df, x=x_column, y=y_column)

#         fig = initial_graph.to_dict()   

#         #Processing data to account for variation from LLM
#         data_list = []
#         layout_dict = {}

#         if isinstance(data, list):
#            data_list = data
#         else:
#            data_list.append(data) 

#         data_dict = {}   
#         for data_obj in data_list:   
#          if isinstance(data_obj, str):
#             data_obj = data_obj.replace("\n", "")
#             if not data_obj.startswith('{') or not data_obj.endswith('}'):
#                data_obj = "{" + data_obj + "}"
#             data_dict = ast.literal_eval(data_obj)
#          else:
#             data_dict = data_obj
    
#         if layout and isinstance(layout, list):
#            layout_obj = layout[0]
#         else:
#            layout_obj = layout

#         if layout and isinstance(layout_obj, str):
#            layout_dict = ast.literal_eval(layout_obj)
#         else:
#            layout_dict = layout_obj

#         #Applying stylings and settings generated from LLM
#         if layout:
#          fig["layout"] = layout_dict

#         for key, value in data_dict.items():
#            if key not in ["x","y"]:
#             for data_item in fig["data"]:
#                data_item[key] = value
     
#         pio.write_html(fig, chart_path, full_html=False)

#         chart_url = f'{root_url}/gradio_api/file/temp/{session_hash}/chart.html'

#         iframe = '<div style=overflow:auto;><iframe\n    scrolling="yes"\n    width="1000px"\n    height="500px"\n    src="' + chart_url + '"\n    frameborder="0"\n    allowfullscreen\n></iframe>\n</div>'

#         return {"reply": iframe}
    
#     except Exception as e:
#       print("CHART ERROR")
#       print(e)
#       reply = f"""There was an error generating the Plotly Chart from {x_column}, {y_column}, {graph_type}, and {layout}
#               The error is {e},
#               You should probably try again.
#               """
#       return {"reply": reply}

# def table_generation_func(session_hash):
#     print("TABLE GENERATION")
#     try: 
#         dir_path = TEMP_DIR / str(session_hash)
#         csv_query_path = f'{dir_path}/query.csv'

#         df = pd.read_csv(csv_query_path)
#         print(df)

#         html_table = df.to_html()
#         print(html_table)

#         return {"reply": html_table}
    
#     except Exception as e:
#       print("TABLE ERROR")
#       print(e)
#       reply = f"""There was an error generating the Pandas DataFrame table
#               The error is {e},
#               You should probably try again.
#               """
#       return {"reply": reply}    

from typing import List
from typing import Dict
import plotly.io as pio
import plotly.express as px
import pandas as pd
from utils import TEMP_DIR
import os
import ast
from dotenv import load_dotenv

load_dotenv()

root_url = os.getenv("ROOT_URL")

def chart_generation_func(data: List[dict], x_column: str, y_column: str, graph_type: str, session_hash: str, layout: List[dict]=[{}], category: str=""):
    print("CHART GENERATION")
    print(data)
    print(graph_type)
    print(x_column)
    print(y_column)
    print(category)
    print(layout)
    try:
        dir_path = TEMP_DIR / str(session_hash)
        chart_path = f'{dir_path}/chart.html'
        csv_query_path = f'{dir_path}/query.csv'

        df = pd.read_csv(csv_query_path)

        #setting up the plotly express objects 
        if graph_type == "bar":
         initial_graph = px.bar(df, x=x_column, y=y_column, barmode="group")
        elif graph_type == "scatter":
         if category in df.columns:
            initial_graph = px.scatter(df, x=x_column, y=y_column, color=category)  
         else:
            initial_graph = px.scatter(df, x=x_column, y=y_column)
        elif graph_type == "line":
         if category in df.columns:
            initial_graph = px.line(df, x=x_column, y=y_column, color=category)
         else:
            initial_graph = px.line(df, x=x_column, y=y_column)   
        elif graph_type == "pie":
         initial_graph = px.pie(df, x=x_column, y=y_column)

        fig = initial_graph.to_dict()   

        #Processing data to account for variation from LLM
        data_list = []
        layout_dict = {}

        if isinstance(data, list):
           data_list = data
        else:
           data_list.append(data) 

        data_dict = {}   
        for data_obj in data_list:   
         if isinstance(data_obj, str):
            data_obj = data_obj.replace("\n", "")
            if not data_obj.startswith('{') or not data_obj.endswith('}'):
               data_obj = "{" + data_obj + "}"
            data_dict = ast.literal_eval(data_obj)
         else:
            data_dict = data_obj
    
        if layout and isinstance(layout, list):
           layout_obj = layout[0]
        else:
           layout_obj = layout

        if layout_obj and isinstance(layout_obj, str):
           layout_dict = ast.literal_eval(layout_obj)
        else:
           layout_dict = layout_obj

        #Applying stylings and settings generated from LLM
        if layout_dict:
         fig["layout"] = layout_dict

        for key, value in data_dict.items():
           if key not in ["x","y"]:
            for data_item in fig["data"]:
               data_item[key] = value
     
        pio.write_html(fig, chart_path, full_html=False)

        chart_url = f'{root_url}/gradio_api/file/temp/{session_hash}/chart.html'

        iframe = '<div style=overflow:auto;><iframe\n    scrolling="yes"\n    width="1000px"\n    height="500px"\n    src="' + chart_url + '"\n    frameborder="0"\n    allowfullscreen\n></iframe>\n</div>'

        return {"reply": iframe}
    
    except Exception as e:
      print("CHART ERROR")
      print(e)
      reply = f"""There was an error generating the Plotly Chart from {x_column}, {y_column}, {graph_type}, and {layout}
              The error is {e},
              You should probably try again.
              """
      return {"reply": reply}

def table_generation_func(session_hash):
    print("TABLE GENERATION")
    try: 
        dir_path = TEMP_DIR / str(session_hash)
        csv_query_path = f'{dir_path}/query.csv'

        df = pd.read_csv(csv_query_path)
        print(df)

        html_table = df.to_html()
        print(html_table)

        return {"reply": html_table}
    
    except Exception as e:
      print("TABLE ERROR")
      print(e)
      reply = f"""There was an error generating the Pandas DataFrame table 
              The error is {e},
              You should probably try again.
              """
      return {"reply": reply} 

