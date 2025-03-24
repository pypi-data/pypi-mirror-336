# ytdebunk  

## Overview  
`ytdebunk` is a command-line tool designed to:  
- Download audio from YouTube videos.  
- Transcribe the audio content.  
- Optionally enhance the transcription using the **Gemini API**.  
- Optionally detect logical faults in the transctiption using the **Gemini API**.  

This tool is particularly useful for analyzing transcriptions to identify **logical fallacies** and **incorrect claims** made by YouTubers.  

## Installation 

For avoiding conflicts better create a virtual environment and start working on it:

```sh
python3.11 -m venv .venv
source .venv/bin/activate
```

Now, you can install from PyPI using,

```sh
pip install ytdebunk
```

Alternatively, for latest updated please try installing directly from Github using:

```sh
pip install git+https://github.com/hissain/youtuber-debunked.git
```

## Usage  

The `ytdebunk.py` script provides a **command-line interface (CLI)** with several options.  

### **Arguments**  
- `video_url` (**str**) – URL of the YouTube video to download audio from.  

### **Options**  
| Option                  | Description |
|-------------------------|-------------|
| `-e, --enhance` (bool) | Enhance the transcription using the **Gemini API**. *(Default: False)* |
| `-d, --detect` (bool) | Detect logical faults in the transcription using **Gemini API**. *(Default: False)* |
| `-v, --verbose` (bool) | Increase output verbosity. |
| `-t, --token` (str) | API token for the **Gemini API** *(Required if `--enhance` or `--detect`is enabled)*. |
| `-st, --start_time` (float) | Start time of the audio clip in seconds |
| `-et, --end_time` (float) | End time of the audio clip in seconds |

### **Example Usage**  

```bash
ytdebunk "https://www.youtube.com/watch?v=example" -e -d -v -t YOUR_GEMINI_API_TOKEN
```


```bash
export GEMINI_API_TOKEN="your_api_key"
ytdebunk "https://www.youtube.com/watch?v=example" -e -d -v #when Gemini API key is in environment
```

See an example notebook [Example Notebook](experiment/exp.ipynb) file for details usage.  

## **Environment Variables**  
If preferred, you can set the **Gemini API token** as an environment variable instead of passing it as a CLI argument:

```sh
export GEMINI_API_TOKEN="your_api_key"
```

## **Detailed Process**  

1. **Download Audio**  
   - Uses the `download_audio` function from `ytdebunk.downloader` to download audio from the given YouTube URL.  

2. **Transcribe Audio**  
   - Uses the `transcribe_audio` function from `ytdebunk.transcriber` to generate a text transcription.  

3. **Enhance Transcription** *(Optional)*  
   - If `--enhance` is enabled, the script uses `enhance_transcription` from `ytdebunk.refiner` to refine the transcription using the **Gemini API**.  
   - The API token must be provided via `--token` or as an **environment variable**.  

3. **Detect Logical Faults** *(Optional)*  
   - If `--detect` is enabled, the script uses `detect_logical_faults` from `ytdebunk.philosopher` to detect logical fults, fallacies, bias, irony and so on in the transcription using the **Gemini API**.  
   - The API token must be provided via `--token` or as an **environment variable**.  

5. **Save Transcription**  
   - The final transcription and logical faults (raw or enhanced) are saved to the ./download folder.  

## **Error Handling**  
- If `--enhance` or `--detect` are enabled but no **Gemini API token** is provided, the script prints an **error message** and exits.

## **License**  
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.  


## Contribution and Contact

You can fork this project and submit pull request in the project. 
Please contact to the author at hissain.khan@gmail.com
