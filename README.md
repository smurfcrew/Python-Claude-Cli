# Personal Claude AI CLI


## Requirements and Set-up

1. API Key from [Anthropic](https://www.anthropic.com/)
2. Python 3.8 or higher
3. Install dependencies from `requirements.txt`
4. Unix-like environment (Linux, macOS, WSL)
 
- Python 3.8+

**Install Dependencies**

From the root directory of the project where `requirements.txt` is located, run:

```bash
pip install -r requirements.txt
```

**Setup API Key**

In your .bashrc or .zshrc file, add the following line:

```bash
export ANTHROPIC_API_KEY="your_api_key_here"
```

or

**Pass an Argument**
```bash
python claude.py --api-key "your_api_key_here" 
```

**Make Executable (optional)**
```bash
chmod +x cli.py
```

## Usage
Using ```python cli.py --help``` will show you the available options:

```bash
$ python cli.py --help                                                                   chris@semtex
usage: cli.py [-h] [--api-key API_KEY] [--model MODEL] [--max-tokens MAX_TOKENS] [--system SYSTEM] [--interactive]
              [--message MESSAGE] [--file FILE] [--load LOAD] [--save SAVE]

Claude CLI - Interact with Claude AI from the command line

options:
  -h, --help            show this help message and exit
  --api-key API_KEY     Anthropic API key (or set ANTHROPIC_API_KEY env var)
  --model MODEL         Claude model to use (default: claude-sonnet-4-20250514)
  --max-tokens MAX_TOKENS
                        Maximum tokens in response (default: 1000)
  --system SYSTEM       System prompt to use
  --interactive, -i     Run in interactive mode
  --message MESSAGE, -m MESSAGE
                        Send a single message
  --file FILE, -f FILE  Read message from file
  --load LOAD           Load conversation from file
  --save SAVE           Save conversation to file after completion
  ```

or

```bash
chmod +x cli.py
```

```bash
./cli.py --help
```