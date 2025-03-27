#!/usr/bin/env python
"""\
命令行入口文件，提供翻译单个tex文件、翻译tex项目和提供arxiv翻译整个文章项目并编译三个功能

Usage: 可执行文件的入口
"""

from .download_paper import download_paper_source, get_arxiv_id, extract_tar_gz, get_paper_title
from .file_selector import select_file
from .preprocess_tex import search_main_tex, search_bib_tex
from .translate_tex import translate_single_tex
from . import __version__
from .config import config
import os
import re
import sys
import dataclasses
import shutil
import subprocess
# 兼容旧版本python
if sys.version_info >= (3, 11):
    import tomllib as toml
else:
    import toml


def main(args=None):
    '''
    命令行入口
    详细参数可以说明可以交给argparse处理
    需要调试可以模拟命令行调用: `main(['arxiv', '-o', 'output.tex'])`
    '''
    import argparse
    parser = argparse.ArgumentParser()

    # 版本号
    parser.add_argument("--version", "-v", action="version", version=f"TransGPTex {__version__}", help="Show the version number and exit")

    parser.add_argument("url", help='arxiv paper url')
    parser.add_argument("-o", type=str, help='output path', default="default:path")
    # 翻译模式，默认翻译arXiv项目
    parser.add_argument("--single_tex", action="store_true", help="whether to translate a single tex file mode")
    parser.add_argument("--own_tex_project", action="store_true", help="Translate the local tex project, if so url parameters fill in the path of the local tex project")
    
    # 翻译的语言模型设置
    parser.add_argument("-llm_model", type=str, help="Select the LLM model to use", default="gpt-4o-mini")
    parser.add_argument("-end_point", type=str, help="Inference endpoint url", default="https://api.openai.com/v1//")
    parser.add_argument("-ENV_API_KEY_NAME", type=str, help="The name of the environment variable that holds the API KEY, which defaults to `LLM_API_KEY`", default="LLM_API_KEY")
    parser.add_argument("-num_concurrent", type=int, default=100, help="The number of parallel requests made to the LLM API")

    # 翻译的prompt设置
    parser.add_argument("--system_prompt", type=str, default=None)
    parser.add_argument("--prompt_template", type=str, default=None)
    parser.add_argument("--cot_prompt_template", type=str, default=None)
    parser.add_argument("--use_cot", action='store_true', help="whether to use cot prompt")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--top_p", type=float, default=0.1)

    # 翻译的后处理
    parser.add_argument("--not_fix_hyphen", action="store_true", help="Disable hyphen space fix")

    # 翻译细节
    parser.add_argument("--chunk_size", type=int, default=4000, help="The maximum length of a segmented Latex file block")
    parser.add_argument("--language_to", type=str, default="Chinese")

    # 是否编译
    parser.add_argument("--no_compile", action='store_true', help="whether need to compile tex project to pdf.(need xelatex)")

    # 是否使用缓存
    parser.add_argument("--no_cache", action='store_true', help="whether to accept cached papers")

    # 是否打印参数，主要是确认一下参数写对没
    parser.add_argument("--print_config", action='store_true')

    options = parser.parse_args(args)

    for option in ["llm_model", "end_point", "num_concurrent", "system_prompt", "prompt_template", "chunk_size", "use_cot", "temperature", "top_p", "cot_prompt_template"]:
        value = getattr(options, option)
        if value is not None:
            setattr(config, option, value)
    config.fix_hyphen = not options.not_fix_hyphen

    # 配置APIKEY
    config.api_key = os.environ.get(options.ENV_API_KEY_NAME, None)
    if not config.api_key:
        print(f"请在 {options.ENV_API_KEY_NAME} 环境变量中设置API KEY，目前该环境变量不存在或为空，请检查")
        sys.exit(101)


    # 如果当前目录下存在用户自己编写的提示模板，加载用户的提示模板
    if os.path.exists("./prompts.toml"):
        # 加载该模板作为提示词
        try:
            with open("./prompts.toml", "r", encoding="utf-8") as prompt_config_file:
                prompt_config_string = prompt_config_file.read()
            prompt_config = toml.loads(prompt_config_string)
            # 获取字段
            for option in ["prompt_template", "system_prompt", "cot_prompt_template"]:
                if prompt_config.get(option, None) is not None:
                    setattr(config, option, prompt_config[option])

        except Exception as e:
            print(f"解析当前 prompt.toml 时发生错误: {e}")
            print("当前目录下的 prompt.ini 配置文件可能存在错误，已忽略")

    
    # 打印参数，主要用于Debug
    if getattr(options, "print_config"):
        print(f"config参数: ")
        fields = dataclasses.fields(config)

        for field in fields:
            # 省略api_key
            if field.name == "api_key":
                continue
            print(f"{field.name}:\t {getattr(config, field.name)}")
        sys.exit(123)


    # 解参数
    need_download_arxiv = not (options.single_tex or options.own_tex_project)
    is_single_tex_translate = options.single_tex
    url = options.url
    output_path = options.o
    language_to = options.language_to
    need_compile = not options.no_compile
    use_cache = not options.no_cache

    # 开始下载/加载项目
    if need_download_arxiv:
        arxiv_id = get_arxiv_id(url)
        
        if output_path == "default:path":
            # 如果不指定路径默认路径改为以title1开头
            title = get_paper_title(arxiv_id)
            # 修改一下无法放入路径的特殊符号为下划线
            title = re.sub(r'[<>:"/\\|?*\0]', "_", title)
            output_path = title + "/"
            print(f"未指定路径，使用论文标题路径: {output_path}")
        
        # 创建输出文件夹
        os.makedirs(output_path, exist_ok=True)

        download_paper_source(arxiv_id, output_path, use_cache)
        # 创建源码储存路径
        source_path = os.path.join(output_path, "source")
        os.makedirs(source_path, exist_ok=True)

        # 解压
        extract_tar_gz(os.path.join(output_path, f"{arxiv_id}.tar.gz"), source_path)
    else:
        # 创建输出文件夹
        if output_path == "default:path":
            # 如果没有合适路径则退出
            print(f"请通过-o指定输出路径!")
            sys.exit(102)
        os.makedirs(output_path, exist_ok=True)

        if url.endswith(".tar.gz"):
            # 如果是未解压的路径的话，就地解压
            file_dir = os.path.dirname(url)
            source_path = os.path.join(file_dir, "source")
            os.makedirs(source_path, exist_ok=True)
            extract_tar_gz(url, source_path)
        else:
            source_path = url
    
    # 翻译项目/文件
    if not is_single_tex_translate:
        translated_file_path = os.path.join(output_path, "translated_source")
        # 这里是翻译项目
        select_file(source_path, translated_file_path, language_to)
    else:
        if not source_path.endswith(".tex"):
            print(f"翻译单个tex文件请输入tex文件路径!")
            sys.exit(102)
        
        translated_file_path = output_path
        if not translated_file_path.endswith(".tex"):
            source_tex_filename = os.path.basename(source_path)
            translated_file_path = os.path.join(translated_file_path, f"translated_{source_tex_filename}")

        translate_single_tex(source_path, translated_file_path, language_to)
    
    # 编译项目
    if need_compile and not is_single_tex_translate:
        # 编译项目，首先找主tex文件，一般是源码的目录下的文件
        candidate_tex_files = {}
        for file in os.listdir(translated_file_path):
            abs_path = os.path.join(translated_file_path, file)
            if os.path.isdir(abs_path) or not file.endswith(".tex"):
                continue

            # 读取文件并加入候选
            with open(abs_path, encoding="utf-8") as f:
                candidate_tex_files[file] = f.read()
        
        # 查找主文件
        tex_to_compile = search_main_tex(candidate_tex_files)
        print(f"查找到主tex文件为 {tex_to_compile} 准备开始编译...")

        need_bibtex = search_bib_tex(translated_file_path)

        subprocess.run(['xelatex', '-interaction=nonstopmode', tex_to_compile, '-output-directory=dist'], cwd=translated_file_path)
        # 这里是依赖编译产生的aux
        if need_bibtex:
            # 一般情况下都是走该分支，通过bibtex生成bbl参考文献
            subprocess.run(['bibtex', f"dist/{tex_to_compile.rsplit('.', 1)[0]}.aux"], cwd=translated_file_path)
        else:
            # 但也有少部分情况是没有提供bib，直接提供了bbl文件的，这里直接将根目录下所有bbl复制到dist目录下
            # 因为根本没bib文件，所以bibtex编译不出东西
            dist_path = os.path.join(translated_file_path, "dist")
            os.makedirs(dist_path, exist_ok=True)
            for ts_file in os.listdir(translated_file_path):
                if ts_file.endswith(".bbl"):
                    shutil.copy(os.path.join(translated_file_path, ts_file), os.path.join(dist_path, ts_file))

        subprocess.run(['xelatex', '-interaction=nonstopmode', tex_to_compile, '-output-directory=dist'], cwd=translated_file_path)
        subprocess.run(['xelatex', '-interaction=nonstopmode', tex_to_compile, '-output-directory=dist'], cwd=translated_file_path)

        # 检查编译文件夹是否有输出
        if os.path.exists(os.path.join(translated_file_path, "dist", tex_to_compile.rsplit('.', 1)[0] + '.pdf')):
            # 把编译结果移动到输出目录下便于查找
            os.rename(os.path.join(translated_file_path, "dist", tex_to_compile.rsplit('.', 1)[0] + '.pdf'), 
                      os.path.join(output_path, f"{arxiv_id}.pdf"))
        else:
            print(f"编译失败，可能需要手动检查源码...翻译后源码位置: {translated_file_path}")
    elif need_compile:
        # 单文件就地编译即可
        subprocess.run(['xelatex', '-interaction=nonstopmode', translated_file_path], cwd=os.path.dirname(translated_file_path))

