"""
Lambalia Feedback Collection System
Handles user feedback, bug reports, feature requests, and user experience data
"""

from fastapi import HTTPException
from datetime import datetime, timezone
from typing import Dict, List, Optional
from pydantic import BaseModel, EmailStr
from enum import Enum
import uuid


class FeedbackType(str, Enum):
    GENERAL = "general"
    BUG = "bug"
    FEATURE = "feature"
    UI = "ui"
    PERFORMANCE = "performance"
    RECIPE = "recipe" 
    PAYMENT = "payment"
    VENDOR = "vendor"
    COMPLIMENT = "compliment"


class UrgencyLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FeedbackStatus(str, Enum):
    NEW = "new"
    REVIEWED = "reviewed"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class FeedbackSubmission(BaseModel):
    type: FeedbackType
    rating: int = 5  # 1-5 stars
    subject: str
    message: str
    urgency: UrgencyLevel = UrgencyLevel.LOW
    email: EmailStr
    name: str
    # Technical metadata
    platform_version: Optional[str] = "1.0"
    browser: Optional[str] = None
    url: Optional[str] = None
    user_id: Optional[str] = None


class FeedbackRecord(BaseModel):
    id: str
    submission: FeedbackSubmission
    status: FeedbackStatus = FeedbackStatus.NEW
    created_at: datetime
    updated_at: datetime
    admin_notes: Optional[str] = None
    assigned_to: Optional[str] = None
    resolved_at: Optional[datetime] = None


