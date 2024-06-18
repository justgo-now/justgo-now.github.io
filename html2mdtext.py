import html2text
import sys
from bs4 import BeautifulSoup

def html_to_markdown(html_content):
    # 初始化html2text
    h = html2text.HTML2Text()
    h.ignore_links = False  # 保留链接
    h.ignore_images = False  # 保留图片
    h.ignore_emphasis = False  # 保留强调
    h.body_width = 0  # 不换行

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 处理代码块
    for code_block in soup.find_all('code'):
        code_text = code_block.get_text()
        code_block.replace_with(f'```\n{code_text}\n```')

    # 将处理后的HTML转为Markdown
    markdown_content = h.handle(str(soup))

    return markdown_content

md_text = open(sys.argv[1], 'r', encoding='utf-8').read()

# text_maker = html2text.HTML2Text()
# text_maker.bypass_tables = False
# markdown = text_maker.handle(md_text)
markdown = html_to_markdown(md_text)
with open(f'{sys.argv[2]}.md', 'w', encoding='utf-8') as file:
    file.write(markdown)