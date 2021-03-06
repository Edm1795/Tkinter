def itemNameFormatter(itemName):
    """This method formats the name of stock items so that new lines are added to the appropriate spots
        making the name fit properly to the labelWidth
        Inputs: itemName string from dictionary, note: also takes the value labelWidth from the parent function, drawCircle()
        Outputs: a string with '\n' added
        """

    string = ''
    cacheList = []
    listOfTerms = itemName.split()
    listToStr = ''
    for term in listOfTerms:
        if listOfTerms.index(term) == 0:  # Check if dealing with very first word in name of item
            if len(term) > labelWidth - 1:
                cacheList.append(string + term + '\n')  # If first word is too long add a newline and cache
            else:
                string = string + term  # If first word is not too long add word to string
        else:
            if len(string) + 1 + len(term) > labelWidth - 1:  # if dealing with second word or onwards
                cacheList.append(string + '\n')  # If next word creates too long of a sequence add newline without new word and cache
                string = term  # after caching put the new word into the string (otherwise that newword will get left out)
            else:
                if string == '':  # if string is empty add term without space
                    string = term
                else:
                    string = string + ' ' + term  # If new word will not create too long a sequence, add space and the new word
    cacheList.append(string)  # cache the string
    return listToStr.join(cacheList)  # converts elements from list to string form
