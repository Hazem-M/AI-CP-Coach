import requests
from typing import Optional, List, Dict, Any

class CodeforcesAPI:
    """Wrapper for the Codeforces API."""
    
    BASE_URL = "https://codeforces.com/api"
    
    def get_user_info(self, handle: str) -> Dict[str, Any]:
        """Fetch user profile information."""
        try:
            r = requests.get(f"{self.BASE_URL}/user.info", params={"handles": handle})
            r.raise_for_status()
            data = r.json()
            if data["status"] == "OK":
                return data["result"][0]
            else:
                raise ValueError(f"Codeforces API Error: {data.get('comment')}")
        except Exception as e:
            print(f"Error fetching user info for {handle}: {e}")
            return {}

    def get_user_submissions(self, handle: str, count: int = 1000) -> List[Dict[str, Any]]:
        """Fetch the latest submissions for a user."""
        try:
            r = requests.get(f"{self.BASE_URL}/user.status", params={"handle": handle, "count": count})
            r.raise_for_status()
            data = r.json()
            if data["status"] == "OK":
                return data["result"]
            else:
                raise ValueError(f"Codeforces API Error: {data.get('comment')}")
        except Exception as e:
            print(f"Error fetching submissions for {handle}: {e}")
            return []

    def get_problemset(self, tags: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch problems, optionally filtered by tags (semicolon separated)."""
        params = {}
        if tags:
            params["tags"] = tags
        try:
            r = requests.get(f"{self.BASE_URL}/problemset.problems", params=params)
            r.raise_for_status()
            data = r.json()
            if data["status"] == "OK":
                return data["result"]["problems"]
            else:
                raise ValueError(f"Codeforces API Error: {data.get('comment')}")
        except Exception as e:
            print(f"Error fetching problemset: {e}")
            return []

    def analyze_weaknesses(self, handle: str) -> Dict[str, Any]:
        """Analyze a user's submissions to find strengths and weaknesses based on tags and ratings."""
        submissions = self.get_user_submissions(handle)
        if not submissions:
            return {"error": "No submissions found or API error."}
            
        user_info = self.get_user_info(handle)
        user_rating = user_info.get("rating", 1200) # Default to 1200 if unrated

        tag_stats = {}
        for sub in submissions:
            if sub.get("verdict") == "OK":
                problem = sub.get("problem", {})
                for tag in problem.get("tags", []):
                    if tag not in tag_stats:
                        tag_stats[tag] = {"solved": 0, "ratings": [], "max": 0}
                    tag_stats[tag]["solved"] += 1
                    if "rating" in problem:
                        tag_stats[tag]["ratings"].append(problem["rating"])
                        tag_stats[tag]["max"] = max(tag_stats[tag]["max"], problem["rating"])

        weaknesses = []
        strengths = []
        
        for tag, stats in tag_stats.items():
            avg = sum(stats["ratings"]) / len(stats["ratings"]) if stats["ratings"] else 0
            entry = {
                "tag": tag, 
                "solved": stats["solved"], 
                "avg_rating": round(avg, 1), 
                "max": stats["max"]
            }
            # A user is weak in a tag if they haven't solved many problems, 
            # or if their average rating in that tag is significantly below their current rating.
            if stats["solved"] < 5 or avg < user_rating - 200:
                weaknesses.append(entry)
            else:
                strengths.append(entry)

        return {
            "handle": handle,
            "current_rating": user_rating,
            "max_rating": user_info.get("maxRating", 0),
            "total_solved_unique": len(set(f"{s['problem']['contestId']}{s['problem']['index']}" for s in submissions if s.get("verdict") == "OK")),
            "strengths": sorted(strengths, key=lambda x: x["avg_rating"], reverse=True),
            "weaknesses": sorted(weaknesses, key=lambda x: x["solved"]),
        }

if __name__ == "__main__":
    # Test the API
    api = CodeforcesAPI()
    print("Testing API for HazemMFarag...")
    analysis = api.analyze_weaknesses("HazemMFarag")
    print(f"Rating: {analysis.get('current_rating')}")
    print(f"Strengths: {[s['tag'] for s in analysis.get('strengths', [])][:3]}")
    print(f"Weaknesses: {[w['tag'] for w in analysis.get('weaknesses', [])][:3]}")
