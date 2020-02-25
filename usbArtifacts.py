import winreg


class UsbArtifacts:

    def __init__(self):
        self.access_registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        self.allUsbDeviceList = []

    def getAllConnectedDeviceDetails(self):
        access_key = winreg.OpenKey(self.access_registry, r"SYSTEM\CurrentControlSet\Enum\USBSTOR")
        # accessing the key to open the registry directories under
        info = winreg.QueryInfoKey(access_key)
        length = info[0]
        for n in range(length):
            try:
                x = winreg.EnumKey(access_key, n)
                accesssubkey = winreg.OpenKey(access_key, r'{}'.format(x))
                subkey = winreg.EnumKey(accesssubkey, 0)
                devicedict = dict()
                devicedict['id'] = subkey
                devicedict['deviceString'] = x

                self.allUsbDeviceList.append(devicedict)
            except Exception as e:
                print(e)


        self._getDataFromDeviceString()

        print(self.allUsbDeviceList)
        return self.allUsbDeviceList

    def _getDataFromDeviceString(self):

        for device in self.allUsbDeviceList:
            deviceStringarray = device['deviceString'].split("&")
            device['type'] = deviceStringarray[0]
            device['vendor'] = deviceStringarray[1][4:]
            device['productname'] = deviceStringarray[2][5:]
            device['serialno'] = deviceStringarray[3][4:]
        #
        # print(self.allUsbDeviceList)











if __name__ == "__main__":
    usbartifacts = UsbArtifacts()
    usbartifacts.getAllConnectedDeviceDetails()
