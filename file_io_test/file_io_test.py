

alphabet = "hello How are u? Hi jlksdhfslkj"
data = alphabet.split() #split string into a list

for temp in data:
    print temp
    write_string = temp + "\n"
    file = open("testfile.txt","a") 
    file.write(write_string)
file.close() 

