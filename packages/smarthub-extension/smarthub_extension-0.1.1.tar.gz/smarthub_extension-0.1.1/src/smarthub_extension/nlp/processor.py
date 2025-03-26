"""Natural Language Query Processor for SmartHub"""
from typing import Dict, Any, List, Optional

class NLPProcessor:
    def __init__(self):
        self.patterns = {
            # Existing patterns
            "retention_analysis": {
                "keywords": ["retention", "churn", "at risk", "churned", "retention opportunity"],
                "risk_levels": ["high risk", "medium risk", "low risk"]
            },
            
            # New Winter 2025 features
            "seller_signals": {
                "gtm": ["card repricing", "cp reprice", "$ impact"],
                "hardware": ["a-device replacement", "square a device"],
                "superpos": ["superpos status", "superpos mode"],
                "leads": ["public web leads", "contact sales"]
            },
            
            "gpv_analysis": {
                "metrics": ["gpv", "processing volume"],
                "comparisons": ["year-over-year", "quarter-over-quarter", "yoy", "qoq"],
                "variable_comp": ["variable compensation", "comp eligible", "excluded sellers"]
            },
            
            # Strategic view segments
            "strategic_segments": {
                "pending": ["not contacted", "pending contact"],
                "attempted": ["contact attempted", "tried contacting"],
                "engaged": ["dm conversation", "engaged this quarter"],
                "all_accounts": ["all accounts", "full portfolio"]
            },
            
            "contact_tracking": {
                "last_contact": ["last dm", "previous contact", "last conversation"],
                "breadth": ["breadth tracking", "contact targets"]
            },
            
            "merchant_identifiers": {
                "business_id": ["business id", "parent account"],
                "merchant_token": ["merchant token", "specific location"],
                "new_seller": ["new this quarter", "newly added"]
            }
        }
        
    def parse_query(self, query: str) -> Dict[str, Any]:
        """Parse natural language query with Winter 2025 features"""
        query = query.lower()
        intent = self._detect_intent(query)
        params = self._extract_parameters(query, intent)
        
        # Handle view-specific logic
        if "strategic" in query:
            params["view_type"] = "strategic"
            params["tabs"] = self._detect_strategic_tabs(query)
        
        return {
            "intent": intent,
            "parameters": params,
            "original_query": query
        }
    
    def _detect_strategic_tabs(self, query: str) -> List[str]:
        """Detect which strategic tabs to include"""
        tabs = []
        for tab, patterns in self.patterns["strategic_segments"].items():
            if any(pattern in query for pattern in patterns):
                tabs.append(tab)
        return tabs or ["all_accounts"]  # Default to all accounts if no specific tab mentioned
        
    def _extract_parameters(self, query: str, intent: str) -> Dict[str, Any]:
        """Extract parameters with support for new features"""
        params = {}
        
        # Check for specific signals
        for signal_type, patterns in self.patterns["seller_signals"].items():
            if any(pattern in query for pattern in patterns):
                params["signal_type"] = signal_type
        
        # Handle GPV analysis parameters
        if intent == "gpv_analysis":
            params["comparison_type"] = self._detect_comparison_type(query)
            params["include_variable_comp"] = "variable" in query or "compensation" in query
        
        # Add merchant identifier type
        params["identifier_type"] = self._detect_identifier_type(query)
        
        return params
    
    def _detect_comparison_type(self, query: str) -> str:
        """Detect GPV comparison type"""
        if any(term in query for term in ["yoy", "year-over-year", "year over year"]):
            return "yoy"
        elif any(term in query for term in ["qoq", "quarter-over-quarter", "quarter over quarter"]):
            return "qoq"
        return "current"  # Default to current period
        
    def _detect_identifier_type(self, query: str) -> str:
        """Detect which identifier to use"""
        if any(term in query for term in self.patterns["merchant_identifiers"]["business_id"]):
            return "business_id"
        elif any(term in query for term in self.patterns["merchant_identifiers"]["merchant_token"]):
            return "merchant_token"
        return "auto"  # Let the system decide based on context
        
    def _detect_intent(self, query: str) -> str:
        """Detect the primary intent of the query"""
        # Check for portfolio segment specific queries first
        for segment, patterns in self.patterns["strategic_segments"].items():
            if any(pattern in query for pattern in patterns):
                return "portfolio_segment_analysis"
        
        # Then check other intents
        if any(kw in query for kw in self.patterns["gpv_analysis"]["metrics"]):
            return "gpv_analysis"
        elif any(kw in query for kw in self.patterns["seller_signals"]["gtm"]):
            return "gtm_analysis"
        return "general_analysis"