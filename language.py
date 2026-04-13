import languagelib, sys, os
if (len(sys.argv) < 3):
    sys.exit()
languageName = sys.argv[1]
sentence = " ".join(sys.argv[2:]).strip()
directory = os.getcwd().replace("\\","/")
if (len(directory) == 0):
    directory += "/"
if not (directory[len(directory)-1:] == "/"):
    directory += "/"
directory += "data/"
languageInstance = languagelib.Language(hash(str(languageName)),directory)
print(str(languageInstance.translateSentence(str(sentence))))
