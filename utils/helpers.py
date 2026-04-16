import os
import math
import subprocess
import tempfile
from pathlib import Path

CHUNK_MB = 24  # OpenAI Whisper API limit is 25MB


# ── Audio splitting ────────────────────────────────────────────────────────────

def get_duration(path: str) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True
    )
    try:
        return float(result.stdout.strip())
    except Exception:
        return 0.0


def split_audio_ffmpeg(path: str) -> list:
    """Split audio file into <25MB chunks using ffmpeg."""
    file_size_mb = os.path.getsize(path) / (1024 * 1024)
    if file_size_mb <= CHUNK_MB:
        return [path]

    duration = get_duration(path)
    n_chunks = math.ceil(file_size_mb / CHUNK_MB)
    chunk_duration = math.ceil(duration / n_chunks)
    tmp_dir = tempfile.mkdtemp()
    chunks = []

    for i in range(n_chunks):
        start = i * chunk_duration
        chunk_path = os.path.join(tmp_dir, f"chunk_{i+1}.mp3")
        subprocess.run(
            ["ffmpeg", "-y", "-i", path,
             "-ss", str(start), "-t", str(chunk_duration),
             "-acodec", "libmp3lame", "-q:a", "4", chunk_path],
            capture_output=True
        )
        if os.path.exists(chunk_path) and os.path.getsize(chunk_path) > 0:
            chunks.append(chunk_path)
    return chunks


def extract_audio_from_video(video_path: str) -> str:
    """Extract audio from MP4/video file using ffmpeg."""
    tmp_dir = tempfile.mkdtemp()
    audio_path = os.path.join(tmp_dir, "extracted_audio.mp3")
    subprocess.run(
        ["ffmpeg", "-y", "-i", video_path,
         "-vn", "-acodec", "libmp3lame", "-q:a", "4", audio_path],
        capture_output=True
    )
    return audio_path


def download_youtube_audio(url: str) -> str:
    """Download audio from YouTube URL using yt-dlp."""
    tmp_dir = tempfile.mkdtemp()
    output_template = os.path.join(tmp_dir, "yt_audio.%(ext)s")
    subprocess.run(
        ["yt-dlp", "-x", "--audio-format", "mp3",
         "--audio-quality", "4",
         "-o", output_template, url],
        capture_output=True
    )
    # Find the downloaded file
    for f in os.listdir(tmp_dir):
        if f.startswith("yt_audio"):
            return os.path.join(tmp_dir, f)
    raise FileNotFoundError("YouTube audio download failed. Check the URL and try again.")


def prepare_audio_chunks(uploaded_files: list) -> list:
    """Save uploaded audio files and split if needed."""
    all_chunks = []
    tmp_dir = tempfile.mkdtemp()
    for i, uploaded_file in enumerate(uploaded_files):
        suffix = Path(uploaded_file.name).suffix
        tmp_path = os.path.join(tmp_dir, f"file_{i+1}{suffix}")
        with open(tmp_path, "wb") as f:
            f.write(uploaded_file.read())
        all_chunks.extend(split_audio_ffmpeg(tmp_path))
    return all_chunks


# ── Transcription ──────────────────────────────────────────────────────────────

