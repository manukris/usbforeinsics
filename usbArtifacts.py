import winreg
import datetime
import re
import os

class UsbArtifacts:

    def __init__(self):
        #for local machine - none remote - PC name
        self.access_registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        self.allUsbDeviceList = []
        file = open('C:\\Windows\\inf\\setupapi.dev.log', "rt")
        self.filestring = file.read()



    def getAllConnectedDeviceDetails(self):

        access_key = winreg.OpenKey(self.access_registry, r"SYSTEM\CurrentControlSet\Enum\USBSTOR")
        # accessing the key to open the registry directories under
        info = winreg.QueryInfoKey(access_key)
        # print(info)
        length = info[0]
        for n in range(length):
            try:
                x = winreg.EnumKey(access_key, n)

                accesssubkey = winreg.OpenKey(access_key, r'{}'.format(x))
                subkey = winreg.EnumKey(accesssubkey, 0)
                devicedict = dict()
                devicedict['id'] = subkey
                devicedict['deviceString'] = x

                if subkey == "0000" or subkey.endswith("0000&0"):
                    continue
                if devicedict['deviceString'].startswith("CdRom"):
                    continue
                print(devicedict)
                # print(x)

#HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Enum\USBSTOR\Disk&Ven_TOSHIBA&Prod_TransMemory&Rev_1.00\54B80A3F9376C110A0021C16&0\Properties\{83da6326-97a6-4088-9453-a1923f573b29}\0064
                try:
                    usbkey1 = winreg.OpenKey(accesssubkey, subkey + r'\Properties\{83da6326-97a6-4088-9453-a1923f573b29}\0064')

                    firsttime = winreg.QueryInfoKey(usbkey1)

                    usbkey2 = winreg.OpenKey(accesssubkey,
                                             subkey + r'\Properties\{83da6326-97a6-4088-9453-a1923f573b29}\0066')

                    lastcontime = winreg.QueryInfoKey(usbkey2)

                    usbkey3 = winreg.OpenKey(accesssubkey,
                                             subkey + r'\Properties\{83da6326-97a6-4088-9453-a1923f573b29}\0067')
                except Exception as e :
                    # continue
                    print("No permission")
                    print(e)

                else:

                    lastremtime = winreg.QueryInfoKey(usbkey3)
                    print(firsttime,lastcontime,lastremtime)
                    devicedict['ftime'] = self.convertToUnixTimeStamp(firsttime[2])
                    devicedict['lastcontime'] = self.convertToUnixTimeStamp(lastcontime[2])
                    devicedict['lastremtime'] = self.convertToUnixTimeStamp(lastremtime[2])


                # usbdetails = winreg.(accesssubkey)

                # print(usbdetails)

                self.allUsbDeviceList.append(devicedict)
            except Exception as e:
                print(e)


        self._getDataFromDeviceString()
        self.getPrefetchApps()
        print(self.allUsbDeviceList)
        return self.allUsbDeviceList

    def convertToUnixTimeStamp(self,filetime):
        # filetime = filetime + (10000000 * 19800)
        unixtimestamp = (filetime // 10000000 ) - 11644473600
        return unixtimestamp



    def _getDataFromDeviceString(self):

        for device in self.allUsbDeviceList:
            deviceStringarray = device['deviceString'].split("&")

            device['type'] = deviceStringarray[0]
            device['vendor'] = deviceStringarray[1][4:]
            device['productname'] = deviceStringarray[2][5:]
            device['serialno'] = deviceStringarray[3][4:]
            # device['id']      = device['id'][:-2]
            device['application executed'] = deviceStringarray[2][6:]
            # device['time'] = self.getConnectTime(device['id'])

        # print(self.allUsbDeviceList)
    def getPrefetchApps(self):
        for device in self.allUsbDeviceList:
            contime = device['lastcontime']
            remtime = device['lastremtime']

            applist = self.selectPrefetchFiles(contime,remtime)
            device['applist'] = applist

    def selectPrefetchFiles(self,start,end):
        directory = "C:\\Windows\\Prefetch\\"
        count = 0
        dirs = os.listdir(directory)
        applist = []
        for file in dirs:
            if file.endswith(".pf") and  ".EXE" in file:


                if "SEARCHFILTERHOST.EXE" in file:
                    continue

                if "SEARCHPROTOCOLHOST.EXE" in file:
                    continue

                if "SVCHOST.EXE" in file:
                    continue




                if "SMARTSCREEN.EXE" in file:
                    continue

                if "TASKHOSTW.EXE" in file:
                    continue

                if "WMIPRVSE.EXE" in file:
                    continue

                if "WUDFHOST.EXE" in file:
                    continue

                if "DLLHOST.EXE" in file:
                    continue

                if "TASKHOST.EXE" in file:
                    continue

                if "CMD.EXE" in file:
                    continue

                if "PECMD.EXE" in file:
                    continue

                if "PYTHON.EXE" in file:
                    continue

                filetime = int(os.path.getmtime(directory + '\\' + file))
                if filetime > start and filetime < end:
                    print(file)
                    applist.append(file)
        return applist



    # def getConnectTime(self,deviceID):
    #     print(deviceID)
    #     pattern = r'\[Device Install.*' + deviceID + '.*\]\n>>>  Section start (.*)'
    #     # print(pattern)
    #     try:
    #         output = re.search(pattern, self.filestring)
    #         print(output.group(1))
    #         return output.group(1)
    #     except:
    #         return "null"


#C:\Windows\inf\
if __name__ == "__main__":
    usbartifacts = UsbArtifacts()
    usbartifacts.getAllConnectedDeviceDetails()



#1589089381.188962