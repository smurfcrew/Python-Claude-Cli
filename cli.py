#!/usr/bin/env python3
"""
claude cli: command-line interface with Claude AI
"""

import os
import sys
import json
import argparse
from typing import List, Dict, Any
import requests
from pathlib import Path

class ClaudeCLI:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("API key required. Set ANTHROPIC_API_KEY environment variable or pass --api-key")
        
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        self.conversation_history = []
        
    def send_message(self, message: str, model: str = "claude-sonnet-4-20250514", 
                    max_tokens: int = 1000, system_prompt: str = None) -> Dict[str, Any]:

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
                "error": f"API request failed: {str(e)}",
                "message": None
            }
        except KeyError as e:
            return {
                "success": False,
                "error": f"Unexpected API response format: {str(e)}",
                "message": None
            }
    
    def clear_conversation(self):
        self.conversation_history = []
        
    def save_conversation(self, filename: str):
        try:
            with open(filename, 'w') as f:
                json.dump(self.conversation_history, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return False
            
    def load_conversation(self, filename: str):
        """Load convo from file"""
        try:
            with open(filename, 'r') as f:
                self.conversation_history = json.load(f)
            return True
        except Exception as e:
            print(f"Error loading conversation: {e}")
            return False

def interactive_mode(claude_cli: ClaudeCLI, model: str, max_tokens: int, system_prompt: str = None):
    """use interactive mode"""
    print("Claude CLI - Interactive Mode")
    print("Type 'quit', 'exit', or 'q' to quit")
    print("Type 'clear' to clear conversation history")
    print("Type 'save <filename>' to save conversation")
    print("Type 'load <filename>' to load conversation")
    print("-" * 50)
    
    if system_prompt:
        print(f"System prompt: {system_prompt}")
        print("-" * 50)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
                
            if user_input.lower() == 'clear':
                claude_cli.clear_conversation()
                print("Conversation cleared.")
                continue
                
            if user_input.lower().startswith('save '):
                filename = user_input[5:].strip()
                if claude_cli.save_conversation(filename):
                    print(f"Conversation saved to {filename}")
                continue
                
            if user_input.lower().startswith('load '):
                filename = user_input[5:].strip()
                if claude_cli.load_conversation(filename):
                    print(f"Conversation loaded from {filename}")
                continue
                
            if not user_input:
                continue
                
            print("\nClaude: ", end="", flush=True)
            response = claude_cli.send_message(user_input, model, max_tokens, system_prompt)
            
            if response["success"]:
                print(response["message"])
                if response.get("usage"):
                    usage = response["usage"]
                    print(f"\n[Tokens - Input: {usage.get('input_tokens', 'N/A')}, "
                          f"Output: {usage.get('output_tokens', 'N/A')}]")
            else:
                print(f"Error: {response['error']}")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break

def single_message_mode(claude_cli: ClaudeCLI, message: str, model: str, 
                       max_tokens: int, system_prompt: str = None):
    """send a single message and print the response"""
    response = claude_cli.send_message(message, model, max_tokens, system_prompt)
    
    if response["success"]:
        print(response["message"])
        if response.get("usage"):
            usage = response["usage"]
            print(f"\n[Tokens - Input: {usage.get('input_tokens', 'N/A')}, "
                  f"Output: {usage.get('output_tokens', 'N/A')}]", file=sys.stderr)
    else:
        print(f"Error: {response['error']}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Claude CLI - Interact with Claude AI from the command line")
    
    # API configuration
    parser.add_argument("--api-key", help="Anthropic API key (or set ANTHROPIC_API_KEY env var)")
    parser.add_argument("--model", default="claude-sonnet-4-20250514", 
                       help="Claude model to use (default: claude-sonnet-4-20250514)")
    parser.add_argument("--max-tokens", type=int, default=1000, 
                       help="Maximum tokens in response (default: 1000)")
    parser.add_argument("--system", help="System prompt to use")
    
    # Input modes
    parser.add_argument("--interactive", "-i", action="store_true", 
                       help="Run in interactive mode")
    parser.add_argument("--message", "-m", help="Send a single message")
    parser.add_argument("--file", "-f", help="Read message from file")
    
    # Conversation management
    parser.add_argument("--load", help="Load conversation from file")
    parser.add_argument("--save", help="Save conversation to file after completion")
    
    args = parser.parse_args()
    
    # Validate arguments
    if not any([args.interactive, args.message, args.file]):
        parser.error("Must specify one of: --interactive, --message, or --file")
    
    try:
        claude_cli = ClaudeCLI(args.api_key)
        
        # Load conversation if specified
        if args.load:
            if not claude_cli.load_conversation(args.load):
                sys.exit(1)
        
        if args.interactive:
            interactive_mode(claude_cli, args.model, args.max_tokens, args.system)
        elif args.message:
            single_message_mode(claude_cli, args.message, args.model, args.max_tokens, args.system)
        elif args.file:
            try:
                with open(args.file, 'r') as f:
                    message = f.read().strip()
                single_message_mode(claude_cli, message, args.model, args.max_tokens, args.system)
            except FileNotFoundError:
                print(f"Error: File '{args.file}' not found", file=sys.stderr)
                sys.exit(1)
        
        # Save conversation if specified
        if args.save:
            if not claude_cli.save_conversation(args.save):
                sys.exit(1)
                
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()