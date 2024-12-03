import re

# M3U文件路径
m3u_file_path = '/opt/iptv/m3u/iptv1.m3u'
output_file_path = '/app/app/data/m3u/iptv.m3u'  # 输出文件仍为M3U格式
txt_file_path = '/opt/iptv/ReplicatedFiles/iptv.txt'  # 指定的TXT文件路径

# 读取TXT文件并获取第一行的数据
with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
    target_user_info = txt_file.readline().strip()  # 获取第一行内容并去掉空格

# 正则表达式匹配第四个 %7E 到指定结束位置的用户信息
pattern = r"(%7E.*?%7E.*?%7E.*?%7E)([\w\-]+)(?=%3D%3D%3A20230101235235%2CEND&GuardEncType=2)"

# 定义替换函数
def replace_user_info(match):
    return match.group(1) + target_user_info

# 读取M3U文件并提取用户信息
with open(m3u_file_path, 'r', encoding='utf-8') as file:
    m3u_content = file.read()

# 使用替换函数进行替换
modified_content = re.sub(pattern, replace_user_info, m3u_content)

# 保存修改后的内容到M3U文件
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write(modified_content)

print("已提取并保存修改后的内容到", output_file_path)