with open(r'dictionary.txt', 'r') as infile, \
     open(r'new_dict.txt', 'w') as outfile:
    data = infile.read()
    data = data.replace("qu", "$")
    data = data.replace("Qu", "$")
    outfile.write(data)