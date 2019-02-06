def exportConfig(ItemName, Value):   # Call this function to export item to 'config.txt' file
    ItemName += ":"
    newlines = ""
    found = False
    with open("config.txt", "r") as f:
        for line in f.readlines():
            if (line.find(ItemName) == 0):
                # replace existing item value with new one
                line = ItemName + str(Value)
            newlines += line
    if not found:
        return False
    with open("config.txt", "w") as f:
        f.writelines(newlines)
    return True


def importConfig(ItemName):          # Call this function to import item from 'config.txt' file
    ItemName += ":"
    item = None
    with open("config.txt") as f:
        for line in f.readlines():
            if(line.find(ItemName) == 0):
                item = line
                break
    if item == None:
        # item not found
        return None
    lenItemName = len(ItemName)
    value = line[lenItemName:]
    #print(str(lenItemName) + " " + value)
    return value

def importConfigInt(ItemName):
    value = importConfig(ItemName)
    if value == None:
        return None
    return int(value)
