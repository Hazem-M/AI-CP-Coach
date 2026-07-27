from langchain_core.prompts import PromptTemplate
from src.output_parsers import CPOutputParsers

class SolutionReviewChain:
    """Chain to review a user's code for a problem."""
    
    def __init__(self, llm):
        self.llm = llm
        self.parser = CPOutputParsers.get_solution_review_parser()
        
        self.prompt = PromptTemplate(
            template="""You are an expert Competitive Programming Coach.
Review the following user code submitted for a problem.

{format_instructions}

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
""",
            input_variables=["problem_text", "user_code", "language"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        
        self.chain = self.prompt | self.llm | self.parser

    def run(self, problem_text: str, user_code: str, language: str = "C++"):
        """Review the user's code."""
        return self.chain.invoke({
            "problem_text": problem_text,
            "user_code": user_code,
            "language": language
        })
