import csv
import os

# USAGE
# Run this command on the predictive tagging utility box:
# ./mlcmd system who_has_foreign_language_trainings
# Save file to MattersWithFL.txt
# Run ParseFLTrainings.py - it will populate PrecisionsText folder
# Run this script - it will populate ConfusionSource folder and then generate a report called report.csv

# REPORT INTERPRETATION
# For any matter with similar tags in more than one language that both have positive and negative signals above 1000,
# the report will include the differences between the recall and f-score (beta = 0.5) between tags across languages pairs.


class tagItem:
    def __init__(self):
        self.tag_id = 0
        self.tag_name = 0
        self.language = 0
        self.positive_signals = 0
        self.negative_signals = 0
        self.pos_precision = 0
        self.neg_precision = 0
        self.tp = 0
        self.fn = 0
        self.tn = 0
        self.fp = 0
        self.no_data = 0
        self.pos_recall = 0
        self.neg_recall = 0
        self.f_score = 0

def cleanPrecisionsText():
    for subdir, dirs, files in os.walk('PrecisionsText'):
        for file in files:
            if file != '.DS_Store':
                path = os.path.join(subdir, file)
                f = open(path, "r")
                contents = f.read()
                f.close()
                # contents="first line\nSignals are here\nwant this"
                #matches = re.match(r'tag_id([.\n]+)',contents,flags=re.MULTILINE)
                idx = contents.index('tag_id')
                print(contents[idx:])
                output = contents[idx:]
                # pattern = re.compile(r"\n(tag_id(.|\n)+)", re.MULTILINE)
                # matches = pattern.match(contents)
                if len(output)> 0:
                    # output = matches[2]
                    f2 = open('ConfusionSource/' + file + '.csv','w+')
                    f2.write(output)
                    f2.close()
                # print("bu")

def getConfusionData(fileName):

    tag_list = []
    beta = 0.5
    with open(fileName, newline='') as csvfile:
        csvReader = csv.DictReader(csvfile)
        for row in csvReader:
            myTagItem = tagItem()
            myTagItem.tag_id = row['tag_id']
            myTagItem.tag_name = row['tag_name']
            myTagItem.language = row['language']
            myTagItem.positive_signals = int(row['positive_signals'])
            myTagItem.negative_signals = int(row['negative_signals'])
            myTagItem.pos_precision = float(row['pos_precision'])
            myTagItem.neg_precision = float(row['neg_precision'])
            myTagItem.tp = int(row['tp'])
            myTagItem.fn = int(row['fn'])
            myTagItem.tn = int(row['tn'])
            myTagItem.fp = int(row['fp'])
            myTagItem.no_data = int(row['no_data'])

            if myTagItem.tp + myTagItem.fn != 0:
                myTagItem.pos_recall = myTagItem.tp / (myTagItem.tp + myTagItem.fn)
            else:
                myTagItem.pos_recall = 0

            if myTagItem.tn + myTagItem.fp != 0:
                myTagItem.neg_recall = myTagItem.tn / (myTagItem.tn + myTagItem.fp)
            else:
                myTagItem.neg_recall = 0

            denom = beta*beta * myTagItem.pos_precision + myTagItem.pos_recall

            if denom > 0:
                myTagItem.f_score = ((1+beta*beta)*(myTagItem.pos_precision*myTagItem.pos_recall)) / denom
            else:
                myTagItem.f_score = 0

            tag_list.append(myTagItem)
    return tag_list

def generateReport():
    output = []
    output.append(('file','tag','lang1','lang2','pos_recall_diff','pos_fscore_diff'))
    for subdir, dirs, files in os.walk('ConfusionSource'):
        for file in files:
            if file != '.DS_Store':
                path = os.path.join(subdir, file)
                print()
                # print(f'File: {file}')
                # print('Tag Name\t | Languages\t | Pos Recall Diff')
                tag_list = getConfusionData(path)
                index1 = 0
                indexMax = len(tag_list)-1
                while index1 <= indexMax - 1:
                    tag1 = tag_list[index1]
                    index2 = index1 + 1
                    while index2 <= indexMax:
                        tag2 = tag_list[index2]
                        if tag1.tag_name == tag2.tag_name and tag1.positive_signals > 999 and tag2.positive_signals > 999 and tag1.negative_signals > 999 and tag2.negative_signals > 999:
                            pos_recall_diff = abs(tag2.pos_recall - tag1.pos_recall)
                            pos_fscore_diff = abs(tag1.f_score - tag2.f_score)
                            output.append((file,tag1.tag_name,tag1.language,tag2.language,pos_recall_diff,pos_fscore_diff))
                            # print(f'| {tag1.tag_name}\t | {tag1.language} / {tag2.language}\t | {pos_recall_diff:.1%} | {pos_fscore_diff:.1%}')
                        index2 += 1
                    index1 += 1
    with open('report.csv','w',newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerows(output)

def main():
    # cleanPrecisionsText()
    generateReport()

main()