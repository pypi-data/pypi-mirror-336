"""VM models for unraid_api."""
from typing import Dict, List, Optional, Any, Union, Literal

from pydantic import BaseModel, ConfigDict, Field


class VMDisk(BaseModel):
    """VM disk model."""
    
    name: str = Field(description="Disk name")
    size: str = Field(description="Disk size")
    driver: str = Field(description="Disk driver")
    interface: str = Field(description="Disk interface")
    
    model_config = ConfigDict(populate_by_name=True)


class VMNic(BaseModel):
    """VM network interface model."""
    
    name: str = Field(description="NIC name")
    mac: str = Field(description="MAC address")
    bridge: str = Field(description="Network bridge")
    
    model_config = ConfigDict(populate_by_name=True)


class VMUSBDevice(BaseModel):
    """VM USB device model."""
    
    name: str = Field(description="Device name")
    id: str = Field(description="Device ID")
    
    model_config = ConfigDict(populate_by_name=True)


class VMUSBConfig(BaseModel):
    """VM USB configuration model."""
    
    enabled: bool = Field(description="USB enabled flag")
    
    model_config = ConfigDict(populate_by_name=True)


class VMSoundConfig(BaseModel):
    """VM sound configuration model."""
    
    enabled: bool = Field(description="Sound enabled flag")
    
    model_config = ConfigDict(populate_by_name=True)


class VM(BaseModel):
    """VM model."""
    
    id: str = Field(description="VM ID")
    name: str = Field(description="VM name")
    coreCount: int = Field(description="Number of CPU cores")
    thread: Optional[int] = Field(None, description="Number of threads per core")
    memorySize: int = Field(description="Memory size in MB")
    status: str = Field(description="VM status")
    icon: Optional[str] = Field(None, description="VM icon URL")
    description: Optional[str] = Field(None, description="VM description")
    primaryGPU: Optional[str] = Field(None, description="Primary GPU")
    autostart: bool = Field(description="Autostart flag")
    template: bool = Field(description="Template flag")
    disks: List[VMDisk] = Field(default_factory=list, description="VM disks")
    nics: List[VMNic] = Field(default_factory=list, description="VM network interfaces")
    usbDevices: List[VMUSBDevice] = Field(default_factory=list, description="VM USB devices")
    usb: VMUSBConfig = Field(description="VM USB configuration")
    sound: VMSoundConfig = Field(description="VM sound configuration")
    
    model_config = ConfigDict(populate_by_name=True)


class VMTemplate(BaseModel):
    """VM template model."""
    
    id: str = Field(description="Template ID")
    name: str = Field(description="Template name")
    icon: Optional[str] = Field(None, description="Template icon URL")
    description: Optional[str] = Field(None, description="Template description")
    
    model_config = ConfigDict(populate_by_name=True)


class MutationResponse(BaseModel):
    """Mutation response model."""
    
    success: bool = Field(description="Success flag")
    message: Optional[str] = Field(None, description="Response message")
    
    model_config = ConfigDict(populate_by_name=True)
