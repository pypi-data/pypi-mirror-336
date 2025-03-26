from typing import List, Optional, Union
from dataclasses import dataclass

from .enums import (
    JobTaskType,
    WebDataSelectorType, SpecificDataExtractionType,
    SpecificDataExtractionOutputFormat, WebScreenCaptureFormat, 
    StructuredDataExtractionAttribute, PdfPaperFormat, PdfOrientation
)

# Data Models
@dataclass
class WebDataSelector:
    type: WebDataSelectorType
    value: str

@dataclass
class StructuredDataExtractionParameter:
    name: str
    selector: Optional[WebDataSelector] = None
    parent_selector: Optional[WebDataSelector] = None
    attribute: Optional[StructuredDataExtractionAttribute] = None
    custom_attribute: Optional[str] = None
    sample: Optional[str] = None

@dataclass
class StructuredDataExtractionOptions:
    parameters: List[StructuredDataExtractionParameter]
    auto_populate_parameters: bool
    parse_with_aI: bool
    execute_with_ai: bool
    parent_selector: Optional[WebDataSelector] = None

@dataclass
class FormDataExtractionOptions:
    selector: Optional[WebDataSelector] = None

@dataclass
class TableDataExtractionOptions:
    selector: Optional[WebDataSelector] = None

@dataclass
class PresetDataExtractionOptions:
    selector: Optional[WebDataSelector] = None

@dataclass
class CustomDataExtractionOptions:
    regex_pattern: Optional[str] = None
    selector: Optional[WebDataSelector] = None

@dataclass
class SpecificDataExtractionOptions:
    type: SpecificDataExtractionType
    options: Union[PresetDataExtractionOptions, TableDataExtractionOptions, FormDataExtractionOptions, StructuredDataExtractionOptions, None]
    max_results: int
    output_format: SpecificDataExtractionOutputFormat

@dataclass
class WebScreenCaptureOptions:
    format: Optional[WebScreenCaptureFormat] = WebScreenCaptureFormat.WEBP.value
    full_page: Optional[bool] = False
    omit_background: Optional[bool] = True
    pdf_format: Optional[PdfPaperFormat] = PdfPaperFormat.A4.value
    pdf_orientation: Optional[PdfOrientation] = PdfOrientation.LANDSCAPE.value
    pdf_print_background: Optional[bool] = True

@dataclass
class WebpageAsMarkdownOptions:
    only_main_content: Optional[bool] = None

@dataclass
class JobTask:
    type: JobTaskType
    options: Union[SpecificDataExtractionOptions, WebpageAsMarkdownOptions, WebScreenCaptureOptions]
