from fpdf import FPDF
import PyPDF2

from django.conf import settings 
from django.core.mail import send_mail 
from django.core.mail import EmailMessage
from django.http import FileResponse, Http404

def email_using_django(context):
    subject = 'Medical Report'
    message = 'Hi, This is your medical report.'
    files = [context["pdfname"]]
    mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [context['email']])
    for file in files:
        with open(file, 'rb') as f:
            file_data = f.read()
            file_name = f.name
        mail.attach(file_name, file_data, 'application/pdf')
    mail.send()


class PDF(FPDF):
    def header(self): 
        self.line(10,10,200,10)
        self.line(200,10,200,280)
        self.line(10,10,10,280)
        self.line(10,280,200,280)    
        self.set_font('Arial', 'B', 20)
        self.cell(80)
        self.cell(30, 10, 'Prescription', 0, 0, 'C')
        self.ln(20)

    # Page footer
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

# Instantiation of inherited class
def body(list):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    pdf.cell(0, 10, '', 0, 1)
    pdf.cell(0, 10, '', 0, 1)
    pdf.cell(0, 10, 'Patient:  '+list['name'],1,1)
    pdf.cell(0, 10, 'Age:  '+list['age'],1,1)
    pdf.cell(0, 10, 'Diagnosis:  '+list['disease'],1,1)
    pdf.cell(0, 10, "Medicine:  "+list['medicine'],1,1)
    pdf.cell(0, 10, "E-Mail ID:  "+list['email'],1,1)
    
    pdf.output('test.pdf','F')
    import PyPDF2
    pdfFile = open('test.pdf', 'rb')
    
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    pdfWriter = PyPDF2.PdfFileWriter()
    
    for pageNum in range(pdfReader.numPages):
        pdfWriter.addPage(pdfReader.getPage(pageNum))
    
    
    resultPdf = open('report.pdf', 'wb')
    
    pdfWriter.write(resultPdf)
    resultPdf.close()



def func(data):
    body(data)
    context = {"email" :  data['email'],
            "name"  : data['name'],
            "pdfname" : 'report.pdf'
            
          }
    email_using_django(context)