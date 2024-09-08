import whisper
import os
from datetime import timedelta
from transformers import MarianMTModel, MarianTokenizer

# 路径到包含音频文件的文件夹
audio_folder_path = '/Users/zhoudexiao/Desktop/Project/testaudio/'
audio_file_name = 'segment-7-f2-v1-a.mp3'  # 你想转换的音频文件名
output_srt_file_path = os.path.join(audio_folder_path,  f'{audio_file_name}.srt')  # 输出 SRT 文件的路径

# 加载 Whisper 模型
whisper_model = whisper.load_model("medium")

# 转录音频文件，指定识别的语言为德语
audio_file_path = os.path.join(audio_folder_path, audio_file_name)
result = whisper_model.transcribe(audio_file_path, language="de", verbose=True)  # 使用verbose参数来实时打印转录进度

# 加载翻译模型和 tokenizer
translation_model_name = 'Helsinki-NLP/opus-mt-de-zh'
tokenizer = MarianTokenizer.from_pretrained(translation_model_name)
translation_model = MarianMTModel.from_pretrained(translation_model_name)

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
        
        # 翻译文本
        print(f"Translating text: {text}")  # 调试信息
        inputs = tokenizer.encode(text, return_tensors='pt', padding=True)
        translated_tokens = translation_model.generate(inputs, max_length=400, num_beams=4, early_stopping=True)
        translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
        
        print(f"Translated text: {translated_text}")  # 调试信息
        
        # 写入 SRT 文件
        srt_file.write(f"{i}\n")
        srt_file.write(f"{start_srt} --> {end_srt}\n")
        srt_file.write(f"{translated_text}\n")
        srt_file.write(f"{text}\n\n")

print(f"SRT file has been saved to: {output_srt_file_path}")