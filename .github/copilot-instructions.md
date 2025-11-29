# GitHub Copilot Instructions

This file provides specific guidance for GitHub Copilot when generating code for this Home Assistant integration.

## Critical Reminders

### Project Information

This integration:

- **Domain:** `ha_integration_domain`
- **Title:** Integration Blueprint
- **Class prefix:** `IntegrationBlueprint`

Use these exact identifiers throughout the codebase. Never hardcode different values.

### Code Quality Baseline

- **Python:** 4 spaces, 120 char lines, full type hints, async for all I/O
- **YAML:** 2 spaces, modern Home Assistant syntax (no legacy `platform:` style)
- **JSON:** 2 spaces, no trailing commas, no comments

### Validation Before Completion

Before considering any coding task complete, the following must pass:

```bash
script/check      # Runs type-check + lint-check + spell-check
```

Generate code that passes these checks on first run. Common pitfalls:

- Missing type annotations → Pyright fails
- Unused imports → Ruff fails
- Blocking I/O in async functions → Design flaw
- Magic numbers → Use module constants

**Linter overrides:** You may use `# noqa: CODE` or `# type: ignore` when necessary, but use sparingly with specific codes and explanatory comments. Prefer fixing issues over suppressing them.

## Workflow Approach

1. **Small, focused changes** - Avoid large refactorings unless explicitly requested
2. **Focus on functionality** - Implement features and fix bugs
3. **Documentation updates** - Update docstrings if behavior changes
4. **Validation** - Run `script/check` to ensure code quality
5. **File organization** - Keep files manageable (~200-400 lines). Split large files into smaller modules.

**Important: Do NOT write tests unless explicitly requested.** Focus on implementing functionality. The developer decides when and if tests are needed.

## When Uncertain - Research First

**Don't guess - look it up!**

If context is insufficient or requirements are ambiguous:

1. **Search [Home Assistant docs](https://developers.home-assistant.io/)** for current patterns
2. Check the [developer blog](https://developers.home-assistant.io/blog/) for recent changes
3. Look at existing patterns in similar files (e.g., existing sensor implementations)
4. Search: `site:developers.home-assistant.io [your question]` for official guidance
5. Run `script/check` early and often - catch issues before they compound
6. Consult [Ruff rules](https://docs.astral.sh/ruff/rules/) or [Pyright docs](https://microsoft.github.io/pyright/) when validation fails
7. Ask for clarification rather than implementing based on assumptions

**Home Assistant evolves rapidly** - verify current best practices rather than relying on outdated knowledge.

Focus on maintainable, testable code that follows established patterns in the integration.

## Working With the Developer

**When requests conflict with these instructions:**

1. Clarify if deviation is intentional
2. Confirm you understood correctly
3. Suggest updating instructions if this is a permanent change
4. Proceed after confirmation

**Maintaining instructions:**

- This project is evolving - instructions should too
- Suggest updates when patterns change
- Keep this file under ~100 lines
- Remove outdated rules, don't just add new ones

**Documentation Strategy:**

- **Developer docs:** Use `docs/development/` (architecture, decisions, internal design)
- **User docs:** Use `docs/user/` (installation, configuration, examples for end-users)
- **Temporary planning:** Use `.ai-scratch/` (never committed, AI-only scratch files)
- **No random markdown files** - all documentation must go into `docs/` or `.ai-scratch/`
- Prefer extending existing docs over creating new files
- Don't write docs unless asked, but suggest when complex features need documentation

**Session management:**

- When a task is complete and developer moves to new topic: suggest committing changes and offer commit message
- Monitor context size - warn if getting large and new topic starts
- Offer to create summary for fresh session if context is strained
- Suggest once, don't nag if declined
