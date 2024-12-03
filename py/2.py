import re
import pandas as pd

# 从HTML文件中提取频道
def extract_channels(file_path):
    channels = []
    channel_pattern = re.compile(
        r'ChannelID="(\d+)",ChannelName="([^"]+)",UserChannelID="(\d+)",ChannelURL="([^|]+)\|([^"]+)"'
    )

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            matches = channel_pattern.findall(content)
            for match in matches:
                channel_id, channel_name, user_channel_id, igmp_url, rtsp_url = match

                # 处理IGMP地址
                igmp_address = re.sub(r'igmp://', 'http://192.168.2.10:6000/udp/', igmp_url)

                # 生成频道信息
                channels.append(
                    {
                        'name': channel_name,
                        'rtsp': rtsp_url,
                        'http': igmp_address
                    }
                )
            print(f"成功从 {file_path} 提取了 {len(channels)} 个频道。")
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")

    return channels

# 从M3U文件追加内容并统计频道数量
def append_m3u_from_other_file(input_m3u_path, output_file):
    additional_channel_count = 0  # 用于记录追加文件中的频道数量

    try:
        with open(input_m3u_path, 'r', encoding='utf-8') as file:
            # 读取整个M3U文件
            content = file.read()
            output_file.write(content)
            output_file.write('\n\n')  # 添加两个换行符以保持格式美观

            # 统计追加文件中的频道数量，通过计数 #EXTINF 标签
            additional_channel_count = content.count('#EXTINF')

            print(f"成功将 {input_m3u_path} 文件内容追加到输出文件中，包含 {additional_channel_count} 个频道。")
    except FileNotFoundError:
        print(f"文件未找到: {input_m3u_path}")

    return additional_channel_count

# 生成M3U文件
def generate_m3u(channels, output_path, sorted_channel_list, name_map, group_titles, additional_m3u_path=None):
    written_channels = set()  # 用于存储已经写入的频道名
    processed_channel_count = 0  # 记录生成的频道数量
    total_channel_count = 0  # 记录所有频道的总数

    with open(output_path, 'w', encoding='utf-8') as file:
        # 写入 #EXTM3U 标签
        file.write("#EXTM3U\n\n")

        # 将xlsx中的频道顺序与提取到的频道匹配并写入M3U文件
        for channel_name in sorted_channel_list:
            for channel in channels:
                if channel['name'] == channel_name and channel['name'] not in written_channels:
                    written_channels.add(channel['name'])
                    processed_channel_count += 1
                    total_channel_count += 2  # 每个频道有RTSP和HTTP两个流

                    # 获取修正后的频道名称和group-title
                    fixed_name = name_map.get(channel_name, channel_name)
                    rtsp_group_title = group_titles.get(channel_name, {}).get('rtsp', "回看")
                    http_group_title = group_titles.get(channel_name, {}).get('http', "直播")

                    # 添加回看的 RTSP 流
                    file.write(
                        f'#EXTINF:-1 tvg-id="{fixed_name}" tvg-name="{fixed_name}" tvg-logo="" group-title="{rtsp_group_title}", {fixed_name}\n')
                    file.write(f'{channel["rtsp"]}\n\n')

                    # 添加直播的 HTTP 流
#                    file.write(
#                        f'#EXTINF:-1 tvg-id="{fixed_name}" tvg-name="{fixed_name}" tvg-logo="" group-title="{http_group_title}", {fixed_name}\n')
#                    file.write(f'{channel["http"]}\n\n')

        # 如果提供了额外的M3U文件路径，将其内容追加到输出文件末尾
        additional_channel_count = 0
        if additional_m3u_path:
            additional_channel_count = append_m3u_from_other_file(additional_m3u_path, file)

    total_channel_count += additional_channel_count  # 包含追加的频道数量

    print(f"成功生成 M3U 文件，共处理了 {processed_channel_count} 个频道，输出文件保存为: {output_path}")
    print(f"生成的 M3U 文件中包含 {total_channel_count} 个流（频道*2，包含RTSP和HTTP，包含追加的频道）。")

# 从xlsx文件中获取排序列表、频道修正名称和group-title
def get_sorted_channel_list_and_name_map_from_xlsx(xlsx_file_path):
    try:
        df = pd.read_excel(xlsx_file_path)
        # 假设xlsx文件的第一列为频道名称，第二列为修正后的名称，第三列为RTSP的group-title，第四列为HTTP的group-title
        sorted_channel_list = df.iloc[:, 0].tolist()  # 第一列是排序用的频道名称
        # 使用第一列的频道名称，如果第二列为空则使用第一列的名称
        name_map = {
            row[0]: row[1] if pd.notna(row[1]) and row[1].strip() != '' else row[0]
            for row in df.itertuples(index=False, name=None)
        }
        # 获取group-title的字典，第三列为rtsp，第四列为http
        group_titles = {
            row[0]: {
                'rtsp': row[2] if pd.notna(row[2]) and row[2].strip() != '' else "回看",
                'http': row[3] if pd.notna(row[3]) and row[3].strip() != '' else "直播"
            }
            for row in df.itertuples(index=False, name=None)
        }
        print(f"成功从 {xlsx_file_path} 读取到频道排序、名称修正和group-title信息。")
        return sorted_channel_list, name_map, group_titles
    except FileNotFoundError:
        print(f"文件未找到: {xlsx_file_path}")
        return [], {}, {}

# 输入和输出路径
input_html_file_path = r"/opt/iptv/DataDownload/res.html"  # 输入HTML文件路径
output_m3u_path = r"/opt/iptv/m3u/iptv.m3u"  # 输出M3U文件路径
additional_m3u_file_path = r""  # 追加的M3U文件路径
xlsx_file_path = r"/opt/iptv/ReplicatedFiles/channel_list.xlsx"  # 排序的xlsx文件路径

# 继续之前的逻辑进行HTML解析和M3U文件生成
try:
    channels = extract_channels(input_html_file_path)
    sorted_channel_list, name_map, group_titles = get_sorted_channel_list_and_name_map_from_xlsx(xlsx_file_path)
    if channels:
        generate_m3u(channels, output_m3u_path, sorted_channel_list, name_map, group_titles, additional_m3u_path=additional_m3u_file_path)
    else:
        print("没有提取到任何频道，未生成文件。")
except FileNotFoundError:
    print(f"文件未找到: {input_html_file_path}")