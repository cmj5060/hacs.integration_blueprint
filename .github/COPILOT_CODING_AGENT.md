# GitHub Copilot Coding Agent Integration

This document explains how to use **GitHub Copilot Coding Agent** with this Integration Blueprint template repository.

## Overview

**GitHub Copilot Coding Agent** is an autonomous coding assistant available at [github.com/copilot/agents](https://github.com/copilot/agents). It can:

- Create and modify code across multiple files
- Run validation scripts and respond to errors
- Create pull requests with comprehensive changes
- Work with template repositories to initialize new projects

## Using Copilot Coding Agent After "Use This Template"

When you create a new repository from this blueprint using "Use this template" on GitHub, you can optionally provide initialization instructions for Copilot Coding Agent.

### Quick Start Prompt

After clicking "Use this template", GitHub may offer an optional prompt field for Copilot Coding Agent. Use this prompt:

```markdown
Initialize this Home Assistant custom integration from the blueprint template using the initialize.sh script in unattended mode.

Integration details:
- Domain: <your_integration_domain>
- Title: <Your Integration Title>
- Namespace: <YourIntegrationPrefix>
- Repository: <your-username/your-repo-name>
- Author: <Your Name>

Steps:
1. Run the initialization script in unattended mode:
   ```bash
   ./initialize.sh \
     --domain <your_integration_domain> \
     --title "<Your Integration Title>" \
     --namespace "<YourIntegrationPrefix>" \
     --repo <your-username/your-repo-name> \
     --author "<Your Name>" \
     --force
   ```

2. Verify the initialization was successful by checking:
   - `custom_components/<your_integration_domain>/` directory exists
   - `manifest.json` has correct domain and repository
   - `README.md` reflects the new integration name

3. If initialization successful, create a pull request with the changes.

Important notes:

- The `--force` flag is REQUIRED for unattended mode
- The initialize.sh script will DELETE ITSELF after successful completion
- All instruction files (.github/instructions/*.instructions.md, AGENTS.md, .github/copilot-instructions.md) will remain and guide future development

```

### Parameter Examples

Replace the placeholders with your actual values:

| Parameter | Example | Description |
|-----------|---------|-------------|
| `<your_integration_domain>` | `my_smart_device` | Python-safe domain name (lowercase, underscores) |
| `<Your Integration Title>` | `My Smart Device` | Human-readable integration name |
| `<YourIntegrationPrefix>` | `MySmartDevice` | CamelCase class prefix (optional, auto-generated if omitted) |
| `<your-username/your-repo-name>` | `johndoe/hacs-my-smart-device` | GitHub repository in `owner/repo` format |
| `<Your Name>` | `John Doe` | Your name for the LICENSE file |

### Detailed Example

```markdown
Initialize this Home Assistant custom integration from the blueprint template using the initialize.sh script in unattended mode.

Integration details:
- Domain: philips_hue_advanced
- Title: Philips Hue Advanced
- Namespace: PhilipsHueAdvanced
- Repository: johndoe/hacs-philips-hue-advanced
- Author: John Doe

Steps:
1. Run the initialization script in unattended mode:
   ```bash
   ./initialize.sh \
     --domain philips_hue_advanced \
     --title "Philips Hue Advanced" \
     --namespace "PhilipsHueAdvanced" \
     --repo johndoe/hacs-philips-hue-advanced \
     --author "John Doe" \
     --force
   ```

2. Verify the initialization was successful by checking:
   - `custom_components/philips_hue_advanced/` directory exists
   - `manifest.json` has correct domain and repository
   - `README.md` reflects the new integration name

3. If initialization successful, create a pull request with the changes.

Important notes:

- The `--force` flag is REQUIRED for unattended mode
- The initialize.sh script will DELETE ITSELF after successful completion
- All instruction files (.github/instructions/*.instructions.md, AGENTS.md, .github/copilot-instructions.md) will remain and guide future development

```

## How Copilot Coding Agent Reads Instructions

Copilot Coding Agent automatically discovers and uses:

1. **`.github/copilot-instructions.md`** - Repository-wide instructions (applies to all files)
2. **`.github/instructions/*.instructions.md`** - Path-specific instructions with `applyTo` frontmatter
3. **`AGENTS.md`** - High-level project guide for AI agents (nearest file in directory tree takes precedence)

All these files are preserved after initialization and will guide the coding agent when working on your integration.

### Agent-Specific Instructions

Since November 2025, you can use the `excludeAgent` frontmatter to control which agents use specific instructions:

```yaml
---
applyTo: "**/*.py"
excludeAgent: "code-review"  # Only coding agent will use these instructions
---
```

Or:

```yaml
---
applyTo: "**/*.py"
excludeAgent: "coding-agent"  # Only code review will use these instructions
---
```

## Working With an Already-Initialized Integration

If you're working with a repository that was already initialized from this blueprint:

1. **Navigate to** [github.com/copilot/agents](https://github.com/copilot/agents)
2. **Select your repository** from the dropdown menu
3. **Describe your task** in natural language

Example prompts:

```markdown
Add a new sensor platform that displays battery level from the API
```

```markdown
Implement rate limiting in the API client to respect the device's limit of 10 requests per minute
```

```markdown
Fix the coordinator error handling - expired credentials should trigger reauth flow instead of logging errors
```

The coding agent will:

- Read `AGENTS.md` for project overview and workflow guidance
- Read `.github/copilot-instructions.md` for repository context
- Apply path-specific instructions from `.github/instructions/*.instructions.md` based on files being edited
- Run validation scripts (`./script/check`) to ensure code quality
- Create a pull request when the task is complete

## Benefits of This Blueprint for Copilot Coding Agent

This blueprint is specifically optimized for AI coding assistants:

✅ **Comprehensive instruction files** guide code generation to follow Home Assistant Core patterns

✅ **Validation scripts** (`script/check`, `script/test`) allow the agent to verify changes immediately

✅ **Clear project structure** documented in `AGENTS.md` and `docs/development/ARCHITECTURE.md`

✅ **Path-specific guidance** ensures appropriate patterns for each file type (Python, YAML, JSON, etc.)

✅ **Unattended initialization** lets the agent set up new projects without manual intervention

## Troubleshooting

### Initialization Script Fails

If `initialize.sh` fails during Copilot Coding Agent execution:

1. **Check the error message** - The script provides detailed error output
2. **Verify parameters** - Ensure domain name is Python-safe (lowercase, underscores only)
3. **Check repository format** - Must be `owner/repo` (e.g., `johndoe/my-integration`)
4. **Missing --force flag** - Unattended mode REQUIRES `--force` for safety

### Agent Doesn't Use Instructions

If the coding agent seems to ignore instruction files:

1. **Verify files exist**:
   - `.github/copilot-instructions.md`
   - `.github/instructions/*.instructions.md`
   - `AGENTS.md`

2. **Check frontmatter** in path-specific instructions:

   ```yaml
   ---
   applyTo: "**/*.py"
   ---
   ```

3. **Enable custom instructions** - Repository settings → Copilot → Code review → "Use custom instructions when reviewing pull requests"

### Agent Creates Code That Fails Validation

If the generated code doesn't pass `script/check`:

1. **Let the agent fix it** - Copilot Coding Agent can read error output and iterate
2. **Check instruction completeness** - Ensure relevant `.instructions.md` files have clear patterns
3. **Update instructions** - If the agent consistently makes the same mistake, update instruction files

## Additional Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Adding Repository Custom Instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot)
- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [Integration Quality Scale](https://developers.home-assistant.io/docs/integration_quality_scale_index)

## Getting Help

If you encounter issues using Copilot Coding Agent with this blueprint:

1. **Check this document** first for common scenarios
2. **Review `AGENTS.md`** for general AI agent guidance
3. **Open an issue** in the [blueprint repository](https://github.com/jpawlowski/hacs.integration_blueprint)
4. **Consult GitHub's Copilot documentation** for agent-specific questions
