def replace_num(initial, new_num):   #Call this function to replace data in '.txt' file
    newline=""
    str_num=str(new_num)
    with open("IP.txt","r") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                line = initial+"%s" %(str_num)
            newline += line
    with open("IP.txt", "w") as f:
        f.writelines(newline)    #Call this function to replace data in '.txt' file


def num_import(initial):            #Call this function to import data from '.txt' file
    with open("IP.txt") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                r=line
    begin=len(list(initial))
    snum=r[begin:]
    n=snum
    return n    
