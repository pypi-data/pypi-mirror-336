"""Response formatter for SmartHub queries"""
from typing import Dict, Any, List, Optional

class ResponseFormatter:
    def format_retention_response(self, results: Dict[str, Any]) -> str:
        """Format retention analysis results with new model context"""
        response_parts = []
        
        # Add summary
        merchant_count = len(results.get("results", []))
        response_parts.append(
            f"Found {merchant_count} high-priority retention opportunities "
            f"(Annualized GPV ≥ $175K, Churn Score > 0.05)"
        )
        
        # Add merchant details
        if merchant_count > 0:
            response_parts.append("\nPriority retention opportunities:")
            for merchant in results["results"][:5]:  # Show top 5
                response_parts.append(
                    f"• {merchant['business_name']}\n"
                    f"  - Risk Level: {merchant['risk_level']}\n"
                    f"  - Annualized GPV: ${merchant['annualized_gpv']:,.2f}\n"
                    f"  - Alert Type: {merchant['alert_type']}\n"
                    f"  - Active Products: {merchant['active_products']}\n"
                    f"  - 12w GPV Trend: {merchant['gpv_12w_trend']}%"
                )
        
        # Add context about the model
        response_parts.append(
            "\n📊 Model Context:\n"
            "- Based on new Churn ML Model (Dec 2023)\n"
            "- Considers 650+ indicators including processing history, product usage, and CS interactions\n"
            "- Focuses on high-value, high-risk merchants for targeted outreach"
        )
        
        # Add Looker link
        looker_url = self._generate_looker_url(results)
        if looker_url:
            response_parts.append(f"\nView detailed analysis: [Open in Looker]({looker_url})")
        
        return "\n".join(response_parts)

    def _generate_looker_url(self, results: Dict[str, Any]) -> Optional[str]:
        """Generate Looker dashboard URL with appropriate filters"""
        # Implementation will depend on your Looker dashboard structure
        return "https://square.cloud.looker.com/dashboards/..."

    def format_pipeline_response(self, results: Dict[str, Any]) -> str:
        """Format pipeline analysis results"""
        response_parts = []
        
        # Add summary
        merchant_count = len(results.get("results", []))
        response_parts.append(f"Found {merchant_count} pipeline merchants with significant growth in the last 30 days.")
        
        # Add merchant details
        if merchant_count > 0:
            response_parts.append("\nTop growing pipeline merchants:")
            for merchant in results["results"][:5]:  # Show top 5
                response_parts.append(
                    f"• {merchant['business_name']}\n"
                    f"  - Growth: {merchant['growth_pct']:.1f}% in last 30 days\n"
                    f"  - Current GPV: ${merchant['current_gpv']:,.2f}\n"
                    f"  - Pipeline Stage: {merchant['pipeline_stage']}"
                )
        
        # Add Looker link
        looker_url = self._generate_looker_url(results)
        if looker_url:
            response_parts.append(f"\nView detailed analysis: [Open in Looker]({looker_url})")
        
        return "\n".join(response_parts)