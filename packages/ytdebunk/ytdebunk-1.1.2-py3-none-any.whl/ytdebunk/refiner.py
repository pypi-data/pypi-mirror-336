import google.generativeai as genai
import ytdebunk.settings as settings
import os

from dotenv import load_dotenv
load_dotenv()

def chunk_text(text, max_chars=3000):
    sentences = text.split("।")
    chunks, current_chunk = [], ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_chars:
            current_chunk += sentence + "।"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + "।"

    if current_chunk:  
        chunks.append(current_chunk.strip())

    return chunks


def enhance_transcription(transcription, 
                          key=os.getenv("GENAI_API_KEY"), 
                          verbose=False, 
                          language=settings.LANUAGE_DEFAULT):

    enchacement_prompt = f"""
You are a {settings.TRANSCRIPTION_MODEL_NAMES[language]} language expert. You have been asked to improve the following {settings.TRANSCRIPTION_MODEL_NAMES[language]} transcription by correcting errors and enhancing readability.

IMPORTANT:
1. Return only the transcription without any additional information or instructions.
2. Do not change the meaning of the transcription.
3. Do not add any new information to the transcription.
4. Do not remove any information from the transcription.

Here is the transcription:

"""

    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    chunks = chunk_text(transcription)
    refined_chunks = []

    print(f"[ytdebunk-refiner] Refining {len(chunks)} chunks of text...")
    for chunk in chunks:
        if verbose:
            print("[ytdebunk-refiner] Refining chunk no. ", chunks.index(chunk) + 1)
        prompt = enchacement_prompt + chunk
        response = model.generate_content(prompt)
        refined_chunks.append(response.text.strip())
    return " ".join(refined_chunks)