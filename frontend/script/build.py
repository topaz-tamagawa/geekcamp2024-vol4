import glob
from bs4 import BeautifulSoup
import os

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
component_paths = glob.glob("component/*.html")

# コンポーネントファイルは出力対象から除外
for i, html_path in enumerate(html_paths):
    if html_path in component_paths:
        html_paths.pop(i)

# 対象のHTMLファイルに処理を実行
for html_path in html_paths:
    soup = resolve_html(html_path)
    output_path = os.path.join("dist", html_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as output_file:
        output_file.write(soup.prettify())
