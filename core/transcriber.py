import os
from faster_whisper import WhisperModel

WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL", "base")

_model = None

# load model in the harddisk of theuser
def load_model():
    global _model
    
    if _model is None:
        print(f"\nLoading Whisper model ({WHISPER_MODEL_SIZE}) locally into RAM...")
        # Local system/CPU ke liye optimized loading
        _model = WhisperModel(WHISPER_MODEL_SIZE, device="cpu", compute_type="int8")
        print("\nWhisper model loaded successfully!")
        
    return _model


# transcribe a single chunk
def transcribe_chunk(chunk_path : str , translate :bool = False)->str:
    model=load_model()

    task="translate" if translate else "transcribe"

    segments,info=model.transcribe(chunk_path,task=task,beam_size=2)

    print(f"\nlanguage detected : {info.language} ({info.language_probability:.0%} confident)\n")

    full_text=" ".join(segment.text for segment in segments)

    return full_text

# transcribe all chunks
def transcribe_all(chunks:list,translate : bool = False , status_callback=None) ->str:
    final_transcribe=""

    for i,chunk in enumerate(chunks):
        if status_callback:
            status_callback(f"🎙️ Transcribing chunk {i+1}/{len(chunks)}")

        print(f"\nTranscribing chunk {i+1}/{len(chunks)}")
        text=transcribe_chunk(chunk,translate=translate)
        final_transcribe+=text + "  "

    print("\nTranscription completed\n")

    return final_transcribe