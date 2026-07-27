from langchain_core.prompts import PromptTemplate
from src.output_parsers import CPOutputParsers

class HintChain:
    """Chain to generate progressive hints for a problem (Socratic method)."""
    
    def __init__(self, llm):
        self.llm = llm
        self.parser = CPOutputParsers.get_hint_response_parser()
        
        self.prompt = PromptTemplate(
            template="""You are an expert Competitive Programming Coach.
The user is stuck on a problem and needs hints. DO NOT give them the full solution immediately.
Instead, provide a series of progressive hints:
1. A small nudge (to point them in the right direction).
2. The algorithmic approach (e.g., "Think about dynamic programming").
3. A detailed hint (explaining state transitions or graph construction).
4. The near-solution logic.

{format_instructions}

Problem Statement:
{problem_text}

Provide the hints formatted strictly as JSON.
""",
            input_variables=["problem_text"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        
        self.chain = self.prompt | self.llm | self.parser

    def run(self, problem_text: str):
        """Generate hints for a problem."""
        return self.chain.invoke({"problem_text": problem_text})
