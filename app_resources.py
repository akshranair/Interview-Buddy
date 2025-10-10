import gradio as gr
def get_Welcome_page_with_title(app_name:str):
    return f"""
            <div class="welcome-screen">
                <div class="welcome-title">{app_name}</div>
                <div class="welcome-subtitle">
                    Ace your coding interviews with AI-powered practice sessions.<br>
                    45 minutes • Real-time feedback • Comprehensive evaluation
                </div>
            </div>
        """
def get_language_selection_title():
    return """
                <div style="text-align: center; margin-bottom: 20px;">
                    <h3 style="color: #2c3e50; font-size: 20px; font-weight: 600;">
                        Select Your Preferred Programming Language
                    </h3>
                </div>
            """

def get_company_selection_title():
    return """
            <div style="text-align: center; margin-bottom: 20px;">
                <h3 style="color: #2c3e50; font-size: 20px; font-weight: 600;">
                    Select Company You are preparing for
                </h3>
            </div>
        """

def get_language_dropdown():
    language_select = gr.Dropdown(
    choices=["Python", "JavaScript", "Java", "C++", "Go"],
    value="Python",
    label="Programming Language",
    elem_classes="language-selector",
    container=True,
    scale=1
    )
    return language_select

def get_welcome_page_start_button():
    start_button = gr.Button("Start Interview", elem_classes="start-button", size = "lg")
    return start_button

def get_welcome_page_company_list():
    company_select = gr.Dropdown(
        choices = ["Google", "Microsoft","Amazon", "Meta", "JPMorgan"],
        value = "Google",
        label = "Companies",
        elem_classes = "company-selctor",
        container = True,
        scale = 1,
    )
    return company_select

def get_APP_TITLE(title:str):
    return f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <h1 style="color: #00aaff; font-size: 32px; font-weight: 700; margin-bottom: 5px;">
                    {title}
                </h1>
            </div>
        """