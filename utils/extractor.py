def extractActiveStatus(response):
    lines = response.split('\n')
    
    for line in lines:
        field = line.strip()

        words = field.split(" ")
        if(words[0]=="Active:"):
            #print(words)
            status = words[1]
            substatus = words[2]

            return words[1] + words[2]