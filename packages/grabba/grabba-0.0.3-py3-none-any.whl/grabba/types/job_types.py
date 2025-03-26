from typing import List, Dict, Optional, Union
from dataclasses import dataclass
from datetime import datetime
from .enums import (
    JobStatus, JobSchedulePolicy,
    JobNavigationType, PuppetDeviceType, PuppetRegion
)
from .task_types import JobTask

# Data Models
@dataclass
class JobSchedule:
    policy: JobSchedulePolicy
    specification: Optional[Dict] = None

@dataclass
class JobNavigation:
    type: JobNavigationType
    options: Optional[Union[Dict, List[str]]] = None
    max_pages: Optional[int] = None

@dataclass
class WebAgentConfig:
    region: PuppetRegion
    device_type: Optional[PuppetDeviceType] = None
    viewport: Optional[Dict] = None

@dataclass
class Job:
    url: str
    tasks: List[JobTask]
    schedule: Optional[JobSchedule]
    navigation: Optional[JobNavigation]
    puppet_config: Optional[WebAgentConfig] = None

@dataclass
class JobDetail():
    id: str
    name: str
    url: str
    tasks: List[JobTask]
    schedule: Optional[JobSchedule] = None
    navigation: Optional[JobNavigation] = None
    puppet_config: Optional[WebAgentConfig] = None
    status: Optional[JobStatus] = None
    results: List[Dict] = None
    created_at: Optional[datetime] = None

@dataclass
class JobResult:
    id: str
    output: Dict[str, Dict]
    start_time: datetime
    stop_time: datetime
    duration: str

@dataclass
class JobExecutionResponse:
    status: str
    message: str
    jobResult: Dict

@dataclass
class GetJobResponse:
    message: str
    job: JobDetail

@dataclass
class GetJobsResponse:
    message: str
    jobs: List[Job]

@dataclass
class GetJobResultResponse:
    message: str
    jobResult: Dict