---
applyTo: "**/*.json"
---

# JSON Instructions

**Applies to:** JSON configuration files

## Schema Validation

**Available schemas:**

- `/schemas/json/manifest_schema.json` - For `manifest.json`
- `/schemas/json/translation_schema.json` - For translation files in `translations/`
- `/schemas/json/hacs_schema.json` - For `hacs.json`

Always validate JSON structure against the appropriate schema when available.

## Formatting

- **2 spaces** for indentation
- No trailing commas
- No comments (JSON spec doesn't support them)
- Use double quotes for all strings
- End files with a single newline

## Common Files

### manifest.json

Located at `custom_components/ha_integration_domain/manifest.json`. Required fields:

- `domain` - Must match directory name
- `name` - Display name (use "Integration Blueprint")
- `version` - Semantic version
- `documentation` - Link to docs
- `issue_tracker` - Link to GitHub issues
- `requirements` - Python package dependencies
- `dependencies` - Home Assistant integration dependencies
- `codeowners` - GitHub usernames (e.g., `["@jpawlowski"]`)

**Schema:** `/schemas/json/manifest_schema.json`

### Translation Files

Located at `custom_components/ha_integration_domain/translations/*.json` (e.g., `en.json`).

Structure:

```json
{
  "config": {
    "step": {
      "user": {
        "title": "Configure Integration Blueprint",
        "description": "Enter configuration details",
        "data": {
          "host": "Host",
          "username": "Username"
        }
      }
    },
    "error": {
      "cannot_connect": "Failed to connect",
      "invalid_auth": "Invalid credentials"
    }
  },
  "options": {},
  "entity": {},
  "selector": {}
}
```

**Schema:** `/schemas/json/translation_schema.json`

### hacs.json

Located at repository root. Defines HACS-specific metadata:

```json
{
  "name": "Integration Blueprint",
  "render_readme": true,
  "homeassistant": "2025.7.0"
}
```

**Schema:** `/schemas/json/hacs_schema.json`

## Validation

JSON files are validated automatically by:

- Home Assistant on startup (manifest.json, translations)
- HACS validation for hacs.json
- Schema validation tools

Use `python -m json.tool <file>.json` to validate syntax.

## Best Practices

- Keep translation keys consistent across languages
- Use semantic versioning in manifest.json
- Document all requirements with version constraints
- Include helpful descriptions in translation strings
- Validate against schema before committing
