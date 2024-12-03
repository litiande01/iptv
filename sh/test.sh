#!/bin/bash

# 第一步：执行认证请求，保存cookie
curl http://125.88.95.8:33200/EPG/jsp/ValidAuthenticationHWCTC.jsp -c /path/to/iptv/DataDownload/cookie.txt -H 'Content-Type: application/x-www-form-urlencoded' --data 'UserID=07620668267&Lang=&SupportHD=1&NetUserID=hy8362249%40iptv.gd&DHCPUserID=hy8362249%40iptv.gd&Authenticator=F60690DFFD7E6AFD1F0B86DD8F0F6407DB3DFC92656C3DFF48543FAB56EF740F66B672255B53B40EBDEF1DDD1E75BDD68DA2DAE1C6EC069F22554D34832C8A54AD09376351E66D3B57EE2B8CADD42A073C5D2CB1ABEFB4492923F910566705B7335A78796B4B8FAC06B799894B9A5813C4F33333C4FCAA66DB14E7A4C8287695&STBType=ZHAONENG_Z86&STBVersion=4.4.2-V1.0.0-20211223.2021v1&conntype=4&STBID=0010059905010860300074CF00828FE6&templateName=iptvsnmv3&areaId=&userToken=8C186D38D267A51B545034AA507C33B6&userGroupId=&productPackageId=&mac=74%3Acf%3A00%3A82%3A8f%3Ae6&UserField=&SoftwareVersion=4.4.2-V1.0.0-20211223.2021v1&IsSmartStb=0&desktopId=&stbmaker=&VIP='

# 等待20秒
sleep 20

# 第二步：使用cookie获取频道列表，保存到res.html
curl http://125.88.95.8:33200/EPG/jsp/getchannellistHWCTC.jsp -b /path/to/iptv/DataDownload/cookie.txt -o /path/to/iptv/DataDownload/res.html

# 等待60秒
sleep 60

# 执行Python脚本
python3 /path/to/iptv/py/iptv.py