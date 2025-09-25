# Extraction & Integration Instructions for T.R.E.E.S. Codex

## Purpose
This file documents the rules and best practices for extracting, summarizing, and integrating content from the UML Codex and related folders into the T.R.E.E.S. master codex. It is intended for use by both human editors and automated assistants.

## Extraction Rules

1. **File Types to Process**
   - Always include: `.md`, `.txt`, `.docx`, `.pdf`, `.py`, `.png`, `.jpeg`, `.jpg`.
   - For `.txt` files, only scan and extract from files that are readable and not excessively large (avoid files that are too big to process or are corrupted).
   - Special handling for conversation exports: `.json` files from OpenAI exports should be processed using the conversation analyzer tools.

2. **Order of Processing**
   - Process by file type and folder, one group at a time: `.md` → `.txt` → `.docx` → `.pdf` → `.py` → conversation extracts → images.
   - Within each group, prioritize files with unique theory, algorithms, diagrams, or foundational content.
   - For conversation analysis, use the tools in the `Conversations` folder to extract categorized insights first.

3. **Conversation Analysis Integration**
   - Use the conversation analyzer in `D:\UML Calculator\Conversations\` to extract insights from OpenAI conversation exports
   - The analyzer categorizes content into: UML Calculator, T.R.E.E.S, Nova AI, Blackwall, Personal, Technical, Philosophy, and Timeline
   - Run `run_analyzer.bat` to process conversations.json and generate categorized extract files
   - Review extracted content before integrating into the main codex to ensure quality and relevance
   - Use `integrate_insights.bat` for automated integration or manually select the most relevant insights

4. **Integration**
   - Summarize and integrate only unique, theory-relevant, or implementation-critical content.
   - Avoid duplicating content already present in the codex.
   - Cross-reference sections and appendices as needed for clarity and completeness.
   - For conversation insights, prioritize content that provides new theoretical understanding or implementation details.

4. **Large Files**
   - If a file is too large to process directly, skip it or summarize its purpose if possible.
   - Note any skipped files in a log or appendix for future review.

5. **Instruction Maintenance**
   - Update this file as new rules, file types, or best practices emerge.
   - Use this as a checklist for future codex expansions or migrations.

## Best Practices

- Always preserve the integrity of UML and RIS logic—these are foundational.
- Document all major integrations and changes in the codex or a changelog.
- When in doubt, ask for clarification or review with the project owner.
- For conversation analysis, focus on extracting insights that reveal new theoretical understanding, implementation approaches, or biographical context that enriches the overall narrative.
- The conversation analyzer includes expanded search terms for: child, builder, architect, archive, framework, whisper, echoe, personality, jarvis, star trek, morality, emergent, emotions, job, money, life, family, kids, education, and many related concepts.

## Conversation Analysis Workflow

1. **Preparation**: Ensure conversations.json is in `D:\UML Calculator\OpenAIExport\`
2. **Analysis**: Run `D:\UML Calculator\Conversations\run_analyzer.bat`
3. **Review**: Check generated extract files for quality and relevance
4. **Integration**: Use `integrate_insights.bat` for automatic integration or manually select insights
5. **Documentation**: Update this file if new patterns or categories are needed

## File Linking and References

- All tools in the `Conversations` folder are properly linked and functional
- The conversation analyzer includes advanced pattern recognition for complex discussions
- Extract files are automatically generated in markdown format for easy integration
- The `additional_search_terms.md` file documents all search capabilities

---

This file ensures that the T.R.E.E.S. codex remains comprehensive, organized, and easy to maintain as your theory and implementation evolve.
