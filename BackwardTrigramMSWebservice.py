import glob
import httplib, urllib, base64
import re
import csv
import json, math

headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '4b60654ed7414d048450385230e94610',
}

params = urllib.urlencode({
    'model': 'title',
    'order': '2'
    })

path = "/Users/Unnati/Documents/NLP/Project/data/training_data/Holmes_Training_Data/"
global index

def readFiles():
    with open('trigramCount1.csv', mode='r') as infile:
        reader = csv.reader(infile)
        myTrigramDict = dict((rows[0], rows[1]) for rows in reader)
    with open('BigramCount.csv', mode='r') as infile:
        reader = csv.reader(infile)
        myBigramDict = dict((rows[0], rows[1]) for rows in reader)
    with open('unigramCount.csv', mode='r') as infile:
        reader = csv.reader(infile)
        myunigramDict = dict((rows[0], rows[1]) for rows in reader)
    testAnswerArray = []
    answerIntToString ={}
    answerIntToString[0] = ''
    answerIntToString[1] = 'a'
    answerIntToString[2] = 'b'
    answerIntToString[3] = 'c'
    answerIntToString[4] = 'd'
    answerIntToString[5] = 'e'
    count=1
    with open("C:/Users/Unnati/Documents/NLP/Project/data/Holmes.machine_format.questions.txt", "r") as file:
        answerNumber =1
        maxAnswerNumber =0
        maxSentenceProbability =0.0
        for line in file:
            if answerNumber == 6:
                testAnswerArray.append(answerIntToString[maxAnswerNumber])
                answerNumber = 1
                maxSentenceProbability = 0.0
                maxAnswerNumber = 0
            line = line[line.index(')')+1:len(line)]
            line = line.replace("[^A-Za-z\[\] ] ","")
            line = line.replace("\s+"," ")
            line = line.strip()
            words = line.split(" ")
            targetWordIndex = 0
            for index in range(0,len(words)):
                if words[index].startswith('['):
                    targetWordIndex = index
            line = re.sub("[^A-Za-z ]", "",line)
            line = re.sub(",", "", line)
            words = line.split(" ")
            backwardBigram = None
            backwardTrigram = None
            backwardFourgram = None
            #trigramProb = 0.0
            # if targetWordIndex -1 > 0 and  words[targetWordIndex] not in [60,000, 800, 1,200]  and words[targetWordIndex-1] is not ',':
            #
            #     if words[targetWordIndex-1] is '':
            #         backwardBigram = words[targetWordIndex-2]
            #         addTarget = words[targetWordIndex]
            #     else:
            #         backwardBigram = words[targetWordIndex-1]
            #         addTarget = words[targetWordIndex]
            #     if words[targetWordIndex] is '':
            #         addTarget = words[targetWordIndex-1]
            #
            #     try:
            #         conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
            #         jsonString = {"queries": [{"words": backwardBigram, "word": addTarget}]}
            #         #print(jsonString)
            #         # conn.request("POST", "/text/weblm/v1.0/calculateConditionalProbability?%s" % params,str(jsonq), headers)
            #         conn.request("POST","/text/weblm/v1.0/calculateConditionalProbability?" + 'model=' + 'title' + "&order" + '2' + "%s+" % params,
            #                      str(jsonString), headers)
            #         response = conn.getresponse()
            #         data = response.read()
            #         response = json.loads(data)
            #         probabilities = response['results']
            #         sentenceProbability = sentenceProbability +   math.pow(10,probabilities[0]['probability'])
            #         #print(sentenceProbability)
            #         conn.close()
            #     except Exception as e:
            #         print("[Errno {0}] {1}".format(e.errno, e.strerror))
            #
            # if targetWordIndex -2 > 0 and not words[targetWordIndex].isdigit() and words[targetWordIndex] not in [60,000, 800, 1,200]:
            #     if words[targetWordIndex-1] is '':
            #         backwardTrigram = words[targetWordIndex-2]
            #         addTarget = words[targetWordIndex]
            #     else:
            #         backwardTrigram = words[targetWordIndex-1]
            #         addTarget = words[targetWordIndex]
            #     if words[targetWordIndex-2] is '':
            #         backwardTrigram = backwardTrigram + " " + words[targetWordIndex-1]
            #     else:
            #         backwardTrigram = backwardTrigram + " " + words[targetWordIndex-2]
            #     if words[targetWordIndex] is '' and words[targetWordIndex-1] is not '':
            #         addTarget = words[targetWordIndex-1]
            #     else:
            #         if words[targetWordIndex] is '' and words[targetWordIndex-2] is not '':
            #             addTarget = words[targetWordIndex-2]
            #     #print (words)
                #print(backwardTrigram)
                #print (addTarget)
                #print('******************')

                #backwardTrigram = words[targetWordIndex-2] + " "+  words[targetWordIndex-1]
                #print(words[targetWordIndex])
                # try:
                #     conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
                #     jsonString = {"queries": [{"words": backwardTrigram, "word": addTarget}]}
                #      # conn.request("POST", "/text/weblm/v1.0/calculateConditionalProbability?%s" % params,str(jsonq), headers)
                #     conn.request("POST","/text/weblm/v1.0/calculateConditionalProbability?" + 'model=' + 'title' + "&order" + '3' + "%s+" % params,str(jsonString), headers)
                #     response = conn.getresponse()
                #     data = response.read()
                #     response = json.loads(data)
                #     probabilities = response['results']
                #     sentenceProbability = sentenceProbability + math.pow(10, probabilities[0]['probability']) * 3
                #     conn.close()
                # except Exception as e:
                #     print("[Errno {0}] {1}".format(e.errno, e.strerror))
            trigramProb = 0.0
            if targetWordIndex -2 > 0  and not words[targetWordIndex].isdigit() and words[targetWordIndex] is not ',':
                trigram = words[targetWordIndex-2] + " " + words[targetWordIndex-1] + " "+ words[targetWordIndex]
                bigram = words[targetWordIndex-1] + " " +  words[targetWordIndex]
                if trigram in myTrigramDict:
                    if bigram not in myBigramDict:
                        if words[targetWordIndex] not in myunigramDict:
                            trigramProb = 1.0
                        else:
                            trigramProb = float(int(myTrigramDict[trigram][0])/int(myunigramDict[words[targetWordIndex]]))
                    else:
                        trigramProb = float(int(myTrigramDict[trigram][0])/int(myBigramDict[bigram][0]))

                else:
                    if bigram not in myBigramDict:
                        if words[targetWordIndex] not in myunigramDict:
                            trigramProb = 1.0
                        else:
                            trigramProb = 1.0 / int(myunigramDict[words[targetWordIndex]])
                    else:
                        trigramProb = 1.0/int(myBigramDict[bigram][0])
            if maxSentenceProbability < trigramProb:
                maxSentenceProbability = trigramProb
                maxAnswerNumber = answerNumber
            answerNumber = answerNumber + 1
        testAnswerArray.append(answerIntToString[maxAnswerNumber])
    print("was here")
    testActualAnswerArray = []

    with open("C:/Users/Unnati/Documents/NLP/Project/data/Holmes.machine_format.answers.txt", "r") as file:
        for line in file:
            line = line[line.index(")") - 1:line.index(")")]
            testActualAnswerArray.append(line)

    testErrorCount = 0
    print(len(testAnswerArray))
    print(len(testActualAnswerArray))
    for i in range(0, len(testActualAnswerArray)-1):
        if testAnswerArray[i] is not testActualAnswerArray[i]:
            testErrorCount = testErrorCount + 1
    print(testErrorCount)
    print("Test Answer prediction Accuracy ")
    print(float)(len(testActualAnswerArray) - testErrorCount) * 100 / len(testAnswerArray)
    print("%")

def main():
    readFiles()


main()