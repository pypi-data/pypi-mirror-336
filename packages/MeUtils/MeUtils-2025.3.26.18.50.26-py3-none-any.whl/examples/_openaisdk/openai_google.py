#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_siliconflow
# @Time         : 2024/6/26 10:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *
from openai import OpenAI
from openai import OpenAI, APIStatusError

client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url=os.getenv("GOOGLE_BASE_URL"),
)

print(client.models.list().model_dump_json(indent=4))
# models/gemini-2.5-pro-exp-03-25
# models/gemini-2.0-flash-exp-image-generation
#
try:
    completion = client.chat.completions.create(
        # model="models/gemini-2.5-pro-exp-03-25",
        model="models/gemini-2.0-flash-thinking-exp",
        messages=[
            {"role": "user", "content": "画条狗"}
        ],
        # top_p=0.7,
        top_p=None,
        temperature=None,
        stream=True,
        max_tokens=4000,
        extra_body={"A": 1}
    )
except APIStatusError as e:
    print(e.status_code)

    print(e.response)
    print(e.message)
    print(e.code)

for chunk in completion: # 剔除extra body
    print(chunk)
    if chunk.choices:
        print(chunk.choices[0].delta.content)
