# 🔌 Hugging Face MCP Course

<div align="center">

<p>
  <img src="https://img.shields.io/badge/Course-Hugging%20Face%20MCP%20Course-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" />
  <img src="https://img.shields.io/badge/Status-Ongoing-FF9800?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Unit%201-Fundamentals%20Completed-00C853?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Unit%202-Hands--On%20Documented-7B61FF?style=for-the-badge" />
</p>

<p>
  <img src="https://img.shields.io/badge/MCP-Architecture%20%26%20Protocol-1565C0?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Gradio-MCP%20Server%20%26%20Client-FF4B4B?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Continue-CLI%20Integration-8E24AA?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Tiny%20Agents-End--to--End%20Tool%20Use-2E7D32?style=for-the-badge" />
</p>

</div>

---

# 🎯 Overview

This folder documents my progress in the **Hugging Face MCP Course** inside my broader Hugging Face AI learning portfolio.

At this stage, the folder covers:

- ✅ **Unit 1 — Fundamentals of MCP**
- ✅ **Unit 2 hands-on practice** for building an end-to-end MCP application
- ✅ **working implementation notes** from an EC2-based practice setup
- ✅ **code/config files** for the MCP server and multiple client styles
- ✅ **renamed screenshots** that show the practical workflow and results

The course itself is still ongoing for me, so this folder is written honestly as **completed fundamentals + documented hands-on practice**, not as a full-course completion claim.

---

# 🧭 Quick Navigation

- [`unit1-fundamentals-of-mcp/`](./unit1-fundamentals-of-mcp/) — Unit 1 notes, resources, and certificate
- [`unit2-end-to-end-mcp-application/`](./unit2-end-to-end-mcp-application/) — Unit 2 practical build, code, configs, screenshots, and notes

---

# 📚 Current Progress Snapshot

| Section | Focus | Status |
|---|---|---|
| Unit 1 | MCP fundamentals, architecture, protocol, SDK, clients, Hugging Face MCP Server, Gradio MCP integration | ✅ Completed |
| Unit 2 | End-to-end MCP application with Gradio server and multiple clients | ✅ Practical sections documented |
| Unit 3+ | Advanced MCP development and later sections | ⏳ Not yet documented here |

---

# 🧠 What This Folder Covers

## 1) Unit 1 — Fundamentals of MCP
This section captures the theory and foundation:
- what MCP is and why it matters
- the M×N integration problem
- host / client / server roles
- JSON-RPC communication and transports
- capabilities such as tools, resources, prompts, and sampling
- official SDK concepts
- MCP clients
- Hugging Face MCP Server
- Gradio MCP integration

## 2) Unit 2 — End-to-End MCP Application
This section captures the practical build path:
- building a Gradio MCP server for sentiment analysis
- verifying the schema and MCP endpoints
- configuring MCP clients
- using Continue as a coding-assistant style MCP client
- building a Gradio UI as an MCP client
- connecting Tiny Agents to the MCP server
- documenting the AMD/Lemonade section honestly as a hardware-specific/local workflow, not an EC2 build

---

# 🧪 Practical Setup Documented Here

The Unit 2 work in this folder is based on a **two-instance AWS EC2 practice setup**:

- **MCP server instance**
  - hosted the Gradio sentiment analysis MCP server
- **MCP client instance**
  - tested remote MCP connectivity
  - ran Continue CLI
  - ran a Gradio MCP client
  - ran Tiny Agents through `mcp-remote`

Public or internal IP values used during practice have **not** been hardcoded into the public code/config files in this folder.  
Templates are written with **placeholders or environment variables** so the repo stays clean and reusable.

---

# 🗂️ Folder Structure

```text
mcp-course/
├── README.md
├── unit1-fundamentals-of-mcp/
│   ├── README.md
│   ├── unit1-notes.md
│   ├── official-resources.md
│   └── unit1-fundamentals-of-mcp-certificate.jpg
└── unit2-end-to-end-mcp-application/
    ├── README.md
    ├── unit2-notes.md
    ├── official-resources.md
    ├── implementations/
    │   ├── client-configs/
    │   │   ├── README.md
    │   │   ├── config.json
    │   │   ├── mcp.json
    │   │   └── server.env.example
    │   ├── continue-cli-client/
    │   │   ├── README.md
    │   │   └── config.yaml
    │   ├── gradio-mcp-client/
    │   │   ├── README.md
    │   │   ├── app.py
    │   │   └── requirements.txt
    │   ├── gradio-mcp-server/
    │   │   ├── README.md
    │   │   ├── app.py
    │   │   └── requirements.txt
    │   └── tiny-agents-client/
    │       ├── README.md
    │       ├── agent.json
    │       └── package-notes.md
    └── screenshots/
        ├── 01-gradio-server-ui.png
        ├── 02-mcp-schema-output.png
        ├── 03-continue-cli-connected.png
        ├── 04-gradio-mcp-client-ui.png
        ├── 05-smolagents-tool-call-log.png
        ├── 06-tiny-agents-tool-call.png
        └── README.md
```

---

# 🧩 Skills Demonstrated In This Folder

<div align="left">

![MCP](https://img.shields.io/badge/Model%20Context%20Protocol-MCP-7B61FF?style=flat-square)
![Architecture](https://img.shields.io/badge/Architecture-Host%20%2F%20Client%20%2F%20Server-1565C0?style=flat-square)
![JSON-RPC](https://img.shields.io/badge/Protocol-JSON--RPC-00897B?style=flat-square)
![Tool Calling](https://img.shields.io/badge/Tool%20Calling-Workflow%20Integration-8E24AA?style=flat-square)
![Gradio](https://img.shields.io/badge/Gradio-MCP%20Server%20%26%20Client-FF4B4B?style=flat-square)
![Continue](https://img.shields.io/badge/Continue-CLI%20Client-6A1B9A?style=flat-square)
![Tiny Agents](https://img.shields.io/badge/Tiny%20Agents-MCP%20Tool%20Use-2E7D32?style=flat-square)
![Python](https://img.shields.io/badge/Python-Implementation-3776AB?style=flat-square&logo=python&logoColor=white)
![API Integration](https://img.shields.io/badge/API%20Integration-Remote%20MCP%20Connections-455A64?style=flat-square)
![AWS EC2](https://img.shields.io/badge/AWS-EC2%20Practice%20Environment-FF9900?style=flat-square&logo=amazonaws&logoColor=white)

</div>

---

# 🏅 Included Evidence

This folder includes both **documentation** and **practical artifacts**:

- course-aligned README sections
- structured notes
- official resource lists
- working code/config templates
- screenshots from the hands-on flow
- Unit 1 certificate image

---

# 🚧 Status Note

This folder is intentionally written in a **portfolio-safe way**:

- Unit 1 is presented as **completed**
- Unit 2 is presented as **practiced and documented**
- later units are **not claimed as completed**
- hardware/local-only sections are **not overclaimed** when they were only reviewed conceptually

---

# 🔜 Next Expansion Points

When I continue the course later, this folder can be extended with:

- advanced MCP workflow servers
- more robust MCP applications
- additional certificates or recap material
- improved implementation variants beyond the current EC2-based practice set
