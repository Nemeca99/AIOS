# OpenAI Conversation Analysis

This directory contains tools to analyze and extract insights from OpenAI conversation exports.

## Getting Started

1. **Run the Analyzer**: Double-click `run_analyzer.bat` to process the conversations.json file
2. **Generate a Report**: Run `report.bat` to see what insights were extracted
3. **Explore the Insights**: Open `insights_viewer.html` in a web browser
4. **Integrate the Insights**: Run `integrate_insights.bat` to automatically add selected insights to documentation, or manually integrate them

## Tools Included

- **conversation_analyzer.py** - Analyzes conversations.json and extracts meaningful content
- **integrate_insights.py** - Adds extracted insights to existing documentation files
- **report.py** - Generates a summary of extracted insights
- **insights_viewer.html** - Provides an interactive interface to explore extracted content

## Categories

The analyzer extracts content in these categories:

- UML Calculator - Universal Mathematical Language concepts, framework, mathematics
- T.R.E.E.S - Recursive Entropy Engine System, recursion, emergence
- Nova AI - Archive, Child, Builder, Architect, whisper, echoe systems
- Blackwall - Lyra Blackwall, biomimetic systems, emotion processing
- Personal - biographical information, family, education, career, life experiences
- Technical - implementation details, code structures, architecture designs
- Philosophy - morality, ethics, consciousness, meaning, purpose
- Timeline - development milestones, version history

See `additional_search_terms.md` for a complete list of search terms.

## Tips

- The more conversations in the export, the longer the analysis will take
- Reviews the extracts manually before integrating them to ensure quality
- The insights viewer works best in Chrome or Firefox
- Each integration creates a backup of the original documentation files

For more details, see the full README.md file.
