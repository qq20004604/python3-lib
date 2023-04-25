from moviepy.editor import VideoFileClip

input_video_path = "123.mp4"
output_video_path = "result.mp4"
end_time = 3 * 60 + 50  # 3分钟50秒

# 加载视频
clip = VideoFileClip(input_video_path)

# 剪辑视频
trimmed_clip = clip.subclip(0, end_time)

# 保存剪辑后的视频
trimmed_clip.write_videofile(output_video_path, codec="libx264", audio_codec="aac")

# 关闭视频对象
clip.close()
trimmed_clip.close()
