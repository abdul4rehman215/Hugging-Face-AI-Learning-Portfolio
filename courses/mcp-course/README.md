# 🔌 Hugging Face MCP Course

<div align="center">

<p>
  <img src="https://img.shields.io/badge/Course-Hugging%20Face%20MCP%20Course-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" />
  <img src="https://img.shields.io/badge/Status-Ongoing-FF9800?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Unit%201-Fundamentals%20Completed-00C853?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Unit%202-End--to--End%20Practice%20Documented-7B61FF?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Unit%203-Production%20Automation%20Completed-1565C0?style=for-the-badge" />
</p>

<p>
  <img src="https://img.shields.io/badge/MCP-Architecture%20%26%20Protocol-6A1B9A?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Claude%20Code-Custom%20Workflow%20Server-D84315?style=for-the-badge" />
  <img src="https://img.shields.io/badge/GitHub%20Actions-Webhooks%20%26%20Prompts-2E7D32?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Slack-Team%20Notifications-4A154B?style=for-the-badge" />
</p>

</div>

---

# 🎯 Overview

This folder documents my progress through the **Hugging Face MCP Course** inside my broader Hugging Face AI learning portfolio.

At this stage, it includes:

- ✅ **Unit 1 — Fundamentals of MCP**
- ✅ **Unit 2 — end-to-end MCP application practice** documented from an EC2-based setup
- ✅ **Unit 3 — MCP for Production Automation** completed with working Claude Code, GitHub Actions, Cloudflare Tunnel, and Slack workflow automation
- ✅ **code, configs, notes, and screenshots** arranged in a publishable portfolio structure

The overall course is still ongoing, so this folder is intentionally written as **completed units + documented practical work**, not as a full-course completion claim.

---

# 🧭 Quick Navigation

- [`unit1-fundamentals-of-mcp/`](./unit1-fundamentals-of-mcp/) — Unit 1 notes, resources, and certificate
- [`unit2-end-to-end-mcp-application/`](./unit2-end-to-end-mcp-application/) — Unit 2 practical build, code, configs, screenshots, and notes
- [`unit3-mcp-for-production-automation/`](./unit3-mcp-for-production-automation/) — Unit 3 automation workflow server, implementation files, screenshots, and certificate

---

# 📚 Current Progress Snapshot

| Section | Focus | Status |
|---|---|---|
| Unit 1 | MCP fundamentals, architecture, protocol, SDK, clients, Hugging Face MCP Server, Gradio MCP integration | ✅ Completed |
| Unit 2 | End-to-end MCP application with Gradio server and multiple client styles | ✅ Practiced and documented |
| Unit 3 | Claude Code workflow server, PR automation, GitHub Actions monitoring, Slack notifications | ✅ Completed |
| Later units | Additional MCP development sections | ⏳ Not yet documented here |

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
- verifying schema and MCP endpoints
- configuring MCP clients
- using Continue as a coding-assistant style MCP client
- building a Gradio UI as an MCP client
- connecting Tiny Agents to the MCP server

## 3) Unit 3 — MCP for Production Automation
This section captures the full workflow-automation path:
- building a FastMCP-based PR Agent for Claude Code
- analyzing changed files and suggesting PR templates
- collecting GitHub Actions webhook events through a local webhook server + Cloudflare Tunnel
- exposing MCP prompts for CI/CD summaries and troubleshooting flows
- formatting and sending Slack notifications through an MCP tool
- documenting the end-to-end workflow with screenshots and reusable implementation files

---

# 🗂️ Folder Structure

```text
mcp-course/
├── README.md
├── unit1-fundamentals-of-mcp/
│   ├── README.md
│   ├── unit1-notes.md
│   ├── official-resources.md
│   └── certificate.jpg
├── unit2-end-to-end-mcp-application/
│   ├── README.md
│   ├── unit2-notes.md
│   ├── official-resources.md
│   ├── ec2-practice-setup.md
│   ├── lemonade-server-notes.md
│   ├── implementations/
│   └── screenshots/
└── unit3-mcp-for-production-automation/
    ├── README.md
    ├── unit3-notes.md
    ├── official-resources.md
    ├── ec2-practice-setup.md
    ├── unit3-mcp-for-production-automation-certificate.jpg
    ├── templates/
    ├── implementations/
    │   ├── module1-build-mcp-server/
    │   ├── module2-github-actions-integration/
    │   └── module3-slack-notification/
    └── screenshots/
```

---

# 🧩 Skills Demonstrated In This Folder

<div align="left">

![MCP](https://img.shields.io/badge/Model%20Context%20Protocol-MCP-7B61FF?style=flat-square)
![Architecture](https://img.shields.io/badge/Architecture-Host%20%2F%20Client%20%2F%20Server-1565C0?style=flat-square)
![JSON-RPC](https://img.shields.io/badge/Protocol-JSON--RPC-00897B?style=flat-square)
![Tool Calling](https://img.shields.io/badge/Tool%20Calling-Workflow%20Integration-8E24AA?style=flat-square)
![Gradio](https://img.shields.io/badge/Gradio-MCP%20Server%20%26%20Client-FF4B4B?style=flat-square)
![Claude Code](https://img.shields.io/badge/Claude%20Code-Custom%20Workflow%20Server-D84315?style=flat-square)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Webhooks%20%26%20Prompts-2E7D32?style=flat-square)
![Slack](https://img.shields.io/badge/Slack-Team%20Notifications-4A154B?style=flat-square)
![Python](https://img.shields.io/badge/Python-Implementation-3776AB?style=flat-square&logo=python&logoColor=white)
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
- certificate images where applicable

---

# 🚧 Status Note

This folder is intentionally written in a **portfolio-safe way**:

- Unit 1 is presented as **completed**
- Unit 2 is presented as **practiced and documented**
- Unit 3 is presented as **completed and demonstrated end-to-end**
