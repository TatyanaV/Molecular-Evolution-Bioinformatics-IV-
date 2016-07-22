with open("pedigree1a.txt", "r") as filestream:
    _unused = filestream.next()
    with open("pedigree1Parsed.txt", "w") as filestreamtwo:
        for line in filestream:
            split_characters = line[1:].split(' ')
            check_females = int(split_characters [7]);
            check_relationship0 = str(split_characters [1]);
            check_relationship = str(split_characters [2]);
            check_relationship1 = str(split_characters [3]);
            check_relationship2 = str(split_characters [9]);
            check_relationship3 = str(split_characters [10]);
            line = line.replace(' ', ',')
            line = line.replace('\n','')
            if check_females == 1:
              line = "femaleArray.push(new Females2(" + line + "))" + ";" + "\n"

            else:
              line = "malesArray.push(new Males2(" + line + "))" + ";" + "\n"
            line2 = "arrayRelationship.push(new Relationship2(" + str(check_relationship0) +','+ str(check_relationship) +','+ str(check_relationship1) + ',' + str(check_relationship2) + ','+ str(check_relationship3) + "))"+ ";" + "\n"
            #currentline = line.split(",")
            #total = str(int(currentline[0]) + int(currentline[1]) + int(currentline [2])) + "\n"
            filestreamtwo.write(line)
            filestreamtwo.write(line2)			

