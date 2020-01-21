import wx

####
class MainWindow(wx.Frame):

    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(600, 300))


        self.Centre()

        self.Show()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainWindow(None, 'usb forensics')
    app.MainLoop()