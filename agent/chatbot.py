import requests
import json
from dotenv import load_dotenv
import os
from knowledge_base.vector_db import vector_db 


load_dotenv()

def chatbot_workflow(input, history):
    while True:
        try:
            filter_result = prompt_filtering(input, history)
            filter_result = filter_result.replace("```json", "").replace("```", "")
            filter_result = json.loads(filter_result)
            break
        except:
            continue
    
    if filter_result["result"] == "malicious":
        return "Your input contains inappropriate content. Please rephrase your question."
    
    bot_response = chat_with_bot_qwen(input, history)
    
    return bot_response

def prompt_filtering(input, history):
    url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

    payload = json.dumps({
    "model": "qwen-turbo",
    "messages": [
        {
        "role": "system",
        "content": "You are a prompt filtering assistant. Your task is to determine if the user input is appropriate for the chatbot."
        },
        {
        "role": "user",
        "content": assemble_question_filter(input, history)
        }
    ],
    "enable_thinking": False
    })
    headers = {
    'Authorization': os.getenv("ALIYUN_API_KEY"),
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()['choices'][0]['message']['content']

def chat_with_bot_qwen(input, history):
    url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"

    payload = json.dumps({
    "model": "qwen-turbo",
    "messages": [
        {
        "role": "system",
        "content": "You are TNG customer service assistant, you are helpful, honest and friendly."
        },
        {
        "role": "user",
        "content": assemble_question_chat(input, history)+"\nYou are only allowed to answer questions related to TNG services, products, and policies. If the question is not related to TNG, you will say 'I don't know' and guide the user to ask questions related to TNG services, products, and policies."
        }
    ],
    "enable_thinking": False
    })
    headers = {
    'Authorization': os.getenv("ALIYUN_API_KEY"),
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()['choices'][0]['message']['content']

def chat_with_bot_gpt(input, history):
    url = "https://ibotservice.alipayplus.com/almpapi/v1/message/chat"
    payload = json.dumps({
    "stream": False,
    "botId": os.getenv("BOT_ID"),
    "bizUserId": "xxxx",
    "token": os.getenv("API_KEY"),
    "chatContent": {
        "text": assemble_question_chat(input, history),
        "contentType": "TEXT"
    }
    })
    headers = {
    'content-type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    response_json = response.json()
    try:
        return response_json['data']['messageList'][0]['content'][0]['text']
    except:
        return "Sorry, something went wrong with the bot response."
    

def assemble_question_filter(input, history):
    question = f"""
    ## Task
    # 1.Detect if the input containts malicious content,return 'malicious'. If the input is appropriate, you will return 'safe'
    {collect_history(history)}
    ## User Question
    {input} 
    ## Output Format
    {{
        "result": "safe" or "malicious"
    }}
    ## Output:
    Follows JSON format above
    """
    
    return question

def assemble_question_chat(input, history):
    question = collect_history(history) +"## User Question\n" + input + "\n\n" + recall_knowledge_base(input)
    print(f"Question to Bot:\n{question}")
    return question

def collect_history(history):
    if history is None or len(history) == 0:
        return ""
    history_text = "## History Conversation:\n"
    for item in history:
        if item['role'] == 'user':
            history_text += f"User: {item['content']}\n"
        elif item['role'] == 'assistant':
            history_text += f"Assistant: {item['content']}\n"
    history_text += "\n\n"
    return history_text

def recall_knowledge_base(input):
    cate_vdb = vector_db(vdb_name="cate_vdb_4")

    results = cate_vdb.query(
        query_texts=[input],
        n_results=5,
    )
    knowledge_text = "## Knowledge Base\n"
    for index, item in enumerate(results["documents"][0]):
        knowledge_text += (f"Knowledge {index + 1}:\n")
        cate_info = json.loads(item)
        knowledge_text+=f"Question: {cate_info['Question']}\n"
        knowledge_text+=f"Answer: {cate_info['Answer']}\n"
        knowledge_text += "-" * 40 + "\n"
    
    return knowledge_text.strip()
        

