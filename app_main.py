import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv
from get_problem import get_system_prompt
from app_resources import get_APP_TITLE, get_company_selection_title, get_language_dropdown, get_language_selection_title, get_welcome_page_company_list,get_welcome_page_start_button,get_Welcome_page_with_title
from get_problem import get_system_prompt, find_random_problem
APP_NAME = "Interview Buddy"

custom_css =  """.language-selector {
    margin-bottom: 16px;
}"""

load_dotenv(override=True)

def start_interview(selected_language, selected_company):
    welcome = gr.update(visible=False)
    interview = gr.update(visible=True)

    question = find_random_problem()
    statement, hints, topics = question[2], question[6], question[7]

    system_prompt = get_system_prompt(selected_company, statement, hints, topics)
    initial_chat = [{"role": "assistant", "content": "Hello! I'm your AI interviewer. I'll be conducting a 45-minute coding interview with you today. Please introduce yourself."}]
    return welcome, interview, initial_chat, system_prompt

def get_Welcome_page_title():
    return get_Welcome_page_with_title(APP_NAME)

def get_app_title():
    return get_APP_TITLE(APP_NAME)

def respond(message, history, prompt):
    messages = [{"role":"system", "content": prompt}] + history + [{"role":"user", "content":message}]
    openai = OpenAI()
    responses = openai.chat.completions.create(
        model = "gpt-4o-mini",
        messages=messages
    )
    response = responses.choices[0].message.content
    updated_history = history + [{"role":"user", "content":message}, {"role":"assistant", "content":response}]

    return updated_history, ""

def Display_Welcome_Screen():
    with gr.Column(elem_id="welcome-container", visible=True) as welcome_screen:
        gr.HTML(get_Welcome_page_title())
        with gr.Row():
            with gr.Column(elem_id="language-selection"):
                gr.HTML(get_language_selection_title())
                language_select = get_language_dropdown()
            with gr.Column(elem_id="language-selection"):
                gr.HTML(get_company_selection_title())
                company_select = get_welcome_page_company_list()
    
        start_button = get_welcome_page_start_button()
    return welcome_screen,language_select, company_select, start_button


def Display_Interview_Screen():
    with gr.Column(elem_id = "interview-container", visible = False) as interview_screen:
        gr.HTML(get_app_title())
    
        with gr.Row():
            with gr.Column(scale = 1) as chat_area:
                gr.HTML('<div class="column-header"><span>Interviewer</span></div>')
                with gr.Column(elem_classes="chatbot-container"):
                    chatbot = gr.Chatbot(
                        type = "messages",
                        value = [],
                        height = 502,
                        show_label= False,
                        elem_classes="chatbot"
                    )
                    with gr.Row(elem_classes="input-row"):
                        msg = gr.Textbox(
                            placeholder = "Type your response here ...",
                            show_label = False,
                            scale=4,
                            container = False
                        )
                    send_chat_button = gr.Button("Send", scale = 1,elem_classes="primary-button")
            with gr.Column( scale = 1) as notes_area:
                gr.HTML('<div class="column-header"><span>Notes</span></div>')
                
                with gr.Column(elem_classes="node-pad-container"):
                    note_pad= gr.Textbox(
                        placeholder= "Write your notes here...",
                        show_label = False,
                        lines=30,
                        container = False
                    )
            with gr.Column(scale = 1) as code_area:
                gr.HTML('<div class="column-header"><span>Code</span></div>')
                with gr.Column(elem_classes="code-editor-container"):
                    code_editor = gr.Code(
                        show_label = False,
                        lines = 32,
                        max_lines=32,
                        elem_classes="code-editor",
                        value = "",
                        wrap_lines=True
                    )
                
                with gr.Row(elem_classes="code-review-button"):
                    review_button = gr.Button(
                        "Review Code",
                        scale = 1,
                        elem_classes="submit-button"
                    )
            


    return interview_screen, chatbot, msg, note_pad, code_editor, review_button, send_chat_button

with gr.Blocks(css = custom_css, title = "Interview-Buddy", theme = gr.themes.Soft()) as app:
    system_prompt = gr.State("")
    welcome_screen, language_select, company_select, start_button = Display_Welcome_Screen()
    interview_screen, chatbot, msg, note_pad, code_editor, review_button, send_chat_button = Display_Interview_Screen()
    start_button.click(
        start_interview,
        inputs = [language_select,company_select],
        outputs=[welcome_screen, interview_screen, chatbot, system_prompt]
    )

    msg.submit(respond, [msg, chatbot, system_prompt], [chatbot, msg])
   

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7862,
        share = False
    )