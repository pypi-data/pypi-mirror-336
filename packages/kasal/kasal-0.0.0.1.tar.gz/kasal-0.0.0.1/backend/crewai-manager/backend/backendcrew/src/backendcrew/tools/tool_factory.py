from typing import Dict, Optional
from crewai.tools import BaseTool
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import Tool, get_db, get_async_db, ApiKey
from .perplexity_tool import PerplexitySearchTool
from .google_slides_tool import GoogleSlidesTool
from .genie_tool import GenieTool
from .sendpulse_tool import SendPulseEmailTool
from .browser_use_tool import BrowserUseTool
from crewai_tools import (
    DallETool, 
    GithubSearchTool, 
    ScrapeWebsiteTool, 
    CodeInterpreterTool, 
    CSVSearchTool, 
    YoutubeChannelSearchTool,
    YoutubeVideoSearchTool,
    ComposioTool, 
    SerperDevTool,
    FirecrawlScrapeWebsiteTool,
    SpiderTool, 
    WebsiteSearchTool,
    DirectoryReadTool,
    FileWriterTool,
    BrowserbaseLoadTool,
    CodeDocsSearchTool,
    DirectorySearchTool,
    DOCXSearchTool,
    EXASearchTool,
    FileReadTool,
    FirecrawlCrawlWebsiteTool,
    FirecrawlSearchTool,
    TXTSearchTool,
    JSONSearchTool,
    LlamaIndexTool,
    MDXSearchTool,
    PDFSearchTool,
    PGSearchTool,
    RagTool,
    ScrapeElementFromWebsiteTool,
    XMLSearchTool,
    VisionTool,
    AIMindTool,
    ApifyActorsTool,
    BraveSearchTool,
    DatabricksQueryTool,
    HyperbrowserLoadTool,
    LinkupSearchTool,
    MultiOnTool,
    MySQLSearchTool,
    NL2SQLTool,
    PatronusEvalTool,
    PatronusLocalEvaluatorTool,
    PatronusPredefinedCriteriaEvalTool,
    QdrantVectorSearchTool,
    ScrapegraphScrapeTool,
    ScrapflyScrapeWebsiteTool,
    SeleniumScrapingTool,
    SerpApiGoogleSearchTool,
    SerpApiGoogleShoppingTool,
    SerplyJobSearchTool,
    SerplyNewsSearchTool,
    SerplyScholarSearchTool,
    SerplyWebSearchTool,
    SerplyWebpageToMarkdownTool,
    SnowflakeSearchTool,
    WeaviateVectorSearchTool
)
from .nixtla_tool import NixtlaTimeGPTTool
from ..api.keys import get_sqlite_api_key, decrypt_value
import logging
import os
import asyncio
import json

logger = logging.getLogger(__name__)

