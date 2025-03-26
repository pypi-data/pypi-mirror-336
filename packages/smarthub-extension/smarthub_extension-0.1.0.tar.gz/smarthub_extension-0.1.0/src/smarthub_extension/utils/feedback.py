"""Feedback collector for SmartHub extension"""
import logging
from datetime import datetime
from typing import Dict, Any, Optional

class FeedbackCollector:
    def __init__(self):
        self.feedback_types = {
            "feature_request": "New feature suggestion",
            "bug_report": "Report a problem",
            "query_improvement": "Query understanding needs improvement",
            "results_feedback": "Results could be better",
            "general": "General feedback"
        }
    
    def format_feedback_prompt(self) -> str:
        """Generate a user-friendly feedback prompt"""
        prompt = "I can help you submit feedback about SmartHub! Choose a feedback type:\n\n"
        for key, desc in self.feedback_types.items():
            prompt += f"• {desc} (use: '{key}')\n"
        return prompt + "\nOr just type your feedback and I'll categorize it."
    
    def categorize_feedback(self, feedback: str) -> str:
        """Automatically categorize feedback based on content"""
        feedback_lower = feedback.lower()
        
        if any(word in feedback_lower for word in ["add", "new", "want", "wish", "could have"]):
            return "feature_request"
        elif any(word in feedback_lower for word in ["wrong", "error", "bug", "broken", "not working"]):
            return "bug_report"
        elif any(word in feedback_lower for word in ["understand", "confused", "unclear", "query"]):
            return "query_improvement"
        elif any(word in feedback_lower for word in ["results", "data", "numbers", "incorrect"]):
            return "results_feedback"
        return "general"
    
    def prepare_feedback_metadata(self, 
                                feedback_type: str,
                                user_email: str,
                                context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Prepare metadata for feedback submission"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "feedback_type": feedback_type,
            "user_email": user_email,
            "extension_version": "0.1.0",  # We should get this from package metadata
            "context": context or {},
            "environment": {
                "smarthub_version": "Winter 2025",
                "source": "goose_extension"
            }
        }