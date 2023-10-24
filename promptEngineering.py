from langchain.prompts import (
    FewShotChatMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain.chat_models import ChatAnthropic

examples = [
    {"input": "2+2", "output": "4"},
    {"input": "2+3", "output": "5"},
]

# This is a prompt template used to format each individual example.
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

print(few_shot_prompt.format())

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a wondrous wizard of math."),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)

chain = final_prompt | ChatAnthropic(temperature=0.0)

chain.invoke({"input": "What's the square of a triangle?"})
