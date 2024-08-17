import sys
import requests
from bs4 import BeautifulSoup
import markdownify
import nbformat as nbf
import argparse
from argparse import ArgumentParser, RawTextHelpFormatter, RawDescriptionHelpFormatter, ArgumentDefaultsHelpFormatter

class MyHelpFormatter(RawTextHelpFormatter, RawDescriptionHelpFormatter, ArgumentDefaultsHelpFormatter):
    pass

def pypi2md(url, file_path):
    # Send a request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the project description
    description_div = soup.find("div", {"class": "project-description"})

    # Convert the HTML to markdown
    description_markdown = markdownify.markdownify(str(description_div), heading_style="ATX")

    # Write the markdown content to a file
    with open(file_path, "w") as file:
        file.write(description_markdown)

    print(f"Markdown file saved as {file_path}")


def md2ipynb(md_file_path, ipynb_file_path):
    # Markdownファイルを読み込む
    with open(md_file_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # 新しいJupyter Notebookを作成
    nb = nbf.v4.new_notebook()

    # Markdownファイルを行単位で処理
    lines = md_content.splitlines()
    in_code_block = False
    code_block = []

    for line in lines:
        if line.startswith("```"):
            if in_code_block:
                # 既存のコードブロックをコードセルに変換して追加
                nb.cells.append(nbf.v4.new_code_cell("\n".join(code_block)))
                code_block = []
            in_code_block = not in_code_block
        elif in_code_block:
            code_block.append(line)
        else:
            # コードブロック外はMarkdownセルとして追加
            if len(nb.cells) > 0 and nb.cells[-1].cell_type == "markdown":
                nb.cells[-1].source += "\n" + line
            else:
                nb.cells.append(nbf.v4.new_markdown_cell(line))

    # 最後に残ったコードブロックがある場合、コードセルに変換
    if code_block:
        nb.cells.append(nbf.v4.new_code_cell("\n".join(code_block)))

    # ipynbファイルとして保存
    with open(ipynb_file_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

    print(f"Converted {md_file_path} to {ipynb_file_path}")


def get_arg():
    # コマンドライン引数をパース
    parser = argparse.ArgumentParser(description="""
PyPI(pypi.org)の「プロジェクトの説明」をJupyter Notebook形式のファイルに変換します。指定したパッケージ名に従い、次のファイルを出力します。
README-<package_name>.md
README-<package_name>.ipynb
""".strip()
                                     , formatter_class=MyHelpFormatter)
    parser.add_argument('package_name', help="パッケージ名を指定してください。")
    parser.add_argument('-V', '--version', action='version', version='%(prog)s 0.1.0')
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    return args.package_name


def get_params():
    # PyPIプロジェクト名
    package_name = get_arg()

    # URL of the project on PyPI
    url = f"https://pypi.org/project/{package_name}/"

    # 出力するmarkdownファイルのパス
    file_path = f"README-{package_name}.md"

    # 出力するipynbファイルのパス
    ipynb_file_path = f"README-{package_name}.ipynb"

    return url, file_path, ipynb_file_path


def main():
    url, file_path, ipynb_file_path = get_params()
    pypi2md(url, file_path)
    md2ipynb(file_path, ipynb_file_path)


if __name__ == "__main__":
    main()
