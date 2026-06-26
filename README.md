# BYTE AGENT

A local, personalized AI coding agent that lives on your machine.

## Features

- **Local-First**: Runs entirely on your machine - no data leaves your computer
- **Personalized**: Adapts to your coding style, preferences, and workflows
- **Multi-Model Support**: Works with OpenAI, Ollama, or any OpenAI-compatible API
- **Code Intelligence**: Read, write, edit, search, and understand codebases
- **Terminal Operations**: Execute commands, run scripts, manage processes
- **Git Integration**: Commit, branch, diff, and manage repositories
- **Memory System**: Learns from interactions and remembers context
- **Skills System**: Extensible with custom skills and plugins
- **Session Management**: Save and resume conversations

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run BYTE AGENT
python -m byte_agent

# Or use the CLI
byte-agent
```

## Configuration

Edit `config.json` to customize:

```json
{
  "agent_name": "BYTE",
  "personality": "helpful",
  "model": "gpt-4",
  "theme": "cyberpunk"
}
```

## Architecture

```
byte_agent/
├── core/           # Core agent logic
├── skills/         # Skill modules
├── memory/         # Memory and context
├── tools/          # Tool implementations
└── utils/          # Utilities
```

## License

MIT
