# Blackwall Terminal Interface

The Blackwall Terminal Interface provides an easy-to-use command-line menu for interacting with the Blackwall system. This tool allows you to:

## Features

- 🌟 **Unified Looking Glass**: Combined visualization and interaction UI
- 📊 **Optimized Dashboard**: Fast and responsive data visualization
- 🪞 **Classic Log Graph**: Original detailed analytics
- 🎮 **Pygame UI**: Interactive fragment visualization
- 🧠 **Continuous Learning Mode**: Keep Blackwall running and learning indefinitely
- 🧪 **Test Batch Mode**: Process a specific number of test prompts
- 💬 **Interactive Mode**: Real-time conversation with Blackwall
- 📜 **Log Viewer**: Display recent log entries
- 🔧 **LLM Configuration**: Configure the LLM service settings

## Quick Start

### Windows

1. Ensure your Anaconda environment is activated: `conda activate blackwall`
2. Start LM Studio and load the Qwen3-14B model at http://169.254.83.107:1234
3. Run `run_blackwall_terminal.bat`

### Linux/Mac

1. Ensure your Anaconda environment is activated: `conda activate blackwall`
2. Start LM Studio and load the Qwen3-14B model at http://169.254.83.107:1234
3. Run `./run_blackwall_terminal.sh`

## Visualization Options

### Unified Looking Glass

The most comprehensive interface that combines all visualization options with direct interaction capabilities. This interface includes:

- Real-time fragment visualization
- Interactive emotional data plotting
- Weight and fusion data visualization
- Direct LLM interaction

### Optimized Dashboard

A faster, more responsive version of the log visualizer with improved performance and reduced lag. Ideal for:

- Reviewing large amounts of log data
- Tracking fragment weight changes over time
- Analyzing blend usage patterns

### Classic Log Graph

The original detailed data visualization tool providing in-depth analysis of Blackwall's emotional processing.

### Pygame UI

An interactive visualization showing fragment activation and providing a more immersive view of Blackwall's internal state.

## Operational Modes

### Continuous Learning Mode

Runs Blackwall indefinitely, processing prompts and learning from interactions. This mode will continue until manually stopped and is ideal for:

- Long-term autonomous learning
- Building up a robust history of interactions
- Developing more refined emotional processing

### Test Batch Mode

Processes a specific number of test prompts from the test prompts file. Useful for:

- Testing specific changes to the pipeline
- Validating fusion logic or style transfer
- Generating controlled data for analysis

### Interactive Mode

Direct conversation with Blackwall in real-time through the terminal. Perfect for:

- Testing specific prompts
- Immediate feedback on responses
- Exploring emotional reactions to various inputs

## LLM Configuration

The terminal interface allows you to configure LLM settings including:

- API endpoint URL
- Model identifier 
- Other parameters (through the config file)

Default values are set to:
- URL: http://169.254.83.107:1234/v1/chat/completions
- Model: qwen/qwen3-14b

## System Requirements

- Anaconda environment with Python 3.8+
- Required packages: pygame, matplotlib, numpy, requests
- Qwen3-14B model running on LM Studio
- Minimum 16GB RAM recommended for optimal performance

## Troubleshooting

If you encounter issues:

1. Verify your Anaconda environment is active
2. Check that LM Studio is running with the correct model loaded
3. Ensure all required Python packages are installed
4. Check the log files for specific error messages

For persistent problems, check the `ERROR_LOG.md` file for detailed error information.
