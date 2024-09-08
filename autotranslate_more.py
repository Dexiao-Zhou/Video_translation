import whisper
import os
from datetime import timedelta
from transformers import MarianMTModel, MarianTokenizer

def generate_translated_srt(audio_file_path, output_srt_file_path, source_lang="de", target_lang="zh"):
    """
    从音频文件生成带翻译的 SRT 字幕文件。
    参数:
    audio_file_path (str): 音频文件的路径。
    output_srt_file_path (str): 输出 SRT 文件的路径。
    source_lang (str): 源语言代码。
    target_lang (str): 目标语言代码。
    """
    # 加载 Whisper 模型
    whisper_model = whisper.load_model("large-v3")

    # 转录音频文件
    result = whisper_model.transcribe(audio_file_path, language=source_lang, verbose=True)

    # 加载翻译模型和 tokenizer
    translation_model_name = f'Helsinki-NLP/opus-mt-{source_lang}-{target_lang}'
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

    print(f"SRT 文件已保存至：{output_srt_file_path}")

# 音频文件路径列表
audio_folder_path = './drive/MyDrive/Colab Notebooks/TPG/'
audio_files = [
    'TPG_LE_08_-_Fertigungsgerechte_Werkstueckgestaltung_V_Wa_Intro_LAUT-1.mp3',
    'TPG_LE_09_-_Fertigungsgerechte_Werkstueckgestaltung_VI_Wa_Intro_LAUT-1.mp3',
    'TPG_LE_10_-_Toleranzgerechtes_Konstruieren_editBS_mid.mp3',
    'TPG_LE_15_-_Umweltgerechtes_Konstruieren_Wa_Intro-1.mp3',
    'TPG_LE_16_-_Nutzerzentrierte_Produktgestaltung_Wa_Intro-1.mp3'
    # 添加其他音频文件名
]

# 遍历音频文件路径列表并生成对应的 SRT 文件
for audio_file in audio_files:
    audio_file_path = os.path.join(audio_folder_path, audio_file)
    # 获取音频文件名，不包括路径和扩展名
    audio_name = os.path.splitext(audio_file)[0]
    # 设置 SRT 输出文件路径
    output_srt_file_path = os.path.join(audio_folder_path, f'{audio_name}.srt')
    # 生成 SRT 文件
    generate_translated_srt(audio_file_path, output_srt_file_path)
