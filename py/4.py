import re

# M3U文件路径
m3u_file_path = '/opt/iptv/m3u/iptv1.m3u'
output_file_path = '/opt/iptv/ReplicatedFiles/iptv.txt'

# 正则表达式匹配第四个 %7E 到指定结束位置的用户信息
pattern = r"(?:%7E.*?%7E.*?%7E.*?%7E)([\w-]+)(?=%3D%3D%3A20230101235235%2CEND&GuardEncType=2)"

# 读取M3U文件并提取用户信息
with open(m3u_file_path, 'r', encoding='utf-8') as file:
    m3u_content = file.read()

# 查找符合条件的用户信息
user_info_list = re.findall(pattern, m3u_content)

# 去重并保持顺序
unique_user_info = []
for user_info in user_info_list:
    if user_info not in unique_user_info:
        unique_user_info.append(user_info)

# 保存去重后的用户信息到txt文件
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for user_info in unique_user_info:
        output_file.write(user_info + '\n')

print("去重后的用户信息已提取并保存到", output_file_path)