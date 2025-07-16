"""
Config mgmt for claude cli
 
contains config constants and settings for the claude cli application,
providing a centralized place for config mgmt.
"""

from typing import Dict, Any

# API config
DEFAULT_MODEL = "claude-3-5-sonnet-20241022"
DEFAULT_MAX_TOKENS = 1000
API_BASE_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"

# env. var
API_KEY_ENV_VAR =  "ANTHROPIC_API_KEY"

# file extensions
CONVERSATION_FILE_EXTENSION = ".json"

# cli config
CLI_NAME = "Claude CLI"
CLI_VERSION = "1.0.0" 
CLI_DESCRIPTION = "Interact with Claude AI from the command line"

# interactive mode commands
INTERACTIVE_COMMANDS = {
    "quit" : ["quit", "exit", "q"],
    "clear" : ["clear"],
    "save" : "save",
    "load" : "load"
}

# http header template
def get_api_headers(api_key: str) -> Dict[str, str]:
    """
    Generate HTTP headers for API requests
    Args: api_key : Anthropic API key
    Returns: Dictionary of HTTP headers 
    """
    return {
        "x-api-key": api_key,
        "anthropic-version": API_VERSION,
        "content-type": "application/json"
    }

# error messages
ERROR_MESSAGES = {
    "no_api_key": f"API key required. Set {API_KEY_ENV_VAR} environment variable or pass --api-key",
    "file_not_found": "File '{}' not found",
    "file_empty": "File is empty",
    "invalid_encoding": "Cannot read file '{}' - invalid encoding",
    "conversation_load_failed": "Failed to load conversation from '{}'",
    "conversation_save_failed": "Failed to save conversation to '{}'",
    "api_request_failed": "API request failed: {}",
    "unexpected_response": "Unexpected API response format: {}",
    "config_error": "Configuration error: {}",
    "unexpected_error": "Unexpected error: {}"
}
# success messages
SUCCESS_MESSAGES = {
    "conversation_loaded": "Conversation loaded successfully from '{}'",
    "conversation_saved": "Conversation saved successfully to '{}'",
    "conversation_cleared": "Conversation cleared."
}