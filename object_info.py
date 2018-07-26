# function to extract basic information on observed objects:
import os

def object_info(par):
    dirList = os.listdir('.')
    for i in range(len(dirList)):
        print dirList[i]


    return
