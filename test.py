import os
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

HUGGINGFACEHUB_API_TOKEN = "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"

os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN


question = "What is 2+2? "

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])

repo_id = "meta-llama/Llama-2-70b-chat-hf"
llm = HuggingFaceHub(
    repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_length": 64}
)
llm_chain = LLMChain(prompt=prompt, llm=llm)

print(llm_chain.run(question))
