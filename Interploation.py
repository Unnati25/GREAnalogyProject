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
    with open('FOurgramCount.csv', mode='r') as infile:
        reader = csv.reader(infile)
        myFourGramDict = dict((rows[0], rows[1]) for rows in reader)

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
            fourgramProb = 0.0
            if targetWordIndex - 3 > 0 and not words[targetWordIndex].isdigit() and words[targetWordIndex] is not ',':
                fourgram = words[targetWordIndex - 3] + " " + words[targetWordIndex - 2] + " " + words[
                    targetWordIndex - 1] + " " + words[targetWordIndex]
                trigram = words[targetWordIndex - 2] + " " + words[targetWordIndex - 1] + " " + words[targetWordIndex]
                bigram = words[targetWordIndex - 1] + " " + words[targetWordIndex]
                if fourgram in myFourGramDict:
                    if trigram not in myTrigramDict:
                        if bigram not in myBigramDict:
                            fourgramProb = float(
                                int(myFourGramDict[fourgram][0]) / int(myunigramDict[words[targetWordIndex]]))
                        else:
                            fourgramProb = float(int(myFourGramDict[fourgram][0]) / int(myBigramDict[bigram]))
                    else:
                        fourgramProb = float(int(myFourGramDict[fourgram][0]) / int(myTrigramDict[trigram][0]))

                else:
                    if trigram not in myTrigramDict:
                        if bigram not in myBigramDict:
                            fourgramProb = 1.0
                        else:
                            fourgramProb = 1.0 / int(myBigramDict[bigram])
                    else:
                        fourgramProb = 1.0 / int(myTrigramDict[trigram][0])
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
            bigramProb = 0.0
            if targetWordIndex -1 > 0  and not words[targetWordIndex].isdigit() and words[targetWordIndex] is not ',':
                bigram = words[targetWordIndex-1] + " " +  words[targetWordIndex]
                if bigram in myBigramDict:
                    if words[targetWordIndex] not in myunigramDict:
                        bigramProb = 1.0
                    else:
                        bigramProb = float(int(myBigramDict[bigram][0])/int(myunigramDict[words[targetWordIndex]]))
                else:
                    if words[targetWordIndex] not in myunigramDict:
                        bigramProb = 1.0
                    else:
                        bigramProb = float(1.0/int(myunigramDict[words[targetWordIndex]]))
            if maxSentenceProbability < trigramProb + fourgramProb + bigramProb:
                maxSentenceProbability = trigramProb + fourgramProb + bigramProb
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