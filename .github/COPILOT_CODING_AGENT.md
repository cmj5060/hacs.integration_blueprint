# GitHub Copilot Coding Agent

Use **[GitHub Copilot Coding Agent](https://github.com/copilot/agents)** to automatically initialize this template or work on your integration.

## Template Initialization (500 Character Limit)

When creating a repository using "Use this template", GitHub provides an optional prompt field. Use this (497 characters):

```markdown
Run ./initialize.sh with: --domain <domain> --title "<Title>" --namespace "<Prefix>" --repo <owner/repo> --author "<Name>" --force

Replace:
- <domain>: lowercase_with_underscores
- <Title>: Your Integration Name
- <Prefix>: YourCamelCase (optional)
- <owner/repo>: github_user/repo_name
- <Name>: Your Name

Verify: custom_components/<domain>/ exists, manifest.json correct, README.md updated. Create PR if successful. The script deletes itself after completion.
```

**Example:** `--domain my_device --title "My Device" --repo user/hacs-my-device --author "John Doe" --force`

## Working With Initialized Integrations

Navigate to [github.com/copilot/agents](https://github.com/copilot/agents), select your repository, and describe your task:

- "Add battery level sensor from API"
- "Implement API rate limiting (10 requests/minute)"
- "Fix coordinator - expired credentials should trigger reauth"

The agent uses `AGENTS.md`, `.github/copilot-instructions.md`, and `.github/instructions/*.instructions.md` for guidance and runs `./script/check` for validation.
