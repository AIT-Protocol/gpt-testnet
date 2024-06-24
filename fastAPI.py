from fastapi import FastAPI, UploadFile, File, Form
from fastapi.exceptions import HTTPException
import PIL.Image
import io
import uvicorn
from openAI import OpenAI
import argparse
import os
from dotenv import load_dotenv, find_dotenv

# Argument Parsing
parser = argparse.ArgumentParser()
parser.add_argument("--model_name", help="The name of the model",
                    default="gpt-3.5-turbo-0125", required=False)
parser.add_argument("--max_tokens", help="Used to specify the maximum number of tokens the model can generate which is the length of the response. The default value is 2048", default=2048, required=False)
parser.add_argument(
    "--temperature", help="Used to specify the temperature of the model which controls the creativeness of the model. The default value is 0.9", default=0.9, required=False)
parser.add_argument("--top_k", help="It's like having a lot of ideas but only picking the few best ones to talk about. This makes the text make more sense. Reducing the number ensures that the model's choices are among the most probable, leading to more coherent text. The default value is 50", default=50)
parser.add_argument("--top_p", help="This is like choosing ideas that together make a good story, instead of just picking the absolute best ones. It helps the text be both interesting and sensible. The default value is 0.9", default=0.9, required=False)

args = parser.parse_args()
print(args.model_name)

# Load environment variables
load_dotenv(find_dotenv())

# Initialize OpenAI
openai = OpenAI(model_name=args.model_name, max_tokens=args.max_tokens,
                temperature=args.temperature, top_p=args.top_p)

# FastAPI setup
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/submit/")
async def submit(input_text: str = Form(...)):
    return openai.get_messages(input_text)


@app.post("/multiple")
async def multiple(input_text: str = Form(...), img: UploadFile = File(...)):
    img.file.seek(0, 2)
    file_size = img.file.tell()
    await img.seek(0)
    print("file size: ", file_size)
    if file_size > 20 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")

    content_type = img.content_type
    if content_type not in ["image/jpeg", "image/png", "image/gif"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    tempfile = await img.read()
    img = PIL.Image.open(io.BytesIO(tempfile))
    return openai.generate_from_TxtandImg(input_text, img)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5049)
