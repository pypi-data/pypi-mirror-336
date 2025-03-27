"""System information models for pyunraid."""
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field


class CPUSetpoint(BaseModel):
    """Model for a CPU setpoint."""
    
    label: str = Field(..., description="The name of the setpoint")
    value: str = Field(..., description="The value of the setpoint")


class CPU(BaseModel):
    """Model for CPU information."""
    
    frequency: float = Field(..., description="The CPU frequency in MHz")
    model: str = Field(..., description="The CPU model name")
    load_avg: float = Field(..., alias="loadAvg", description="The CPU load average")
    temperature: Optional[float] = Field(None, description="The CPU temperature in celsius")
    
    class Config:
        """Pydantic config."""
        
        populate_by_name = True


class SystemInfo(BaseModel):
    """Model for system information."""
    
    name: str = Field(..., description="The system name")
    description: Optional[str] = Field(None, description="The system description")
    version: str = Field(..., description="The Unraid version")
    uptime: int = Field(..., description="The system uptime in seconds")
    local_master: bool = Field(..., alias="localMaster", description="Whether this is the local master")
    reg_guid: Optional[str] = Field(None, alias="regGUID", description="Registration GUID")
    reg_token: Optional[str] = Field(None, alias="regTOKEN", description="Registration token")
    reg_file: Optional[str] = Field(None, alias="regFILE", description="Registration file")
    reg_time: Optional[int] = Field(None, alias="regTIME", description="Registration time")
    reg_to: Optional[str] = Field(None, alias="regTO", description="Registration TO")
    update_available: bool = Field(..., alias="updateAvailable", description="Whether an update is available")
    write_journaling: bool = Field(..., alias="writeJournaling", description="Whether write journaling is enabled")
    internal_flash: Optional[str] = Field(None, alias="internalFlash", description="Internal flash type")
    show_notices: bool = Field(..., alias="showNotices", description="Whether to show notices")
    port_number: int = Field(..., alias="portNumber", description="Web UI port number")
    cpu_setpoints: List[CPUSetpoint] = Field(..., alias="cpuSetpoints", description="CPU setpoints")
    num_orphans: int = Field(..., alias="numOrphans", description="Number of orphaned files")
    alert_cpu_high: bool = Field(..., alias="alertCPUHigh", description="Whether to alert on high CPU")
    alert_memory_high: bool = Field(..., alias="alertMemoryHigh", description="Whether to alert on high memory")
    alert_disk_utilization_high: bool = Field(..., alias="alertDiskUtilizationHigh", description="Whether to alert on high disk utilization")
    alert_disk_temp_high: bool = Field(..., alias="alertDiskTempHigh", description="Whether to alert on high disk temperature")
    display_board_model: Optional[str] = Field(None, alias="displayBoardModel", description="The display board model")
    processor_count: int = Field(..., alias="processorCount", description="Number of processors")
    memory: int = Field(..., description="Total memory in bytes")
    load_avg: float = Field(..., alias="loadAvg", description="System load average")
    cpu: CPU = Field(..., description="CPU information")
    
    class Config:
        """Pydantic config."""
        
        populate_by_name = True


class DockerInfo(BaseModel):
    """Model for Docker information."""
    
    enabled: bool = Field(..., description="Whether Docker is enabled")
    version: str = Field(..., description="Docker version")
    status: str = Field(..., description="Docker status")
    root_path: str = Field(..., alias="rootPath", description="Docker root path")
    config_path: str = Field(..., alias="configPath", description="Docker config path")
    image_path: str = Field(..., alias="imagePath", description="Docker image path")
    autostart: bool = Field(..., description="Whether Docker autostart is enabled")
    network_default: str = Field(..., alias="networkDefault", description="Default Docker network")
    custom_networks: List[str] = Field(..., alias="customNetworks", description="Custom Docker networks")
    privileged: bool = Field(..., description="Whether privileged mode is enabled")
    log_rotation: bool = Field(..., alias="logRotation", description="Whether log rotation is enabled")
    
    class Config:
        """Pydantic config."""
        
        populate_by_name = True


class VMInfo(BaseModel):
    """Model for VM information."""
    
    enabled: bool = Field(..., description="Whether VM support is enabled")
    version: str = Field(..., description="VM version")
    status: str = Field(..., description="VM status")
    core_path: str = Field(..., alias="corePath", description="VM core path")
    config_path: str = Field(..., alias="configPath", description="VM config path")
    image_path: str = Field(..., alias="imagePath", description="VM image path")
    autostart: bool = Field(..., description="Whether VM autostart is enabled")
    win_vm_count: int = Field(..., alias="winVmCount", description="Number of Windows VMs")
    linux_vm_count: int = Field(..., alias="linuxVmCount", description="Number of Linux VMs")
    other_vm_count: int = Field(..., alias="otherVmCount", description="Number of other VMs")
    cpu_isolated_cores: List[int] = Field(..., alias="CPUisolatedCores", description="CPU isolated cores")
    pcie_iommu_groups: List[int] = Field(..., alias="PCIeiommuGroups", description="PCIe IOMMU groups")
    
    class Config:
        """Pydantic config."""
        
        populate_by_name = True
