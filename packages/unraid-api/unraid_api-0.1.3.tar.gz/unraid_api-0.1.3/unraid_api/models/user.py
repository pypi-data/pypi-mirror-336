"""User models for unraid_api."""
from typing import Dict, List, Optional, Any, Union
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserRole(str, Enum):
    """User role enum."""
    
    ADMIN = "admin"
    USER = "user"
    READONLY = "readonly"


class User(BaseModel):
    """User model."""
    
    id: str = Field(description="User ID")
    username: str = Field(description="Username")
    name: Optional[str] = Field(None, description="Display name")
    description: Optional[str] = Field(None, description="User description")
    roles: List[str] = Field(default_factory=list, description="User roles")
    lastLogin: Optional[int] = Field(None, description="Last login timestamp")
    email: Optional[str] = Field(None, description="Email address")
    
    model_config = ConfigDict(populate_by_name=True)


class CreateUserInput(BaseModel):
    """Create user input model."""
    
    username: str = Field(description="Username")
    password: str = Field(description="Password")
    name: Optional[str] = Field(None, description="Display name")
    description: Optional[str] = Field(None, description="User description")
    roles: Optional[List[str]] = Field(None, description="User roles")
    email: Optional[str] = Field(None, description="Email address")
    
    model_config = ConfigDict(populate_by_name=True)


class UpdateUserInput(BaseModel):
    """Update user input model."""
    
    username: Optional[str] = Field(None, description="Username")
    name: Optional[str] = Field(None, description="Display name")
    description: Optional[str] = Field(None, description="User description")
    roles: Optional[List[str]] = Field(None, description="User roles")
    email: Optional[str] = Field(None, description="Email address")
    
    model_config = ConfigDict(populate_by_name=True)


class UserMutationResponse(BaseModel):
    """User mutation response model."""
    
    success: bool = Field(description="Success flag")
    message: Optional[str] = Field(None, description="Response message")
    user: Optional[User] = Field(None, description="User data")
    
    model_config = ConfigDict(populate_by_name=True)


class MutationResponse(BaseModel):
    """General mutation response model."""
    
    success: bool = Field(description="Success flag")
    message: Optional[str] = Field(None, description="Response message")
    
    model_config = ConfigDict(populate_by_name=True)
