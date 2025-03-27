"""Disk data models for pyunraid."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class DiskPartition(BaseModel):
    """Model for a disk partition."""
    
    number: int = Field(..., description="The partition number")
    name: str = Field(..., description="The partition name")
    fs_type: Optional[str] = Field(None, alias="fsType", description="The filesystem type")
    mountpoint: Optional[str] = Field(None, description="The mount point")
    size: int = Field(..., description="The size of the partition in bytes")
    used: Optional[int] = Field(None, description="The used space in bytes")
    free: Optional[int] = Field(None, description="The free space in bytes")
    color: Optional[str] = Field(None, description="The color code for the partition")
    temp: Optional[int] = Field(None, description="The temperature of the partition in celsius")
    device_id: str = Field(..., alias="deviceId", description="The device identifier")
    is_array: bool = Field(..., alias="isArray", description="Whether the partition is part of the array")
    
    class Config:
        """Pydantic config."""
        
        populate_by_name = True


class Disk(BaseModel):
    """Model for a disk."""
    
    id: str = Field(..., description="The disk ID")
    device: str = Field(..., description="The device path (e.g., '/dev/sda')")
    device_id: str = Field(..., alias="deviceId", description="The device identifier")
    device_node: str = Field(..., alias="deviceNode", description="The device node")
    name: str = Field(..., description="The disk name")
    partitions: List[DiskPartition] = Field(default_factory=list, description="The partitions on the disk")
    size: int = Field(..., description="The size of the disk in bytes")
    temp: Optional[int] = Field(None, description="The temperature of the disk in celsius")
    status: str = Field(..., description="The status of the disk")
    interface: Optional[str] = Field(None, description="The disk interface")
    model: Optional[str] = Field(None, description="The disk model")
    protocol: Optional[str] = Field(None, description="The disk protocol")
    rotation_rate: Optional[int] = Field(None, alias="rotationRate", description="The disk rotation rate in RPM")
    serial: Optional[str] = Field(None, description="The disk serial number")
    type: str = Field(..., description="The disk type")
    num_reads: int = Field(..., alias="numReads", description="Number of read operations")
    num_writes: int = Field(..., alias="numWrites", description="Number of write operations")
    num_errors: int = Field(..., alias="numErrors", description="Number of errors")
    color: Optional[str] = Field(None, description="The color code for the disk")
    rotational: bool = Field(..., description="Whether the disk is rotational (HDD vs SSD)")
    vendor: Optional[str] = Field(None, description="The disk vendor")
    
    class Config:
        """Pydantic config."""
        
        populate_by_name = True