def transcribe_chunks(chunks: list, openai_key: str, progress_bar=None, status_text=None) -> str:
    """Transcribe audio chunks via OpenAI Whisper API."""
    from openai import OpenAI
    client = OpenAI(api_key=openai_key)
    full_transcript = []

    for i, chunk_path in enumerate(chunks):
        if status_text:
            status_text.markdown(f"**Transcribing** part {i+1} of {len(chunks)}…")
        if progress_bar:
            progress_bar.progress(0.05 + (i + 1) / len(chunks) * 0.60)

        with open(chunk_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        full_transcript.append(response.strip())

        try:
            if "chunk_" in chunk_path or "yt_audio" in chunk_path or "extracted" in chunk_path:
                os.unlink(chunk_path)
        except Exception:
            pass

    return "\n\n".join(full_transcript)


# ── Summarization ──────────────────────────────────────────────────────────────

STYLE_PROMPTS = {
    "Bullet highlights": (
        "Summarize the following discourse as clear bullet points grouped under bold thematic headers. "
        "Each bullet should be concise and capture a key idea."
    ),
    "Main takeaways": (
        "List only the top 8–10 main takeaways from this discourse, numbered, each in one or two sentences."
    ),
    "Detailed paragraphs": (
        "Write a detailed, well-structured summary in prose paragraphs covering all major themes, "
        "arguments, and conclusions."
    ),
    "Executive brief": (
        "Write a crisp executive brief (max 300 words). Lead with the key message, "
        "then main points and any action items."
    ),
    "Academic digest": (
        "Produce an academic-style digest with sections: Overview, Key Arguments, "
        "Evidence/Examples, Conclusions, and Notable Quotes."
    ),
    "Structured table": (
        "You will produce a structured table summary. Instructions are handled separately."
    ),
}

TABLE_COLUMNS = {
    "Main Point (verbatim)": "Extract the key point exactly as spoken or as close as possible.",
    "Explanation": "Explain what this point means in your own words.",
    "Example from discourse": "If an example was given, include it here. Otherwise write 'N/A'.",
    "Personal Reflection": "Leave this column empty for the reader to fill in.",
}


def summarize_text(transcript: str, style: str, columns: list, anthropic_key: str) -> str:
    """Summarize transcript using Claude. Returns text or markdown table."""
    import anthropic
    client = anthropic.Anthropic(api_key=anthropic_key)

    max_chars = 150_000

    def call_claude(prompt: str, text: str, max_tokens: int = 2000) -> str:
        if len(text) > max_chars:
            parts = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
            partials = []
            for part in parts:
                msg = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1500,
                    messages=[{"role": "user", "content": f"Summarize this section:\n\n{part}"}],
                )
                partials.append(msg.content[0].text)
            combined = "\n\n".join(partials)
            final = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": f"{prompt}\n\n{combined}"}],
            )
            return final.content[0].text
        else:
            msg = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": f"{prompt}\n\n{text}"}],
            )
            return msg.content[0].text

    if style == "Structured table":
        col_desc = "\n".join([f"- **{c}**: {TABLE_COLUMNS[c]}" for c in columns if c in TABLE_COLUMNS])
        prompt = (
            f"Create a markdown table from this discourse with these columns:\n{col_desc}\n\n"
            f"Extract 10–15 key points. Format as a proper markdown table with | separators. "
            f"Leave the 'Personal Reflection' column empty if included."
        )
        return call_claude(prompt, transcript, max_tokens=3000)
    else:
        prompt = STYLE_PROMPTS.get(style, STYLE_PROMPTS["Bullet highlights"])
        return call_claude(prompt, transcript)


# ── Export helpers ─────────────────────────────────────────────────────────────

def make_pdf(title: str, content: str) -> bytes:
    """Generate a PDF from text content using reportlab."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    import io

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=2.5*cm, rightMargin=2.5*cm,
                            topMargin=2.5*cm, bottomMargin=2.5*cm)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle('Title', parent=styles['Title'],
                                  fontSize=18, textColor=colors.HexColor('#c9a96e'),
                                  spaceAfter=12, alignment=TA_CENTER)
    body_style = ParagraphStyle('Body', parent=styles['Normal'],
                                 fontSize=11, leading=16, spaceAfter=8,
                                 textColor=colors.HexColor('#222222'))

    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.4*cm))

    for line in content.split('\n'):
        if line.strip():
            safe_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            story.append(Paragraph(safe_line, body_style))
        else:
            story.append(Spacer(1, 0.2*cm))

    doc.build(story)
    return buffer.getvalue()


def make_docx(title: str, content: str) -> bytes:
    """Generate a DOCX from text content using python-docx."""
    from docx import Document
    from docx.shared import Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    import io

    doc = Document()

    # Title
    title_para = doc.add_heading(title, level=0)
    title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in title_para.runs:
        run.font.color.rgb = RGBColor(0xC9, 0xA9, 0x6E)
        run.font.size = Pt(20)

    doc.add_paragraph()

    for line in content.split('\n'):
        if line.startswith('## '):
            doc.add_heading(line[3:], level=2)
        elif line.startswith('# '):
            doc.add_heading(line[2:], level=1)
        elif line.startswith('- ') or line.startswith('• '):
            p = doc.add_paragraph(style='List Bullet')
            p.add_run(line[2:])
        elif line.strip():
            doc.add_paragraph(line)

    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer.getvalue()
