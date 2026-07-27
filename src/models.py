from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

# ==========================================
# ENUMS
# ==========================================

class ProblemTag(str, Enum):
    DP = "dp"
    GRAPHS = "graphs"
    GREEDY = "greedy"
    BINARY_SEARCH = "binary search"
    MATH = "math"
    STRINGS = "strings"
    TREES = "trees"
    DATA_STRUCTURES = "data structures"
    SORTING = "sortings"
    DFS_BFS = "dfs and similar"
    TWO_POINTERS = "two pointers"
    NUMBER_THEORY = "number theory"
    GEOMETRY = "geometry"
    BRUTE_FORCE = "brute force"
    CONSTRUCTIVE = "constructive algorithms"
    BITMASKS = "bitmasks"
    DIVIDE_AND_CONQUER = "divide and conquer"
    OTHER = "other"

class Verdict(str, Enum):
    CORRECT = "correct"
    WRONG_ANSWER = "wrong_answer"
    TLE = "time_limit_exceeded"
    MLE = "memory_limit_exceeded"
    RUNTIME_ERROR = "runtime_error"
    PARTIALLY_CORRECT = "partially_correct"

class HintLevel(str, Enum):
    NUDGE = "nudge"
    APPROACH = "approach"
    DETAILED = "detailed"
    SOLUTION = "solution"

# ==========================================
# PROBLEM ANALYSIS MODELS
# ==========================================

class ProblemAnalysis(BaseModel):
    problem_name: str
    problem_url: Optional[str] = None
    estimated_rating: int = Field(ge=800, le=3500, description="Codeforces rating")
    tags: List[ProblemTag]
    key_observations: List[str] = Field(description="Key insights required to solve the problem")
    suggested_approach: str = Field(description="The algorithmic approach to solve it")
    time_complexity: str
    space_complexity: str
    similar_problems: List[str] = Field(description="Names of similar problems for practice")
    prerequisite_topics: List[str] = Field(description="Topics you must know to solve this")

# ==========================================
# HINT MODELS
# ==========================================

class Hint(BaseModel):
    level: HintLevel
    content: str
    reveals: str = Field(description="What this hint reveals to the user")

class HintResponse(BaseModel):
    problem_name: str
    hints: List[Hint]  # Ordered from nudge to solution
    thinking_questions: List[str] = Field(
        description="Questions to guide the user's thinking process"
    )

# ==========================================
# SOLUTION REVIEW MODELS
# ==========================================

class CodeIssue(BaseModel):
    line_number: Optional[int] = None
    issue_type: str = Field(description="'bug', 'tle_risk', 'style', or 'edge_case'")
    severity: str = Field(description="'critical', 'warning', or 'suggestion'")
    description: str
    fix: str = Field(description="How to fix this issue")

class SolutionReview(BaseModel):
    verdict: Verdict
    issues: List[CodeIssue]
    time_complexity_user: str = Field(description="Time complexity of the user's solution")
    time_complexity_optimal: str = Field(description="Optimal time complexity for the problem")
    is_optimal: bool
    optimization_suggestions: List[str]
    corrected_code: Optional[str] = Field(description="The fully corrected and optimized code")
    edge_cases_missed: List[str]
    score: float = Field(ge=0, le=100, description="Quality score of the solution")

# ==========================================
# PROFILE ANALYSIS MODELS
# ==========================================

class TopicStrength(BaseModel):
    tag: str
    solved_count: int
    avg_rating_solved: float
    max_rating_solved: int
    strength_level: str = Field(description="'weak', 'medium', 'strong', or 'expert'")

class ProfileAnalysis(BaseModel):
    handle: str
    current_rating: int
    max_rating: int
    total_solved: int
    strengths: List[TopicStrength]
    weaknesses: List[TopicStrength]
    rating_trend: str = Field(description="'improving', 'stable', or 'declining'")
    recommended_rating_range: str = Field(
        description="The rating range the user should practice in (e.g., '1400-1600')"
    )
    training_plan: List[str] = Field(description="Actionable steps to improve")
    problems_to_solve: List[str] = Field(description="Specific topics or problems to focus on")

# ==========================================
# RECOMMENDATION MODELS
# ==========================================

class RecommendedProblem(BaseModel):
    name: str
    contest_id: int
    index: str
    rating: int
    tags: List[str]
    url: str
    reason: str = Field(description="Why this problem is recommended for the user")

class Recommendations(BaseModel):
    weak_topics: List[str]
    problems: List[RecommendedProblem]
    daily_target: int = Field(description="Recommended number of problems to solve daily")
    estimated_days_to_next_rank: Optional[int] = None
