import glob
import re

path = "/Users/Unnati/Documents/NLP/Project/data/training_data/Holmes_Training_Data/"
global index

def readFiles():
    unigramCount = {}
    bigramTotalWordCount = {}
    for files in glob.glob(path + '*.txt'):
        with open(files, "r") as file:
            for line in file:
                previousWord = ""
                line = re.sub("[^A-Za-z\[\] ] ", "", line)
                line = re.sub("\s+", " ", line)
                words = line.split(" ")
                for word in words:
                    if word in unigramCount:
                        unigramCount[word] += 1
                    else:
                        unigramCount[word] = 1
                    if previousWord is not None:
                        bigram = previousWord + " " + word
                        if bigram in bigramTotalWordCount:
                            bigramTotalWordCount[bigram] += 1
                        else:
                            bigramTotalWordCount[bigram] = 1
                    previousWord = word

    totalCount = 0;

    for bigramCount in bigramTotalWordCount.values():
        totalCount +=bigramCount
    uniqueWordCount = len(unigramCount)
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
            line = re.sub("[^A-Za-z\[\] ] ","", line)
            line = re.sub("\s+"," ",line)
            line = line.strip()
            words = line.split(" ")
            targetWordIndex = 0
            for index in range(0,len(words)):
                if words[index].startswith('['):
                    targetWordIndex = index
            line = re.sub("[^A-Za-z ]", "",line)
            sentenceProbability = 1.0
            words = line.split(" ")

            backwardBigram = None
            if targetWordIndex > 0 :
                backwardBigram = words[targetWordIndex - 1] + " " + words[targetWordIndex]

            forwardBigram = None
            if targetWordIndex < len(words)-1:
                forwardBigram = words[targetWordIndex] + " " + words[targetWordIndex + 1]

            backwardbigramProbability = 0.0
            forwardBigramProbability = 0.0
            if targetWordIndex > 0 and words[targetWordIndex -1] is not None:
                if (words[targetWordIndex-1] in unigramCount) and (backwardBigram is not None):
                    if backwardBigram in bigramTotalWordCount:
                        backwardbigramProbability = (float)(bigramTotalWordCount[backwardBigram]+ 1)/((unigramCount[words[targetWordIndex-1]])+ uniqueWordCount)
                    else:
                        backwardbigramProbability = (float)(1.0/(unigramCount[words[targetWordIndex - 1]])) + uniqueWordCount
                else:
                    if backwardBigram in bigramTotalWordCount:
                        backwardbigramProbability = (float)(bigramTotalWordCount[backwardBigram] +1)/uniqueWordCount

                    else:
                        backwardbigramProbability = (float)(1.0/uniqueWordCount)
            if targetWordIndex < len(words) - 1 and words[targetWordIndex + 1] in unigramCount and forwardBigram is not None:
                if forwardBigram in bigramTotalWordCount:
                    forwardBigramProbability = (float)(bigramTotalWordCount[forwardBigram] + 1)/((unigramCount[words[targetWordIndex + 1]])+ uniqueWordCount)
                else:
                    forwardBigramProbability = (float)(1.0/((unigramCount[words[targetWordIndex + 1]])) + uniqueWordCount)
            else:
                if forwardBigram in bigramTotalWordCount:
                    forwardBigramProbability = (float)(bigramTotalWordCount[forwardBigram] +1)/uniqueWordCount
                else:
                    forwardBigramProbability = (float)(1.0/uniqueWordCount)
            sentenceProbability = (backwardbigramProbability + forwardBigramProbability)
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