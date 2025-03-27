"""Notification models for unraid_api."""
from typing import Dict, List, Optional, Any, Union, Literal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class NotificationType(str, Enum):
    """Notification type enum."""
    
    NORMAL = "normal"
    WARNING = "warning"
    ALERT = "alert"
    INFO = "info"


class NotificationImportance(str, Enum):
    """Notification importance enum."""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Notification(BaseModel):
    """Notification model."""
    
    id: str = Field(description="Notification ID")
    type: NotificationType = Field(description="Notification type")
    importance: NotificationImportance = Field(description="Notification importance")
    subject: str = Field(description="Notification subject")
    description: str = Field(description="Notification description")
    timestamp: int = Field(description="Notification timestamp")
    read: bool = Field(description="Read status")
    
    model_config = ConfigDict(populate_by_name=True)


class MutationResponse(BaseModel):
    """Mutation response model."""
    
    success: bool = Field(description="Success flag")
    message: Optional[str] = Field(None, description="Response message")
    
    model_config = ConfigDict(populate_by_name=True)
