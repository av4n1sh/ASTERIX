# ASTERIX

### Local AI Assistant for Automation, Data Analysis, and Defensive Cybersecurity

ASTERIX is a personal AI assistant built with Python and a local large language model. It combines conversational AI with practical tools for system information, dataset analysis, defensive cybersecurity log analysis, persistent memory, and voice output.

The project is designed to explore how AI can be combined with automation and cybersecurity-focused tools in a single desktop application.

---

## Features

### AI Assistant
- Powered locally using Ollama
- Uses the Qwen3 language model
- Natural conversational responses
- Context from previous conversations through persistent memory
- Beginner-friendly explanations and programming assistance

### Persistent Memory
ASTERIX can store previous conversations in a local JSON file.

This allows the assistant to use previous interactions as context during future conversations.

### System Information
ASTERIX can retrieve information about the computer it is running on, including:

- Operating system
- OS version
- Computer name
- CPU
- Physical CPU cores
- Logical CPU cores
- Total RAM
- Available RAM

### Data Analysis
ASTERIX includes tools for analyzing:

- CSV files
- JSON files

The data-analysis system can identify:

- Number of rows
- Number of columns
- Column names
- Missing values
- Duplicate records
- JSON structure

### Defensive Cybersecurity Analysis
ASTERIX can analyze security log files for potentially unusual activity.

The security analyzer can detect:

- Failed login attempts
- Successful login attempts
- IP addresses
- Repeated IP addresses
- Multiple failed login attempts
- Basic security warnings

These tools are intended for defensive analysis of systems and logs that the user is authorized to examine.

### Voice Output
ASTERIX uses Kokoro text-to-speech to provide spoken responses.

The voice system runs locally and allows responses to be spoken instead of only displayed as text.

### Tool Routing
ASTERIX contains a tool router that determines which tool should handle a user's request.

For example:

```text
User
 ↓
ASTERIX Brain
 ↓
Tool Router
 ├── System Information
 ├── Data Analysis
 └── Security Analysis