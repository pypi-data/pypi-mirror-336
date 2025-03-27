"""Config models for unraid_api."""
from typing import Dict, List, Optional, Any, Union, Literal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, EmailStr


class NetworkInterface(BaseModel):
    """Network interface model."""
    
    name: str = Field(description="Interface name")
    mac: str = Field(description="MAC address")
    ip: Optional[str] = Field(None, description="IP address")
    netmask: Optional[str] = Field(None, description="Netmask")
    gateway: Optional[str] = Field(None, description="Gateway")
    up: bool = Field(description="Interface up status")
    speed: Optional[int] = Field(None, description="Interface speed")
    duplex: Optional[str] = Field(None, description="Interface duplex mode")
    
    model_config = ConfigDict(populate_by_name=True)


class NetworkConfig(BaseModel):
    """Network configuration model."""
    
    interfaces: List[NetworkInterface] = Field(default_factory=list, description="Network interfaces")
    dnsServers: List[str] = Field(default_factory=list, description="DNS servers")
    hostname: str = Field(description="Network hostname")
    
    model_config = ConfigDict(populate_by_name=True)


class CPUConfig(BaseModel):
    """CPU configuration model."""
    
    model: str = Field(description="CPU model")
    cores: int = Field(description="CPU cores")
    threads: int = Field(description="CPU threads")
    
    model_config = ConfigDict(populate_by_name=True)


class MemoryConfig(BaseModel):
    """Memory configuration model."""
    
    total: int = Field(description="Total memory in bytes")
    used: int = Field(description="Used memory in bytes")
    free: int = Field(description="Free memory in bytes")
    
    model_config = ConfigDict(populate_by_name=True)


class DisplayConfig(BaseModel):
    """Display configuration model."""
    
    branding: str = Field(description="UI branding")
    theme: str = Field(description="UI theme")
    language: str = Field(description="UI language")
    
    model_config = ConfigDict(populate_by_name=True)


class EmailConfig(BaseModel):
    """Email notification configuration model."""
    
    enabled: bool = Field(description="Email notifications enabled")
    to: Optional[str] = Field(None, description="Recipient email")
    from_field: Optional[str] = Field(None, alias="from", description="Sender email")
    server: Optional[str] = Field(None, description="SMTP server")
    port: Optional[int] = Field(None, description="SMTP port")
    secure: bool = Field(description="Use secure connection")
    authType: Optional[str] = Field(None, description="Authentication type")
    username: Optional[str] = Field(None, description="SMTP username")
    
    model_config = ConfigDict(populate_by_name=True)


class PushoverConfig(BaseModel):
    """Pushover notification configuration model."""
    
    enabled: bool = Field(description="Pushover notifications enabled")
    userKey: Optional[str] = Field(None, description="Pushover user key")
    appKey: Optional[str] = Field(None, description="Pushover app key")
    
    model_config = ConfigDict(populate_by_name=True)


class NotificationAgents(BaseModel):
    """Notification agents configuration model."""
    
    arrayStart: bool = Field(description="Notify on array start")
    arrayStop: bool = Field(description="Notify on array stop")
    diskWarning: bool = Field(description="Notify on disk warning")
    cpuWarning: bool = Field(description="Notify on CPU warning")
    memoryWarning: bool = Field(description="Notify on memory warning")
    updateAvailable: bool = Field(description="Notify on update available")
    
    model_config = ConfigDict(populate_by_name=True)


class NotificationsConfig(BaseModel):
    """Notifications configuration model."""
    
    email: EmailConfig = Field(description="Email configuration")
    pushover: PushoverConfig = Field(description="Pushover configuration")
    agents: NotificationAgents = Field(description="Notification agents configuration")
    
    model_config = ConfigDict(populate_by_name=True)


class VMConfig(BaseModel):
    """VM configuration model."""
    
    enabled: bool = Field(description="VMs enabled")
    isolatedCpuPinning: bool = Field(description="Isolated CPU pinning")
    pciPassthrough: bool = Field(description="PCI passthrough enabled")
    
    model_config = ConfigDict(populate_by_name=True)


class DockerConfig(BaseModel):
    """Docker configuration model."""
    
    enabled: bool = Field(description="Docker enabled")
    auto: bool = Field(description="Docker autostart")
    image: Optional[str] = Field(None, description="Default image")
    privileged: bool = Field(description="Default privileged mode")
    
    model_config = ConfigDict(populate_by_name=True)


class SharesConfig(BaseModel):
    """Shares configuration model."""
    
    enableNetbios: bool = Field(description="NetBIOS enabled")
    enableWsd: bool = Field(description="WSD enabled")
    enableAvahi: bool = Field(description="Avahi enabled")
    localMaster: bool = Field(description="Local master")
    security: str = Field(description="Security mode")
    
    model_config = ConfigDict(populate_by_name=True)


