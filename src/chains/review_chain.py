from langchain_core.prompts import PromptTemplate
from src.output_parsers import CPOutputParsers

class SolutionReviewChain:
    """Chain to review a user's code for a problem."""
    
    def __init__(self, llm):
        self.llm = llm
        self.parser = CPOutputParsers.get_solution_review_parser()
        
        self.prompt = PromptTemplate(
            template="""<|im_start|>system
You are an expert Competitive Programming Coach.
Review the following user code submitted for a problem.

{format_instructions}
<|im_end|>
<|im_start|>user
Problem Statement:
{problem_text}

User's Code:
{user_code}

Language: {language}

Analyze the code for:
1. Bugs (Logic errors, off-by-one, etc.)
2. Time Limit Exceeded (TLE) risks (Is the complexity optimal?)
3. Memory Limit Exceeded (MLE) risks
4. Edge cases missed (e.g., n=1, empty array, negative numbers, overflow)

Output your analysis strictly in the requested JSON format.
<|im_end|>
<|im_start|>assistant
""",
            input_variables=["problem_text", "user_code", "language"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        
        self.chain = self.prompt | self.llm

    def run(self, problem_text: str, user_code: str, language: str = "C++"):
        """Review the user's code."""
        raw_output = self.chain.invoke({
            "problem_text": problem_text,
            "user_code": user_code,
            "language": language
        })
        
        marker = "<|im_start|>assistant"
        if marker in raw_output:
            raw_output = raw_output.split(marker)[-1].strip()
            
        return self.parser.parse(raw_output)
