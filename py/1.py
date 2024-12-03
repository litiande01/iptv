def append_txt_to_html(txt_file_path, html_file_path):
    # 读取TXT文件的内容
    with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
        txt_content = txt_file.read()

    # 读取HTML文件的内容
    with open(html_file_path, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

    # 在HTML内容末尾前加入TXT内容
    updated_html_content = html_content.replace("</html>", f"{txt_content}\n</html>")

    # 将修改后的HTML内容写回文件
    with open(html_file_path, 'w', encoding='utf-8') as html_file:
        html_file.write(updated_html_content)

    print("内容已成功添加到HTML文件末尾！")

# 使用示例
txt_file_path = '/opt/iptv/ReplicatedFiles/tianjia.txt'  # 替换为你的TXT文件路径
html_file_path = '/opt/iptv/DataDownload/res.html'  # 替换为你的HTML文件路径
append_txt_to_html(txt_file_path, html_file_path)