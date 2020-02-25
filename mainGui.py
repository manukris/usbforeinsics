import wx

from usbArtifacts import UsbArtifacts

####
class MainWindow(wx.Frame):

    def __init__(self, parent, title ):
        super().__init__(parent, title=title, size=(1200, 600))

        self.Centre()
        self.GUI()
        self.Show()

    def GUI(self):
        menubar = wx.MenuBar()

        #File
        fileMenu1 = wx.Menu()

        fileItem1 = fileMenu1.Append(wx.ID_ADD, 'Run', 'Run application')
        fileItem2 = fileMenu1.Append(wx.ID_SAVE, 'Save', 'Save Artifacts')
        fileItem3 = fileMenu1.Append(wx.ID_EXIT, 'Quit', 'Quit application')

        #Edit
        fileMenu2 = wx.Menu()

        #
        #
        #
        #

        #View
        fileMenu3 = wx.Menu()
        #
        #
        #
        #

        #Options
        fileMenu4 = wx.Menu()
        #
        #
        #
        #

        #Help
        fileMenu5 = wx.Menu()
        #
        #
        #
        #

        menubar.Append(fileMenu1, '&File')
        menubar.Append(fileMenu2, '&Edit')
        menubar.Append(fileMenu3, '&View')
        menubar.Append(fileMenu4, '&Options')
        menubar.Append(fileMenu5, '&Help')

        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnQuit, fileItem3)

        self.Bind(wx.EVT_MENU, self.OnScan, fileItem1)

        self.body()


    def body(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        panel = wx.Panel(self)

        self.list = wx.ListCtrl(panel, wx.ID_ANY, style=wx.LC_REPORT|wx.LC_HRULES,size=(1200,400))
        self.list.InsertColumn(0, 'No',  wx.LIST_FORMAT_RIGHT,width=140)
        self.list.InsertColumn(1, 'Name', wx.LIST_FORMAT_RIGHT, width=130)
        self.list.InsertColumn(3, 'Model No', wx.LIST_FORMAT_RIGHT, width=140)
        self.list.InsertColumn(4, 'Connected Date', wx.LIST_FORMAT_RIGHT, width=140)
        self.list.InsertColumn(5, 'Drive Name', wx.LIST_FORMAT_RIGHT, width=140)
        self.list.InsertColumn(6, 'Device install date', wx.LIST_FORMAT_RIGHT, width=140)
        self.list.InsertColumn(7, 'Vendor Name', wx.LIST_FORMAT_RIGHT, width=140)
        self.list.InsertColumn(8, 'Firmware Version', wx.LIST_FORMAT_RIGHT, width=140)


    def OnQuit(self, e):
        self.Close()

    def OnScan(self,e):


        usbDetails = UsbArtifacts()
        self.usbConnectDetailsList = usbDetails.getAllConnectedDeviceDetails()
        self.usbConnectDetailsList.reverse()
        # print(self.usbConnectDetailsList)
        counter = len(self.usbConnectDetailsList)
        for device in self.usbConnectDetailsList:
            print(device)
            index = self.list.InsertItem(0, str(counter ))
            self.list.SetItem(index, 1, device['type'])
            self.list.SetItem(index, 2, device['vendor'])
            self.list.SetItem(index, 3, device['productname'])
            self.list.SetItem(index, 4, device['productname'])
            self.list.SetItem(index, 5, device['serialno'])
            counter -= 1



if __name__ == "__main__":
    app = wx.App(False)
    frame = MainWindow(None, 'usb forensics')

    app.MainLoop()
