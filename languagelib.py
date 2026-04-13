import random, bisect, math

alphabet = []
for i in range(0,26):
    alphabet.append(chr(ord('a')+i))

sentencePunctuation = []
sentencePunctuation.append('.')
sentencePunctuation.append('!')
sentencePunctuation.append('?')

wordPunctuation = []
wordPunctuation.append(',')
wordPunctuation.append(':')
wordPunctuation.append(';')

vowels = []
vowels.append('a')
vowels.append('e')
vowels.append('i')
vowels.append('o')
vowels.append('u')
vowels.append('y')

def checkVowel(letter):
    """
    vowels = []
    vowels.append('a')
    vowels.append('e')
    vowels.append('i')
    vowels.append('o')
    vowels.append('u')
    vowels.append('y')
    """
    if (letter in vowels):
        return True
    return False

def countVowels(string):
    count = 0
    for letter in string:
        if (checkVowel(letter)):
            count += 1
    return count

def getHashRotate(x, y):
    return ((x<<y)|(x>>(32-y)))

def getHashMix(a, b, c):
    a -= c
    a ^= getHashRotate(c,4)
    c += b
    b -= a
    b ^= getHashRotate(a,6)
    a += c
    c -= b
    c ^= getHashRotate(b,8)
    b += a
    a -=c
    a ^= getHashRotate(c,16)
    c += b
    b -= a
    b ^= getHashRotate(a,19)
    a += c
    c -= b
    c ^= getHashRotate(b,4)
    b += a
    return [a,b,c]

def getHashMixFinal(a, b, c):
    c ^= b
    c -= getHashRotate(b,14)
    a ^= c
    a -= getHashRotate(c,11)
    b ^= a
    b -= getHashRotate(a,25)
    c ^= b
    c -= getHashRotate(b,16)
    a ^= c
    a -= getHashRotate(c,4)
    b ^= a
    b -= getHashRotate(a,14)
    c ^= b
    c -= getHashRotate(b,24)
    return c

def getStringHash(string):
    a = 0
    b = 0
    c = 0
    i = 0
    length = len(string)
    a = 0xdeadbeef+(length<<2)
    b = a
    c = a
    while (length > 3):
        a += ord(string[(i*3)+0])
        b += ord(string[(i*3)+1])
        c += ord(string[(i*3)+2])
        temp = getHashMix(a,b,c)
        a = temp[0]
        b = temp[1]
        c = temp[2]
        length -= 3
        i += 1
    if (length == 3):
        c += ord(string[2])
        length -= 1
    if (length == 2):
        b += ord(string[1])
        length -= 1
    if (length == 1):
        a += ord(string[0])
        c = getHashMixFinal(a,b,c)
    return c

def getLetterCode(letter):
    return ord(letter)-ord('a')

def getSubstring(string, start, end):
    result = ""
    if (start >= end):
        return result
    for i in range(int(start),int(end)):
        if ((i < 0) or (i >= len(string))):
            break
        result += str(string[i])
    return result

def getPrefix(string, end):
    return getSubstring(string,0,end)

def getSuffix(string, start):
    return getSubstring(string,start,len(string))

def insertSubstring(string, index, substring):
    return getPrefix(string,index)+substring+getSuffix(string,index+len(substring))

