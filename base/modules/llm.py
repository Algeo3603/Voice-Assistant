import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# client = Groq(
#     api_key=GROQ_API_KEY,
# )

# chat_completion = client.chat.completions.create(
#     #
#     # Required parameters
#     #
#     messages=[
#         # Set an optional system message. This sets the behavior of the
#         # assistant and can be used to provide specific instructions for
#         # how it should behave throughout the conversation.
#         {
#             "role": "system",
#             "content": "you are a helpful assistant. Answer as Jon Snow"
#         },
#         # Set a user message for the assistant to respond to.
#         {
#             "role": "user",
#             "content": "Explain the importance of low latency LLMs",
#         }
#     ],

#     # The language model which will generate the completion.
#     model="llama3-70b-8192",

#     #
#     # Optional parameters
#     #

#     # Controls randomness: lowering results in less random completions.
#     # As the temperature approaches zero, the model will become deterministic
#     # and repetitive.
#     temperature=0.5,

#     # The maximum number of tokens to generate. Requests can use up to
#     # 2048 tokens shared between prompt and completion.
#     max_tokens=1024,

#     # Controls diversity via nucleus sampling: 0.5 means half of all
#     # likelihood-weighted options are considered.
#     top_p=1,

#     # A stop sequence is a predefined or user-specified text string that
#     # signals an AI to stop generating content, ensuring its responses
#     # remain focused and concise. Examples include punctuation marks and
#     # markers like "[end]".
#     stop=None,

#     # If set, partial message deltas will be sent.
#     stream=False,
# )

# # Print the completion returned by the LLM.
# print(chat_completion.choices[0].message.content, type(chat_completion.choices[0].message.content))

class LLM:
    def __init__(self)->None:
        self.messages = [{'role': 'system', "content": "You are developed by IPD studios"},
            {'role': 'system', "content": "You have various full names, the most popular one is 'Just Another Rather Very Intelligent System', second most popular one is 'Just Another Remarkable Various Intelligence System'"},
            {'role': 'system', "content": "You will only introduce yourself when asked who are you, only then will you introduce yourself"},
            {'role': 'system', "content": "You will introduce yourself as jarvis, state your full name and your capabilities."},
            {'role': 'system', "content": "Do not write in bold or italic, you will not use bold or italic characters"}
        ]

    def AI(self, message):
        assert message
        
        self.messages.append({'role':'user', 'content': message})
        try: 
            client = Groq(
                api_key=GROQ_API_KEY,
            )

            chat_completion = client.chat.completions.create(
                #
                # Required parameters
                #
                messages= self.messages,

                # The language model which will generate the completion.
                model="llama3-70b-8192",

                #
                # Optional parameters
                #

                # Controls randomness: lowering results in less random completions.
                # As the temperature approaches zero, the model will become deterministic
                # and repetitive.
                temperature=0.5,

                # The maximum number of tokens to generate. Requests can use up to
                # 2048 tokens shared between prompt and completion.
                max_tokens=1024,

                # Controls diversity via nucleus sampling: 0.5 means half of all
                # likelihood-weighted options are considered.
                top_p=1,

                # A stop sequence is a predefined or user-specified text string that
                # signals an AI to stop generating content, ensuring its responses
                # remain focused and concise. Examples include punctuation marks and
                # markers like "[end]".
                stop=None,

                # If set, partial message deltas will be sent.
                stream=False,
            )

            self.messages.append({'role':'assistant',"content": chat_completion.choices[0].message.content})

            return chat_completion.choices[0].message.content

        except Exception as e:
            print(f"Error occurred: {e}")
            return f"Error occurred: {e}"            

if __name__ == "__main__":
    LLM_demo = LLM()
    while True:
        query = input("Enter the query: ")
        response = LLM_demo.AI(query)
        print(response)