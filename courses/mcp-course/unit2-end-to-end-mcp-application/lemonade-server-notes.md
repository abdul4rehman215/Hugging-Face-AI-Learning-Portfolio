# 🧃 Lemonade / Local Models Note

This note corresponds to the **Local Tiny Agents with AMD NPU and iGPU Acceleration** page from Unit 2.

## What that page is about
The page demonstrates a different deployment style from the rest of the EC2 workflow documented in this folder.

Its focus is:
- running an open-source model locally
- using an OpenAI-compatible local inference endpoint
- combining Tiny Agents with local MCP-accessible tools
- taking advantage of local AMD hardware acceleration where available

## Why it was not reproduced here 1:1
My public practice for Unit 2 was centered on:
- AWS EC2 server/client setup
- remote MCP connectivity
- Gradio server/client flows
- Continue CLI
- Tiny Agents over a remote MCP endpoint

That means the Lemonade page was useful conceptually, but it did not map directly to the same cloud workflow.

## Honest portfolio position
For this repository, I treat that page as:
- reviewed
- understood in context
- not claimed as a completed local-hardware implementation

## Why this still matters
It highlights an important MCP idea:
the same client/tool patterns can be reused across very different environments:

- cloud-hosted servers
- local inference servers
- desktop tool workflows
- hardware-accelerated local agents
