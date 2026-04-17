import os

import gradio as gr
from smolagents import CodeAgent, InferenceClientModel, MCPClient

MCP_URL = os.getenv("MCP_SERVER_SSE_URL", "http://127.0.0.1:7860/gradio_api/mcp/sse")

mcp_client = None
agent = None


def setup_agent():
    global mcp_client, agent

    if agent is not None:
        return agent

    token = os.getenv("HUGGINGFACE_API_TOKEN")
    if not token:
        raise RuntimeError("HUGGINGFACE_API_TOKEN is not set")

    mcp_client = MCPClient(
        {
            "url": MCP_URL,
            "transport": "sse",
        }
    )

    tools = mcp_client.get_tools()
    model = InferenceClientModel(token=token)

    agent = CodeAgent(
        tools=[*tools],
        model=model,
        additional_authorized_imports=["json", "ast", "urllib", "base64"],
    )
    return agent


def chat_fn(message, history):
    current_agent = setup_agent()
    result = current_agent.run(message)
    return str(result)


demo = gr.ChatInterface(
    fn=chat_fn,
    examples=[
        "Analyze the sentiment of: I failed in the exam.",
        "Analyze the sentiment of: I got selected for my dream internship.",
        "Use the sentiment_analysis tool and explain the result for: Today was okay.",
    ],
    title="Gradio MCP Client",
    description="A Gradio UI app that connects to a remote MCP server.",
)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7861)
