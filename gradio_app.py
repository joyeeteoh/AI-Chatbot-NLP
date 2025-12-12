import gradio as gr
from agent.chatbot import chatbot_workflow

custom_theme = gr.themes.Base(
    primary_hue="blue", secondary_hue="gray", neutral_hue="blue"
).set(
    body_background_fill="#e6f0ff",
    button_primary_background_fill="#004eaa",
    button_primary_text_color="white",
    block_background_fill="white",
    border_color_primary="#004eaa",
)

with gr.Blocks(
    theme=custom_theme,
    css="""
        #title-text {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
        }
        #description-text {
            text-align: center;
            font-size: 24px;
        }
        .gr-chatbot, #chatbot {
            max-height: none !important;
            height: auto !important;
            overflow: visible !important;
            flex-direction: column;
            min-height: 400px;
        } 
        #chatbot .wrapper {
            background: inherit;
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        #chatbot .bubble-wrap {
            background: inherit;
            flex: 1;
        }        
        .input-container {
            gap: 10px;
        }
    """,
) as app:
    gr.Image(
        "assets/tng_logo.jpg",
        height=80,
        show_label=False,
        container=False,
        show_fullscreen_button=False,
        show_download_button=False,
    )
    gr.Markdown("# 🟦 Touch 'n Go - FAQ Chatbot", elem_id="title-text")
    gr.Markdown(
        "💬 Ask any question about Touch 'n Go eWallet, tolls, payments, and more!",
        elem_id="description-text",
    )

    gr.ChatInterface(
        fn=chatbot_workflow,
        chatbot=gr.Chatbot(elem_id="chatbot", type="messages", container=True),
        textbox=gr.Textbox(
            placeholder="Ask me about Touch 'n Go services...",
            label="Your Question",
            autofocus=True,
            submit_btn="🚀Send",
        ),
        fill_height=False,
        type="messages",
        show_progress="hidden",
    )

app.launch()