class FeedbackService:
    def __init__(self):
        # In production, this would be stored in MongoDB
        self.feedback_storage: Dict[str, FeedbackRecord] = {}
        self.feedback_stats = {
            "total_submissions": 0,
            "by_type": {},
            "by_urgency": {},
            "by_rating": {},
            "average_rating": 0.0,
            "resolution_rate": 0.0
        }
    
    async def submit_feedback(self, feedback: FeedbackSubmission) -> Dict:
        """Submit new user feedback"""
        try:
            # Generate unique feedback ID
            feedback_id = str(uuid.uuid4())
            
            # Create feedback record
            record = FeedbackRecord(
                id=feedback_id,
                submission=feedback,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            
            # Store feedback
            self.feedback_storage[feedback_id] = record
            
            # Update statistics
            await self._update_stats(feedback)
            
            # Trigger notifications for critical issues
            if feedback.urgency == UrgencyLevel.CRITICAL:
                await self._send_critical_alert(record)
            
            return {
                "success": True,
                "feedback_id": feedback_id,
                "message": "Feedback submitted successfully",
                "estimated_response_time": self._get_response_time(feedback.urgency)
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to submit feedback: {str(e)}")
    
    async def get_feedback_stats(self) -> Dict:
        """Get platform feedback statistics for admin dashboard"""
        total_feedback = len(self.feedback_storage)
        if total_feedback == 0:
            return self.feedback_stats
        
        # Calculate current stats
        ratings = [f.submission.rating for f in self.feedback_storage.values()]
        resolved_count = len([f for f in self.feedback_storage.values() if f.status == FeedbackStatus.RESOLVED])
        
        stats = {
            "total_submissions": total_feedback,
            "by_type": {},
            "by_urgency": {},
            "by_rating": {},
            "average_rating": sum(ratings) / len(ratings) if ratings else 0.0,
            "resolution_rate": (resolved_count / total_feedback * 100) if total_feedback > 0 else 0.0,
            "recent_feedback": await self._get_recent_feedback(5)
        }
        
        # Count by type
        for feedback in self.feedback_storage.values():
            feedback_type = feedback.submission.type
            stats["by_type"][feedback_type] = stats["by_type"].get(feedback_type, 0) + 1
            
            urgency = feedback.submission.urgency
            stats["by_urgency"][urgency] = stats["by_urgency"].get(urgency, 0) + 1
            
            rating = feedback.submission.rating
            stats["by_rating"][f"{rating}_star"] = stats["by_rating"].get(f"{rating}_star", 0) + 1
        
        return stats
    
    async def get_feedback_by_priority(self, limit: int = 20) -> List[Dict]:
        """Get feedback sorted by priority for admin review"""
        priority_order = {
            UrgencyLevel.CRITICAL: 4,
            UrgencyLevel.HIGH: 3, 
            UrgencyLevel.MEDIUM: 2,
            UrgencyLevel.LOW: 1
        }
        
        feedback_list = list(self.feedback_storage.values())
        feedback_list.sort(
            key=lambda x: (priority_order[x.submission.urgency], x.created_at),
            reverse=True
        )
        
        return [
            {
                "id": f.id,
                "type": f.submission.type,
                "urgency": f.submission.urgency,
                "rating": f.submission.rating,
                "subject": f.submission.subject,
                "message": f.submission.message[:200] + "..." if len(f.submission.message) > 200 else f.submission.message,
                "user_name": f.submission.name,
                "user_email": f.submission.email,
                "created_at": f.created_at.isoformat(),
                "status": f.status,
                "platform_info": {
                    "version": f.submission.platform_version,
                    "browser": f.submission.browser,
                    "url": f.submission.url
                }
            }
            for f in feedback_list[:limit]
        ]
    
    async def update_feedback_status(self, feedback_id: str, status: FeedbackStatus, admin_notes: Optional[str] = None) -> Dict:
        """Update feedback status (admin function)"""
        if feedback_id not in self.feedback_storage:
            raise HTTPException(status_code=404, detail="Feedback not found")
        
        record = self.feedback_storage[feedback_id]
        record.status = status
        record.updated_at = datetime.now(timezone.utc)
        
        if admin_notes:
            record.admin_notes = admin_notes
        
        if status == FeedbackStatus.RESOLVED:
            record.resolved_at = datetime.now(timezone.utc)
        
        return {
            "success": True,
            "feedback_id": feedback_id,
            "new_status": status,
            "message": f"Feedback status updated to {status}"
        }
    
    async def _update_stats(self, feedback: FeedbackSubmission):
        """Update internal statistics"""
        self.feedback_stats["total_submissions"] += 1
        
        # Update type stats
        if feedback.type not in self.feedback_stats["by_type"]:
            self.feedback_stats["by_type"][feedback.type] = 0
        self.feedback_stats["by_type"][feedback.type] += 1
        
        # Update urgency stats  
        if feedback.urgency not in self.feedback_stats["by_urgency"]:
            self.feedback_stats["by_urgency"][feedback.urgency] = 0
        self.feedback_stats["by_urgency"][feedback.urgency] += 1
    
    async def _send_critical_alert(self, record: FeedbackRecord):
        """Send alert for critical feedback (placeholder for email/Slack integration)"""
        # In production, this would send alerts via email, Slack, etc.
        print(f"🚨 CRITICAL FEEDBACK ALERT: {record.submission.subject}")
        print(f"User: {record.submission.name} ({record.submission.email})")
        print(f"Message: {record.submission.message[:100]}...")
        print(f"Feedback ID: {record.id}")
    
    def _get_response_time(self, urgency: UrgencyLevel) -> str:
        """Get estimated response time based on urgency"""
        response_times = {
            UrgencyLevel.CRITICAL: "Within 2 hours",
            UrgencyLevel.HIGH: "Within 24 hours", 
            UrgencyLevel.MEDIUM: "Within 3 business days",
            UrgencyLevel.LOW: "Within 1 week"
        }
        return response_times.get(urgency, "Within 1 week")
    
    async def _get_recent_feedback(self, count: int) -> List[Dict]:
        """Get recent feedback for dashboard"""
        recent = sorted(
            self.feedback_storage.values(),
            key=lambda x: x.created_at,
            reverse=True
        )[:count]
        
        return [
            {
                "id": f.id,
                "type": f.submission.type,
                "rating": f.submission.rating,
                "subject": f.submission.subject,
                "urgency": f.submission.urgency,
                "created_at": f.created_at.isoformat(),
                "status": f.status
            }
            for f in recent
        ]


# Global service instance
feedback_service = FeedbackService()


# Utility functions for analysis
def analyze_user_satisfaction(feedback_records: List[FeedbackRecord]) -> Dict:
    """Analyze user satisfaction trends"""
    if not feedback_records:
        return {"error": "No feedback data available"}
    
    ratings = [f.submission.rating for f in feedback_records]
    rating_distribution = {}
    for rating in range(1, 6):
        count = ratings.count(rating)
        rating_distribution[f"{rating}_star"] = {
            "count": count,
            "percentage": (count / len(ratings) * 100) if ratings else 0
        }
    
    # Calculate Net Promoter Score (NPS)
    promoters = len([r for r in ratings if r >= 4])  # 4-5 stars
    detractors = len([r for r in ratings if r <= 2])  # 1-2 stars
    nps = ((promoters - detractors) / len(ratings) * 100) if ratings else 0
    
    return {
        "average_rating": sum(ratings) / len(ratings),
        "total_feedback": len(ratings),
        "rating_distribution": rating_distribution,
        "net_promoter_score": nps,
        "satisfaction_level": "High" if nps > 50 else "Medium" if nps > 0 else "Low"
    }


def get_feedback_insights(feedback_records: List[FeedbackRecord]) -> Dict:
    """Generate actionable insights from feedback"""
    if not feedback_records:
        return {"insights": []}
    
    insights = []
    
    # Analyze feedback types
    type_counts = {}
    urgency_counts = {}
    
    for record in feedback_records:
        feedback_type = record.submission.type
        urgency = record.submission.urgency
        
        type_counts[feedback_type] = type_counts.get(feedback_type, 0) + 1
        urgency_counts[urgency] = urgency_counts.get(urgency, 0) + 1
    
    # Generate insights
    most_common_type = max(type_counts, key=type_counts.get) if type_counts else None
    if most_common_type:
        insights.append({
            "type": "most_reported_issue",
            "message": f"Most common feedback type is '{most_common_type}' ({type_counts[most_common_type]} reports)",
            "action": f"Consider prioritizing improvements in {most_common_type} area"
        })
    
    critical_count = urgency_counts.get(UrgencyLevel.CRITICAL, 0)
    if critical_count > 0:
        insights.append({
            "type": "critical_issues",
            "message": f"{critical_count} critical issues reported",
            "action": "Immediate attention required for critical feedback"
        })
    
    # Low rating insights
    low_ratings = [f for f in feedback_records if f.submission.rating <= 2]
    if len(low_ratings) > len(feedback_records) * 0.2:  # More than 20% low ratings
        insights.append({
            "type": "satisfaction_concern",
            "message": f"{len(low_ratings)} users gave ratings of 2 stars or below",
            "action": "Review user experience and address satisfaction issues"
        })
    
    return {
        "insights": insights,
        "total_analyzed": len(feedback_records),
        "generated_at": datetime.now(timezone.utc).isoformat()
    }