from moviepy.editor import VideoFileClip

# 视频文件路径
video_file_path = '/Users/zhoudexiao/Desktop/Project/testaudio/'  # 替换为你的视频文件路径
video_name = 'segment-7-f2-v1-a1.ts'
full_video_path = video_file_path + video_name  # 合并路径和文件名

# 尝试加载视频文件
try:
    video_clip = VideoFileClip(full_video_path)
except Exception as e:
    print(f"加载视频时出错: {e}")
    raise

# 提取音频部分
audio_clip = video_clip.audio

# 设置输出的音频文件路径
audio_file_path = f'{video_name[:-4]}.mp3'  # 从视频名称中去掉.mp4并添加.mp3

# 尝试将音频部分写入文件
try:
    audio_clip.write_audiofile(audio_file_path)
except Exception as e:
    print(f"写入音频文件时出错: {e}")
    raise
finally:
    # 释放资源
    if audio_clip:
        audio_clip.close()
    if video_clip:
        video_clip.close()

print(f"音频已保存至：{audio_file_path}")
