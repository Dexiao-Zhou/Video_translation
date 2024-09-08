import whisper
import os
from datetime import timedelta

# 路径到包含音频文件的文件夹
audio_folder_path = '/Users/zhoudexiao/Desktop/Project/testaudio/'
audio_file_name = 'segment-7-f2-v1-a.mp3'  # 你想转换的音频文件名
output_srt_file_path = os.path.join(audio_folder_path, f'{audio_file_name}.srt')  # 输出 SRT 文件的路径

# 加载模型
# model = whisper.load_model("medium")
model = whisper.load_model("tiny")

# 转录音频文件，指定识别的语言为中文
audio_file_path = os.path.join(audio_folder_path, audio_file_name)
result = model.transcribe(audio_file_path, language="de", verbose=True)  # 使用verbose参数来实时打印转录进度


# 将转录结果转换为 SRT 格式并保存
with open(output_srt_file_path, 'w', encoding='UTF-8') as srt_file:
    for i, segment in enumerate(result["segments"], start=1):
        start_seconds = segment["start"]
        end_seconds = segment["end"]
        # 格式化开始和结束时间为 SRT 规范
        start_srt = str(timedelta(seconds=start_seconds)).replace('.', ',')
        end_srt = str(timedelta(seconds=end_seconds)).replace('.', ',')
        # 确保毫秒是三位数字
        if ',' not in start_srt:
            start_srt += ',000'
        if ',' not in end_srt:
            end_srt += ',000'
        text = segment["text"]
        srt_file.write(f"{i}\n")
        srt_file.write(f"{start_srt} --> {end_srt}\n")
        srt_file.write(f"{text}\n\n")

print(f"SRT file has been saved to: {output_srt_file_path}")
