# from data_sources import process_data_upload
# from functions import example_question_generator, chatbot_with_fc
# from utils import TEMP_DIR, message_dict
# import gradio as gr

# import ast
# import os
# from getpass import getpass
# from dotenv import load_dotenv

# load_dotenv()

# if "OPENAI_API_KEY" not in os.environ:
#     os.environ["OPENAI_API_KEY"] = getpass("Enter OpenAI API key:")

# def delete_db(req: gr.Request):
#     import shutil
#     dir_path = TEMP_DIR / str(req.session_hash)
#     if os.path.exists(dir_path):
#         shutil.rmtree(dir_path)
#         message_dict[req.session_hash] = None

# def run_example(input):
#     return input

# def example_display(input):
#     if input == None:
#         display = True
#     else:
#         display = False
#     return [gr.update(visible=display),gr.update(visible=display)]

# css= ".file_marker .large{min-height:50px !important;} .example_btn{max-width:300px;}"

# with gr.Blocks(css=css, delete_cache=(3600,3600)) as demo:
#     title = gr.HTML("<h1 style='text-align:center;'>Virtual Data Analyst</h1>")
#     description = gr.HTML("""<p style='text-align:center;'>Upload a data file and chat with our virtual data analyst 
#                           to get insights on your data set. Currently accepts CSV, TSV, TXT, XLS, XLSX, XML, and JSON files. 
#                           Can now generate charts and graphs! Can run linear regressions!
#                           Try a sample file to get started!</p>""")
#                         #   <p style='text-align:center;'>This tool is under active development. If you experience bugs with use, 
#                         #   open a discussion in the community tab and I will respond.</p>""")
#     example_file_1 = gr.File(visible=False, value="samples/bank_marketing_campaign.csv")
#     example_file_2 = gr.File(visible=False, value="samples/online_retail_data.csv")
#     with gr.Row():
#         example_btn_1 = gr.Button(value="Try Me: bank_marketing_campaign.csv", elem_classes="example_btn", size="md", variant="primary")
#         example_btn_2 = gr.Button(value="Try Me: online_retail_data.csv", elem_classes="example_btn", size="md", variant="primary")

#     file_output = gr.File(label="Data File (CSV, TSV, TXT, XLS, XLSX, XML, JSON)", show_label=True, elem_classes="file_marker", file_types=['.csv','.xlsx','.txt','.json','.ndjson','.xml','.xls','.tsv'])
#     example_btn_1.click(fn=run_example, inputs=example_file_1, outputs=file_output)
#     example_btn_2.click(fn=run_example, inputs=example_file_2, outputs=file_output)
#     file_output.change(fn=example_display, inputs=file_output, outputs=[example_btn_1, example_btn_2])

#     @gr.render(inputs=file_output)
#     def data_options(filename, request: gr.Request):
#         print(filename)
#         message_dict[request.session_hash] = None
#         if filename:
#             process_upload(filename, request.session_hash)
#             if "bank_marketing_campaign" in filename:
#                 example_questions = [
#                                         ["Describe the dataset"],
#                                         ["What levels of education have the highest and lowest average balance?"],
#                                         ["What job is most and least common for a yes response from the individuals, not counting 'unknown'?"],
#                                         ["Can you generate a bar chart of education vs. average balance?"],
#                                         ["Can you generate a table of levels of education versus average balance, percent married, percent with a loan, and percent in default?"],
#                                         ["Can we predict the relationship between the number of contacts performed before this campaign and the average balance?"],
#                                     ]
#             elif "online_retail_data" in filename:
#                 example_questions = [
#                                         ["Describe the dataset"],
#                                         ["What month had the highest revenue?"],
#                                         ["Is revenue higher in the morning or afternoon?"],
#                                         ["Can you generate a line graph of revenue per month?"],
#                                         ["Can you generate a table of revenue per month?"],
#                                         ["Can we predict how time of day affects revenue in this data set?"],
#                                     ]
#             else:
#                 try:
#                     generated_examples = ast.literal_eval(example_question_generator(request.session_hash))
#                     example_questions = [
#                                             ["Describe the dataset"]
#                                         ]
#                     for example in generated_examples:
#                         example_questions.append([example])
#                 except:
#                     example_questions = [
#                                         ["Describe the dataset"],
#                                         ["List the columns in the dataset"],
#                                         ["What could this data be used for?"],
#                                     ]
#             parameters = gr.Textbox(visible=False, value=request.session_hash)
#             bot = gr.Chatbot(type='messages', label="CSV Chat Window", render_markdown=True, sanitize_html=False, show_label=True, render=False, visible=True, elem_classes="chatbot")
#             chat = gr.ChatInterface(
#                                 fn=chatbot_with_fc,
#                                 type='messages',
#                                 chatbot=bot,
#                                 title="Chat with your data file",
#                                 concurrency_limit=None,
#                                 examples=example_questions,
#                                 additional_inputs=parameters
#                                 ) 
    
#     def process_upload(upload_value, session_hash):
#         if upload_value:
#             process_data_upload(upload_value, session_hash)
#         return [], []
    
