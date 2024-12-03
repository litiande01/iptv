import re

def simplify_rtsp_link(rtsp_link):
    # 使用正则表达式匹配并提取需要保留的部分
    match = re.search(r'^(rtsp://[^?]+)\?.*accountinfo=(\S+)%7EExtInfoPC2ZKLw95m5z2wHEEFeSaQ.*&GuardEncType=(\d+)', rtsp_link)
    if match:
        base_url = match.group(1)
        accountinfo = match.group(2)
        guard_enc_type = match.group(3)
        # 构建精简后的链接
        simplified_link = f"{base_url}?accountinfo={accountinfo}%3D%3D%3A20230101235235%2CEND&GuardEncType={guard_enc_type}"
        return simplified_link
    else:
        return rtsp_link  # 如果不符合格式，返回原链接

def process_m3u_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        lines = infile.readlines()
        for line in lines:
            if line.startswith('rtsp://'):
                simplified_link = simplify_rtsp_link(line.strip())
                outfile.write(simplified_link + '\n')
            else:
                outfile.write(line)

if __name__ == "__main__":
    input_file = '/opt/iptv/m3u/iptv.m3u'  # 输入文件，包含原始链接
    output_file = '/opt/iptv/m3u/iptv1.m3u'  # 输出文件，包含精简后的链接
    process_m3u_file(input_file, output_file)
    print(f"处理完成，已保存到 {output_file}")