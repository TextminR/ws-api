from langchain.prompts import (
    FewShotChatMessagePromptTemplate,
    ChatPromptTemplate,
)

examples = [
    {"input": "What is the name of the author and the publishment date of the following text? 'The text was written by Arnold Schwarzennegger in 2020.'", "output": "Arnold Schwarzennegger and 2020"},
    {"input": "What is the name of the author and the publishment date of the following text? 'Lukas Böhl 1998 Die Ratten Die Ratten sind giftig.'", "output": "Lukas Böhl and 1998"},
    {"input": "What is the name of the author and the publishment date of the following text? 'Das Brot - Wolfgang Borchert (1947) Plötzlich wachte sie auf. Es war halb drei'", "output": "Wolfgang Borchert and 1947"},
    {"input": "What is the name of the author and the publishment date of the following text? 'Der 54-Jährige wurde in den 1990er-Jahren durch seine Rolle des Chandler Bing in der Kult-Fernsehserie *Friends* berühmt Astrid Ebenführer 29. Oktober 2023, 07:47, 359 Postings'", "output": "Astrid Ebenführer and 2023"},
]

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

# print(few_shot_prompt.format())

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a wondrous wizard of math."),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)

print(final_prompt)