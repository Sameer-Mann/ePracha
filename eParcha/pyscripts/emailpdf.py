def Ee_mail_karo(context):
    #context = { "email" :  
    #            "name"  :
    #            "pdfname" : ### preferably in the same folder as this script  
    # }
    import os
    import smtplib
    import imghdr
    from email.message import EmailMessage
    
    #change acc to your environment variables 
    EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    msg = EmailMessage()
    msg['Subject'] = 'Medical prescription'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = context["email"]

    #pass the name of the patient in the context and edit the text content of the mail accordingly
    msg.set_content('This is a plain text email')

    files = [context["pdfname"]]

    for file in files:
        with open(file, 'rb') as f:
            file_data = f.read()
            file_name = f.name
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename = file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)



from fpdf import FPDF
import PyPDF2

class PDF(FPDF):
    def header(self): 
        self.line(10,10,200,10)
        self.line(200,10,200,280)
        self.line(10,10,10,280)
        self.line(10,280,200,280)    
        # Logo
        self.image('logo.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 20)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'Prescription', 0, 0, 'C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

# Instantiation of inherited class
def body(list):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 10, '', 0, 1)
    pdf.cell(0, 10, '', 0, 1)
    pdf.cell(0, 10, 'Patient:  '+list[0],1,1)
    pdf.cell(0, 10, 'Age:  '+list[1],1,1)
    pdf.cell(0, 10, 'Gender:  '+list[2],1,1)
    pdf.cell(0, 10, 'Diagnosis:  '+list[3],1,1)
    pdf.cell(0, 10, "Prognosis:  "+list[4],1,1)
    pdf.cell(0, 10, "Medicine:  "+list[5],1,1)
    pdf.cell(0, 10, "Comments:  "+list[6],1,1)
    pdf.cell(0, 10, "E-Mail ID:  "+list[7],1,1)
    
    pdf.output('test.pdf','F')
    import PyPDF2
    pdfFile = open('test.pdf', 'rb')
    
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    pdfWriter = PyPDF2.PdfFileWriter()
    
    for pageNum in range(pdfReader.numPages):
        pdfWriter.addPage(pdfReader.getPage(pageNum))
    
    pdfWriter.encrypt(list[0][:3]+list[1])
    
    resultPdf = open('encrypted_output.pdf', 'wb')
    
    pdfWriter.write(resultPdf)
    resultPdf.close()


pres = ['Amogh','69','Male','coughing','CORONA','Bat Soup','RIP','719.sn33@gmail.com']

body(pres)
context = {"email" :  pres[7],
            "name"  : pres[0],
            "pdfname" : 'encrypted_output.pdf'
          }
Ee_mail_karo(context)