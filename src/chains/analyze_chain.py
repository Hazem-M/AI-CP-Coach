from langchain_core.prompts import PromptTemplate

class ProblemAnalysisChain:
    def __init__(self, llm, vector_store=None):
        self.llm = llm
        self.prompt = PromptTemplate(
            template='''<|im_start|>system
You are a Grandmaster Competitive Programming Coach. 
Analyze the problem, share your thoughts in <think>...</think> tags, and provide the solution.
<|im_end|>
<|im_start|>user
Problem Statement:
{problem_text}
<|im_end|>
<|im_start|>assistant
<think>
''',
            input_variables=["problem_text"]
        )
        self.chain = self.prompt | self.llm

    def run(self, problem_text: str):
        # بنرجع النص زي ما هو من غير أي JSON
        raw_output = self.chain.invoke({"problem_text": problem_text})
        
        # عشان نضمن إن الـ prompt ما يطبعش مع الإجابة
        marker = "<|im_start|>assistant"
        if marker in raw_output:
            raw_output = raw_output.split(marker)[-1]
            # نشيل الـ think اللي في الأول لو موجودة عشان هنضيفها احنا
            raw_output = raw_output.replace("<think>", "", 1).strip()
            
        return "<think>\n" + raw_output
