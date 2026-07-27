import json
from langchain_core.prompts import PromptTemplate
from src.output_parsers import CPOutputParsers

class ProfileAnalysisChain:
    """Chain to analyze a Codeforces profile based on API stats."""
    
    def __init__(self, llm):
        self.llm = llm
        self.parser = CPOutputParsers.get_profile_analysis_parser()
        
        self.prompt = PromptTemplate(
            template="""You are an expert Competitive Programming Coach.
Analyze the following Codeforces user profile statistics.

{format_instructions}

User Statistics (from Codeforces API):
{user_stats}

Analyze their strengths and weaknesses. What should they focus on?
Are they avoiding math? Are they weak at dynamic programming? 
Provide an actionable training plan.
Output strictly as JSON matching the format instructions.
""",
            input_variables=["user_stats"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        
        self.chain = self.prompt | self.llm | self.parser

    def run(self, user_stats: dict):
        """Analyze user profile."""
        stats_str = json.dumps(user_stats, indent=2)
        return self.chain.invoke({"user_stats": stats_str})


class RecommendationChain:
    """Chain to recommend problems based on user weaknesses."""
    
    def __init__(self, llm, vector_store=None):
        self.llm = llm
        self.vector_store = vector_store
        self.parser = CPOutputParsers.get_recommendations_parser()
        
        self.prompt = PromptTemplate(
            template="""You are an expert Competitive Programming Coach.
Based on the user's weaknesses and current rating, recommend problems for them to solve.

{format_instructions}

User's Current Rating: {current_rating}
User's Weaknesses:
{weaknesses}

Candidate Problems from Vector Store (if any):
{candidate_problems}

Filter the candidates and recommend a targeted practice set. Give a reason for each recommendation.
Output strictly as JSON matching the format instructions.
""",
            input_variables=["current_rating", "weaknesses", "candidate_problems"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        
        self.chain = self.prompt | self.llm | self.parser

    def _get_candidates(self, weaknesses: list, rating: int) -> str:
        """Fetch candidates from vector store based on weak tags."""
        if not self.vector_store or not self.vector_store.vector_store:
            return "No specific candidates found from local database."
            
        candidates = []
        try:
            # Query the vector store for the top weakness
            if weaknesses:
                top_weakness = weaknesses[0].get("tag", "dynamic programming")
                # We could add more sophisticated filtering here
                docs = self.vector_store.search_similar_problems(top_weakness, k=10)
                # Filter by rating manually if needed
                valid_docs = [d for d in docs if d.metadata.get("rating", 0) >= rating - 100 and d.metadata.get("rating", 0) <= rating + 200]
                
                candidates = [f"{d.metadata.get('name')} (Rating: {d.metadata.get('rating')}, Tags: {', '.join(d.metadata.get('tags', []))})" for d in valid_docs[:5]]
            return "\n".join(candidates)
        except Exception as e:
            return f"Error retrieving candidates: {e}"

    def run(self, current_rating: int, weaknesses: list):
        """Recommend problems."""
        weaknesses_str = json.dumps(weaknesses, indent=2)
        candidates = self._get_candidates(weaknesses, current_rating)
        return self.chain.invoke({
            "current_rating": current_rating,
            "weaknesses": weaknesses_str,
            "candidate_problems": candidates
        })