#     demo.unload(delete_db)

# ## Uncomment the line below to launch the chat app with UI
# demo.launch(debug=True, allowed_paths=["temp/"])

from data_sources import process_data_upload
from functions import example_question_generator, chatbot_with_fc
from utils import TEMP_DIR, message_dict
import gradio as gr

import ast
import os
from getpass import getpass
from dotenv import load_dotenv

load_dotenv()

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = getpass("Enter OpenAI API key:")

def delete_db(req: gr.Request):
    import shutil
    dir_path = TEMP_DIR / str(req.session_hash)
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        message_dict[req.session_hash] = None

def run_example(input):
    return input

def example_display(input):
    if input == None:
        display = True
    else:
        display = False
    return [gr.update(visible=display),gr.update(visible=display)]

css= ".file_marker .large{min-height:50px !important;} .example_btn{max-width:300px;}"

with gr.Blocks(css=css, delete_cache=(3600,3600)) as demo:
    title = gr.HTML("<h1 style='text-align:center;'>Virtual Data Analyst</h1>")
    description = gr.HTML("""<p style='text-align:center;'>Upload a data file and chat with our virtual data analyst 
                          to get insights on your data set. Currently accepts CSV, TSV, TXT, XLS, XLSX, XML, and JSON files. 
                          Can now generate charts and graphs! Can run linear regressions!
                          Try a sample file to get started!</p>""")
                        #   <p style='text-align:center;'>This tool is under active development. If you experience bugs with use, 
                        #   open a discussion in the community tab and I will respond.</p>""")
    example_file_1 = gr.File(visible=False, value="samples/bank_marketing_campaign.csv")
    example_file_2 = gr.File(visible=False, value="samples/online_retail_data.csv")
    with gr.Row():
        example_btn_1 = gr.Button(value="Try Me: bank_marketing_campaign.csv", elem_classes="example_btn", size="md", variant="primary")
        example_btn_2 = gr.Button(value="Try Me: online_retail_data.csv", elem_classes="example_btn", size="md", variant="primary")

    file_output = gr.File(label="Data File (CSV, TSV, TXT, XLS, XLSX, XML, JSON)", show_label=True, elem_classes="file_marker", file_types=['.csv','.xlsx','.txt','.json','.ndjson','.xml','.xls','.tsv'])
    example_btn_1.click(fn=run_example, inputs=example_file_1, outputs=file_output)
    example_btn_2.click(fn=run_example, inputs=example_file_2, outputs=file_output)
    file_output.change(fn=example_display, inputs=file_output, outputs=[example_btn_1, example_btn_2])

    @gr.render(inputs=file_output)
    def data_options(filename, request: gr.Request):
        print(filename)
        message_dict[request.session_hash] = None
        if filename:
            process_message = process_upload(filename, request.session_hash)
            gr.HTML(value=process_message[1], padding=False)
            if process_message[0] == "success":
                if "bank_marketing_campaign" in filename:
                    example_questions = [
                                            ["Describe the dataset"],
                                            ["What levels of education have the highest and lowest average balance?"],
                                            ["What job is most and least common for a yes response from the individuals, not counting 'unknown'?"],
                                            ["Can you generate a bar chart of education vs. average balance?"],
                                            ["Can you generate a table of levels of education versus average balance, percent married, percent with a loan, and percent in default?"],
                                            ["Can we predict the relationship between the number of contacts performed before this campaign and the average balance?"],
                                        ]
                elif "online_retail_data" in filename:
                    example_questions = [
                                            ["Describe the dataset"],
                                            ["What month had the highest revenue?"],
                                            ["Is revenue higher in the morning or afternoon?"],
                                            ["Can you generate a line graph of revenue per month?"],
                                            ["Can you generate a table of revenue per month?"],
                                            ["Can we predict how time of day affects revenue in this data set?"],
                                        ]
                else:
                    try:
                        generated_examples = ast.literal_eval(example_question_generator(request.session_hash))
                        example_questions = [
                                                ["Describe the dataset"]
                                            ]
                        for example in generated_examples:
                            example_questions.append([example])
                    except:
                        example_questions = [
                                            ["Describe the dataset"],
                                            ["List the columns in the dataset"],
                                            ["What could this data be used for?"],
                                        ]
                parameters = gr.Textbox(visible=False, value=request.session_hash)
                bot = gr.Chatbot(type='messages', label="CSV Chat Window", render_markdown=True, sanitize_html=False, show_label=True, render=False, visible=True, elem_classes="chatbot")
                chat = gr.ChatInterface(
                                    fn=chatbot_with_fc,
                                    type='messages',
                                    chatbot=bot,
                                    title="Chat with your data file",
                                    concurrency_limit=None,
                                    examples=example_questions,
                                    additional_inputs=parameters
                                    ) 
    
    def process_upload(upload_value, session_hash):
        if upload_value:
            process_message = process_data_upload(upload_value, session_hash)
        return process_message
    
    demo.unload(delete_db)

## Uncomment the line below to launch the chat app with UI
demo.launch(debug=True, allowed_paths=["temp/"])