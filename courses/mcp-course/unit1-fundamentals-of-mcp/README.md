# 📘 Unit 1: Fundamentals of MCP

<p align="center">
  <img src="https://img.shields.io/badge/Unit-1-7B61FF?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Topic-Fundamentals%20of%20MCP-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" />
  <img src="https://img.shields.io/badge/Status-Completed-00C853?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Certificate-Achievement-FF7043?style=for-the-badge" />
</p>

---

# 🎯 Overview

This unit introduced the **foundational concepts of the Model Context Protocol (MCP)** and how it enables AI systems to connect with external tools, resources, and services through a standardized interface.

It focused on both the **theory** and the **practical developer view** of MCP, including architecture, message flow, capability types, SDK usage, client configuration, and Hugging Face specific MCP integrations.

---

# 🧠 Key Concepts Learned

## 🔹 1. What is MCP?
- MCP stands for **Model Context Protocol**
- it is a standardized protocol for connecting AI models with tools, data sources, and environments
- it improves interoperability across different AI applications and external systems

## 🔹 2. The Integration Problem
- without standardization, AI developers face the **M×N integration problem**
- each AI application would need separate custom integrations for each tool or data source
- MCP reduces this complexity by defining a consistent interface

## 🔹 3. Core MCP Terminology
- **Host** — the user-facing AI application
- **Client** — the component that manages communication with a specific MCP server
- **Server** — the external program or service exposing capabilities through MCP
- **Capabilities** — what the server offers to the client

## 🔹 4. MCP Architecture
- MCP uses a **client-server architecture**
- clients typically maintain **1:1 relationships** with servers
- the architecture is modular and designed for extensibility

## 🔹 5. Communication Protocol
- MCP uses **JSON-RPC 2.0** as its message format
- it supports:
  - requests
  - responses
  - notifications
- common transport patterns include:
  - `stdio` for local integrations
  - `HTTP + SSE / Streamable HTTP` for remote integrations

## 🔹 6. MCP Capabilities
- **Tools** — executable functions that can perform actions
- **Resources** — read-only context/data sources
- **Prompts** — reusable templates or interaction patterns
- **Sampling** — controlled model generation support inside workflows

## 🔹 7. MCP SDK Concepts
- official SDKs simplify implementation of MCP clients and servers
- SDKs handle protocol communication, serialization, discovery, and connection management
- FastMCP-style server building provides a cleaner developer experience

## 🔹 8. MCP Clients
- learned the role of MCP clients in real workflows
- explored configuration patterns such as `mcp.json`
- looked at client environments including:
  - VS Code
  - Cursor
  - Zed
  - Claude Desktop

## 🔹 9. Hugging Face MCP Server
- learned how the Hugging Face MCP Server connects MCP-compatible assistants to the Hugging Face Hub
- explored use cases such as searching:
  - models
  - datasets
  - Spaces
  - papers
- understood how built-in tools and community tools can be surfaced through MCP

## 🔹 10. Gradio MCP Integration
- learned how Gradio apps can act as MCP servers
- explored launching Gradio with MCP enabled
- understood how standard functions can be automatically converted into MCP tools

---

# 🛠️ Practical Exposure In This Unit

Through this unit, I built understanding of how MCP is used in modern AI tooling and developer workflows, including:

- reading MCP architecture and message lifecycle concepts
- understanding how clients discover and call tools
- learning the role of transport protocols in MCP communication
- seeing how SDKs simplify server implementation
- understanding how Hugging Face and Gradio make MCP more accessible in practice

---

# 📂 Files In This Folder

- `README.md` — unit overview and learning summary
- `unit1-notes.md` — detailed structured notes from Unit 1
- `official-resources.md` — organized list of the official pages covered in this unit
- `unit1-fundamentals-of-mcp-certificate.jpg` — earned certificate for Unit 1

---

# 🎯 Key Takeaways

- I now understand the purpose and architecture of MCP
- I can explain the difference between host, client, and server in MCP systems
- I understand how JSON-RPC and transport layers support MCP communication
- I understand the main capability types exposed by MCP servers
- I have practical familiarity with MCP SDKs, client setup, the Hugging Face MCP Server, and Gradio-based MCP exposure

---

# 🏆 Certificate

![Fundamentals of MCP Certificate](./unit1-fundamentals-of-mcp-unit1-fundamentals-of-mcp-certificate.jpg)

---

# 📊 Status

✅ Completed  
🚧 Continuing the full MCP Course

---

# 🔜 Next Steps

- move from MCP fundamentals into hands-on MCP application work
- document future MCP units in the same portfolio structure
- add deeper implementation examples as I progress in the course
