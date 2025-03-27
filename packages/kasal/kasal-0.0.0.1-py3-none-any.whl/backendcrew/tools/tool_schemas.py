from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

# Base class for all tool outputs
class BaseToolOutput(BaseModel):
    """Base class for all tool outputs"""
    pass

# SendPulse Models
class EmailRecipient(BaseModel):
    """Model for email recipient"""
    name: str
    email: str

class EmailSender(BaseModel):
    """Model for email sender"""
    name: str
    email: str

class EmailContent(BaseModel):
    """Model for email content"""
    subject: str
    html: str
    text: Optional[str] = None
    from_: EmailSender = Field(..., alias="from")
    to: list[EmailRecipient]

class SerperResult(BaseModel):
    """Model for individual Serper search result"""
    Title: str
    Link: str
    Snippet: str

class SerperDevToolOutput(BaseToolOutput):
    """Output model for SerperDev search tool"""
    results: List[SerperResult]

class URLData(BaseModel):
    """Model for URL data with associated metadata"""
    Title: str
    Link: str = Field(..., description="URL must not be empty")
    Snippet: str

class MultiURLToolOutput(BaseToolOutput):
    """Output model for handling multiple URLs with their metadata"""
    results: List[URLData]
    total_count: Optional[int] = None
    source: Optional[str] = None
    timestamp: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class WebBrowserToolOutput(BaseToolOutput):
    """Output model for Web Browser tool"""
    url: str
    content: str
    title: Optional[str] = None

class FileToolOutput(BaseToolOutput):
    """Output model for File tool"""
    path: str
    content: str
    metadata: Optional[Dict[str, Any]] = None

class DatabaseToolOutput(BaseToolOutput):
    """Output model for Database tool"""
    query_result: Any
    affected_rows: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

class APIToolOutput(BaseToolOutput):
    """Output model for API tool"""
    response: Any
    status_code: Optional[int] = None
    headers: Optional[Dict[str, str]] = None

class CustomToolOutput(BaseToolOutput):
    """Output model for Custom tool"""
    result: Any
    metadata: Optional[Dict[str, Any]] = None

class GoogleSlidesToolOutput(BaseToolOutput):
    """Output model for Google Slides tool"""
    slide_id: str
    content: str
    presentation_id: Optional[str] = None

class PerplexityToolOutput(BaseToolOutput):
    """Output model for Perplexity tool"""
    answer: str
    references: List[Dict[str, str]]

class NixtlaToolOutput(BaseToolOutput):
    """Output model for Nixtla forecasting tool"""
    forecast: List[float]
    confidence_intervals: Optional[Dict[str, List[float]]] = None

class ArxivPaper(BaseModel):
    """Schema for an arXiv paper."""
    id: str
    title: str
    abstract: str
    authors: List[str]
    categories: List[str]
    published_date: str
    pdf_url: Optional[str] = None

class ArxivSearchResult(BaseModel):
    """Schema for arXiv search results."""
    papers: List[ArxivPaper]
    total_results: int = 0

class SendPulseEmailOutput(BaseToolOutput):
    """Output model for SendPulse email tool"""
    success: bool
    message_id: Optional[str] = None
    error: Optional[str] = None

class BrowserUseToolOutput(BaseToolOutput):
    """Output model for Browser Use tool"""
    status: str
    browser_use_objective: str
    result: Dict[str, Any] = {}
    message: Optional[str] = None

# Tool Configuration Schemas
class PerplexityToolConfig(BaseModel):
    """Configuration for Perplexity Tool"""
    perplexity_api_key: str

class SerperDevToolConfig(BaseModel):
    """Configuration for SerperDev Tool"""
    n_results: int = 10

class ComposioToolConfig(BaseModel):
    """Configuration for Composio Tool"""
    composio_api_key: str

class NixtlaToolConfig(BaseModel):
    """Configuration for Nixtla Tool"""
    nixtla_api_key: str

class SendPulseToolConfig(BaseModel):
    """Configuration for SendPulse Tool"""
    sendpulse_api_id: str
    sendpulse_api_secret: str
    default_from_name: str
    default_from_email: str
    default_to_name: str
    default_to_email: str
    token_storage: str = "file"

class BrowserUseToolConfig(BaseModel):
    """Configuration for Browser Use Tool"""
    browser_use_api_url: str
    username: Optional[str] = None  
    password: Optional[str] = None
    openai_api_key: Optional[str] = None
    model_name: Optional[str] = None

# Dictionary mapping tool names to their output models
TOOL_OUTPUT_MODELS = {
    "serper": SerperDevToolOutput,
    "SerperDevToolOutput": SerperDevToolOutput,
    "WebBrowserToolOutput": WebBrowserToolOutput,
    "FileToolOutput": FileToolOutput,
    "DatabaseToolOutput": DatabaseToolOutput,
    "APIToolOutput": APIToolOutput,
    "CustomToolOutput": CustomToolOutput,
    "MultiURLToolOutput": MultiURLToolOutput,
    "google_slides": GoogleSlidesToolOutput,
    "perplexity": PerplexityToolOutput,
    "nixtla": NixtlaToolOutput,
    'arxiv_paper': ArxivPaper,
    'arxiv_search': ArxivSearchResult,
    'sendpulse_email': SendPulseEmailOutput,
    'browser_use_tool': BrowserUseToolOutput
}

def get_tool_output_model(tool_name: str) -> type:
    """Get the output model class for a given tool name"""
    return TOOL_OUTPUT_MODELS.get(tool_name, BaseToolOutput)