from langchain_core.output_parsers import PydanticOutputParser
from src.models import (
    ProblemAnalysis,
    HintResponse,
    SolutionReview,
    ProfileAnalysis,
    Recommendations
)

class CPOutputParsers:
    """Provides Pydantic output parsers for the various AI chains."""

    @staticmethod
    def get_problem_analysis_parser() -> PydanticOutputParser:
        return PydanticOutputParser(pydantic_object=ProblemAnalysis)

    @staticmethod
    def get_hint_response_parser() -> PydanticOutputParser:
        return PydanticOutputParser(pydantic_object=HintResponse)

    @staticmethod
    def get_solution_review_parser() -> PydanticOutputParser:
        return PydanticOutputParser(pydantic_object=SolutionReview)

    @staticmethod
    def get_profile_analysis_parser() -> PydanticOutputParser:
        return PydanticOutputParser(pydantic_object=ProfileAnalysis)

    @staticmethod
    def get_recommendations_parser() -> PydanticOutputParser:
        return PydanticOutputParser(pydantic_object=Recommendations)

    @staticmethod
    def get_format_instructions() -> dict:
        """Helper to get format instructions for all parsers to inject into prompts."""
        return {
            "problem_analysis": CPOutputParsers.get_problem_analysis_parser().get_format_instructions(),
            "hint_response": CPOutputParsers.get_hint_response_parser().get_format_instructions(),
            "solution_review": CPOutputParsers.get_solution_review_parser().get_format_instructions(),
            "profile_analysis": CPOutputParsers.get_profile_analysis_parser().get_format_instructions(),
            "recommendations": CPOutputParsers.get_recommendations_parser().get_format_instructions(),
        }
