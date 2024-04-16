
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.callbacks import get_openai_callback
from langchain_core.output_parsers import StrOutputParser
import  os
from dotenv import load_dotenv, find_dotenv

class OpenAI:
    def __init__(self,model_name,max_tokens,temperature,top_p):
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
        promtFile = open('prompt.txt', 'r')
        self.system_prompt =promtFile.read()
        promtFile.close()
    def get_messages(self,input):
        prompt = ChatPromptTemplate.from_messages([("system", self.system_prompt), ("user", "{input}")])
        chain = prompt | self.model | StrOutputParser()
        role = "user"
        response = chain.invoke({"role": role, "input": input})
        return response

