class ToolFactory:
    def __init__(self, config):
        self.config = config
        self.db: Session = next(get_db())
        self._available_tools: Dict[str, Tool] = {}
        self._load_available_tools()
        
        # Map tool names to their implementations
        self._tool_implementations = {
            "PerplexityTool": PerplexitySearchTool,
            "GoogleSlidesTool": GoogleSlidesTool,
            "Dall-E Tool": DallETool,
            "Vision Tool": VisionTool,
            "GithubSearchTool": GithubSearchTool,
            "ScrapeWebsiteTool": ScrapeWebsiteTool,
            "CodeInterpreterTool": CodeInterpreterTool,
            "CSVSearchTool": CSVSearchTool,
            "NixtlaTimeGPTTool": NixtlaTimeGPTTool,
            "YoutubeChannelSearchTool": YoutubeChannelSearchTool,
            "YoutubeVideoSearchTool": YoutubeVideoSearchTool,
            "GenieTool": GenieTool,
            "ComposioTool": ComposioTool,
            "SerperDevTool": SerperDevTool,
            "FirecrawlScrapeWebsiteTool": FirecrawlScrapeWebsiteTool,
            "SpiderTool": SpiderTool,
            "WebsiteSearchTool": WebsiteSearchTool,
            "SendPulseEmailTool": SendPulseEmailTool,
            "DirectoryReadTool": DirectoryReadTool,
            "BrowserUseTool": BrowserUseTool,
            "FileWriterTool": FileWriterTool,
            "BrowserbaseLoadTool": BrowserbaseLoadTool,
            "CodeDocsSearchTool": CodeDocsSearchTool,
            "DirectorySearchTool": DirectorySearchTool,
            "DOCXSearchTool": DOCXSearchTool,
            "EXASearchTool": EXASearchTool,
            "FileReadTool": FileReadTool,
            "FirecrawlCrawlWebsiteTool": FirecrawlCrawlWebsiteTool,
            "FirecrawlSearchTool": FirecrawlSearchTool,
            "TXTSearchTool": TXTSearchTool,
            "JSONSearchTool": JSONSearchTool,
            "LlamaIndexTool": LlamaIndexTool,
            "MDXSearchTool": MDXSearchTool,
            "PDFSearchTool": PDFSearchTool,
            "PGSearchTool": PGSearchTool,
            "RagTool": RagTool,
            "ScrapeElementFromWebsiteTool": ScrapeElementFromWebsiteTool,
            "XMLSearchTool": XMLSearchTool,
            "AIMindTool": AIMindTool,
            "ApifyActorsTool": ApifyActorsTool,
            "BraveSearchTool": BraveSearchTool,
            "DatabricksQueryTool": DatabricksQueryTool,
            "HyperbrowserLoadTool": HyperbrowserLoadTool,
            "LinkupSearchTool": LinkupSearchTool,
            "MultiOnTool": MultiOnTool,
            "MySQLSearchTool": MySQLSearchTool,
            "NL2SQLTool": NL2SQLTool,
            "PatronusEvalTool": PatronusEvalTool,
            "PatronusLocalEvaluatorTool": PatronusLocalEvaluatorTool,
            "PatronusPredefinedCriteriaEvalTool": PatronusPredefinedCriteriaEvalTool,
            "QdrantVectorSearchTool": QdrantVectorSearchTool,
            "ScrapegraphScrapeTool": ScrapegraphScrapeTool,
            "ScrapflyScrapeWebsiteTool": ScrapflyScrapeWebsiteTool,
            "SeleniumScrapingTool": SeleniumScrapingTool,
            "SerpApiGoogleSearchTool": SerpApiGoogleSearchTool,
            "SerpApiGoogleShoppingTool": SerpApiGoogleShoppingTool,
            "SerplyJobSearchTool": SerplyJobSearchTool,
            "SerplyNewsSearchTool": SerplyNewsSearchTool,
            "SerplyScholarSearchTool": SerplyScholarSearchTool,
            "SerplyWebSearchTool": SerplyWebSearchTool,
            "SerplyWebpageToMarkdownTool": SerplyWebpageToMarkdownTool,
            "SnowflakeSearchTool": SnowflakeSearchTool,
            "WeaviateVectorSearchTool": WeaviateVectorSearchTool
        }
    
    def _load_available_tools(self):
        """Load all available tools from the database"""
        tools = self.db.query(Tool).all()
        # Store tools by both title and ID
        self._available_tools = {}
        for tool in tools:
            self._available_tools[tool.title] = tool
            self._available_tools[str(tool.id)] = tool  # Convert ID to string since it might come as string from config
        logger.info(f"Loaded {len(tools)} tools from database")
        logger.debug(f"Available tools: {[f'{t.id}:{t.title}' for t in tools]}")
    
    def get_tool_info(self, tool_identifier: str) -> Optional[Tool]:
        """Get tool information from database by ID or title"""
        tool = self._available_tools.get(tool_identifier)
        if not tool:
            logger.warning(f"Tool '{tool_identifier}' not found in available tools. Available tools are: {list(self._available_tools.keys())}")
        return tool
    
    async def _get_api_key_from_db(self, key_name: str) -> Optional[str]:
        """Get an API key from the database"""
        try:
            # Get an async database session
            async for db in get_async_db():
                api_key_data = await get_sqlite_api_key(db, key_name)
                if api_key_data and api_key_data["value"]:
                    api_key = api_key_data["value"]
                    # Log first and last 4 characters of the key for debugging
                    key_preview = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "***"
                    logger.info(f"Using {key_name} from database: {key_preview}")
                    return api_key
                else:
                    logger.warning(f"{key_name} not found in database")
                    return None
        except Exception as e:
            logger.error(f"Error getting {key_name} from database: {str(e)}")
            return None
    
    def _get_api_key(self, key_name: str) -> Optional[str]:
        """Get an API key from the database using SQLAlchemy ORM"""
        try:
            # Query the database for the API key
            api_key_record = self.db.query(ApiKey).filter(ApiKey.name == key_name).first()
            
            if api_key_record and api_key_record.encrypted_value:
                # Decrypt the value
                decrypted_value = decrypt_value(api_key_record.encrypted_value)
                
                # Log first and last 4 characters of the key for debugging
                key_preview = f"{decrypted_value[:4]}...{decrypted_value[-4:]}" if len(decrypted_value) > 8 else "***"
                logger.info(f"Using {key_name} from database: {key_preview}")
                return decrypted_value
            
            # Key not found or no value
            logger.warning(f"{key_name} not found in database")
            return None
        except Exception as e:
            logger.error(f"Error getting {key_name} from database: {str(e)}")
            return None
    
    def create_tool(self, tool_identifier: str) -> Optional[BaseTool]:
        """Create a tool instance if it exists in database"""
        tool_info = self.get_tool_info(tool_identifier)
        logger.info(f"Looking up tool '{tool_identifier}' in database: {tool_info}")
        
        if not tool_info:
            logger.error(f"Tool '{tool_identifier}' not found in database. Please ensure the tool is registered.")
            return None
            
        # Use the tool's title to look up the implementation
        tool_name = tool_info.title
        tool_class = self._tool_implementations.get(tool_name)
        logger.info(f"Found implementation for '{tool_name}': {tool_class}")
        
        if not tool_class:
            logger.warning(f"No implementation found for tool '{tool_name}'")
            return None
            
        try:
            # Get tool config from database
            tool_config = tool_info.config if tool_info else {}
            logger.info(f"{tool_name} config from database: {tool_config}")
            
            if tool_name == "PerplexityTool":
                api_key = tool_config.get('perplexity_api_key', '')
                logger.info(f"Using perplexity_api_key from config for PerplexityTool (tool_id: {tool_identifier})")
                return tool_class(api_key=api_key)
                
            elif tool_name == "GoogleSlidesTool":
                credentials_path = tool_config.get('credentials_path', self.config.get('google_credentials_path'))
                return tool_class(credentials_path=credentials_path)
                
            elif tool_name == "Dall-E Tool":
                api_key = self.config.get('openai_api_key')
                model = tool_config.get('model', 'dall-e-3')
                size = tool_config.get('size', '1024x1024')
                quality = tool_config.get('quality', 'standard')
                n = tool_config.get('n', 1)
                return tool_class(api_key=api_key, model=model, size=size, quality=quality, n=n)
                
            elif tool_name == "Vision Tool":
                api_key = self.config.get('openai_api_key')
                model = tool_config.get('model', 'gpt-4-vision-preview')
                return tool_class(api_key=api_key, model=model)
                
            elif tool_name == "GithubSearchTool":
                api_key = self.config.get('github_api_key')
                content_types = tool_config.get('content_types', ["code", "repo", "pr", "issue"])
                config = tool_config.get('config')
                return tool_class(api_key=api_key, content_types=content_types, config=config)
                
            elif tool_name == "NixtlaTimeGPTTool":
                api_key = tool_config.get('nixtla_api_key', '')
                logger.info(f"Using nixtla_api_key from config for NixtlaTimeGPTTool (tool_id: {tool_identifier})")
                return tool_class(api_key=api_key)
                
            elif tool_name == "CodeInterpreterTool":
                api_key = self.config.get('openai_api_key')
                timeout = tool_config.get('timeout', 60)
                working_directory = tool_config.get('working_directory', './code_interpreter_workspace')
                return tool_class(api_key=api_key, timeout=timeout, working_directory=working_directory)
                
            elif tool_name == "GenieTool":
                return tool_class(tool_config=tool_config)
                
            elif tool_name == "ComposioTool":
                api_key = tool_config.get('composio_api_key', '')
                logger.info(f"Using composio_api_key from config for ComposioTool (tool_id: {tool_identifier})")
                return tool_class(api_key=api_key)
                
            elif tool_name == "SerperDevTool":
                # Get parameters from tool config
                n_results = tool_config.get('n_results', 10)
                search_url = tool_config.get('search_url', "https://google.serper.dev/search")
                country = tool_config.get('country', 'us')
                locale = tool_config.get('locale', 'en')
                location = tool_config.get('location', '')
                
                # Try to get the key from environment first
                serper_api_key = os.environ.get("SERPER_API_KEY")
                
                # If not found in environment, try to get it from the database
                if not serper_api_key:
                    logger.info("SERPER_API_KEY not found in environment, trying database")
                    db_api_key = self._get_api_key("SERPER_API_KEY")
                    if db_api_key:
                        # Set the key as an environment variable
                        os.environ["SERPER_API_KEY"] = db_api_key
                        serper_api_key = db_api_key
                        logger.info("Set SERPER_API_KEY from database to environment variable")
                    else:
                        logger.warning("SERPER_API_KEY not found in database either")
                
                # Create the tool with the API key now in environment
                if serper_api_key:
                    # Create the tool with configured parameters
                    logger.info(f"Creating SerperDevTool with n_results={n_results}, search_url={search_url}, country={country}, locale={locale}, location={location}")
                    return tool_class(
                        n_results=n_results,
                        search_url=search_url,
                        country=country,
                        locale=locale,
                        location=location
                    )
                else:
                    logger.warning("SERPER_API_KEY not found in environment or database")
                    return None
                    
            elif tool_name == "FirecrawlScrapeWebsiteTool":
                api_key = tool_config.get('api_key', '')
                page_options = tool_config.get('page_options', {
                    "onlyMainContent": True,
                    "includeHtml": False,
                    "fetchPageContent": True
                })
                return tool_class(api_key=api_key, page_options=page_options)
                
            elif tool_name == "FirecrawlSearchTool":
                api_key = tool_config.get('api_key', '')
                page_options = tool_config.get('page_options', {
                    "onlyMainContent": True,
                    "includeHtml": False,
                    "fetchPageContent": True
                })
                search_options = tool_config.get('search_options', {"limit": 10})
                return tool_class(api_key=api_key, page_options=page_options, search_options=search_options)
                
            elif tool_name == "FirecrawlCrawlWebsiteTool":
                api_key = tool_config.get('api_key', '')
                page_options = tool_config.get('page_options', {
                    "onlyMainContent": True,
                    "includeHtml": False,
                    "fetchPageContent": True
                })
                return tool_class(api_key=api_key, page_options=page_options)
                
            elif tool_name == "SpiderTool":
                params = tool_config.get('params', {"return_format": "markdown"})
                request = tool_config.get('request', "smart")
                limit = tool_config.get('limit', 10)
                depth = tool_config.get('depth', 3)
                cache = tool_config.get('cache', True)
                stealth = tool_config.get('stealth', True)
                metadata = tool_config.get('metadata', True)
                return tool_class(
                    params=params,
                    request=request,
                    limit=limit,
                    depth=depth,
                    cache=cache,
                    stealth=stealth,
                    metadata=metadata
                )
                
            elif tool_name == "WebsiteSearchTool":
                config = tool_config.get('config')
                return tool_class(config=config)
                
            elif tool_name == "SendPulseEmailTool":
                return tool_class(
                    api_id=tool_config.get('sendpulse_api_id', ''),
                    api_secret=tool_config.get('sendpulse_api_secret', ''),
                    default_from_name=tool_config.get('default_from_name', 'CrewAI Agent'),
                    default_from_email=tool_config.get('default_from_email', 'agent@example.com'),
                    default_to_name=tool_config.get('default_to_name', 'User'),
                    default_to_email=tool_config.get('default_to_email', 'user@example.com')
                )
                
            elif tool_name == "DirectoryReadTool":
                directory = tool_config.get('directory', './')
                return tool_class(directory=directory)
                
            elif tool_name == "BrowserUseTool":
                # Get API URL from config or fall back to environment
                browser_use_api_url = tool_config.get('browser_use_api_url') or tool_config.get('BROWSER_USE_API_URL')
                if not browser_use_api_url:
                    browser_use_api_url = os.environ.get('BROWSER_USE_API_URL')
                    if not browser_use_api_url:
                        logger.error("browser_use_api_url not found in tool config or environment variables")
                        return None
                
                logger.info(f"Using browser_use_api_url: {browser_use_api_url} for BrowserUseTool (tool_id: {tool_identifier})")
                # Use the factory method instead of constructor
                return tool_class.from_config(browser_use_api_url=browser_use_api_url)
                
            elif tool_name == "FileWriterTool":
                # Get configuration parameters
                default_directory = tool_config.get('default_directory', './file_outputs')
                overwrite = tool_config.get('overwrite', True)
                encoding = tool_config.get('encoding', 'utf-8')
                
                # Create directory if it doesn't exist
                if default_directory and not os.path.exists(default_directory):
                    try:
                        os.makedirs(default_directory, exist_ok=True)
                        logger.info(f"Created directory {default_directory} for FileWriterTool")
                    except Exception as e:
                        logger.warning(f"Failed to create directory {default_directory} for FileWriterTool: {e}")
                
                logger.info(f"Initializing FileWriterTool with directory={default_directory}, overwrite={overwrite}, encoding={encoding}")
                return tool_class(
                    directory=default_directory,
                    overwrite=overwrite,
                    encoding=encoding
                )
                
            elif tool_name == "FileReadTool":
                file_path = tool_config.get('file_path', '')
                return tool_class(file_path=file_path)
                
            elif tool_name == "PDFSearchTool":
                config = tool_config.get('config')
                return tool_class(config=config)
                
            elif tool_name == "BrowserbaseLoadTool":
                return tool_class()
                
            elif tool_name == "CSVSearchTool":
                config = tool_config.get('config')
                return tool_class(config=config)
                
            elif tool_name == "CodeDocsSearchTool":
                config = tool_config.get('config')
                return tool_class(config=config)
                
            elif tool_name == "DirectorySearchTool":
                config = tool_config.get('config')
                return tool_class(config=config)
                
            elif tool_name == "DOCXSearchTool":
                config = tool_config.get('config')
                return tool_class(config=config)
                
            elif tool_name == "EXASearchTool":
                config = tool_config.get('config')
                return tool_class(config=config)
                
            elif tool_name == "TXTSearchTool":
                config = tool_config.get('config')
                return tool_class(config=config)
                
            elif tool_name == "JSONSearchTool":
                config = tool_config.get('config')
                return tool_class(config=config)
                
            elif tool_name == "LlamaIndexTool":
                return tool_class()
                
            elif tool_name == "MDXSearchTool":
                config = tool_config.get('config')
                return tool_class(config=config)
                
            elif tool_name == "PGSearchTool":
                config = tool_config.get('config')
                return tool_class(config=config)
                
            elif tool_name == "RagTool":
                config = tool_config.get('config')
                return tool_class(config=config)
                
            elif tool_name == "ScrapeElementFromWebsiteTool":
                return tool_class()
                
            elif tool_name == "XMLSearchTool":
                config = tool_config.get('config')
                return tool_class(config=config)
                
            elif tool_name == "YoutubeChannelSearchTool":
                config = tool_config.get('config')
                return tool_class(config=config)
                
            elif tool_name == "YoutubeVideoSearchTool":
                config = tool_config.get('config')
                return tool_class(config=config)
                
            # Handle newly added tools
            elif tool_name == "AIMindTool":
                model = tool_config.get('model', 'gpt-4')
                return tool_class(model=model)
                
            elif tool_name == "ApifyActorsTool":
                api_key = tool_config.get('apify_api_key', '')
                return tool_class(api_key=api_key)
                
            elif tool_name == "BraveSearchTool":
                api_key = tool_config.get('api_key', '')
                country = tool_config.get('country', 'us')
                count = tool_config.get('count', 10)
                return tool_class(api_key=api_key, country=country, count=count)
                
            elif tool_name == "DatabricksQueryTool":
                host = tool_config.get('host', '')
                token = tool_config.get('token', '')
                http_path = tool_config.get('http_path', '')
                catalog = tool_config.get('catalog', '')
                schema = tool_config.get('schema', '')
                return tool_class(host=host, token=token, http_path=http_path, catalog=catalog, schema=schema)
                
            elif tool_name == "HyperbrowserLoadTool":
                # Get API key from tool config or environment
                api_key = tool_config.get('api_key')
                if not api_key:
                    api_key = os.environ.get('HYPERBROWSER_API_KEY')
                    if not api_key:
                        # Try to get from database
                        db_api_key = self._get_api_key("HYPERBROWSER_API_KEY")
                        if db_api_key:
                            api_key = db_api_key
                            # Also set in environment for future use
                            os.environ['HYPERBROWSER_API_KEY'] = db_api_key
                            
                if not api_key:
                    logger.error("HyperbrowserLoadTool requires an API key. Please set HYPERBROWSER_API_KEY in environment or tool configuration.")
                    return None
                
                return tool_class(api_key=api_key)
                
            elif tool_name == "LinkupSearchTool":
                api_key = tool_config.get('api_key', '')
                return tool_class(api_key=api_key)
                
            elif tool_name == "MultiOnTool":
                return tool_class()
                
            elif tool_name == "MySQLSearchTool":
                host = tool_config.get('host', 'localhost')
                user = tool_config.get('user', '')
                password = tool_config.get('password', '')
                database = tool_config.get('database', '')
                config = tool_config.get('config')
                return tool_class(host=host, user=user, password=password, database=database, config=config)
                
            elif tool_name == "NL2SQLTool":
                database_uri = tool_config.get('database_uri', '')
                api_key = tool_config.get('api_key', '')
                return tool_class(database_uri=database_uri, api_key=api_key)
                
            elif tool_name == "PatronusEvalTool":
                api_key = tool_config.get('api_key', '')
                return tool_class(api_key=api_key)
                
            elif tool_name == "PatronusLocalEvaluatorTool":
                model = tool_config.get('model', 'gpt-4')
                return tool_class(model=model)
                
            elif tool_name == "PatronusPredefinedCriteriaEvalTool":
                api_key = tool_config.get('api_key', '')
                return tool_class(api_key=api_key)
                
            elif tool_name == "QdrantVectorSearchTool":
                url = tool_config.get('url', '')
                api_key = tool_config.get('api_key', '')
                collection_name = tool_config.get('collection_name', '')
                return tool_class(url=url, api_key=api_key, collection_name=collection_name)
                
            elif tool_name == "ScrapegraphScrapeTool":
                api_key = tool_config.get('api_key', '')
                return tool_class(api_key=api_key)
                
            elif tool_name == "ScrapflyScrapeWebsiteTool":
                api_key = tool_config.get('api_key', '')
                return tool_class(api_key=api_key)
                
            elif tool_name == "SeleniumScrapingTool":
                return tool_class()
                
            elif tool_name == "SerpApiGoogleSearchTool":
                api_key = tool_config.get('api_key', '')
                num_results = tool_config.get('num_results', 10)
                return tool_class(api_key=api_key, num_results=num_results)
                
            elif tool_name == "SerpApiGoogleShoppingTool":
                api_key = tool_config.get('api_key', '')
                num_results = tool_config.get('num_results', 10)
                return tool_class(api_key=api_key, num_results=num_results)
                
            elif tool_name == "SerplyJobSearchTool":
                api_key = tool_config.get('api_key', '')
                num_results = tool_config.get('num_results', 10)
                return tool_class(api_key=api_key, num_results=num_results)
                
            elif tool_name == "SerplyNewsSearchTool":
                api_key = tool_config.get('api_key', '')
                num_results = tool_config.get('num_results', 10)
                return tool_class(api_key=api_key, num_results=num_results)
                
            elif tool_name == "SerplyScholarSearchTool":
                api_key = tool_config.get('api_key', '')
                num_results = tool_config.get('num_results', 10)
                return tool_class(api_key=api_key, num_results=num_results)
                
            elif tool_name == "SerplyWebSearchTool":
                api_key = tool_config.get('api_key', '')
                num_results = tool_config.get('num_results', 10)
                return tool_class(api_key=api_key, num_results=num_results)
                
            elif tool_name == "SerplyWebpageToMarkdownTool":
                api_key = tool_config.get('api_key', '')
                return tool_class(api_key=api_key)
                
            elif tool_name == "SnowflakeSearchTool":
                account = tool_config.get('account', '')
                user = tool_config.get('user', '')
                password = tool_config.get('password', '')
                database = tool_config.get('database', '')
                schema = tool_config.get('schema', '')
                warehouse = tool_config.get('warehouse', '')
                role = tool_config.get('role', '')
                config = tool_config.get('config')
                return tool_class(
                    account=account,
                    user=user,
                    password=password,
                    database=database,
                    schema=schema,
                    warehouse=warehouse,
                    role=role,
                    config=config
                )
                
            elif tool_name == "WeaviateVectorSearchTool":
                url = tool_config.get('url', '')
                api_key = tool_config.get('api_key', '')
                class_name = tool_config.get('class_name', '')
                return tool_class(url=url, api_key=api_key, class_name=class_name)
                
            # Default case for any other tools
            return tool_class()
            
        except Exception as e:
            logger.error(f"Error creating tool '{tool_name}': {e}")
            return None