class Language:

    globalTranslationBank = None

    def initializeGlobalTranslationBank(self, directory):
        if (Language.globalTranslationBank == None):
            Language.globalTranslationBank = []
            data = open(directory+"letterchances.txt","r")
            lines = data.readlines()
            letterChances = []
            for i in range(0,26):
                letterChances.append([])
                for j in range(0,26):
                    letterChances[i].append(0.0)
            chanceTotal = 0.0
            chances = [-1,-1]
            check = False
            for line in lines:
                line = line.strip()
                if (line == "Chances:"):
                    check = True
                if (check):
                    if (line[len(line)-1] == ':'):
                        Language.globalTranslationBank.append({})
                        chances[1] += 1
                        chances[0] = 0
                        chanceTotal = 0.0
                    else:
                        if (chances[1] < 2):
                            chanceTotal += float(line)
                            if (chances[1] == 1):
                                Language.globalTranslationBank[chances[1]][chanceTotal] = vowels[chances[0]]
                            else:
                                Language.globalTranslationBank[chances[1]][chanceTotal] = alphabet[chances[0]]
                        else:
                            letterChances[chances[1]-2][chances[0]] = float(line)
                        chances[0] += 1
            for i in range(0,26):
                chanceTotal = 0.0
                for j in range(0,26):
                    chanceTotal += letterChances[i][j]
                    Language.globalTranslationBank[i+2][chanceTotal] = alphabet[j]
            for i in range(0,len(Language.globalTranslationBank)):
                temp = Language.globalTranslationBank[i]
                Language.globalTranslationBank[i] = [temp,sorted(list(temp.keys()),key=float)]
            data.close()

    def getFromGlobalTranslationBank(self, which, key, mode):
        if ((which < len(Language.globalTranslationBank)) and (which >= 0)):
            temp = Language.globalTranslationBank[which]
            keys = temp[1]
            index = -1
            if (mode):
                index = bisect.bisect_right(keys,key)
            else:
                index = bisect.bisect_left(keys,key)
            if ((index < len(keys)) and (index >= 0)):
                return temp[0][keys[index]]
        return " "

    def handleRandomState(self, mode):
        if not (self.randomMode == mode):
            self.randomStates[self.randomMode] = random.getstate()
            self.randomMode = mode
            randomState = self.randomStates[mode]
            if not (randomState == None):
                random.setstate(randomState)

    def getRandomInteger(self, mode, minimum, maximum):
        self.handleRandomState(mode)
        return random.randint(int(minimum),int(maximum))

    def getRandomFloat(self, mode, minimum, maximum):
        self.handleRandomState(mode)
        return random.uniform(float(minimum),float(maximum))

    def getShuffledLetters(self):
        letters = list(range(0,26))
        for i in range(25,-1,-1):
            index = self.getRandomInteger(0,0,i)
            temp = letters[index]
            letters[index] = letters[i]
            letters[i] = chr(ord('a')+temp)
        return letters

    def getShuffledString(self, string):
        if (len(string) < 2):
            return string
        for i in range(len(string)-1,-1,-1):
            index = self.getRandomInteger(1,0,i)
            temp = getSubstring(string,index,index+1)
            string = insertSubstring(string,index,getSubstring(string,i,i+1))
            string = insertSubstring(string,i,temp)
        return string

    def applyCipher(self, string):
        for i in range(0,len(string)):
            temp = getSubstring(string,i,i+1)
            string = insertSubstring(string,i,self.cipher[temp])
        return string

    def executeLetterCorrection(self, string, seed, consonants):
        check = False
        ranges = []
        for i in range(0,len(string)):
            temp = checkVowel(string[i])
            if (consonants):
                if (temp):
                    temp = False
                else:
                    temp = True
            if (temp):
                if (check):
                    ranges[len(ranges)-1][1] += 1
                    ranges[len(ranges)-1][2] += 1
                else:
                    ranges.append([i,1,i+1])
                    check = True
            else:
                check = False
        if not (len(ranges) == 0):
            for i in range(0,len(ranges)):
                current = ranges[i]
                if (current[1] > 1):
                    temp = seed^getStringHash(getSubstring(string,current[0],current[2]))
                    self.handleRandomState(2)
                    random.seed(temp)
                    temp = current[0]
                    if (current[1] == 2):
                        if (temp == 0):
                            string = insertSubstring(string,0,self.getFromGlobalTranslationBank(0,self.getRandomFloat(2,0.0,1.0),True))
                        else:
                            if (temp+1 == len(string)-1):
                                string = insertSubstring(string,temp+1,self.getFromGlobalTranslationBank(getLetterCode(string[temp])+2,self.getRandomFloat(2,0.0,1.0),True))
                    else:
                        for j in range(temp+1,temp+int(current[1]/2)+1):
                            if (j >= len(string)):
                                break
                            string = insertSubstring(string,j,self.getFromGlobalTranslationBank(getLetterCode(string[j-1])+2,self.getRandomFloat(2,0.0,1.0),True))
                        if (consonants):
                            consonants = False
                        else:
                            consonants = True
                        string = insertSubstring(string,temp,self.executeLetterCorrection(getSubstring(string,temp,current[2]),seed,consonants))
                        if (consonants):
                            consonants = False
                        else:
                            consonants = True
        return string

    def translateWord(self, word):
        if (word == None):
            return ""
        if (len(word) == 0):
            return ""
        word = word.lower()
        step = 0
        stepSize = 2
        stepSizeFactor = 2
        length = 0
        seed = getStringHash(self.applyCipher(word))^self.uid
        translation = ""
        stepString = ""
        self.handleRandomState(1)
        random.seed(seed)
        if (self.getRandomFloat(1,0.0,10.0) < math.pi):
            if (len(word) < 3):
                word += self.getShuffledString(word)
            else:
                while (2**step < len(word)):
                    step += 1
                step = (2**step)/2
                if (step > 1):
                    stepString = getPrefix(word,self.getRandomInteger(1,1,int(len(word)/step)))
                    word += self.getShuffledString(stepString)
                step = 0
        while not (len(word) == 0):
            if (stepSize >= len(word)):
                stepString = word
                word = ""
            else:
                stepString = getPrefix(word,stepSize)
                word = getSuffix(word,stepSize)
            seed = getStringHash(self.applyCipher(stepString))^self.uid
            self.handleRandomState(2)
            random.seed(seed)
            if (length == 0):
                length = self.getRandomInteger(2,1,max(len(word),2))
                length = (self.getRandomInteger(1,1,max(len(word),2))^length)|length
                length += self.getRandomInteger(2,0,2)
            seed = len(word)/stepSizeFactor
            if ((seed > 1) and (seed <= len(word))):
                stepSize = self.getRandomInteger(2,1,seed)
                stepSize = (self.getRandomInteger(1,1,seed)^stepSize)|stepSize
            else:
                stepSize = len(word)
            for i in range(0,len(stepString)):
                seed = len(self.translationBank[stepString[i]])
                if (seed == 0):
                    continue
                for j in range(0,seed):
                    if (self.getRandomFloat(2,0.0,1.0) <= 1.0/float(seed)):
                        stepString = insertSubstring(stepString,i,self.translationBank[stepString[i]][j])
                        break
            translation += stepString
            step += 1
            if (len(translation) >= length):
                break
        self.initializeGlobalTranslationBank(self.directory)
        seed = getHashMixFinal(getStringHash(self.applyCipher(translation)),step,self.uid)
        for i in range(0,12):
            if (i%4 == 0):
                word = self.executeLetterCorrection(translation,seed,False)
            else:
                word = self.executeLetterCorrection(translation,seed,True)
            if not (i%2 == 0):
                if (word == translation):
                    break
            translation = word
        if (countVowels(translation) == 0):
            translation = insertSubstring(translation,len(translation)/2,self.getFromGlobalTranslationBank(1,self.getRandomFloat(1,0.0,1.0),True))
        return translation

    def translateSentence(self, sentence):
        if (sentence == None):
            return ""
        if (len(sentence) == 0):
            return ""
        translation = ""
        index = 0
        while (index < len(sentence)):
            if not (str(sentence[index]).isalpha()):
                if not (sentence[index] == ' '):
                    if ((not sentence[index] in sentencePunctuation) and (not sentence[index] in wordPunctuation)):
                        sentence = getPrefix(sentence,index)+getSuffix(sentence,index+1)
                        continue
            index += 1
        words = sentence.split(" ")
        if (len(words) == 0):
            return translation
        wordLast = words[len(words)-1]
        translationSentencePunctuation = ""
        if (wordLast[len(wordLast)-1] in sentencePunctuation):
            translationSentencePunctuation = str(wordLast[len(wordLast)-1])
        for i in range(0,len(words)):
            index = 0
            word = words[i]
            translationWordPunctuation = ""
            while (index < len(word)):
                if not (str(word[index]).isalpha()):
                    if (index == len(word)-1):
                        if ((word[index] in wordPunctuation) or (word[index] in sentencePunctuation)):
                            translationWordPunctuation = str(word[index])
                    word = getPrefix(word,index)+getSuffix(word,index+1)
                    continue
                index += 1
            translation += self.translateWord(word)
            if not (i == len(words)-1):
                translation += translationWordPunctuation
                translation += " "
        translation += translationSentencePunctuation
        return translation.capitalize()

    def __init__(self, uid, directory):
        self.uid = uid
        self.directory = directory
        self.randomMode = True
        self.randomStates = [None,None,None]
        self.cipher = {}
        self.translationBank = {}
        self.handleRandomState(0)
        random.seed(self.uid)
        letters = self.getShuffledLetters()
        for i in range(0,26):
            self.cipher[alphabet[i]] = letters[i]
        self.initializeGlobalTranslationBank(self.directory)
        total = 0
        chance = self.getRandomFloat(0,0.1,0.9)
        for i in range(0,26):
            letters = []
            if (self.getRandomFloat(0,0.0,1.0) <= chance):
                while (True):
                    if (self.getRandomFloat(0,0.0,1.0) > 1.0/float(len(letters)+1)):
                        break
                    letters.append(self.getFromGlobalTranslationBank(2,self.getRandomFloat(0,0.0,1.0),True))
            total += len(letters)
            if not (total == 0):
                if (self.getRandomFloat(0,0.0,1.0) < float(len(letters))/float(total)):
                    chance *= self.getRandomFloat(0,chance,1.0)
                else:
                    chance /= self.getRandomFloat(0,chance,1.0)
            self.translationBank[alphabet[i]] = letters
