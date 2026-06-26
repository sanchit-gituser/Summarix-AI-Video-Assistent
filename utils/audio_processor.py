import yt_dlp
from pydub import AudioSegment
import os
import re

DOWNLOAD_DIR='downloads'
os.makedirs(DOWNLOAD_DIR,exist_ok=True)

# extracting audio from any youtube file and converting to wav format
def download_youtube_audio(url :str)->str:
    output_path=os.path.join(DOWNLOAD_DIR,"%(title)s.%(ext)s")
    ydl_opts={
        "format":"bestaudio/best",
        "outtmpl":output_path,
        "quiet":True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info=ydl.extract_info(url,download=True)
        filename=ydl.prepare_filename(info)
    return filename




#  extracting audio from any file and converting to wav format
def convert_to_wav(input_path: str) -> str:
    # extract the file name only from the complete big path 
    file_name = os.path.basename(input_path)

    new_file_name = os.path.splitext(file_name)[0] + "_converted.wav"
    output_path = os.path.join(DOWNLOAD_DIR, new_file_name)
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")

    # deleting the previous file before formatting for youtube file  
    if os.path.exists(input_path) and input_path != output_path:
        os.remove(input_path)
    return output_path


# chunking the video 
def chunking(input_path :str , chunk_size_in_mins:int=20)->list:
    audio = AudioSegment.from_wav(input_path)
    chunk_ms = chunk_size_in_mins * 60 * 1000  # chunk size in ms

    chunks = []
    
    
    base_path = os.path.splitext(input_path)[0]

    for i, start in enumerate(range(0, len(audio), chunk_ms), start=1):
        chunk = audio[start:start+chunk_ms]
        
        # Ekdum clean filename: downloads/filename_converted_chunk_1.wav
        final_chunk_path = f"{base_path}_chunk_{i}.wav"
        chunk.export(final_chunk_path, format="wav")
        
        chunks.append(final_chunk_path)

    return chunks 


# full flow execution
def  process_input(source :str)->list:
    if source.startswith("http://") or source.startswith("https://"):
        print("\nDetected Youtube URL . Downloading audio...")
        file_path=download_youtube_audio(source)
        wav_path=convert_to_wav(file_path)

    else:
        print("\nDetected Loacal File . Downloading audio...")
        wav_path=convert_to_wav(source)

    print("\nChunking audio...")
    chunks=chunking(wav_path)
    print(f"Audio Ready - {len(chunks)} chunks created.")
    return chunks

