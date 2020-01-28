

alphabet = "a b c d e f g"
data = alphabet.split() #split string into a list

for temp in data:
    print temp
    file = open("testfile.txt","a") 
    file.write(temp)
file.close() 

