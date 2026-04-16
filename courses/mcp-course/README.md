# 🔌 Hugging Face MCP Course

<p align="center">
  <img src="https://img.shields.io/badge/Course-Hugging%20Face%20MCP%20Course-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" />
  <img src="https://img.shields.io/badge/Status-In%20Progress-FF9800?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Unit%201-Fundamentals%20Completed-00C853?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Portfolio-Documentation%20First-7B61FF?style=for-the-badge" />
</p>

---

# 🎯 Overview

This folder documents my progress in the **Hugging Face MCP Course**.

At this stage, I have completed **Unit 1 — Fundamentals of MCP**, which gave me a strong foundation in:

- what MCP is and why it matters
- the M×N integration problem and standardization benefits
- host, client, and server architecture
- JSON-RPC based communication in MCP
- MCP capabilities such as tools, resources, prompts, and sampling
- official MCP SDK concepts
- MCP client configuration and setup
- Hugging Face MCP Server usage
- Gradio MCP integration for exposing tools through MCP

This course section is being documented in a way that fits my broader **Hugging Face AI Learning Portfolio**.

---

# 📚 Progress

| Section | Topic | Status |
|--------|-------|--------|
| Unit 1 | Fundamentals of MCP | ✅ Completed |
| Unit 2 | End-to-End MCP Application | ⏳ Planned / In Progress |
| Unit 3 | Advanced MCP Development | ⏳ Planned |
| Use Case | Build a Pull Request Agent on the Hub | ⏳ Planned |

---

# 🧠 What I Covered In Unit 1

## 1. Introduction to MCP
- what Model Context Protocol is
- why MCP is important in the AI ecosystem
- how MCP helps standardize interactions between AI applications and external systems

## 2. MCP Terminology and Core Concepts
- the M×N integration problem
- interoperability through a shared protocol
- common MCP vocabulary and primitives

## 3. Architectural Components
- host
- client
- server
- 1:1 client-to-server relationship model

## 4. Communication Protocol
- JSON-RPC 2.0 foundations
- requests, responses, and notifications
- transport methods such as `stdio` and `HTTP + SSE / Streamable HTTP`

## 5. MCP Capabilities
- tools
- resources
- prompts
- sampling

## 6. MCP SDK and Development Flow
- official SDK role in building MCP applications
- server implementation concepts
- capability registration and discovery

## 7. MCP Clients
- MCP client responsibilities
- `mcp.json` structure and configuration basics
- connecting clients such as VS Code, Cursor, Zed, and Claude Desktop

## 8. Hugging Face MCP Server
- connecting an MCP-compatible assistant to the Hugging Face Hub
- exploring models, datasets, Spaces, and papers from MCP-compatible tools

## 9. Gradio MCP Integration
- exposing Gradio apps as MCP servers
- launching with `mcp_server=True`
- bridging human-friendly UIs and AI-accessible tools

---

# 📂 Included In This Folder

- `unit1-fundamentals-of-mcp/` — documentation, notes, resources, and certificate for Unit 1

---

# 🧩 Folder Structure

```text
mcp-course/
├── README.md
└── unit1-fundamentals-of-mcp/
    ├── README.md
    ├── unit1-notes.md
    ├── official-resources.md
    └── certificate.jpg
```

---

# 🏅 Certificate

The Unit 1 certificate is included inside:

[`unit1-fundamentals-of-mcp/`](./unit1-fundamentals-of-mcp/)

---

# 🧠 Skills Demonstrated So Far

- Model Context Protocol (MCP)
- AI Engineering
- Tool Calling
- API Integration
- Client-Server Architecture
- JSON-RPC
- Hugging Face
- Gradio
- Python
- MCP Client Configuration

---

# 🚧 Status

**Unit 1 completed.**

The full MCP Course is still in progress, and this folder is designed to grow as I complete more units and add hands-on implementations.
