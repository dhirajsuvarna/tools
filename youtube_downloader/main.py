"""
Things to do - 

- The `info` command should check if the url is playlist or a video and display the information accordingly
- decide the header information to be added in the transcript
"""


import typer
from pytube import YouTube, Playlist
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from slugify import slugify
import json
import logging
import sys
import os
from logging import StreamHandler, FileHandler

logging.basicConfig(
    handlers=[
        StreamHandler(stream=sys.stdout),
        FileHandler(filename="youtube_downloader.log", mode="w", encoding="utf-8"),
    ],
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)


app = typer.Typer()


def download_video(iVideo, iOutDirPath=r"./"):
    iVideo.streams.filter(progressive=True, file_extension="mp4").order_by(
        "resolution"
    ).desc().first().download(iOutDirPath)


def get_available_transcripts(iVideo_id):
    all_transcripts = YouTubeTranscriptApi.list_transcripts(iVideo_id)
    codes = []
    for transcript in all_transcripts:
        codes.append(transcript.language_code)
    return codes


def download_transcript(iVideoID, iVideoTitle, iOutDirPath=r"./"):
    all_transcripts = YouTubeTranscriptApi.list_transcripts(iVideoID)
    fetched_transcript = None
    for transcript in all_transcripts:
        if transcript.language_code in ["en", "en-IN"]:
            fetched_transcript = transcript.fetch()
            break

    if fetched_transcript is None:
        logging.error("Transcript Not Found")
        logging.info(f"Available Transcirpts: {get_available_transcripts(iVideoID)}")
        exit()

    transcript_text = TextFormatter().format_transcript(fetched_transcript)
    # here the title of the video should not contain any characters which are not allowed by the file system of the particular os
    # eg. windows path separators, space, colon, comma, dot, slash, star, tilde, etc.
    # to do this we use python-slugify library - https://stackoverflow.com/a/29942164/2241802
    outFilePath = os.path.join(iOutDirPath, slugify(iVideoTitle) + ".txt")
    with open(outFilePath, "w", encoding="utf-8") as outFile:
        outFile.write(transcript_text)


def get_video_info(iURL):
    yt = YouTube(iURL)
    available_lang_codes = get_available_transcripts(yt.video_id)
    return {
        "title": yt.title,
        "id": yt.video_id,
        "available_transcripts": "; ".join(available_lang_codes),
        "url": yt.watch_url,
        "views": yt.views,
        "length": yt.length,
        # "description": yt.description,
        "channel": yt.author,
        "channel_url": yt.channel_url,
        # "published": yt.publish_date,
        "rating": yt.rating,
    }


@app.command()
def video(
    url=typer.Argument(..., help="A valid Youtube Video URL"),
    download: bool = typer.Option(True, help="download video"),
    transcript: bool = typer.Option(False, help="download transcript"),
):
    yt = YouTube(url)

    if download:
        logging.info(f"Downloading Video: {yt.title}")
        download_video(yt)

    if transcript:
        video_id = yt.video_id
        video_title = yt.title
        logging.info(f"Downloading trascript for: {video_title}")
        download_transcript(video_id, video_title)


@app.command()
def playlist(
    url=typer.Argument(..., help="A valid url Youtube Playlist"),
    download: bool = typer.Option(True, help="download all videos from playlist"),
    transcript: bool = typer.Option(
        False, help="downlaod all the transcripts from the playlist"
    ),
):
    p = Playlist(url)
    outputDir = slugify(p.title)
    os.makedirs(outputDir, exist_ok=True)

    if download:
        for video in p.videos:
            print(f"Downloading Video: {video.title}")
            print(f"Video url: {video.watch_url}")
            download_video(video, outputDir)
    if transcript:
        for video in p.videos:
            print(f"Downloading trascript for: {video.title}")
            print(f"Video url: {video.watch_url}")
            download_transcript(video.video_id, video.title, outputDir)


@app.command()
def info(url=typer.Argument(..., help="A valid Youtube Video URL")):
    yt = YouTube(url)
    print(json.dumps(get_video_info(url), indent=4))


if __name__ == "__main__":
    app()
