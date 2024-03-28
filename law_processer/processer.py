import PyPDF2
import pandas as pd
import re
class PDFProcessor:
    def __init__(self, pdf_path, save_path):
        self.pdf_path = pdf_path
        self.save_path = save_path
        self.data_dict = {}
        self.pdf_text = ""
        self.clean_text = ""

    def extract_text_from_pdf(self):
        text = ""
        with open(self.pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            for page_number in range(num_pages):
                page = reader.pages[page_number]
                text += page.extract_text()
            self.pdf_text = text
            
    def get_clean_text(self):
        return self.clean_text
    
    def get_origin_text(self):
        return self.pdf_text

    def get_data_csv(self):
        return pd.DataFrame(self.data_dict)
    
    def save_to_csv(self):
        # Split the text into lines
        df = self.get_data_csv()
        df.to_csv(self.save_path, index = False)
        print(f"File is saved to {self.save_path}")


class CommonLawProcessor(PDFProcessor):
    def __init__(self, pdf_path, save_path):
        super().__init__(pdf_path, save_path)
        self.num2alpha = {"1":"A", "2":"B", "3":"C", "4":"D"}

    def _extract_question_index(self, question_text):
        pattern = r"^(\d+)\."
        match = re.match(pattern, question_text)
        if match:
            question_index = match.group(1)
            return question_index, re.sub(pattern, "", question_text)
        else:
            return None
        
    def context_cleaning(self):
        pdf_text = self.pdf_text
        pdf_text = re.sub(r'（\s*',"(", pdf_text)
        pdf_text = re.sub(r'\s*）',")", pdf_text)
        self.clean_text = pdf_text

    def formating_questions(self):
        self.clean_text = re.sub(r'\n|\s+',"", self.clean_text)
        questions, answers = [], []
        col_A, col_B, col_C, col_D  = [], [], [], []
        for complete_question in re.findall(r'\((\d+)\)\d+\.([\s\S]*?)(?=\(\d+\)\d+\.|$)', self.clean_text):
            if len(complete_question)==2:
                #print(complete_question)
                question = re.findall(r"(.*?)\(1\)", complete_question[1])
                options = re.findall(r'\(1\)(.*?)\(2\)(.*?)\(3\)(.*?)\(4\)(.*?)。', complete_question[1])
                if len(options)!=0:
                    if len(question)==1 and len(options[0])==4:
                        answers.append(self.num2alpha[str(complete_question[0])])
                        questions.append(question[0])
                        col_A.append(options[0][0])
                        col_B.append(options[0][1])
                        col_C.append(options[0][2])
                        col_D.append(options[0][3])

        self.data_dict['Question'] = questions
        self.data_dict['Answer'] = answers
        self.data_dict['A'] = col_A
        self.data_dict['B'] = col_B
        self.data_dict['C'] = col_C
        self.data_dict['D'] = col_D

        print("Number of Data:", len(questions))
    def pipline(self):
        print(f"Now extracting PDF from {self.pdf_path}.")
        self.extract_text_from_pdf()
        print("Cleaning PDF context...")
        self.context_cleaning()
        print("Extracting question and correct answer...")
        self.formating_questions()
        print("Process finish!")

class MinistryOfExamQuestionProcessor(PDFProcessor):
    def __init__(self, pdf_path, save_path):
        super().__init__(pdf_path, save_path)
        self.num2alpha = {"1":"A", "2":"B", "3":"C", "4":"D"}

class MinistryOfExamAnswerProcessor(PDFProcessor):
    def __init__(self, pdf_path, save_path):
        super().__init__(pdf_path, save_path)
        self.num2alpha = {"1":"A", "2":"B", "3":"C", "4":"D"}