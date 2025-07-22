# Personal Claude AI CLI

Useful for when people cannot access a graphical interface/browser. 

So that people can interact with Claude AI from the command line, this project provides a simple and flexible CLI tool. It supports multiple modes of interaction, including interactive sessions, single message queries, and file-based input.

## Features
 - **Interactive Mode**
 - **Single Message Mode**
 - **File Input Mode**
 - **Conversation Management**

## Requirements and Set-up

### Pre-requisites
1. Python 3.8 or higher
2. API Key from [Anthropic](https://www.anthropic.com/) Costs may apply based on usage.
3. Unix-like environment (Linux, macOS, WSL)

**UNTESTED Windows support (may require additional configuration) by using API key as an argument or setting it as an environment variable.**

**Installation**

**Option 1: Basic Installation**

From the root directory of the project where `requirements.txt` is located, run:

```bash
pip install -r requirements.txt
```

**Option 2: Basic Installation**
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

**Option 3: Package Installation (Recommended)**
```bash
pip install -e . # where -e is for editable install
```

## API Key Configuration

**Environment Variable(Recommended)**
In your .bashrc or .zshrc file, add the following line:

```bash
export ANTHROPIC_API_KEY="your_api_key_here"
```

**Pass as an Argument**
```bash
python cli.py --api-key "your_api_key_here" 
```

**Make Executable (optional)**
```bash
chmod +x cli.py
```

## Usage

**Command Line Help**

```bash
 python cli.py -h
usage: cli.py [-h] [--api-key API_KEY] [--model MODEL] [--max-tokens MAX_TOKENS] [--system SYSTEM]
              (--interactive | --message MESSAGE | --file FILE) [--load LOAD] [--save SAVE]

Interact with Claude AI from the command line

options:
  -h, --help            show this help message and exit
  --api-key API_KEY     Anthropic API key (or set ANTHROPIC_API_KEY env var)
  --model MODEL         Claude model to use (default: claude-3-5-sonnet-20241022)
  --max-tokens MAX_TOKENS
                        Maximum tokens in response (default: 1000)
  --system SYSTEM       System prompt to guide the AI behavior
  --interactive, -i     Run in interactive mode
  --message MESSAGE, -m MESSAGE
                        Send a single message and exit
  --file FILE, -f FILE  Read message from file and send
  --load LOAD           Load conversation from file
  --save SAVE           Save conversation to file after completion

Examples:
  cli.py -i                                    # Interactive mode
  cli.py -m "Hello, Claude!"                   # Single message
  cli.py -f input.txt                          # Read from file
  cli.py -m "Explain this code" --system "You are a code reviewer"
```

### Interactive Mode

Start a conversation session with Claude:

```bash
python cli.py --interactive
# or 
python cli.py -i
```
**Interactive Commands:**
- `quit`, `exit`, `q` - Exit the session
- `clear` - Clear conversation history
- `save <filename>` - Save conversation to JSON file
- `load <filename>` - Load conversation from JSON file

### Single Message Mode
Send a one-off message:
```bash
python cli.py --message "Explain quantum computing"
# or
python cli.py -m "What is the capital of France?"
```

### File Input Mode
Process text from a file:
```bash
python cli.py --file document.txt
# or
python cli.py -f code.py
```

## Error Handling

The CLI provides comprehensive error handling for:
- Invalid API keys
- Network connectivity issues
- File access problems
- Malformed JSON in conversation files
- Invalid command line arguments
- API rate limiting and errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run tests and linting
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
