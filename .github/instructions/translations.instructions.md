---
applyTo: "**/translations/*.json"
---

# Translation Files Instructions

**Applies to:** `custom_components/ha_integration_domain/translations/*.json`

## Schema Validation

**Schema:** `/schemas/json/translation_schema.json`

Translation files define user-facing text for config flows, options, entities, and errors.

## Structure

```json
{
  "config": {
    "step": {},
    "error": {},
    "abort": {}
  },
  "options": {
    "step": {},
    "error": {}
  },
  "entity": {},
  "entity_component": {},
  "selector": {},
  "services": {}
}
```

## Config Flow Translations

**Step translations:**

```json
"config": {
  "step": {
    "user": {
      "title": "Configure Integration Blueprint",
      "description": "Enter your device details",
      "data": {
        "host": "Host",
        "username": "Username",
        "password": "Password"
      },
      "data_description": {
        "host": "IP address or hostname of the device"
      }
    }
  }
}
```

**Error translations:**

```json
"config": {
  "error": {
    "cannot_connect": "Failed to connect to the device",
    "invalid_auth": "Invalid username or password",
    "unknown": "An unexpected error occurred"
  }
}
```

**Abort reasons:**

```json
"config": {
  "abort": {
    "already_configured": "This device is already configured",
    "reauth_successful": "Re-authentication successful"
  }
}
```

## Entity Translations

Override entity names and state values:

```json
"entity": {
  "sensor": {
    "air_quality": {
      "name": "Air Quality Index"
    },
    "temperature": {
      "name": "Temperature"
    }
  }
}
```

## Entity Component Translations

For entity attributes and states:

```json
"entity_component": {
  "_": {
    "name": "Integration Blueprint",
    "state": {
      "problem": {
        "off": "OK",
        "on": "Problem Detected"
      }
    }
  }
}
```

## Service Translations

Translate service names and descriptions:

```json
"services": {
  "reset_filter": {
    "name": "Reset Filter",
    "description": "Resets the filter replacement indicator"
  }
}
```

## Selector Translations

For custom selectors used in config/options:

```json
"selector": {
  "update_mode": {
    "options": {
      "auto": "Automatic",
      "manual": "Manual"
    }
  }
}
```

## Best Practices

- Use clear, concise language
- Provide helpful descriptions for non-obvious fields
- Keep consistent terminology across translations
- Include units where applicable
- Use proper capitalization
- Avoid technical jargon when possible

## Multi-Language Support

Create separate files for each language:

- `en.json` - English (base language)
- `de.json` - German
- `fr.json` - French
- etc.

All files should have the same structure with translated values.

## Translation Keys

Keys reference config flow steps, entity IDs, and service names from code:

- Config step: `config.step.{step_id}.title`
- Error: `config.error.{error_key}`
- Entity: `entity.{domain}.{entity_key}.name`
- Service: `services.{service_name}.name`

## Common Mistakes

- ❌ Inconsistent key structure across languages
- ❌ Missing required keys (title, description)
- ❌ Untranslated English text in non-English files
- ❌ Invalid JSON syntax
- ❌ Keys that don't match code

## Validation

Translation files are validated by Home Assistant on load. Missing keys fall back to entity/service names from code.

## References

- [Translation Documentation](https://developers.home-assistant.io/docs/internationalization/)
- [Translation Best Practices](https://developers.home-assistant.io/docs/internationalization/core)
