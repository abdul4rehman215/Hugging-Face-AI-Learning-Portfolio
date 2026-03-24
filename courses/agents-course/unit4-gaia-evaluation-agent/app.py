import os
import re
import base64
import mimetypes
import subprocess
from pathlib import Path

import gradio as gr
import requests
import pandas as pd
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi

print("BOOT: imports loaded", flush=True)

DEFAULT_API_URL = "https://agents-course-unit4-scoring.hf.space"

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
TRANSCRIBE_MODEL = os.getenv("TRANSCRIBE_MODEL", "gpt-4o-mini-transcribe")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
TEST_MODE = os.getenv("TEST_MODE", "1") == "1"   # 1 = random-question, 0 = full evaluation


def to_data_url(file_path: str) -> str:
    mime, _ = mimetypes.guess_type(file_path)
    if not mime:
        mime = "application/octet-stream"
    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def clean_final_answer(text: str) -> str:
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r"^\s*(final answer|answer)\s*[:\-]\s*", "", text, flags=re.I)
    return text.strip().strip('"').strip("'")


def extract_youtube_id(text: str) -> str | None:
    patterns = [
        r"youtube\.com/watch\?v=([A-Za-z0-9_-]{11})",
        r"youtu\.be/([A-Za-z0-9_-]{11})",
    ]
    for pattern in patterns:
        m = re.search(pattern, text)
        if m:
            return m.group(1)
    return None


def answer_rules(question: str) -> str:
    return (
        "Return ONLY the final answer.\n"
        "Do not explain.\n"
        "Do not include reasoning.\n"
        "Do not say FINAL ANSWER.\n"
        "Match the required format exactly.\n"
        "If the question asks for a comma-separated list, return only that list.\n"
        "If it asks for sorted/alphabetical output, obey exactly.\n"
        f"\nQUESTION:\n{question}"
    )


