import os
import re

# See instructions in ParseConfusionData.py file

def getMatterID(fileName):
    f = open(fileName, "r")
    contents = f.read()
    f.close()
    ids = re.findall(r'\[(.*?)\]', contents)
    return ids

def queryMetrics(matterIDs):
    for id in matterIDs:
        print(f'ID: {id}')
        os.system('ssh -i  ~/.ssh/janus.pem ubuntu@10.20.8.222 "(cd ~/src/predictive-tagging;./mlcmd tags dump_tag_precisions -m ' + id + ')" | tee PrecisionsText/metrics_' + id + '.txt')

def main():
    matterIDs = getMatterID('MattersWithFL.txt')
    queryMetrics(matterIDs)

main()