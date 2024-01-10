import typer

# from pydantic import HttpUrl
from pytube import YouTube, Playlist
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from slugify import slugify 
import json

app = typer.Typer()


def download_video(iVideo):
  iVideo.streams.filter(
  progressive=True,
  file_extension="mp4").order_by("resolution").desc().first().download()

def download_transcript(iVideoID, iVideoTitle):

  all_transcripts = YouTubeTranscriptApi.list_transcripts(iVideoID)
  for transcript in all_transcripts:
    if transcript.language_code == "en":
      fetched_transcript = transcript.fetch()
      break

  transcript_text = TextFormatter().format_transcript(fetched_transcript)
  # here the title of the video should not contain any characters which are not allowed by the file system of the particular os
  # eg. windows path separators, space, colon, comma, dot, slash, star, tilde, etc.
  # to do this we use python-slugify library - https://stackoverflow.com/a/29942164/2241802
  with open(slugify(iVideoTitle) + ".txt", "w", encoding="utf-8") as outFile:
    outFile.write(transcript_text)

def get_video_info(iURL):
  yt = YouTube(iURL)
  return  {
    "title": yt.title,
    "id": yt.video_id,
    "url": yt.watch_url,
    "views": yt.views,
    "length": yt.length,
    # "description": yt.description,
    "channel": yt.author,
    "channel_url": yt.channel_url,
    # "published": yt.publish_date,
    "rating": yt.rating
  }

@app.command()
def video(
    url=typer.Argument(..., help="A valid Youtube Video URL"),
    download: bool = typer.Option(True, help="download video"),
    transcript: bool = typer.Option(False, help="download transcript"),
):
  yt = YouTube(url)

  if download:
    print(f"Downloading Video: {iVideo.title}")
    download_video(yt)
  
  if transcript:
    video_id = yt.video_id
    video_title = yt.title
    print(f"Downloading trascript for: {video_title}")
    download_transcript(video_id, video_title)
    


@app.command()
def playlist(
    url=typer.Argument(..., help="A valid url Youtube Playlist"),
    download: bool = typer.Option(True,
                                  help="download all videos from playlist"),
    transcript: bool = typer.Option(
        False, help="downlaod all the transcripts from the playlist"),
):
  p = Playlist(url)

  if download:
    for video in p.videos:
      print(f"Downloading Video: {video.title}")
      print(f"Video url: {video.watch_url}")
      download_video(video)
  if transcript:
    for video in p.videos:
      print(f"Downloading trascript for: {video.title}")
      print(f"Video url: {video.watch_url}")
      download_transcript(video.video_id, video.title)

@app.command()
def info(url = typer.Argument(..., help="A valid Youtube Video URL")):
  yt = YouTube(url)
  print(json.dumps(get_video_info(url), indent=4))


if __name__ == "__main__":
  app()
