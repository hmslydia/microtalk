f = open('toChris.nyt.0d.typed.data.wr.txt')
lines = f.readlines()
f.close()





def eltsOfLine(line):
    lineParts = line.strip().split("\t")
    mentionStart = int(lineParts[0])
    mentionEnd = int(lineParts[1])
    sentence = lineParts[2]
    task = {"mentionStart": mentionStart, "mentionEnd": mentionEnd, "sentence": sentence}
    
    
    answers = []
    
    answer1 = lineParts[3]
    answer2 = lineParts[4]
    answers.append({"answer": answer1})
    answers.append({"answer": answer2})
    
    obj = {"task": task, "turkResponse": {"answers": answers}}
    return obj


jsonArray = [eltsOfLine(lines[i]) for i in range(len(lines)) if i % 3 == 0]

print jsonArray[:2]

import json
with open('data.txt', 'w') as outfile:
  json.dump(jsonArray[:50], outfile)