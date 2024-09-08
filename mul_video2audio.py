from moviepy.editor import VideoFileClip
import os

# 视频文件路径
video_file_path = '/Users/zhoudexiao/Downloads/DL'  # 替换为你的视频文件路径

# 指定要处理的视频文件名列表
video_names = ['20200930-LECPORCR-Maier-OC-1280x720.m4v',
               '20201002-LECPORCR-Maier-OC-1280x720.m4v','20201004-LECPORCR-Maier-OC-1280x720-2.m4v','20201004-LECPORCR-Maier-OC-1280x720-3.m4v','20201004-LECPORCR-Maier-OC-1280x720.m4v'
               ]

# 遍历所有指定的视频文件
for video_name in video_names:
    full_video_path = os.path.join(video_file_path, video_name)  # 合并路径和文件名

    # 尝试加载视频文件
    try:
        video_clip = VideoFileClip(full_video_path)
    except Exception as e:
        print(f"加载视频文件 {video_name} 时出错: {e}")
        continue  # 处理下一个文件

    # 提取音频部分
    audio_clip = video_clip.audio

    # 设置输出的音频文件路径
    audio_file_path = os.path.join(video_file_path, f'{video_name[:-4]}.mp3')  # 从视频名称中去掉.mp4并添加.mp3

    # 尝试将音频部分写入文件
    try:
        audio_clip.write_audiofile(audio_file_path)
    except Exception as e:
        print(f"写入音频文件 {audio_file_path} 时出错: {e}")
    finally:
        # 释放资源
        if audio_clip:
            audio_clip.close()
        if video_clip:
            video_clip.close()

    print(f"音频已保存至：{audio_file_path}")
