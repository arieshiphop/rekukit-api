import PyPDF2
import base64
import langid
from googletrans import Translator

class CvReader:
    def __init__(self,base64str,requirements):
        self.cv = base64str
        self.requirements = requirements
        self.pdf_path = "src/cv.pdf"
        self.whole_text = None
    def convert_base64_to_pdf(self):
        with open(self.pdf_path, "wb") as the_file:
            the_file.write(base64.b64decode(self.cv))
        content = self.get_text_from_all_pdf_pages()
        return content
    def get_text_from_all_pdf_pages(self):
        pdf_file = open(self.pdf_path, "rb")
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        whole_text = ""
        for page in range(num_pages):
            page_obj = pdf_reader.pages[page]
            catched_text = page_obj.extract_text()
            whole_text += catched_text
        self.whole_text = whole_text
        pdf_file.close()
        return whole_text
    def replace_simbols(self,word):
       return word.replace(","," ").strip().replace("\n"," ").strip().replace("."," ").strip().replace("-"," ").strip().replace("/"," ").strip().replace("\\"," ").strip().replace("\r"," ").strip().replace(":"," ").strip().replace("("," ").strip().replace(")"," ").strip()
    def procces_words(self,words):

    
        words = [self.replace_simbols(word).split(" ") for word in words ]
        proccesed_words = []
        for word in words:
            for realWord in word:
                proccesed_words.append(realWord)
        return proccesed_words
    def get_common_knowledges(self):
        whole_text = self.get_text_from_all_pdf_pages()
        words = whole_text.split(" ")
        words = self.procces_words(words)
        knowledges = [requirement.lower() for requirement in self.requirements["knowledges"]]
        knowledges_found = [word for word in words if word.lower() in knowledges]
        return list(set(knowledges_found))
    def join_words_into_string(self):
        whole_text = self.get_text_from_all_pdf_pages()
        words = whole_text.split(" ")
        words = self.procces_words(words)
        return ' '.join(words)
    def text_lang(self):
        text = self.join_words_into_string()
        return langid.classify(text)[0]
    def translate_text(self):
        text = self.join_words_into_string()
        translator = Translator()
        translation = translator.translate(text, src=self.text_lang(),dest='en')
        return translation.text
    def get_common_educations(self):
        whole_text = self.get_text_from_all_pdf_pages()
        words = whole_text.split(" ")
        words = self.procces_words(words)
        educations = [education.lower() for education in self.requirements["education"]]
        educations_found = [word for word in words if word.lower() in educations]
        return list(set(educations_found))
    def get_common_soft_skills(self):
        whole_text = self.get_text_from_all_pdf_pages()
        words = whole_text.split(" ")
        words = self.procces_words(words)
        soft_skills = [soft_skill.lower() for soft_skill in self.requirements["soft"]]
        soft_skills_found = [word for word in words if word.lower() in soft_skills]
        return list(set(soft_skills_found))
    def get_percentage(self):
        requirements = self.requirements
        knowledges = requirements["knowledges"]
        education = requirements["education"]
        soft = requirements["soft"]
        len_1 = len(soft) + len(knowledges) + len(education)
        len_2 = len(self.get_common_knowledges()) + len(self.get_common_educations()) + len(self.get_common_soft_skills())
        return str(len_2/len_1*100)[:2]
    def get_all_commons(self):
        common = {
            "knowledges":self.get_common_knowledges(),
            "education":self.get_common_educations(),
            "soft":self.get_common_soft_skills(),
            "compatibility":self.get_percentage(),
            "text_lang":self.text_lang(),
        }
        return common
