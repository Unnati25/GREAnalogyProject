import glob
import httplib, urllib, base64
import re
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
    testAnswerArray = []
    answerIntToString ={}
    answerIntToString[0] = ''
    answerIntToString[1] = 'a'
    answerIntToString[2] = 'b'
    answerIntToString[3] = 'c'
    answerIntToString[4] = 'd'
    answerIntToString[5] = 'e'
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
            line = line.strip()
            words = line.split(" ")
            targetWordIndex = 0
            for index in range(0,len(words)):
                if words[index].startswith('['):
                    targetWordIndex = index
            line = re.sub("[^A-Za-z ]", "",line)
            line = re.sub(",", "", line)
            words = line.split(" ")
            sentenceProbability = 0.0
            if targetWordIndex -1 > 0 and words[targetWordIndex] not in [60,000, 800, 1,200] and words[targetWordIndex-1] is not ',':

                if words[targetWordIndex-1] is '':
                    backwardBigram = words[targetWordIndex-2]
                    addTarget = words[targetWordIndex]
                else:
                    backwardBigram = words[targetWordIndex-1]
                    addTarget = words[targetWordIndex]
                if words[targetWordIndex] is '':
                    addTarget = words[targetWordIndex-1]

                try:
                    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
                    jsonString = {"queries": [{"words": backwardBigram, "word": addTarget}]}
                    conn.request("POST","/text/weblm/v1.0/calculateConditionalProbability?" + 'model=' + 'title' + "&order" + '2' + "%s+" % params,
                                 str(jsonString), headers)
                    response = conn.getresponse()
                    data = response.read()
                    response = json.loads(data)
                    probabilities = response['results']
                    sentenceProbability = sentenceProbability + math.pow(10,probabilities[0]['probability'])
                    conn.close()
                except Exception as e:
                    print("[Errno {0}] {1}".format(e.errno, e.strerror))
            if maxSentenceProbability < sentenceProbability:
                maxSentenceProbability = sentenceProbability
                maxAnswerNumber = answerNumber
            answerNumber = answerNumber + 1
        testAnswerArray.append(answerIntToString[maxAnswerNumber])
    testActualAnswerArray = []

    with open("C:/Users/Unnati/Documents/NLP/Project/data/Holmes.machine_format.answers.txt", "r") as file:
        for line in file:
            line = line[line.index(")") - 1:line.index(")")]
            testActualAnswerArray.append(line)

    testErrorCount = 0
    for i in range(0, len(testActualAnswerArray)):
        if testAnswerArray[i] is not testActualAnswerArray[i]:
            testErrorCount = testErrorCount + 1
    print(testErrorCount)
    print("Test Answer prediction Accuracy ")
    print((float)(len(testActualAnswerArray) - testErrorCount) * 100 / len(testAnswerArray))
    print("%")

def main():
    readFiles()
main()