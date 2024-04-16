# 📲 Installation
1. This repository requires python3.10 or higher. To install it, simply clone this repository
 ```bash
   git clone https://github.com/AIT-Protocol/gpt-testnet.git
   cd gpt-testnet
   pip install -r requiremets.txt
   ```
# 🧾 Run the sever

   ```bash
   python fastAPI.py \
   model_name gpt-3.5-turbo-0125 \
   max_tokens 2048 \
   temperature 0.9 \
   top_p 0.9 \
   top_k 50
   ```
   *- The `model_name` flag is used to specify the model you want to use. The default value is `gpt3.5-turbo` which is the latest model from OpenAI, you can find out more about the models [here](https://platform.openai.com/docs/models/)*

   *- The `max_tokens` flag is used to specify the maximum number of tokens the model can generate which is the length of the response. The default value is `256`*

   *- The `temperature` flag is used to specify the temperature of the model which controls the creativeness of the model. The default value is `0.7`*

   *- The `top_p` This is like choosing ideas that together make a good story, instead of just picking the absolute best ones. It helps the text be both interesting and sensible. The default value is `0.95`*

   *- The `top_k` It's like having a lot of ideas but only picking the few best ones to talk about. This makes the text make more sense.  Reducing the number ensures that the model's choices are among the most probable, leading to more coherent text. The default value is `50`*