from moviepy.editor import VideoFileClip, AudioFileClip

def merge_video_audio_moviepy(video_url, audio_url, output_filename):
    print("Downloading and merging with moviepy...")
    video = VideoFileClip(video_url)
    audio = AudioFileClip(audio_url)
    final_clip = video.set_audio(audio)
    final_clip.write_videofile(output_filename)
    print(f"Video saved as {output_filename}")
