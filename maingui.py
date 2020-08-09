import wx
import prefetchartifacts
from usbArtifacts import UsbArtifacts
from pdfGeneration import PdfGenaration
import os
# from fortools import *

from datetime import datetime, timedelta, tzinfo
from io import StringIO 
import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


class UsbTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.gui()
        self.window = parent


    def gui(self):
        self.btn = wx.Button(self, -1, label=" Run and Generate report", pos=(10, 10))
        self.btn.Bind(wx.EVT_BUTTON, self.Reportgenerate)

        self.list = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT|wx.LC_HRULES,size=(1200,400),pos=(0,40))
        self.list.InsertColumn(0, 'No',  wx.LIST_FORMAT_RIGHT,width=140)
        self.list.InsertColumn(1, 'Vender Name', wx.LIST_FORMAT_RIGHT, width=130)
        self.list.InsertColumn(3, 'Product Name', wx.LIST_FORMAT_RIGHT, width=140)
        self.list.InsertColumn(4, 'Firmware Version', wx.LIST_FORMAT_RIGHT, width=140)
        self.list.InsertColumn(5, 'Device Id', wx.LIST_FORMAT_RIGHT, width=140)
        self.list.InsertColumn(6, 'First Connect Time boot', wx.LIST_FORMAT_RIGHT, width=160)
        self.list.InsertColumn(7, 'Last Connect Time', wx.LIST_FORMAT_RIGHT, width=160)
        self.list.InsertColumn(8, 'Last Removal Time', wx.LIST_FORMAT_RIGHT, width=160)



    def OnScan(self):
        usbDetails = UsbArtifacts()
        self.usbConnectDetailsList = usbDetails.getAllConnectedDeviceDetails()
        self.usbConnectDetailsList.reverse()
        # print(self.usbConnectDetailsList)
        counter = len(self.usbConnectDetailsList)
        self.list.DeleteAllItems()
        for device in self.usbConnectDetailsList:
            print(device)
            index = self.list.InsertItem(0, str(counter))
            self.list.SetItem(index, 1, device['vendor'])
            self.list.SetItem(index, 2, device['productname'])
            self.list.SetItem(index, 3, device['serialno'])
            self.list.SetItem(index, 4, device['id'])
            self.list.SetItem(index, 5, str(datetime.fromtimestamp(device['ftime'])))
            self.list.SetItem(index, 6, str(datetime.fromtimestamp(device['lastcontime'])))
            self.list.SetItem(index, 7, str(datetime.fromtimestamp(device['lastremtime'])))
            counter -= 1


    def Reportgenerate(self, e):

        self.OnScan()
        pdf = PdfGenaration()

        pdf.generateReport(self.usbConnectDetailsList)
        dialog = wx.MessageDialog(self, message="Usb report Generated", caption="message",
                                  style=wx.OK | wx.CANCEL | wx.ICON_WARNING | wx.STAY_ON_TOP)
        result = dialog.ShowModal()


class PrefetchTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.gui()

    def gui(self):
        self.btn = wx.Button(self, -1, label=" Run and Generate report", pos=(10, 10))
        self.btn.Bind(wx.EVT_BUTTON, self.PrefetchReportgenerate)

        self.list = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_HRULES, size=(1200, 400), pos=(0, 40))
        self.list.InsertColumn(0, 'No', wx.LIST_FORMAT_RIGHT, width=140)
        self.list.InsertColumn(1, 'Vender Name', wx.LIST_FORMAT_RIGHT, width=130)
        self.list.InsertColumn(2, 'Product Name', wx.LIST_FORMAT_RIGHT, width=140)
        self.list.InsertColumn(3, 'Time of execution ', wx.LIST_FORMAT_RIGHT, width=150)
        self.list.InsertColumn(4, 'Apps Executed', wx.LIST_FORMAT_RIGHT, width=400)




    def PrefetchReportgenerate(self,e):


        usbDetails = UsbArtifacts()
        self.usbConnectDetailsList = usbDetails.getAllConnectedDeviceDetails()
        self.usbConnectDetailsList.reverse()
        # print(self.usbConnectDetailsList)
        counter = len(self.usbConnectDetailsList)
        self.list.DeleteAllItems()
        for device in self.usbConnectDetailsList:
            index = self.list.InsertItem(0, str(counter))
            self.list.SetItem(index, 1, device['vendor'])
            self.list.SetItem(index, 2, device['productname'])
            directory = "C:\\Windows\\Prefetch\\"
            try:
                timeofexe =  str(datetime.fromtimestamp(int(os.path.getmtime(directory + '\\' + device['applist'][0]))))
            except:
                timeofexe = "N/A"

            self.list.SetItem(index, 3, (timeofexe))
            applist = ""
            for apps in device['applist']:
                applist += apps[:-12] + " , "

            self.list.SetItem(index, 4, (applist))

            device['appdetails'] = prefetchartifacts.getPrefetchDetails(device['applist'])

            counter -= 1




        pdf = PdfGenaration()
        pdf.pregenerateReport(self.usbConnectDetailsList)

        dialog = wx.MessageDialog(None, message="Prefetch report Generated" , caption="message",
                                  style=wx.OK | wx.CANCEL | wx.ICON_WARNING|wx.STAY_ON_TOP)
        result = dialog.ShowModal()




class IconCaheTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.gui()

    def gui(self):
        self.iconCahebtn = wx.Button(self, -1, label="Generate IconCahe report", pos=(10, 10))
        self.iconCahebtn.Bind(wx.EVT_BUTTON, self.IconCaheReportgenerate)

        self.list = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_HRULES, size=(1200, 400), pos=(0, 40))
        self.list.InsertColumn(0, 'No', wx.LIST_FORMAT_RIGHT, width=140)
        self.list.InsertColumn(1, 'Icon', wx.LIST_FORMAT_RIGHT, width=130)
        self.list.InsertColumn(2, 'Path', wx.LIST_FORMAT_RIGHT, width=700)

    def IconCaheReportgenerate(self, e):

        # path = r'‪C:\Users\VIPIN S\AppData\Local\IconCache.db'
        # file = Iconcache.file_open(path)
        # with Capturing() as output:
        #     file.Favorite.show_info_by_section([3])
	    # self.list.DeleteAllItems()
        # for device in output[0].split(","):
        #     print(device)
        #     index = self.list.InsertItem(0, str(counter))
        #     #self.list.SetItem(index, 1, device)
        #     #self.list.SetItem(index, 2, device)
        #
        #     counter -= 1
        # pdf = PdfGenaration()
        # pdf.icongenerateReport(output[0])

        dialog = wx.MessageDialog(self, message="IconCahe  report Generated" , caption="message",
                                  style=wx.OK | wx.CANCEL | wx.ICON_WARNING)
        result = dialog.ShowModal()


####
class MainWindow(wx.Frame):

    def __init__(self, parent, title ):
        super().__init__(parent, title=title, size=(1200, 600))

        self.Centre()
        self.GUI()
        self.Show()
        self.runCount = 0

    def GUI(self):
        menubar = wx.MenuBar()

        #File
        fileMenu1 = wx.Menu()

        # fileItem1 = fileMenu1.Append(wx.ID_ADD, 'Run', 'Run application')
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

        # self.Bind(wx.EVT_MENU, self.OnScan, fileItem1)



        self.body()


    def body(self):

        panel = wx.Panel(self)

        nb = wx.Notebook(panel)

        # Create the tab windows
        tab1 = UsbTab(nb)
        tab2 = PrefetchTab(nb)
        # tab3 = IconCaheTab(nb)

        nb.AddPage(tab1, "USB Artifacts")
        nb.AddPage(tab2, "Prefetch  Artifacts")
        # nb.AddPage(tab3, "IconCache Artifacts")


        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        panel.SetSizer(sizer)



        # self.btn = wx.Button(panel, -1, label="Generate report", pos=(10, 10))
        #
        # self.prefetchbtn = wx.Button(panel, -1, label="Generate Prefetch report", pos=(150, 10))
        #
        # self.iconCahebtn = wx.Button(panel, -1, label="Generate IconCahe report", pos=(350, 10))
        #
        # self.btn.Disable()
        # # self.prefetchbtn.Disable()
        #
        # self.btn.Bind(wx.EVT_BUTTON, self.Reportgenerate)
        # self.prefetchbtn.Bind(wx.EVT_BUTTON, self.PrefetchReportgenerate)
        #
        # self.iconCahebtn.Bind(wx.EVT_BUTTON, self.IconCaheReportgenerate)
        #
        #
        # self.list = wx.ListCtrl(panel, wx.ID_ANY, style=wx.LC_REPORT|wx.LC_HRULES,size=(1200,400),pos=(0,40))
        # self.list.InsertColumn(0, 'No',  wx.LIST_FORMAT_RIGHT,width=140)
        # self.list.InsertColumn(1, 'Vender Name', wx.LIST_FORMAT_RIGHT, width=130)
        # self.list.InsertColumn(3, 'Product Name', wx.LIST_FORMAT_RIGHT, width=140)
        # self.list.InsertColumn(4, 'Firmware Version', wx.LIST_FORMAT_RIGHT, width=140)
        # self.list.InsertColumn(5, 'Device Id', wx.LIST_FORMAT_RIGHT, width=140)
        #
        # self.list.InsertColumn(6, 'Device Type', wx.LIST_FORMAT_RIGHT, width=140)
        #self.list.InsertColumn(7, 'First Connect time ', wx.LIST_FORMAT_RIGHT, width=140)
        # self.list.InsertColumn(8, 'Firmware Version', wx.LIST_FORMAT_RIGHT, width=140)



    def OnQuit(self, e):
        self.Close()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainWindow(None, 'usb forensics')
    def messageBox(messsage,caption):
        dialog = wx.MessageDialog(frame, messsage, caption,
                                  style=wx.OK | wx.CANCEL | wx.ICON_WARNING | wx.STAY_ON_TOP)
        result = dialog.ShowModal()
    app.MainLoop()

