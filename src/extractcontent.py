from pypdf import PdfReader
from docx import Document
import docx2txt

class ExtractContent:
    def __init__(self, file_type, file_path=None):
        self.__file_type = file_type
        self.__file_path = file_path
        self.__words = 0
        self.__content = ""
        self.__pages = 0
        self.read()
    
    def getInformation(self):
        return f"FILE DESCRIPTION\nFile Path : {self.__file_path}\nNumber of Words : {self.__words}\nNumber of Pages : {self.__pages}"
    
    @staticmethod
    def readPdf(file_path):
        reader = PdfReader(file_path)
        pages = len(reader.pages)
        content = ""
        for i in range(pages):
            page = reader.pages[i]
            text = page.extract_text()
            content += text
        words = len(content.split())
        content = content.replace("\n"," ")
        return content, words, pages
    
    @staticmethod
    def readText(file_path):
        content = ""
        with open(file_path,"r") as f:
            content = f.read()
            f.close()
        words = len(content.split())
        return content, words, 1
        
    @staticmethod
    def readDocx(file_path):
        doc = Document(file_path)
        content = ""
        for para in doc.paragraphs:
            content+=para.text
        words = len(content.split())
        return content, words, 1
    
    def read(self):
        if self.__file_type == "pdf":
            self.__content,self.__words, self.__pages  = ExtractContent.readPdf(self.__file_path)
        elif self.__file_type == "txt":
            self.__content,self.__words, self.__pages  = ExtractContent.readText(self.__file_path)
        elif self.__file_type == "docx":
            self.__content,self.__words, self.__pages  = ExtractContent.readDocx(self.__file_path)
        else:
            raise Exception("Only .pdf, .txt, .docx files are allowed")
    
    def getContent(self):
        return self.__content
    

if __name__ == "__main__":
    a = ExtractContent("docx",r"C:\D\B Tech AIE\Semester 4\Mathematics for Computing 4 22MAT230\Assignment\End Semester Project\Project\DocxTest.docx")
    print(a.getInformation())
    print(a.getContent())

"""
def get_pdf_text(pdf_docs):
text = ""
for pdf in pdf_docs:
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
        text += page.extract_text()
return text
"""