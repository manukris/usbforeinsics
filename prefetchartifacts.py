# class PreFetchArtifacts:
#
#     def __init__(self):
#

# import admin
# if not admin.isUserAdmin():
#         admin.runAsAdmin()
import os
import subprocess
import  re


def getPrefetchFile(device=""):

    directory = "C:\\Windows\\Prefetch\\"
    count = 0


    print(os.path.getmtime(directory+"\\RUFUS-3.10.EXE-2AC46945.pf"))





def getPrefetchDetails(filelist):


    prefetchappdetails = []
    for file in filelist:

                print(file)
                out = subprocess.run(['PECmd.exe', '-f', 'C:\\Windows\\Prefetch\\'+file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                result = out.stdout.decode('utf-8')
                result = result[ : 1100]
                print(result)
                prefetchappdetails.append(result)
    print(len(prefetchappdetails))
    return (formatPrefetchDetails(prefetchappdetails))



def formatPrefetchDetails(prefetchappdetails):
    formatPrefetchDetails = []
    for details in prefetchappdetails:
        startindex = details.find("Created on:")
        stopindex  = details.find("Directories referenced:")
        details = details[startindex : stopindex + 1 ]
        details = details.replace("\n","<br>")
        details = details.replace("\r", "<br>")
        formatPrefetchDetails.append(details)

    return(formatPrefetchDetails)




if __name__ == "__main__":
    # getPrefetchDetails(5)
    getPrefetchFile()
             # exedetail = re.search(r"\#\\DEVICE\\HARDDISKVOLUME2\\\$EXTEND",result)
#             if "#\DEVICE\HARDDISKVOLUME2\$EXTEND" in result:
#               print("found")


# file = open("jsonfiles\\20200427080655_PECmd_Output.json","rt")
# filestring = file.read()
# print(filestring)

            #out = os.system("PECmd.exe -f C:\\Windows\\Prefetch\\"+file+" ")
# out = subprocess.run(['PECmd.exe', '-f', 'C:\\Windows\\Prefetch\\RUFUS-3.10.EXE-1F1A0C7C.pf'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# result = out.stdout.decode('utf-8')
# print(result)
#
# if "#\DEVICE\HARDDISKVOLUME2\$EXTEND" in result:
#         print("found")