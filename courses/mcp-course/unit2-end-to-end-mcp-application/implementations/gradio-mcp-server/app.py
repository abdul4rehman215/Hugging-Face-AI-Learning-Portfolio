import json
import os

import gradio as gr
from textblob import TextBlob


def sentiment_analysis(text: str) -> str:
    """Analyze the sentiment of the given text and return JSON."""
    text = text.strip()

    if not text:
        return json.dumps(
            {
                "polarity": 0.0,
                "subjectivity": 0.0,
                "assessment": "neutral",
                "note": "Empty input received"
            },
            indent=2,
        )

    blob = TextBlob(text)
    sentiment = blob.sentiment
    polarity = round(sentiment.polarity, 2)
    subjectivity = round(sentiment.subjectivity, 2)

    if polarity > 0:
        assessment = "positive"
    elif polarity < 0:
        assessment = "negative"
    else:
        assessment = "neutral"

    result = {
        "polarity": polarity,
        "subjectivity": subjectivity,
        "assessment": assessment,
    }

    return json.dumps(result, indent=2)


demo = gr.Interface(
    fn=sentiment_analysis,
    inputs=gr.Textbox(lines=6, placeholder="Enter text to analyze..."),
    outputs=gr.Textbox(label="Sentiment Result"),
    title="Text Sentiment Analysis",
    description="Analyze the sentiment of text using TextBlob",
)


if __name__ == "__main__":
    server_name = os.getenv("GRADIO_SERVER_NAME", "127.0.0.1")
    server_port = int(os.getenv("GRADIO_SERVER_PORT", "7860"))

    demo.launch(
        server_name=server_name,
        server_port=server_port,
        mcp_server=True,
    )
