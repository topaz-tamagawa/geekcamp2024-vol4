import glob
from bs4 import BeautifulSoup
import os
import re

def resolve_html(file_path):
    """
    file_pathで示されたHTMLファイルを解析し、iframe要素の依存関係を解決する
    """
    with open(file_path, "r") as file:
        soup = BeautifulSoup(file.read(), "html.parser")
    for iframe in soup.select("iframe"):
        iframe_path: str = iframe.get("src")
        component_path = os.path.join(os.path.dirname(file_path), iframe_path)
        component_soup = resolve_html(component_path)
        component_body = component_soup.find("body")
        iframe.replace_with(*component_body.children)
    return soup


html_paths = glob.glob("*.html") + glob.glob("**/*.html")

# 対象外のファイルをlistから削除
html_paths = [p for p in html_paths if not re.search(r"^(component|dist)", p)]

# 対象のHTMLファイルに処理を実行
for html_path in html_paths:
    soup = resolve_html(html_path)
    output_path = os.path.join("dist", html_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as output_file:
        output_file.write(soup.prettify())
