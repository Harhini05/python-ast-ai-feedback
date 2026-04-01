# reflex_app.py

import reflex as rx
from codereviewer.code_analyzer import analyze_code
from codereviewer.ai_suggestor import chat_with_ai_bot


# ---------- STATE ----------
class State(rx.State):
    code: str = ""
    code2: str = ""
    analysis: str = ""
    comparison: str = ""
    chat_input: str = ""
    chat_history: list[str] = []

    # ---------- CODE ANALYZER ----------
    def review_code(self):
        self.analysis = analyze_code(self.code)

    def clear_code(self):
        self.code = ""
        self.analysis = ""

    def compare_code(self):
        if self.code == self.code2:
            self.comparison = "Both codes are identical ✅"
        else:
            self.comparison = "Codes are different ❌"

    def clear_compare(self):
        self.code = ""
        self.code2 = ""
        self.comparison = ""

    # ---------- CHATBOT ----------
    def chat_with_ai(self):
        if self.chat_input.strip() == "":
            return

        user_msg = f"👤 You: {self.chat_input}"
        ai_reply = chat_with_ai_bot(self.chat_input)

        self.chat_history = self.chat_history + [
            user_msg,
            f"🤖 AI: {ai_reply}"
        ]
        self.chat_input = ""

    def clear_chat(self):  # ✅ NEW FUNCTION
        self.chat_history = []
        self.chat_input = ""


# ---------- STYLE ----------
def page_style():
    return {
        "min_height": "100vh",
        "background": "linear-gradient(135deg, #667eea, #764ba2)",
        "padding": "20px",
    }


def card_style():
    return {
        "bg": "rgba(255,255,255,0.1)",
        "backdrop_filter": "blur(10px)",
        "padding": "20px",
        "border_radius": "15px",
        "width": "100%",
    }


# ---------- NAVBAR ----------
def navbar():
    return rx.hstack(
        rx.heading("💻 AI Reviewer", size="5", color="white"),
        rx.spacer(),
        rx.link("Home", href="/"),
        rx.link("Analyzer", href="/analyzer"),
        rx.link("AI Bot", href="/chatbot"),
        rx.link("Settings", href="/settings"),
        spacing="6",
        padding="15px",
        bg="rgba(0,0,0,0.3)",
        border_radius="10px",
        margin_bottom="20px",
        color="white"
    )


# ---------- HOME ----------
def home():
    return rx.container(
        rx.box(
            navbar(),
            rx.vstack(
                rx.heading("AI Code Reviewer 🚀", size="8", color="white"),
                rx.text(
                    "Analyze, compare and improve your code with AI.",
                    color="white",
                    size="5"
                ),
                spacing="4",
                align="center",
                justify="center",
                min_height="70vh",
            ),
            **page_style()
        )
    )


# ---------- ANALYZER ----------
def analyzer():
    return rx.container(
        rx.box(
            navbar(),
            rx.vstack(
                rx.heading("Code Analyzer", color="white"),
                rx.box(
                    rx.text_area(
                        placeholder="Paste your code here...",
                        value=State.code,
                        on_change=State.set_code,
                        height="200px"
                    ),
                    rx.hstack(
                        rx.button(
                            "Analyze Code",
                            on_click=State.review_code,
                            color_scheme="purple"
                        ),
                        rx.button(
                            "Clear",
                            on_click=State.clear_code,
                            color_scheme="red",
                            variant="outline"
                        ),
                    ),
                    rx.code_block(State.analysis, language="python"),
                    spacing="4",
                    **card_style()
                ),
            ),
            spacing="6",
            **page_style()
        )
    )


# ---------- CHATBOT ----------
def chatbot():
    return rx.container(
        rx.box(
            navbar(),
            rx.vstack(
                rx.heading("AI Chatbot 🤖", color="white"),

                # ✅ CLEAR BUTTON ON TOP
                rx.hstack(
                    rx.spacer(),
                    rx.button(
                        "Clear Chat",
                        on_click=State.clear_chat,
                        color_scheme="red",
                        variant="outline"
                    )
                ),

                rx.box(
                    rx.vstack(
                        rx.foreach(
                            State.chat_history,
                            lambda msg: rx.text(msg, color="white")
                        ),
                        height="300px",
                        overflow="auto"
                    ),

                    rx.hstack(
                        rx.input(
                            placeholder="Ask something...",
                            value=State.chat_input,
                            on_change=State.set_chat_input,
                            width="70%"
                        ),
                        rx.button(
                            "Send",
                            on_click=State.chat_with_ai,
                            color_scheme="purple"
                        ),
                    ),
                    spacing="4",
                    **card_style()
                ),
            ),
            spacing="6",
            **page_style()
        )
    )


# ---------- SETTINGS ----------
def settings():
    return rx.container(
        rx.box(
            navbar(),
            rx.vstack(
                rx.heading("Settings ⚙️", color="white"),
                rx.box(
                    rx.checkbox("Enable AI Suggestions", default_checked=True),
                    rx.checkbox("Dark Mode (Coming Soon)"),
                    spacing="3",
                    **card_style()
                ),
            ),
            spacing="6",
            **page_style()
        )
    )


# ---------- APP ----------
app = rx.App()
app.add_page(home, route="")
app.add_page(analyzer, route="analyzer")
app.add_page(chatbot, route="chatbot")
app.add_page(settings, route="settings")