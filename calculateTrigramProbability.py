
import pandas as pd
import csv
import re
def calulate():
    reader = csv.reader(open('trigramCount.csv'))

    result = {}
    for row in reader:
        key = row[0]
        if key in result:
            # implement your duplicate row handling here
            pass
        result[key] = row[1:]
    # #print result
    #
    # for trigram in result.keys():
    #     print(trigram)
    #     print(result[trigram][0])
 #
    bigramTotalWordCount = {}
    with open('unigramCount.csv', mode='r') as infile:
        reader = csv.reader(infile)
        myUnigramdict = dict((rows[0], rows[1]) for rows in reader)
        #print(myUnigramdict)
    with open('BigramCount.csv', mode='r') as infile:
        reader = csv.reader(infile)
        myBigramDict = dict((rows[0], rows[1]) for rows in reader)
        #print(mydict)

    #print(totalCount)
    uniqueWordCount = len(myUnigramdict)
    print(uniqueWordCount)
    # print(uniqueWordCount)
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
        maxSentenceProbability = 0.0
        global line, word
        for line in file:
            if answerNumber == 6:
                testAnswerArray.append(answerIntToString[maxAnswerNumber])
                answerNumber = 1
                maxSentenceProbability = 0.0
                maxAnswerNumber = 0
            line = line[line.index(')')+1:len(line)]
            line = re.sub("[^A-Za-z]"," ",line)
            line = re.sub("\s+"," ",line)
            line = line.strip()
            words = line.split(" ")
            sentenceProbability = 1.0
            previousWord = None
            #print(myUnigramdict)
            #print(myBigramDict)
            for word in words:
                #print(word)
                if previousWord is not None:
                    bigram = previousWord + " " + word
                    #print(bigram)
                    bigramProbability = 0.0
                    if previousWord in myUnigramdict:
                        if bigram in myBigramDict:
                            bigramProbability = (float)(int(myBigramDict[bigram][0]) + 1.0)/(int((myUnigramdict[previousWord][0])) + uniqueWordCount)
                        else:
                            bigramProbability = (float)(1.0/((int((myUnigramdict[previousWord][0]))) + uniqueWordCount))
                    else:
                        if bigram in bigramTotalWordCount:
                            bigramProbability = (float)((int(myBigramDict[bigram][0]) + 1.0))/uniqueWordCount
                        else:
                            bigramProbability = (float)(1.0/uniqueWordCount)
                    sentenceProbability = sentenceProbability * bigramProbability
                    #print(sentenceProbability)
                previousWord = word
                print(sentenceProbability)
            if maxSentenceProbability < sentenceProbability:
                maxSentenceProbability = sentenceProbability
                maxAnswerNumber = answerNumber
            answerNumber = answerNumber + 1
            #print(answerNumber)
        print("I am here****")
        testAnswerArray.append(answerIntToString[maxAnswerNumber])
        print(testAnswerArray)
    testActualAnswerArray = []
    with open("C:/Users/Unnati/Documents/NLP/Project/data/Holmes.machine_format.answers.txt", "r") as file:
        answerNumber = 1
        for line in file:
            line = line[line.index(")")-1:line.index(")")]
            testActualAnswerArray.append(line)

    testErrorCount = 0
    for i in range(0,len(testActualAnswerArray)):
        if testAnswerArray[i] is not testActualAnswerArray[i]:
            testErrorCount = testErrorCount + 1
    print (testErrorCount)
    print("Test Answer prediction Accuracy ")
    print(float)(len(testActualAnswerArray) - testErrorCount) * 100/ len(testAnswerArray)
    print("%")

def main():
    calulate()
main()