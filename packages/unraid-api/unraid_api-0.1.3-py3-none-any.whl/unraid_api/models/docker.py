"""Docker models for unraid_api."""
from typing import Dict, List, Optional, Any, Union

from pydantic import BaseModel, ConfigDict, Field


class DockerPort(BaseModel):
    """Docker port mapping model."""
    
    IP: str = Field(description="IP address for the port mapping")
    PrivatePort: int = Field(description="Private port inside the container")
    PublicPort: Optional[int] = Field(None, description="Public port on the host")
    Type: str = Field(description="Port type (e.g., tcp, udp)")
    
    model_config = ConfigDict(populate_by_name=True)


class DockerMount(BaseModel):
    """Docker mount model."""
    
    name: Optional[str] = Field(None, description="Name of the mount")
    source: str = Field(description="Source path on the host")
    destination: str = Field(description="Destination path in the container")
    driver: Optional[str] = Field(None, description="Mount driver")
    mode: str = Field(description="Mount mode")
    rw: bool = Field(description="Read/write flag")
    propagation: Optional[str] = Field(None, description="Mount propagation")
    
    model_config = ConfigDict(populate_by_name=True)


class DockerContainer(BaseModel):
    """Docker container model."""
    
    id: str = Field(description="Container ID")
    name: str = Field(description="Container name")
    image: str = Field(description="Image name")
    imageId: str = Field(description="Image ID")
    status: str = Field(description="Container status")
    state: str = Field(description="Container state")
    created: int = Field(description="Creation timestamp")
    started: Optional[int] = Field(None, description="Start timestamp")
    finished: Optional[int] = Field(None, description="Finish timestamp")
    exitCode: Optional[int] = Field(None, description="Exit code")
    autostart: bool = Field(description="Autostart flag")
    network: str = Field(description="Network mode")
    repository: str = Field(description="Image repository")
    command: str = Field(description="Container command")
    registry: Optional[str] = Field(None, description="Image registry")
    index: Optional[str] = Field(None, description="Image index")
    nohc: Optional[bool] = Field(None, description="No health check flag")
    temp: Optional[float] = Field(None, description="Container temperature")
    cpuPercent: float = Field(description="CPU usage percentage")
    memUsage: int = Field(description="Memory usage in bytes")
    memLimit: int = Field(description="Memory limit in bytes")
    memPercent: float = Field(description="Memory usage percentage")
    networkMode: str = Field(description="Network mode")
    privileged: bool = Field(description="Privileged flag")
    restartPolicy: str = Field(description="Restart policy")
    logRotation: Optional[str] = Field(None, description="Log rotation policy")
    ports: List[DockerPort] = Field(default_factory=list, description="Port mappings")
    mounts: List[DockerMount] = Field(default_factory=list, description="Volume mounts")
    icon: Optional[str] = Field(None, description="Container icon URL")
    
    model_config = ConfigDict(populate_by_name=True)


class DockerImage(BaseModel):
    """Docker image model."""
    
    id: str = Field(description="Image ID")
    name: str = Field(description="Image name")
    repository: str = Field(description="Image repository")
    tag: str = Field(description="Image tag")
    created: int = Field(description="Creation timestamp")
    size: int = Field(description="Image size in bytes")
    containers: List[str] = Field(default_factory=list, description="Container IDs using this image")
    
    model_config = ConfigDict(populate_by_name=True)


class DockerNetwork(BaseModel):
    """Docker network model."""
    
    id: str = Field(description="Network ID")
    name: str = Field(description="Network name")
    driver: str = Field(description="Network driver")
    scope: str = Field(description="Network scope")
    subnet: Optional[str] = Field(None, description="Network subnet")
    gateway: Optional[str] = Field(None, description="Network gateway")
    containers: List[str] = Field(default_factory=list, description="Container IDs connected to this network")
    
    model_config = ConfigDict(populate_by_name=True)


class MutationResponse(BaseModel):
    """Mutation response model."""
    
    success: bool = Field(description="Success flag")
    message: Optional[str] = Field(None, description="Response message")
    
    model_config = ConfigDict(populate_by_name=True)
