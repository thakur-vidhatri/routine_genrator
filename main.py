
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

app = FastAPI()

llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0.7,
    groq_api_key="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"
)

prompt = PromptTemplate(
    input_variables=["products"],
    template="""
You are a dermatology expert building Indian skincare routines.

Given these products:
{products}

Build a sequential routine. Indicate:
- AM or PM
- Number of uses per day
- Duration in weeks
- When to switch between products
- Priority: acne > pigmentation > wrinkles > dark circles > dryness > fine lines > whiteheads > blackheads

Return only the final plan.
"""
)

chain = LLMChain(llm=llm, prompt=prompt)

class ProductInput(BaseModel):
    products: List[str]

@app.post("/generate-routine/")
def generate_routine(req: ProductInput):
    formatted = "\n".join(req.products)
    result = chain.run(products=formatted)
    return {"routine": result}
