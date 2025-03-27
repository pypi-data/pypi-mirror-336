"""\
翻译单个tex文件

Usage: 翻译单个tex文件
"""
from typing import List

from .latex_spilter import LatexTextSplitter
from .llm_api_async import Translator
from .preprocess_tex import preprocess_tex_content
from .config import config
import os
import re

def translate_single_tex(tex_file_path: str, output_path: str, language_to: str):
    # 指示翻译中
    print(f"正在翻译 {os.path.basename(tex_file_path)} ...")

    # 读取tex文件
    with open(tex_file_path, "r", encoding="utf-8") as f:
        tex_text = f.read()
    
    # 进行预处理
    tex_text, holder_index_to_content = preprocess_tex_content(tex_text)

    # 切分器，注意参数设置
    ls = LatexTextSplitter(chunk_size=config.chunk_size)
    tex_texts = ls.split_text(tex_text)

    # 实例化翻译器
    translator = Translator()

    combined_texts = translator.translate_batch(tex_texts, language_to)

    # 后处理，清除多余的```，deepseek会多加这样的符号，但latex中没有这个语法，如果源内容中没有可以直接移除
    for i in range(len(combined_texts)):
        if "```" not in tex_texts[i]:
            combined_texts[i] = combined_texts[i].replace("```", "")

    translated_tex = "\n".join(combined_texts)

    # 后处理，把占位符还原
    postprocess_tex = ""
    for line in translated_tex.split("\n"):
        if line.strip().startswith("ls_replace_holder_"):
            holder_index = line.strip().replace("ls_replace_holder_", "")
            if holder_index.isdigit() and int(holder_index) >= 0 and int(holder_index) < len(holder_index_to_content):
                holder_index = int(holder_index)
                holder_content = holder_index_to_content[holder_index]
                postprocess_tex += "\n" + holder_content
            else:
                print(f"{line} 疑似占位符但未解析成功...")
                postprocess_tex += "\n" + line
        elif line.strip().startswith("====="):
            # 可能是标识符被llm翻译进去了，忽略即可
            continue
        else:
            postprocess_tex += "\n" + line

    # 写入文件
    with open(os.path.join(output_path, os.path.basename(tex_file_path)), "w", encoding="utf-8") as f:
        f.write(postprocess_tex)

    print(f" {os.path.basename(tex_file_path)} 翻译完成!")


def generate_tex_chunks(tex_file_path: str):
    # 如果latex项目中有很多小文件，那么依次调用`translate_single_tex`会导致并行性很低速度变慢的问题。
    # 一种方式就是把translate这个操作从单文件翻译中独立出来，先生成整个项目里所有待翻译的块，之后全部块翻译完之后再执行后处理。

    # 读取tex文件
    with open(tex_file_path, "r", encoding="utf-8") as f:
        tex_text = f.read()

    # 进行预处理
    tex_text, holder_index_to_content = preprocess_tex_content(tex_text)

    # 切分器，注意参数设置
    ls = LatexTextSplitter(chunk_size=config.chunk_size)
    tex_texts = ls.split_text(tex_text)

    return tex_texts, holder_index_to_content


command_adhesion_pattern = re.compile(r"(\\[a-zA-Z\d_\-]*)(?=[\u4e00-\u9fa5\u3000-\u303f\uFF00-\uFFEF])")


def handle_command_adhesion(text):
    # 处理命令粘连问题，比如`一种基于\modelname的数据选择器`处理为`一种基于\modelname{}的数据选择器`从而减少编译错误
    text = command_adhesion_pattern.sub(r"\1{}", text)
    return text

def postprocess_tex_line(text):
    # 最后的行处理，目前用于处理命令粘连
    return handle_command_adhesion(text)

def postprocess_tex_content(translated_tex_texts: List[str], original_tex_texts: List[str], holder_index_to_content, output_path: str):
    # 后处理，清除多余的```，deepseek会多加这样的符号，但latex中没有这个语法，如果源内容中没有可以直接移除
    for i in range(len(translated_tex_texts)):
        if "```" not in original_tex_texts[i]:
            translated_tex_texts[i] = translated_tex_texts[i].replace("```", "")
        
        # 已知gpt-4o-mini会在\end{abstract}后加\end{document}，导致编译停止。做一下替换回避问题
        if "\end{document}" in translated_tex_texts[i] and "\end{document}" not in original_tex_texts[i]:
            translated_tex_texts[i] = translated_tex_texts[i].replace("\end{document}", "")

        # doubao-1.5-pro-32k会自作主张在"-"左右加空格，比如"gpt-4o"会变成"gpt - 4o"
        # 因为这是激进地后处理手段，可能会带来其他影响，在config内提供关闭的选项
        if config.fix_hyphen:
            translated_tex_texts[i] = re.sub(r'\s*-\s*', '-', translated_tex_texts[i])

    translated_tex = "\n".join(translated_tex_texts)

    # 后处理，把占位符还原
    postprocess_tex = ""
    for line in translated_tex.split("\n"):
        if line.strip().startswith("ls_replace_holder_"):
            holder_index = line.strip().replace("ls_replace_holder_", "")
            if holder_index.isdigit() and int(holder_index) >= 0 and int(holder_index) < len(holder_index_to_content):
                holder_index = int(holder_index)
                holder_content = holder_index_to_content[holder_index]
                postprocess_tex += "\n" + holder_content
            else:
                print(f"{line} 疑似占位符但未解析成功...")
                postprocess_tex += "\n" + postprocess_tex_line(line)
        elif line.strip().startswith("====="):
            # 可能是标识符被llm翻译进去了，忽略即可
            continue
        else:
            postprocess_tex += "\n" + postprocess_tex_line(line)

    # 写入文件
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(postprocess_tex)

    print(f" {os.path.basename(output_path)} 写入完成!")