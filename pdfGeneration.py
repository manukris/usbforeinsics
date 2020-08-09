from fpdf import FPDF, HTMLMixin
import time
from  datetime import datetime


class PdfGenaration(FPDF, HTMLMixin):

    def generateReport(self,deviceList):
        pdf = self

        table = """
        <h1> USB Forensic Report </h1>
        
         """
        trows = ""
        counter = 1
        for device in deviceList:
            trows += """
                        <br>
                            Serial No  - """ + str(counter) +  """<br>
                            <br> Vendor Name - """ + device['vendor']+  """<br>
                            <br> Product Name - """ + device['productname']+  """<br>
                            <br> Serial No - """ + device['serialno']+  """<br>
                            <br> Device Id - """ + device['id']+  """<br>
                            <br> First Connect Time  - """ + str(datetime.fromtimestamp(device['ftime'])) +  """<br>
                            <br> Last Connect Time - """ + str(datetime.fromtimestamp(device['lastcontime'])) +  """<br>
                            <br> Last Removal Time  - """ + str(datetime.fromtimestamp(device['lastremtime'])) +  """<br>
                        
                        <hr>
                        <hr>
                    """
            counter += 1

        table = table + trows
        print(table)
        pdf.add_page()
        pdf.write_html(table)
        ts = time.time()
        ts = int(ts)
        # path = r"‪C:\\Users\\HP\\Desktop"
        pdfname =  "USBREPORT" + str(ts) +".pdf"
        pdf.output(pdfname)

    def icongenerateReport(self,icondetails):
        pdf = self

        table = """
            <h1> Applications Forensic Report </h1>
    <br>
    <br>
            <table border="0" align="center" width="100%">
               
                <tbody> """
        trows = ""
        counter = 1
        for key,value in icondetails:
            trows += """
                            <tr>
                                <th>""" + key + """<br>
                                <br>""" +   value + """<br>
                               
                            </tr>
                        """
            counter += 1

        table = table + trows + " </tbody> </table> "
        print(table)
        pdf.add_page()
        pdf.write_html(table)
        ts = time.time()
        ts = int(ts)
        # path = r"‪C:\\Users\\HP\\Desktop"
        pdfname = str(ts) + ".pdf"
        pdf.output(pdfname)
        
    def pregenerateReport(self, deviceList):
        pdf = self

        table = """
            <h1> Applications Forensic Report </h1>
    <br>
    <br>
             """
        trows = ""
        counter = 1
        for device in deviceList:
            trows += """
                            <br>
                            Serial No  - """ + str(counter) +  """<br>
                            <br> Vendor Name - """ + device['vendor']+  """<br>
                            <br> Product Name - """ + device['productname']+  """<br>
                            <br> Serial No - """ + device['serialno']+  """<br>
                            <br> Device Id - """ + device['id']+  """<br>
                           """
            approws = "<br> <h3>"
            if len(device['appdetails']) != 0:
                for details in device['appdetails']:
                    approws += "<br> Application Details<h3><br> <br>" + details + "<br> "
            approws += "</h3>"
            trows = trows + approws + "<hr>"

                        


            counter += 1

        table = table + trows
        print(table)
        pdf.add_page()
        pdf.write_html(table)
        ts = time.time()
        ts = int(ts)
        # path = r"‪C:\\Users\\HP\\Desktop"
        pdfname = "prefetchReports"+str(ts) + ".pdf"
        pdf.output(pdfname)



if __name__ == '__main__':
    getpdf = PdfGenaration()
    getpdf.generateReport()
