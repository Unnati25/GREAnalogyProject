import glob

path = "/Users/Unnati/Documents/NLP/Project/data/training_data/Holmes_Training_Data/"
global index

def readFiles():
    unigramCount = {}
    bigramTotalWordCount = {}
    for files in glob.glob(path + '*.txt'):
        with open(files, "r") as file:
            for line in file:
                previousWord = ""
                words = line.split()
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
    for element in bigramTotalWordCount.keys():
        if bigramTotalWordCount[element]>20:
            del bigramTotalWordCount[element]

    for bigramCount in bigramTotalWordCount.values():
        totalCount +=bigramCount
        uniqueWordCount = len(bigramTotalWordCount)
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
        global line
        for line in file:
            if answerNumber == 6:
                testAnswerArray.append(answerIntToString[maxAnswerNumber])
                answerNumber = 1
                maxSentenceProbability = 0.0
                maxAnswerNumber = 0
            line = line[line.index(')')+1:len(line)]
            line = line.replace("[^A-Za-z]"," ")
            line = line.replace("\s+"," ")
            line = line.strip()
            words = line.split(" ")
            sentenceProbability = 1.0
            previousWord = None
            for word in words:
                if previousWord is not None:
                    bigram = previousWord + " " + word
                    bigramProbability = 0.0
                    if previousWord in uniqueWordCount:
                        if bigram in bigramTotalWordCount:
                            bigramProbability = (float)(bigramTotalWordCount[bigram] + 1)/(uniqueWordCount[previousWord] + uniqueWordCount)
                        else:
                            bigramProbability = (float)(1/(uniqueWordCount[previousWord] + uniqueWordCount))
                else:
                    if bigram in bigramTotalWordCount:
                        bigramProbability = (float)(bigramTotalWordCount[bigram] + 1)/uniqueWordCount
                    else:
                        bigramProbability = (float)(1/uniqueWordCount)
                sentenceProbability = sentenceProbability * bigramProbability
            previousWord = word
            if maxSentenceProbability < sentenceProbability:
                maxSentenceProbability = sentenceProbability
                maxAnswerNumber = answerNumber
            answerNumber = answerNumber + 1
        testAnswerArray.append(answerIntToString[maxAnswerNumber])
    testActualAnswerArray = []
    with open("C:/Users/Unnati/Documents/NLP/Project/data/Holmes.machine_format.answers.txt", "r") as file:
        answerNumber = 1
        for line in file:
            maxSentenceProbability = 0.0
            line = line[line.index(")")-1:line.index(")")]
            testActualAnswerArray.append(line)

    testErrorCount = 0
    for i in range(0,len(testActualAnswerArray)):
        if testAnswerArray[i] is not testActualAnswerArray[i]:
            testErrorCount = testErrorCount + 1
    print("Test Answer prediction Accuracy ")
    print((float)(len(testActualAnswerArray) - testErrorCount) * 100/ len(testAnswerArray))
    print("%")

def main():
    readFiles()


main()