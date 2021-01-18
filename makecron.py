import os
import requests
from string import Template

crontab_URL = "https://github.com/VidocqH/jd_scripts/raw/master/docker/crontab_list.sh"
r = requests.get(crontab_URL)
rarr = r.text.splitlines()

res = []
count = 0
for i in rarr[5:]:
    # 无用行
    if "#短期活动#" in i or "#长期活动#" in i:
        continue
    # 处理>>符号
    idx = i.find(">")
    if idx == -1:
        idx = len(i)
    i = i[:idx]
    if "node" in i:
        # crontab行
        i = i.rstrip()
        iarr = i.split(" ")
        # 0-4元素为cron
        # 5-6元素为脚本执行命令
        cron = ' '.join(iarr[:5])
        comm = ' '.join(iarr[5:])
        res[count].append(cron)
        res[count].append(comm)
        count += 1
    else:
        # action名字行
        name = i[1:].strip()
        res.append([name])

# convert array to dict
crondic = []
for i in res:
    if i[0] == "签到": # 懒得处理的特别情况
        crondic.append({
            'nameCN': i[0],
            'nameEN': 'bean_sign',
            'cron': i[1],
            'comm': 'node jd_bean_sign.js',
            'filename': 'jd_bean_sign'
        })
    else:
        crondic.append({
            'nameCN': i[0],
            'nameEN': i[2][i[2].rfind('/')+4:len(i[2])-3],
            'cron': i[1],
            'comm': 'node ' + i[2][i[2].rfind('/')+1:], # node xxx.js
            'filename': i[2][i[2].rfind('/')+1:len(i[2])-3] # 无拓展名的文件名
        })

with open('./template.txt', 'r') as f:
    template = Template(f.read())

for i in crondic:
    ymlPath = './.github/workflows/' + i['filename'] + '.yml'
    with open(ymlPath, 'w') as f:
        f.write(template.safe_substitute(i))
