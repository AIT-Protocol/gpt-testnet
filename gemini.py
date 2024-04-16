import os
import pathlib
import textwrap
import google.generativeai as genai
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import google.generativeai as genai
class Gemini:
    def __init__(self):
        import os
        load_dotenv()
        self.GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        print(self.GOOGLE_API_KEY)
        self.myllm = ChatGoogleGenerativeAI(model='gemini-pro')
        self.my_prompt = PromptTemplate.from_template(
            'you are Einstein an advanced Math AI Solver. Which is trained by AIT .Your task is to provide users with clear and concise explanations and answers to their math questions. And you need to Solve {prompt}')
        self.chain = LLMChain(
            llm=self.myllm,
            prompt=self.my_prompt,
            verbose=True
        )

    def setup(self):
        try:
            if self.GOOGLE_API_KEY is None:
                raise Exception("GEMINI_API_KEY is not set")
            genai.configure(api_key=self.GOOGLE_API_KEY)
        except Exception as exception:
            raise Exception("An error occurred during setup:", exception)

    def generate_from_ImgandTxt(self,prompt, img):
        try:
            model = genai.GenerativeModel(model_name='gemini-pro-vision')
            response = model.generate_content([prompt, img], stream=True)
            response.resolve()
            return response.text
        except Exception as exception:
            raise Exception("An error occurred during the process:", exception)

    def generate_from_txt(self, prompt):
        try:
            model = genai.GenerativeModel(model_name='gemini-pro')
            response = model.generate_content(prompt, stream=True)
            response.resolve()
            return response.text
        except Exception as exception:
            raise Exception("An error occurred during the process:", exception)

    def generate_from_img(self, img):
        try:
            model = genai.GenerativeModel(model_name='gemini-pro-vision')
            response = model.generate_content(img, stream=True)
            response.resolve()
            return response.text
        except Exception as exception:
            raise Exception("An error occurred during the process:", exception)

    def langchainGemini(self,prompt):
        response = self.chain.invoke(input=prompt)
        return response['text']
