# ✅ Healify AI (Improved Output Box Version)
import os, json, hashlib, random, traceback
from pathlib import Path
import gradio as gr
from langchain.prompts import PromptTemplate
from langchain_nvidia_ai_endpoints import ChatNVIDIA

# must set your NVIDIA key
os.environ["NVIDIA_API_KEY"] = "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"

llm = ChatNVIDIA(model="meta/llama-3.1-70b-instruct")

def extract_text(out):
    if isinstance(out, str):
        return out
    for attr in ("content", "text", "response", "result"):
        if hasattr(out, attr):
            v = getattr(out, attr)
            if isinstance(v, str) and v.strip():
                return v.strip()
            if hasattr(v, "content"):
                return getattr(v, "content")
    return str(out)

def detect_emotion(user_input):
    prompt = f'Identify one emotion word for: "{user_input}"\nEmotion:'
    out = llm.invoke(prompt)
    return extract_text(out).split()[0].lower()

def generate_story_simple(user_input):
    emotion = detect_emotion(user_input)
    prompt = f"Write a 10-line inspiring story about someone who felt {emotion} and overcame it."
    out = llm.invoke(prompt)
    story = extract_text(out)
    return f"🧠 Detected Emotion: {emotion}\n\n📖 Story:\n{story}"

def handler(user_text):
    try:
        return generate_story_simple(user_text)
    except Exception as e:
        return f"❌ Error generating story: {e}\n\nTraceback:\n" + traceback.format_exc()

# ✅ Interface with larger output box
iface = gr.Interface(
    fn=handler,
    inputs=gr.Textbox(lines=3, label="💬 Share your feelings or problem"),
    outputs=gr.Textbox(lines=20, label="✨ Healify's Inspiring Story"),  # Bigger output box
    title="🌈 Healify AI - Stories That Heal",
    description="Tell me how you feel, and I’ll share a story that helps you move forward 💪",
)

iface.launch()
