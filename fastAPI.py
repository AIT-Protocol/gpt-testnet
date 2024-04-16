from fastapi import FastAPI,UploadFile,File,Form
from fastapi.exceptions import HTTPException
import matplotlib as plt
import PIL.Image
from gemini import Gemini
import io
import uvicorn
gemini = Gemini()
gemini.setup()
app = FastAPI()
from openAI import OpenAI
import argparse




if __name__ == "__main__":
    parser =argparse.ArgumentParser()
    parser.add_argument("--model_name",help="The name of the model",default="gpt-3.5-turbo-0125",required=False)
    parser.add_argument("--max_tokens",help=" used to specify the maximum number of tokens the model can generate which is the length of the response. The default value is 2048",default=2048,required=False)
    parser.add_argument("--temperature",help=" used to specify the temperature of the model which controls the creativeness of the model. The default value is 0.9",default=0.9,required=False)
    parser.add_argument("--top_k",help=" It's like having a lot of ideas but only picking the few best ones to talk about. This makes the text make more sense. Reducing the number ensures that the model's choices are among the most probable, leading to more coherent text. The default value is 50",default=50)
    parser.add_argument("--top_p",help="This is like choosing ideas that together make a good story, instead of just picking the absolute best ones. It helps the text be both interesting and sensible. The default value is 0.9",default=0.9,required=False)

    args = parser.parse_args()
    print(args.model_name)
    openai= OpenAI(model_name=args.model_name,max_tokens=args.max_tokens,temperature=args.temperature,top_p=args.top_p)

    @app.get("/")  # giống flask, khai báo phương thức get và url
    async def root():  # do dùng ASGI nên ở đây thêm async, nếu bên thứ 3 không hỗ trợ thì bỏ async đi
        return {"message": "Hello World"}


    @app.post("/multiple")
    async def multiple(promt: str, image: UploadFile = File(...)):
        image.file.seek(0, 2)
        file_size = image.file.tell()
        await image.seek(0)

        if file_size > 20 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large")

        content_type = image.content_type
        if content_type not in ["image/jpeg", "image/png", "image/gif"]:
            raise HTTPException(status_code=400, detail="Invalid file type")
        tempfile = await image.read()
        img = PIL.Image.open(io.BytesIO(tempfile))
        # do something with the valid file
        return gemini.generate_from_ImgandTxt(promt, img)


    @app.post("/image")
    async def multiple(image: UploadFile = File(...)):

        image.file.seek(0, 2)
        file_size = image.file.tell()
        await image.seek(0)

        if file_size > 20 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large")

        content_type = image.content_type
        if content_type not in ["image/jpeg", "image/png", "image/gif"]:
            raise HTTPException(status_code=400, detail="Invalid file type")
        # do something with the valid file
        tempfile = await image.read()
        img = PIL.Image.open(io.BytesIO(tempfile))
        return gemini.generate_from_img(img)


    @app.post("/prompt")
    async def multiple(prompt: str = Form(...)):

        return gemini.generate_from_txt(prompt)


    @app.post("/submit/")
    async def submit(prom: str = Form(...)):
        return openai.get_messages(prom)
    uvicorn.run(app, host="127.0.0.1", port=5049)