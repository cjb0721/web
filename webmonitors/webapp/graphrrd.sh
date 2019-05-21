#!/bin/bash
rrdfile=$1
pngfile=$2
rrdtype=$3
appname=$4
GraphStart=$5
GraphEnd=$6
ymax=$7
Alarm=$8

rrdtool_font_msyhbd="/static/fonts/msyhbd.ttf"
rrdtool_font_msyh="/static/fonts/msyh.ttf"
export LANG=zh_CN.utf8
export LC_ALL=zh_CN.utf8
export LANG=zh_CN.utf8
export LANGUAGE=zh_CN.utf8
export LC_CTYPE=zh_CN.utf8
export LC_TIME=zh_CN.utf8

if [ "$rrdtype" == "time" ]; then
/usr/bin/rrdtool graph ${pngfile} -w 500 -h 207 \
-n TITLE:9:${rrdtool_font_msyhbd} \
-n UNIT:8:${rrdtool_font_msyh} \
-n LEGEND:8:${rrdtool_font_msyh} \
-n AXIS:8:${rrdtool_font_msyh} \
-c SHADEA#808080 \
-c SHADEB#808080 \
-c FRAME#006600 \
-c ARROW#FF0000 \
-c AXIS#000000 \
-c FONT#000000 \
-c CANVAS#eeffff \
-c BACK#ffffff \
--title "业务请求响应时间统计-${appname}" -v "速度 (秒)" \
--start ${GraphStart} \
 --end ${GraphEnd} \
--lower-limit=0 \
--base=1024 \
-u ${ymax} -r  \
DEF:dns_lookup_time=${rrdfile}:dns_lookup_time:AVERAGE \
DEF:connect_time=${rrdfile}:connect_time:AVERAGE \
DEF:pre_transfer_time=${rrdfile}:pre_transfer_time:AVERAGE \
DEF:start_transfer_time=${rrdfile}:start_transfer_time:AVERAGE \
DEF:total_time=${rrdfile}:total_time:AVERAGE \
COMMENT:" \n" \
AREA:total_time#0011ff:总共时间 \
GPRINT:total_time:LAST:"当前\:%0.2lf %Ss"  \
GPRINT:total_time:AVERAGE:"平均\:%0.2lf %Ss"  \
GPRINT:total_time:MAX:"最大\:%0.2lf %Ss"  \
GPRINT:total_time:MIN:"最小\:%0.2lf %Ss"  \
COMMENT:" \n" \
LINE1:dns_lookup_time#eeee00:域名解析 \
GPRINT:dns_lookup_time:LAST:"当前\:%0.2lf %Ss"  \
GPRINT:dns_lookup_time:AVERAGE:"平均\:%0.2lf %Ss"  \
GPRINT:dns_lookup_time:MAX:"最大\:%0.2lf %Ss"  \
GPRINT:dns_lookup_time:MIN:"最小\:%0.2lf %Ss"  \
COMMENT:" \n" \
LINE1:connect_time#00aa00:连接时间 \
GPRINT:connect_time:LAST:"当前\:%0.2lf %Ss"  \
GPRINT:connect_time:AVERAGE:"平均\:%0.2lf %Ss"  \
GPRINT:connect_time:MAX:"最大\:%0.2lf %Ss"  \
GPRINT:connect_time:MIN:"最小\:%0.2lf %Ss"  \
COMMENT:" \n" \
LINE1:pre_transfer_time#ff5511:开始传输 \
GPRINT:pre_transfer_time:LAST:"当前\:%0.2lf %Ss"  \
GPRINT:pre_transfer_time:AVERAGE:"平均\:%0.2lf %Ss"  \
GPRINT:pre_transfer_time:MAX:"最大\:%0.2lf %Ss"  \
GPRINT:pre_transfer_time:MIN:"最小\:%0.2lf %Ss"  \
COMMENT:" \n" \
LINE1:start_transfer_time#004455:第一字节 \
GPRINT:start_transfer_time:LAST:"当前\:%0.2lf %Ss"  \
GPRINT:start_transfer_time:AVERAGE:"平均\:%0.2lf %Ss"  \
GPRINT:start_transfer_time:MAX:"最大\:%0.2lf %Ss"  \
GPRINT:start_transfer_time:MIN:"最小\:%0.2lf %Ss"  \
COMMENT:" \n" \
HRULE:${Alarm}#ff0000:"(告警值)" \
COMMENT:" \n" \
COMMENT:" \n" \
COMMENT:"\t\t\t\t\t\t\t\t\t\t最后更新 \:$(date '+%Y-%m-%d %H\:%M')\n"

elif [ "$rrdtype" == "download" ]; then
/usr/bin/rrdtool graph ${pngfile} -w 320 -h 102 \
-n TITLE:9:${rrdtool_font_msyhbd} \
-n UNIT:8:${rrdtool_font_msyh} \
-n LEGEND:8:${rrdtool_font_msyh} \
-n AXIS:8:${rrdtool_font_msyh} \
-c SHADEA#808080 \
-c SHADEB#808080 \
-c FRAME#006600 \
-c ARROW#FF0000 \
-c AXIS#000000 \
-c CANVAS#eeffff \
-c BACK#ffffff \
-t "业务下载速度统计-${appname}" -v "速度 (字节/秒)" \
--start ${GraphStart} \
 --end ${GraphEnd} \
--lower-limit=0 \
--base=1024 \
-u ${ymax} -r  \
DEF:download_speed=${rrdfile}:download_speed:AVERAGE \
COMMENT:" \n" \
AREA:download_speed#68CEFF:下载速度 \
GPRINT:download_speed:AVERAGE:"平均\:%6.0lf%Sbyte"  \
GPRINT:download_speed:MAX:"最大\:%6.0lf%Sbyte"  \
GPRINT:download_speed:MIN:"最小\:%6.0lf%Sbyte"  \
COMMENT:" \n"

elif [ "$rrdtype" == "unavailable" ]; then
/usr/bin/rrdtool graph ${pngfile}  -w 320 -h 102 \
-n TITLE:9:${rrdtool_font_msyhbd} \
-n UNIT:8:${rrdtool_font_msyh} \
-n LEGEND:8:${rrdtool_font_msyh} \
-n AXIS:8:${rrdtool_font_msyh} \
-c SHADEA#808080 \
-c SHADEB#808080 \
-c FRAME#006600 \
-c ARROW#FF0000 \
-c AXIS#000000 \
-c CANVAS#eeffff \
-c BACK#ffffff \
-t "业务可用性统计-${appname}" -v "次数 (次)" \
--start ${GraphStart} \
 --end ${GraphEnd} \
--lower-limit=0 \
--base=1024 \
-u 1 -r  \
DEF:UNAVAILABLE=${rrdfile}:UNAVAILABLE:AVERAGE \
COMMENT:" \n" \
AREA:UNAVAILABLE#33ff00:服务不可用 \
GPRINT:UNAVAILABLE:AVERAGE:"平均\:%0.2lf"  \
GPRINT:UNAVAILABLE:MAX:"最大\:%0.2lf"  \
GPRINT:UNAVAILABLE:MIN:"最小\:%0.2lf"  \
COMMENT:" \n"
else
    echo "ERROR!"
fi