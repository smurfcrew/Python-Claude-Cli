#!/usr/bin/env python3
"""
claude cli: command-line interface with Claude AI
"""

import os
import sys
import json
import argparse
from typing import List, Dict, Any, Optional, Union
import requests
from pathlib import Path
# adding color to the text
from colorama import Fore, Back, Style, init

import config

init(autoreset=True)

class ClaudeCLI:
    def __init__(self, api_key: Optional[str] = None) -> None:
        """
        command-line interface for interacting with Claude AI.
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')

        if not self.api_key:
            raise ValueError(config.ERROR_MESSAGES["no_api_key"])
        
        self.base_url = config.API_BASE_URL
        self.headers = config.get_api_headers(self.api_key)
        # takes a list of dictionary that has a kvp of str,str
        self.conversation_history: List[Dict[str, str]] = [] 

    def send_message(self, message: str, model: str = config.DEFAULT_MODEL, 
                    max_tokens: int = config.DEFAULT_MAX_TOKENS, 
                    system_prompt: Optional[str] = None) -> Dict[str, Any]:

        """send message to claude and return the response"""
        messages = self.conversation_history + [{"role": "user", "content": message}]
        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": messages
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            assistant_message = result["content"][0]["text"]
            
            # update convo
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            return {
                "success": True,
                "message": assistant_message,
                "usage": result.get("usage", {}),
                "model": result.get("model", model)
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": config.ERROR_MESSAGES["api_request_failed"].format(str(e)),
                "message": None
            }
        except KeyError as e:
            return {
                "success": False,
                "error": config.ERROR_MESSAGES["api_request_failed"].format(str(e)),
                "message": None
            }
    
    def clear_conversation(self) -> None:
        """
        Removes all messages from the current convo. history 
        """
        self.conversation_history = []
        
    def save_conversation(self, filename: str) -> bool:
        """
        Save the current history to a json file
        args:
            filename: path to the file where convo. should be saved
        returns:
            bool: true if successful, false otherwise 
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return False
            
    def load_conversation(self, filename: str) -> bool:
        """load convo from file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.conversation_history = json.load(f)
            return True
        except Exception as e:
            print(f"Error loading conversation: {e}")
            return False


def print_header(text: str) -> None:
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 60}")
    print(f"{Fore.CYAN}{Style.BRIGHT}{text.center(60)}")
    print(f"{Fore.CYAN}{Style.BRIGHT}{'=' * 60}{Style.RESET_ALL}")

def print_info(text: str) -> None:
    print(f"{Fore.BLUE}{Style.BRIGHT}{text}{Style.RESET_ALL}")

def print_success(text: str) -> None:
    print(f"{Fore.GREEN}{Style.BRIGHT}{text}{Style.RESET_ALL}")

def print_warning(text: str) -> None:
    print(f"{Fore.YELLOW}{Style.BRIGHT}{text}{Style.RESET_ALL}")

def print_error(text: str) -> None:
    print(f"{Fore.RED}{Style.BRIGHT}{text}{Style.RESET_ALL}")

def print_separator() -> None:
    print(f"{Fore.CYAN}{'-' * 60}{Style.RESET_ALL}")


def interactive_mode(claude_cli: ClaudeCLI, model: str, max_tokens: int,
                      system_prompt: Optional[str] = None) -> None:
    """use interactive mode"""
    print(f"{config.CLI_NAME} - Interactive Mode")

    # added color 
    print(f"  {Fore.MAGENTA}quit{Style.RESET_ALL}, {Fore.MAGENTA}exit{Style.RESET_ALL},{Fore.MAGENTA}q{Style.RESET_ALL} - Exit session")
    print(f"  {Fore.MAGENTA}clear{Style.RESET_ALL} - Clear Conversation History")
    print(f"  {Fore.MAGENTA}save <filename>{Style.RESET_ALL} - Save conversation")
    print(f"  {Fore.MAGENTA}load <filename>{Style.RESET_ALL} - Load conversation")
    print_separator()    
 
    if system_prompt:
        print(f"{Fore.YELLOW}{Style.BRIGHT}System prompt: {Style.RESET_ALL}{system_prompt}")
        print_separator()
    
    while True:
        try:
            user_input = input(f"\n{Fore.GREEN}{Style.BRIGHT}You: {Style.RESET_ALL}").strip()
            
            if user_input.lower() in config.INTERACTIVE_COMMANDS["quit"]:
                print_success("Goodbye!")
                break
                
            if user_input.lower() == config.INTERACTIVE_COMMANDS["clear"][0]:
                claude_cli.clear_conversation()
                print("Conversation cleared")
                continue
                
            if user_input.lower().startswith(f'{config.INTERACTIVE_COMMANDS["save"]} '):
                filename = user_input[5:].strip()
                if claude_cli.save_conversation(filename):
                    print(f"Conversation saved to {filename}")
                continue
                
            if user_input.lower().startswith(f'{config.INTERACTIVE_COMMANDS["load"]} '):
                filename = user_input[5:].strip()
                if claude_cli.load_conversation(filename):
                    print(f"Conversation loaded from {filename}")
                continue
                
            if not user_input:
                continue
                
            print("\n{Fore.BLUE}{Style.BRIGHT}Claude: {Style.RESET_ALL}", end="", flush=True)
            response = claude_cli.send_message(user_input, model, max_tokens, system_prompt)
            
            if response["success"]:
                print(f"{Fore.WHITE}{response['message']}{Style.RESET_ALL}")
                if response.get("usage"):
                    usage = response["usage"]
                    print(f"\n{Fore.CYAN}{Style.DIM}[Tokens - Input: {usage.get('input_tokens', 'N/A')}, "
                          f"Output: {usage.get('output_tokens', 'N/A')}]{Style.RESET_ALL}")
            else:
                print(f"Error: {response['error']}")
                
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Interrupted by user. Goodbye!{Style.RESET_ALL}")
            break
        except EOFError:
            print(f"\n{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
            break

def single_message_mode(claude_cli: ClaudeCLI, message: str, model: str, 
                       max_tokens: int, system_prompt: Optional[str] = None) -> None:
    """
    send a single message and print the response. One-off queries

    args:
        claude_cli:
        message:
        model:
        max_tokens:
        system_prompt:
    exit codes:
        0; success
        1. error occurred 
    """
    response = claude_cli.send_message(message, model, max_tokens, system_prompt)
    
    if response["success"]:
        print(f"{Fore.WHITE}{response['message']}{Style.RESET_ALL}")
        if response.get("usage"):
            usage = response["usage"]
            print(f"\n{Fore.CYAN}{Style.DIM}[Tokens - Input: {usage.get('input_tokens', 'N/A')}, "
                  f"Output: {usage.get('output_tokens', 'N/A')}]{Style.RESET_ALL}", file=sys.stderr)
    else:
        #print(f"Error: {response['error']}", file=sys.stderr)
        print_error(response['error'])
        sys.exit(1)

def main() -> None:
    parser = argparse.ArgumentParser(
        description=config.CLI_DESCRIPTION,
        formatter_class= argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -i                                    # Interactive mode
  %(prog)s -m "Hello, Claude!"                   # Single message
  %(prog)s -f input.txt                          # Read from file
  %(prog)s -m "Explain this code" --system "You are a code reviewer"
        """
    )
    
    # API configuration
    parser.add_argument("--api-key",
                        help=f"Anthropic API key (or set {config.API_KEY_ENV_VAR} env var)")
    parser.add_argument("--model",
                        default=config.DEFAULT_MODEL, 
                       help="Claude model to use (default: %(default)s)")
    parser.add_argument("--max-tokens",
                        type=int,
                        default=config.DEFAULT_MAX_TOKENS, 
                        help="Maximum tokens in response (default: %(default)d)")
    parser.add_argument("--system",
                        help="System prompt to guide the AI behavior")
    
    # input
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--interactive", "-i",
                        action="store_true", 
                        help="Run in interactive mode")
    input_group.add_argument("--message", "-m",
                        help="Send a single message and exit")
    input_group.add_argument("--file", "-f",
                        help="Read message from file and send")

    # load /save convo
    parser.add_argument("--load",
                        help="Load conversation from file")
    parser.add_argument("--save",
                        help="Save conversation to file after completion")
    
    args = parser.parse_args()

    try:
        #init. claude cli
        claude_cli = ClaudeCLI(args.api_key)
 
        # load convo if specified
        if args.load:
            print(f"Loading conversation from {args.load}...")
            if not claude_cli.load_conversation(args.load):
                print(config.ERROR_MESSAGES["conversation_load_failed"].format(args.load),
                      file=sys.stderr)
                sys.exit(1)
            print(config.SUCCESS_MESSAGES["conversation_loaded"].format(args.load))

        # route to appro mode
        if args.interactive:
            interactive_mode(claude_cli, args.model, args.max_tokens, args.system)
        elif args.message:
            single_message_mode(claude_cli, args.message, args.model,
                              args.max_tokens, args.system)
        elif args.file:
            try:
                file_path = Path(args.file)
                if not file_path.exists():
                    print(config.ERROR_MESSAGES["file_not_found"].format(args.file),
                          file=sys.stderr)
                    sys.exit(1)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    message = f.read().strip()

                if not message:
                    print(config.ERROR_MESSAGES["file_empty"], file=sys.stderr)
                    sys.exit(1)

                single_message_mode(claude_cli, message, args.model,
                                    args.max_tokens, args.system)
            except UnicodeDecodeError:
                print(config.ERROR_MESSAGES["invalid_encoding"])

            except Exception as e:
                print(f"Error reading file: {e}", file= sys.stderr)
                sys.exit(1)

            # save convo if needed
            if args.save:
                print(f"Saving conversation to {args.save}...")
                if not claude_cli.save_conversation(args.save):
                    print(config.ERROR_MESSAGES["conversation_save_failed"].format(args.save),
                          file=sys.stderr)
                    sys.exit(1)
                print(config.SUCCESS_MESSAGES["conversation_saved"].format(args.save))

                
    except ValueError as e:
        print(config.ERROR_MESSAGES["config_error"].format(str(e)), file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(config.ERROR_MESSAGES["unexpected_error"].format(str(e)), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()