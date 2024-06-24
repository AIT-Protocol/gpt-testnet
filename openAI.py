from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv, find_dotenv
# import logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


class OpenAI:
    def __init__(self, model_name, max_tokens, temperature, top_p):
        _ = load_dotenv(find_dotenv())
        api_key = os.environ.get("OPENAI_API_KEY")
        print(api_key)
        self.model = ChatOpenAI(
            api_key=api_key,
            model_name=model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p
        )
        with open('prompt.txt', 'r') as promtFile:
            self.system_prompt = promtFile.read()

    def get_messages(self, input_text):
        prompt = ChatPromptTemplate.from_messages(
            [("system", self.system_prompt), ("user", "{input}")])
        chain = prompt | self.model | StrOutputParser()
        response = chain.invoke({"role": "user", "input": input_text})
        print("chain: {}".format(chain))
        print("response: {}".format(response))
        return response

    def generate_from_TxtandImg(self, input_text, img):
        # try:
            # model = genai.GenerativeModel(model_name='gemini-pro-vision')
        response = self.model.generate_content(
            [input_text, img], stream=True)
        print("response: {}".format(response))
        response.resolve()
        return response.text
        # except Exception as exception:
        #     raise Exception("An error occurred during the process:", exception)
