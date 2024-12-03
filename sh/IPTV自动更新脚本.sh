#!/bin/bash

# 定义日志文件路径
LOG_FILE="/path/to/iptv/DataDownload/error.log"

# 第一步：执行第一个 curl 请求并保存 cookie
curl http://125.88.95.8:33200/EPG/jsp/ValidAuthenticationHWCTC.jsp \
    -c /path/to/iptv/DataDownload/cookie.txt \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    --data 'UserID=07620668267&Lang=&SupportHD=1&NetUserID=hy8362249%40iptv.gd&DHCPUserID=hy8362249%40iptv.gd&Authenticator=F60690DFFD7E6AFD1F0B86DD8F0F6407DB3DFC92656C3DFF48543FAB56EF740F66B672255B53B40EBDEF1DDD1E75BDD68DA2DAE1C6EC069F22554D34832C8A54AD09376351E66D3B57EE2B8CADD42A073C5D2CB1ABEFB4492923F910566705B7335A78796B4B8FAC06B799894B9A5813C4F33333C4FCAA66DB14E7A4C8287695&STBType=ZHAONENG_Z86&STBVersion=4.4.2-V1.0.0-20211223.2021v1&conntype=4&STBID=0010059905010860300074CF00828FE6&templateName=iptvsnmv3&areaId=&userToken=8C186D38D267A51B545034AA507C33B6&userGroupId=&productPackageId=&mac=74%3Acf%3A00%3A82%3A8f%3Ae6&UserField=&SoftwareVersion=4.4.2-V1.0.0-20211223.2021v1&IsSmartStb=0&desktopId=&stbmaker=&VIP=' \
    || { echo "Step 1 failed: Authentication request failed" >> "$LOG_FILE"; exit 1; }

# 第二步：执行第二个 curl 请求并将结果输出到文件
curl http://125.88.95.8:33200/EPG/jsp/getchannellistHWCTC.jsp \
    -b /path/to/iptv/DataDownload/cookie.txt \
    -o /path/to/iptv/DataDownload/res.html \
    || { echo "Step 2 failed: Channel list request failed" >> "$LOG_FILE"; exit 1; }

# 第三步：给获取到的res.html文件添加外部频道信息
python3 /path/to/iptv/py/1.py \
    || { echo "Step 3 failed: Python script 1.py execution failed" >> "$LOG_FILE"; exit 1; }

# 第四步：整理res.html文件频道信息
python3 /path/to/iptv/py/2.py \
    || { echo "Step 4 failed: Python script 2.py execution failed" >> "$LOG_FILE"; exit 1; }

# 第五步：精简第四步获取到的m3u文件
python3 /path/to/iptv/py/3.py \
    || { echo "Step 5 failed: Python script 3.py execution failed" >> "$LOG_FILE"; exit 1; }

# 第六步：提取第五步的m3u鉴权用户信息
python3 /path/to/iptv/py/4.py \
    || { echo "Step 6 failed: Python script 4.py execution failed" >> "$LOG_FILE"; exit 1; }

# 第七步：替换鉴权用户信息
python3 /path/to/iptv/py/5.py \
    || { echo "Step 7 failed: Python script 5.py execution failed" >> "$LOG_FILE"; exit 1; }