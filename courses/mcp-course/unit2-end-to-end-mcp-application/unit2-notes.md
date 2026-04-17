# 📝 Unit 2 Notes — End-to-End MCP Application

This file captures the practical lessons, design decisions, and implementation notes from my Unit 2 MCP Course work.

---

# 1. Core Shift From Unit 1 To Unit 2

Unit 1 explained the ideas behind MCP.  
Unit 2 turned those ideas into a real workflow.

The important shift was:

- from understanding **what MCP is**
- to building **something that actually exposes and consumes MCP tools**

That made the protocol much clearer in practice.

---

# 2. Why The Gradio Server Was Useful

Using Gradio for the first MCP server made the entry point simple because one app could provide:

- a normal web interface for humans
- a schema endpoint for discovery
- an MCP endpoint for client use

This was valuable because it showed that the same logic can support both UI use and machine use.

The server implementation I documented here uses:
- `TextBlob` for sentiment analysis
- structured JSON output
- `mcp_server=True` to expose the function through MCP

---

# 3. Remote EC2 Practice Was Helpful

Instead of running everything in one local session, I split the practice into:

- server EC2
- client EC2

That taught me a few important operational ideas:

## A. MCP is not just a local dev toy
Once the server was on one machine and the client on another, the connection model felt much more realistic.

## B. Private network communication matters
For machine-to-machine testing inside AWS, private IPs made more sense than public URLs.

## C. Configuration matters as much as code
The server could be perfectly fine, but the client still needed the correct transport, endpoint, and config structure.

---

# 4. MCP Endpoints Became More Concrete

After building and testing the Gradio server, the important pieces became easy to distinguish:

## Web UI
Human-facing page.

## Schema
Machine-readable description of the tool and its input.

## MCP Endpoint
The actual endpoint a client uses to connect and invoke tools.

That difference was confusing at first, but once the server was running and the outputs were visible, the mental model became much clearer.

---

# 5. Continue Lesson — What It Taught Practically

The course page was written around Continue in an IDE workflow.

My adaptation used:
- Ollama
- Continue CLI
- MCP config via YAML
- remote SSE connection to the MCP server

Important lesson:
the *idea* of the page matters more than the exact UI.

The real point was:
- register an MCP server with a client
- let the model see the tool
- allow the client to execute it
- receive the result back into the interaction

That handshake mattered more than whether the interface was VS Code or terminal.

---

# 6. Gradio As A Client Was A Good Contrast

After using Gradio as a server, using it again as a client was useful because it highlighted both sides of MCP:

- Gradio can expose tools
- Gradio can also consume tools through an agent/client workflow

This was a strong example of how flexible MCP-based application design can become.

The Gradio client I documented here:
- connects to the remote server
- fetches tools through `MCPClient`
- uses `CodeAgent`
- wraps the interaction inside `gr.ChatInterface`

---

# 7. Tiny Agents Made The Tool Flow Very Visible

The Tiny Agents section was one of the clearest demonstrations of end-to-end MCP behavior.

Why it mattered:
- the terminal output made tool listing obvious
- the agent clearly loaded `sentiment_analysis`
- the tool call and result were visible
- it felt like a clean proof that the server was not merely “up” but truly usable

The `mcp-remote` bridge was also an important concept because it helped connect remote MCP services into a local stdio-style workflow.

---

# 8. Local AMD / Lemonade Section — Honest Interpretation

This page was useful conceptually, but it did not match my public practice architecture.

The lesson there is really about:
- local open-source models
- OpenAI-compatible local inference endpoints
- local file/tool workflows
- AMD hardware acceleration

Because my practice for this unit was centered on cloud EC2 instances, I documented this section as:
- **reviewed**
- **understood in context**
- **not reproduced as a public implementation claim**

That is the honest way to keep the portfolio accurate.

---

# 9. Common Friction Points During Practice

These were the real setup issues I ran into while working through the unit:

## A. Remote access confusion
Understanding when to use:
- localhost
- public IP
- private IP
- schema endpoint
- SSE endpoint

## B. Dependency issues
Some client-side workflows failed until missing packages were installed.

## C. Storage issues
Local model tooling can fail if the instance does not have enough disk space.

## D. Version mismatch issues
Some code patterns from the course pages needed small changes because installed package versions were slightly different.

These are worth documenting because they reflect real implementation work, not just copying course text.

---

# 10. What I Actually Demonstrated By The End

By the end of the documented Unit 2 work, I had demonstrated:

- MCP server creation
- MCP schema verification
- client configuration
- remote connectivity validation
- MCP use inside a coding assistant workflow
- Gradio as an MCP client
- Tiny Agents using the MCP tool end-to-end

That makes this unit the first strongly implementation-heavy MCP section in my portfolio.

---

# 11. Portfolio-Safe Documentation Choices

For public GitHub use, I intentionally changed a few things:

- private infrastructure values are not hardcoded
- configs use placeholders
- screenshots were selected so they show the workflow without publishing private details
- files are organized by implementation type instead of raw terminal history

This keeps the folder useful to readers while staying clean and safe to publish.

---

# 12. Best Summary Of This Unit

Unit 2 helped me move from MCP theory into practice by building a Gradio MCP server, connecting multiple MCP clients to it, validating remote tool access, and documenting the entire workflow in a reusable portfolio structure.