class FTPConfig(BaseModel):
    """FTP configuration model."""
    
    enabled: bool = Field(description="FTP enabled")
    port: int = Field(description="FTP port")
    allowReset: bool = Field(description="Allow password reset")
    publicAccess: bool = Field(description="Public access")
    
    model_config = ConfigDict(populate_by_name=True)


class DynamicDNSConfig(BaseModel):
    """Dynamic DNS configuration model."""
    
    enabled: bool = Field(description="Dynamic DNS enabled")
    service: Optional[str] = Field(None, description="Dynamic DNS service")
    domain: Optional[str] = Field(None, description="Domain name")
    username: Optional[str] = Field(None, description="Service username")
    
    model_config = ConfigDict(populate_by_name=True)


class TunableConfig(BaseModel):
    """Tunable parameters model."""
    
    cacheDirectoryMethod: Optional[str] = Field(None, description="Cache directory method")
    cacheNoCache: Optional[bool] = Field(None, description="Cache no cache")
    sharesMissingEnable: bool = Field(description="Enable missing shares")
    shareNfsEnable: bool = Field(description="Enable NFS shares")
    shareNfsGuest: bool = Field(description="Allow NFS guest access")
    shareNfsSecure: bool = Field(description="NFS secure mode")
    shareAftpEnable: bool = Field(description="Enable anonymous FTP")
    shareAftpPublicEnable: bool = Field(description="Enable public anonymous FTP")
    shareAftpSecure: bool = Field(description="Secure anonymous FTP")
    
    model_config = ConfigDict(populate_by_name=True)


class UpdatesConfig(BaseModel):
    """Updates configuration model."""
    
    auto: bool = Field(description="Auto update OS")
    autoNerdpack: bool = Field(description="Auto update Nerdpack")
    autoDocker: bool = Field(description="Auto update Docker")
    autoPlugins: bool = Field(description="Auto update plugins")
    autoCommunityApplications: bool = Field(description="Auto update Community Applications")
    
    model_config = ConfigDict(populate_by_name=True)


class SystemConfig(BaseModel):
    """System configuration model."""
    
    hostname: str = Field(description="System hostname")
    description: Optional[str] = Field(None, description="System description")
    model: Optional[str] = Field(None, description="System model")
    version: str = Field(description="Unraid version")
    motherboard: Optional[str] = Field(None, description="Motherboard model")
    cpu: CPUConfig = Field(description="CPU configuration")
    memory: MemoryConfig = Field(description="Memory configuration")
    network: NetworkConfig = Field(description="Network configuration")
    display: DisplayConfig = Field(description="Display configuration")
    timezone: str = Field(description="System timezone")
    notifications: NotificationsConfig = Field(description="Notifications configuration")
    vm: VMConfig = Field(description="VM configuration")
    docker: DockerConfig = Field(description="Docker configuration")
    shares: SharesConfig = Field(description="Shares configuration")
    ftp: FTPConfig = Field(description="FTP configuration")
    dynamicDns: DynamicDNSConfig = Field(description="Dynamic DNS configuration")
    tunable: TunableConfig = Field(description="Tunable parameters")
    updates: UpdatesConfig = Field(description="Updates configuration")
    
    model_config = ConfigDict(populate_by_name=True)


class ShareConfig(BaseModel):
    """Share configuration model."""
    
    name: str = Field(description="Share name")
    comment: Optional[str] = Field(None, description="Share comment")
    allocator: str = Field(description="Share allocator")
    fsType: str = Field(description="Filesystem type")
    include: Optional[str] = Field(None, description="Include pattern")
    exclude: Optional[str] = Field(None, description="Exclude pattern")
    useCache: Optional[str] = Field(None, description="Cache usage mode")
    exportEnabled: bool = Field(description="Export enabled")
    security: str = Field(description="Security mode")
    accessMode: str = Field(description="Access mode")
    ownership: str = Field(description="Ownership")
    diskIds: List[str] = Field(default_factory=list, description="Disk IDs")
    
    model_config = ConfigDict(populate_by_name=True)


class PluginConfig(BaseModel):
    """Plugin configuration model."""
    
    name: str = Field(description="Plugin name")
    version: str = Field(description="Plugin version")
    author: str = Field(description="Plugin author")
    description: Optional[str] = Field(None, description="Plugin description")
    support: Optional[str] = Field(None, description="Support URL")
    icon: Optional[str] = Field(None, description="Plugin icon")
    settings: Dict[str, Any] = Field(default_factory=dict, description="Plugin settings")
    
    model_config = ConfigDict(populate_by_name=True)


class MutationResponse(BaseModel):
    """Mutation response model."""
    
    success: bool = Field(description="Success flag")
    message: Optional[str] = Field(None, description="Response message")
    
    model_config = ConfigDict(populate_by_name=True)
