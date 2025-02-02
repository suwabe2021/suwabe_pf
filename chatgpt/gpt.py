from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from django.conf import settings

OPENAI_API_KEY = settings.OPENAI_API_KEY

def sentgpt(question):
     
    llm = ChatOpenAI(api_key = OPENAI_API_KEY, model="gpt-4o-mini", temperature=0.5)
    
    #プロンプトテンプレート。長いと応答が遅くなるので一旦短いプロンプトを使う。
    template = "質問内容をできるだけ短い文章で明瞭に正しく説明してください。専門用語を使う場合は明快な例や比喩を使い説明してください。【質問内容】{question}"
    prompt = PromptTemplate(input_variables=["question"], template=template)

    #プロンプト | LLM設定 | gptの応答から文字列を解析
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    gpt_response = chain.invoke({"question":question})
    return gpt_response