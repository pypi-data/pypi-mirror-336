# Re-export all types from individual files
from .enums import (
    JobStatus,
    JobTaskType,
    SpecificDataExtractionType,
    StructuredDataExtractionAttribute,
    SpecificDataExtractionOutputFormat,
    WebScreenCaptureFormat,
    PdfPaperFormat,
    PdfOrientation,
    JobSchedulePolicy,
    JobNavigationType,
    PuppetDeviceType,
    PuppetRegion,
    WebDataSelectorType
)

from .job_types import (
    Job,
    JobDetail,
    JobSchedule,
    JobNavigation,
    JobResult,
    JobExecutionResponse,
    GetJobResponse,
    GetJobsResponse,
    GetJobResultResponse,
    WebAgentConfig
)

from .task_types import (
    JobTask,
    SpecificDataExtractionOptions,
    WebScreenCaptureOptions,
    WebpageAsMarkdownOptions,
    StructuredDataExtractionOptions,
    StructuredDataExtractionParameter,
    FormDataExtractionOptions,
    TableDataExtractionOptions,
    PresetDataExtractionOptions,
    CustomDataExtractionOptions,
)

# Optional: Define __all__ to explicitly list what should be exported
__all__ = [
    "JobStatus",
    "JobTaskType",
    "SpecificDataExtractionType",
    "StructuredDataExtractionAttribute",
    "SpecificDataExtractionOutputFormat",
    "WebScreenCaptureFormat",
    "PdfPaperFormat",
    "PdfOrientation",
    "JobSchedulePolicy",
    "JobNavigationType",
    "PuppetDeviceType",
    "PuppetRegion",
    "WebDataSelectorType",
    "Job",
    "JobSchedule",
    "JobNavigation",
    "JobDetail",
    "JobResult",
    "JobExecutionResponse",
    "GetJobResponse",
    "GetJobsResponse",
    "GetJobResultResponse",
    "JobTask",
    "SpecificDataExtractionOptions",
    "WebScreenCaptureOptions",
    "WebpageAsMarkdownOptions",
    "StructuredDataExtractionOptions",
    "StructuredDataExtractionParameter",
    "FormDataExtractionOptions",
    "TableDataExtractionOptions",
    "PresetDataExtractionOptions",
    "CustomDataExtractionOptions",
    "WebAgentConfig"
]