class BasicAgent:
    def __init__(self):
        if not LLM_API_KEY:
            raise ValueError("Missing LLM_API_KEY secret.")
        self.client = OpenAI(api_key=LLM_API_KEY)
        self.api_url = DEFAULT_API_URL
        print(f"BOOT: agent initialized with model={MODEL_NAME}", flush=True)

    def download_task_file(self, task_id: str, file_name: str) -> str | None:
        if not file_name:
            return None
        url = f"{self.api_url}/files/{task_id}"
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        suffix = Path(file_name).suffix
        local_path = f"/tmp/{task_id}{suffix}"
        with open(local_path, "wb") as f:
            f.write(r.content)
        return local_path

    def ask_plain(self, question: str, extra_context: str = "", image_path: str | None = None) -> str:
        content = [{"type": "input_text", "text": answer_rules(question) + "\n\n" + extra_context}]
        if image_path:
            content.append({"type": "input_image", "image_url": to_data_url(image_path)})

        response = self.client.responses.create(
            model=MODEL_NAME,
            input=[{"role": "user", "content": content}],
        )
        return clean_final_answer(response.output_text)

    def ask_web(self, question: str, extra_context: str = "") -> str:
        prompt = answer_rules(question)
        if extra_context:
            prompt += "\n\nCONTEXT:\n" + extra_context

        response = self.client.responses.create(
            model=MODEL_NAME,
            tools=[{"type": "web_search"}],
            input=prompt,
        )
        return clean_final_answer(response.output_text)

    def transcribe_audio(self, file_path: str) -> str:
        with open(file_path, "rb") as audio_file:
            transcript = self.client.audio.transcriptions.create(
                model=TRANSCRIBE_MODEL,
                file=audio_file,
            )
        return getattr(transcript, "text", "") or ""

    def get_youtube_transcript(self, question: str) -> str | None:
        video_id = extract_youtube_id(question)
        if not video_id:
            return None
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
            return " ".join(chunk["text"] for chunk in transcript)
        except Exception as e:
            print(f"YouTube transcript failed: {e}", flush=True)
            return None

    def summarize_excel(self, file_path: str) -> str:
        blocks = []
        xls = pd.ExcelFile(file_path)
        for sheet_name in xls.sheet_names[:5]:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            blocks.append(f"SHEET: {sheet_name}")
            blocks.append("COLUMNS: " + ", ".join(map(str, df.columns.tolist())))
            blocks.append("ROWS:")
            blocks.append(df.to_csv(index=False))
            blocks.append("")
        return "\n".join(blocks)[:50000]

    def execute_python_file(self, file_path: str) -> str:
        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    def read_text_file(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    def __call__(self, task: dict) -> str:
        task_id = task.get("task_id", "")
        question = task.get("question", "")
        file_name = task.get("file_name", "") or ""

        print(f"SOLVING task={task_id} file={file_name}", flush=True)

        yt_transcript = self.get_youtube_transcript(question)
        if yt_transcript:
            return self.ask_plain(
                question,
                extra_context=f"YOUTUBE TRANSCRIPT:\n{yt_transcript[:40000]}",
            )

        local_file = self.download_task_file(task_id, file_name) if file_name else None
        if local_file:
            ext = Path(local_file).suffix.lower()

            if ext in {".mp3", ".wav", ".m4a", ".mpeg", ".mp4", ".webm"}:
                transcript = self.transcribe_audio(local_file)
                return self.ask_plain(
                    question,
                    extra_context=f"AUDIO TRANSCRIPT:\n{transcript[:30000]}",
                )

            if ext in {".png", ".jpg", ".jpeg", ".webp"}:
                return self.ask_plain(question, image_path=local_file)

            if ext in {".xlsx", ".xls"}:
                sheet_dump = self.summarize_excel(local_file)
                return self.ask_plain(
                    question,
                    extra_context=f"SPREADSHEET CONTENT:\n{sheet_dump}",
                )

            if ext == ".py":
                code_text = self.read_text_file(local_file)
                exec_text = self.execute_python_file(local_file)
                return self.ask_plain(
                    question,
                    extra_context=f"PYTHON FILE:\n{code_text}\n\nEXECUTION RESULT:\n{exec_text}",
                )

            text_data = self.read_text_file(local_file)
            return self.ask_plain(question, extra_context=text_data[:40000])

        return self.ask_web(question)


def run_and_submit_all(profile: gr.OAuthProfile | None):
    space_id = os.getenv("SPACE_ID", "")

    if profile:
        username = f"{profile.username}"
        print(f"User logged in: {username}", flush=True)
    else:
        print("User not logged in.", flush=True)
        return "Please login to Hugging Face first.", None

    api_url = DEFAULT_API_URL
    questions_url = f"{api_url}/questions"
    submit_url = f"{api_url}/submit"

    try:
        agent = BasicAgent()
    except Exception as e:
        print(f"Agent init error: {e}", flush=True)
        return f"Error initializing agent: {e}", None

    agent_code = f"https://huggingface.co/spaces/{space_id}/tree/main"

    try:
        if TEST_MODE:
            print("TEST_MODE=1 -> fetching /random-question", flush=True)
            response = requests.get(f"{api_url}/random-question", timeout=30)
            response.raise_for_status()
            questions_data = [response.json()]
        else:
            print("TEST_MODE=0 -> fetching /questions", flush=True)
            response = requests.get(questions_url, timeout=30)
            response.raise_for_status()
            questions_data = response.json()

        if not questions_data:
            return "No questions returned by API.", None

        print(f"Fetched {len(questions_data)} questions.", flush=True)
    except Exception as e:
        print(f"Question fetch error: {e}", flush=True)
        return f"Error fetching questions: {e}", None

    results_log = []
    answers_payload = []

    for item in questions_data:
        task_id = item.get("task_id")
        question_text = item.get("question")
        if not task_id or question_text is None:
            continue

        try:
            submitted_answer = agent(item)
            answers_payload.append({
                "task_id": task_id,
                "submitted_answer": submitted_answer
            })
            results_log.append({
                "Task ID": task_id,
                "Question": question_text,
                "File": item.get("file_name", ""),
                "Submitted Answer": submitted_answer
            })
        except Exception as e:
            print(f"Task error {task_id}: {e}", flush=True)
            results_log.append({
                "Task ID": task_id,
                "Question": question_text,
                "File": item.get("file_name", ""),
                "Submitted Answer": f"AGENT ERROR: {e}"
            })

    if TEST_MODE:
        return "Test mode finished. Check the answer table below before running full evaluation.", pd.DataFrame(results_log)

    if not answers_payload:
        return "Agent produced no answers.", pd.DataFrame(results_log)

    submission_data = {
        "username": username.strip(),
        "agent_code": agent_code,
        "answers": answers_payload
    }

    try:
        response = requests.post(submit_url, json=submission_data, timeout=120)
        response.raise_for_status()
        result_data = response.json()

        final_status = (
            f"Submission Successful!\n"
            f"User: {result_data.get('username')}\n"
            f"Overall Score: {result_data.get('score', 'N/A')}% "
            f"({result_data.get('correct_count', '?')}/{result_data.get('total_attempted', '?')} correct)\n"
            f"Message: {result_data.get('message', 'No message received.')}"
        )
        return final_status, pd.DataFrame(results_log)

    except requests.exceptions.HTTPError as e:
        detail = f"Server responded with status {e.response.status_code}."
        try:
            detail += f" Detail: {e.response.json()}"
        except Exception:
            detail += f" Response: {e.response.text[:500]}"
        return f"Submission failed: {detail}", pd.DataFrame(results_log)

    except Exception as e:
        return f"Submission failed: {e}", pd.DataFrame(results_log)


with gr.Blocks() as demo:
    gr.Markdown("# Basic Agent Evaluation Runner")
    gr.Markdown(
        """
        1. Login with Hugging Face.
        2. In TEST_MODE=1, this runs one random question only.
        3. Change TEST_MODE=0 for full evaluation and submission.
        """
    )

    gr.LoginButton()
    run_button = gr.Button("Run Evaluation & Submit All Answers")
    status_output = gr.Textbox(label="Run Status / Submission Result", lines=6, interactive=False)
    results_table = gr.DataFrame(label="Questions and Agent Answers", wrap=True)

    run_button.click(
        fn=run_and_submit_all,
        outputs=[status_output, results_table]
    )

print("BOOT: gradio blocks created", flush=True)

if __name__ == "__main__":
    print("BOOT: launching gradio", flush=True)
    port = int(os.environ.get("PORT", "7860"))
    demo.launch(server_name="0.0.0.0", server_port=port, show_error=True)
