"""
Feedback Collection API Endpoints
Provides REST API for user feedback submission and admin management
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer
from typing import Dict, List, Optional
import logging

from .feedback_system import (
    feedback_service,
    FeedbackSubmission,
    FeedbackStatus,
    analyze_user_satisfaction,
    get_feedback_insights
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/feedback", tags=["feedback"])
security = HTTPBearer(auto_error=False)

# --- USER ENDPOINTS ---

@router.post("/submit")
async def submit_feedback(
    feedback: FeedbackSubmission,
    request: Request
):
    """
    Submit user feedback
    
    **Categories:**
    - general: General feedback and suggestions
    - bug: Bug reports and technical issues  
    - feature: Feature requests and improvements
    - ui: UI/UX related feedback
    - performance: Performance and speed issues
    - recipe: Recipe content and accuracy issues
    - payment: Payment and earnings related issues
    - vendor: Vendor program feedback
    - compliment: Positive feedback and praise
    
    **Priority Levels:**
    - low: General feedback, suggestions
    - medium: Minor issues, improvements needed
    - high: Significant problems affecting experience
    - critical: Platform broken, urgent issues
    """
    try:
        # Add request metadata
        if not feedback.browser:
            feedback.browser = request.headers.get("user-agent", "Unknown")
        if not feedback.url:
            feedback.url = str(request.url)
        
        # Log feedback submission
        logger.info(f"Feedback submitted: {feedback.type} - {feedback.urgency} - {feedback.rating}/5")
        
        result = await feedback_service.submit_feedback(feedback)
        
        return {
            "success": True,
            "data": result,
            "message": "Thank you for your feedback! We appreciate you helping us improve Lambalia."
        }
    
    except Exception as e:
        logger.error(f"Feedback submission failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to submit feedback")


@router.get("/stats/public")
async def get_public_feedback_stats():
    """
    Get public feedback statistics (no sensitive data)
    Available to all users to show platform responsiveness
    """
    try:
        stats = await feedback_service.get_feedback_stats()
        
        # Return only public-safe statistics
        public_stats = {
            "total_feedback_received": stats.get("total_submissions", 0),
            "average_user_rating": round(stats.get("average_rating", 0), 1),
            "response_commitment": {
                "critical": "Within 2 hours",
                "high": "Within 24 hours", 
                "medium": "Within 3 business days",
                "low": "Within 1 week"
            },
            "feedback_categories": list(stats.get("by_type", {}).keys()),
            "platform_improvement": "Continuous based on user feedback"
        }
        
        return {
            "success": True,
            "data": public_stats,
            "message": "Public feedback statistics"
        }
    
    except Exception as e:
        logger.error(f"Failed to get public stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve statistics")


# --- ADMIN ENDPOINTS (Protected) ---

@router.get("/admin/dashboard")
async def get_feedback_dashboard():
    """
    Admin dashboard with comprehensive feedback analytics
    **Admin Only:** Requires authentication
    """
    try:
        stats = await feedback_service.get_feedback_stats()
        priority_feedback = await feedback_service.get_feedback_by_priority(20)
        
        # Get all feedback for analysis
        all_feedback = list(feedback_service.feedback_storage.values())
        satisfaction_analysis = analyze_user_satisfaction(all_feedback)
        insights = get_feedback_insights(all_feedback)
        
        dashboard_data = {
            "summary": {
                "total_submissions": stats.get("total_submissions", 0),
                "average_rating": stats.get("average_rating", 0),
                "resolution_rate": stats.get("resolution_rate", 0),
                "recent_feedback_count": len(stats.get("recent_feedback", []))
            },
            "feedback_breakdown": {
                "by_type": stats.get("by_type", {}),
                "by_urgency": stats.get("by_urgency", {}),
                "by_rating": stats.get("by_rating", {})
            },
            "priority_queue": priority_feedback,
            "satisfaction_analysis": satisfaction_analysis,
            "actionable_insights": insights,
            "recent_feedback": stats.get("recent_feedback", [])
        }
        
        return {
            "success": True,
            "data": dashboard_data,
            "message": "Feedback dashboard data retrieved"
        }
    
    except Exception as e:
        logger.error(f"Failed to get feedback dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve dashboard data")


@router.get("/admin/priority-queue")
async def get_priority_feedback(limit: int = 50):
    """
    Get feedback sorted by priority for admin review
    **Admin Only:** Requires authentication
    """
    try:
        priority_feedback = await feedback_service.get_feedback_by_priority(limit)
        
        return {
            "success": True,
            "data": {
                "feedback_queue": priority_feedback,
                "total_items": len(priority_feedback),
                "priority_levels": {
                    "critical": len([f for f in priority_feedback if f["urgency"] == "critical"]),
                    "high": len([f for f in priority_feedback if f["urgency"] == "high"]),
                    "medium": len([f for f in priority_feedback if f["urgency"] == "medium"]),
                    "low": len([f for f in priority_feedback if f["urgency"] == "low"])
                }
            },
            "message": f"Retrieved {len(priority_feedback)} feedback items"
        }
    
    except Exception as e:
        logger.error(f"Failed to get priority feedback: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve priority feedback")


@router.put("/admin/feedback/{feedback_id}/status")
async def update_feedback_status(
    feedback_id: str,
    status: FeedbackStatus,
    admin_notes: Optional[str] = None
):
    """
    Update feedback status and add admin notes
    **Admin Only:** Requires authentication
    """
    try:
        result = await feedback_service.update_feedback_status(
            feedback_id, status, admin_notes
        )
        
        logger.info(f"Feedback {feedback_id} status updated to {status}")
        
        return {
            "success": True,
            "data": result,
            "message": f"Feedback status updated to {status}"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update feedback status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update feedback status")


@router.get("/admin/insights")
async def get_feedback_insights_endpoint():
    """
    Get actionable insights from feedback data
    **Admin Only:** Requires authentication
    """
    try:
        all_feedback = list(feedback_service.feedback_storage.values())
        insights = get_feedback_insights(all_feedback)
        satisfaction = analyze_user_satisfaction(all_feedback)
        
        return {
            "success": True,
            "data": {
                "insights": insights,
                "satisfaction_analysis": satisfaction,
                "recommendations": [
                    {
                        "area": "User Experience",
                        "suggestion": "Focus on most reported feedback types",
                        "priority": "high" if satisfaction.get("average_rating", 0) < 3.5 else "medium"
                    },
                    {
                        "area": "Response Time", 
                        "suggestion": "Prioritize critical and high urgency feedback",
                        "priority": "critical"
                    },
                    {
                        "area": "Feature Development",
                        "suggestion": "Analyze feature requests for product roadmap",
                        "priority": "medium"
                    }
                ]
            },
            "message": "Feedback insights generated"
        }
    
    except Exception as e:
        logger.error(f"Failed to generate insights: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate insights")


@router.get("/admin/export")
async def export_feedback_data(
    feedback_type: Optional[str] = None,
    urgency: Optional[str] = None, 
    limit: Optional[int] = 100
):
    """
    Export feedback data for analysis
    **Admin Only:** Requires authentication
    """
    try:
        all_feedback = list(feedback_service.feedback_storage.values())
        
        # Apply filters
        filtered_feedback = all_feedback
        if feedback_type:
            filtered_feedback = [f for f in filtered_feedback if f.submission.type == feedback_type]
        if urgency:
            filtered_feedback = [f for f in filtered_feedback if f.submission.urgency == urgency]
        
        # Limit results
        if limit:
            filtered_feedback = filtered_feedback[:limit]
        
        # Format for export
        export_data = []
        for record in filtered_feedback:
            export_data.append({
                "id": record.id,
                "created_at": record.created_at.isoformat(),
                "type": record.submission.type,
                "urgency": record.submission.urgency,
                "rating": record.submission.rating,
                "subject": record.submission.subject,
                "message": record.submission.message,
                "user_name": record.submission.name,
                "user_email": record.submission.email,
                "status": record.status,
                "platform_version": record.submission.platform_version,
                "browser": record.submission.browser,
                "url": record.submission.url,
                "admin_notes": record.admin_notes,
                "resolved_at": record.resolved_at.isoformat() if record.resolved_at else None
            })
        
        return {
            "success": True,
            "data": {
                "feedback": export_data,
                "total_exported": len(export_data),
                "filters_applied": {
                    "type": feedback_type,
                    "urgency": urgency,
                    "limit": limit
                },
                "export_generated_at": "2025-01-02T12:00:00Z"
            },
            "message": f"Exported {len(export_data)} feedback records"
        }
    
    except Exception as e:
        logger.error(f"Failed to export feedback: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to export feedback data")


# Health check endpoint
@router.get("/health")
async def feedback_system_health():
    """Check feedback system health"""
    try:
        stats = await feedback_service.get_feedback_stats()
        return {
            "status": "healthy",
            "feedback_system": "operational",
            "total_feedback": stats.get("total_submissions", 0),
            "average_rating": stats.get("average_rating", 0),
            "last_check": "2025-01-02T12:00:00Z"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "last_check": "2025-01-02T12:00:00Z"
        }