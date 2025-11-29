---
applyTo: "**/*.{yaml,yml}"
---

# YAML Instructions

**Applies to:** YAML files (Home Assistant configuration, blueprints, services)

## Schema Validation

**Available schemas:**

- `/schemas/yaml/services_schema.yaml` - For `services.yaml` files
- `/schemas/yaml/configuration_schema.yaml` - For Home Assistant configuration

Consult these schemas when unsure about structure or available options.

## Formatting

- **2 spaces** for indentation (never tabs)
- No trailing whitespace
- End files with a single newline
- Use lowercase for keys (except where case matters)

## Home Assistant Configuration

### Modern Syntax Only

**Always use modern trigger/condition/action syntax:**

```yaml
# ✅ Correct (modern)
automation:
  - alias: "Motion detected"
    trigger:
      - trigger: state
        entity_id: binary_sensor.motion
        to: "on"
    action:
      - action: light.turn_on
        target:
          entity_id: light.hallway
```

**Never use legacy platform-based syntax:**

```yaml
# ❌ Wrong (legacy)
automation:
  - alias: "Motion detected"
    trigger:
      platform: state # Don't use this!
      entity_id: binary_sensor.motion
      to: "on"
```

### Service Calls

**Use `action:` key (not `service:` in actions):**

```yaml
action:
  - action: light.turn_on # Correct
    target:
      entity_id: light.living_room
    data:
      brightness: 255
```

## Services Definition (services.yaml)

**Structure:**

```yaml
service_name:
  name: Human-Readable Name
  description: Clear description of what the service does.
  fields:
    parameter_name:
      name: Parameter Name
      description: What this parameter does.
      required: true
      example: "example_value"
      selector:
        text:
```

**Key points:**

- Always include `description` for service and each field
- Mark fields as `required: true` or `required: false`
- Provide realistic `example` values
- Use appropriate `selector` types for UI

**Selector types (common):**

- `text:` - String input
- `number:` - Numeric input
- `boolean:` - On/off switch
- `entity:` - Entity picker
- `device:` - Device picker
- `select:` - Dropdown menu

## Blueprints

### Structure

```yaml
blueprint:
  name: Blueprint Name
  description: Clear description of what this blueprint does.
  domain: automation
  input:
    trigger_entity:
      name: Trigger Entity
      description: Entity that triggers the automation.
      selector:
        entity:
          domain: binary_sensor

trigger:
  - trigger: state
    entity_id: !input trigger_entity
    to: "on"

action:
  - action: !input action_name
    target: !input target_device
```

**Best practices:**

- Clear, descriptive names for inputs
- Include helpful descriptions
- Use appropriate selectors for user-friendly UI
- Add default values where sensible

## Home Assistant Configuration (configuration.yaml)

**Minimal, clean structure:**

```yaml
# Load default configuration
default_config:

# Enable your integration
ha_integration_domain:

# Logging for development
logger:
  default: info
  logs:
    custom_components.ha_integration_domain: debug
```

**Notes:**

- Use placeholders (`ha_integration_domain`) consistently
- Keep test configuration minimal
- Use `logger:` for debugging during development

## Common Patterns

### Conditions

```yaml
condition:
  - condition: state
    entity_id: input_boolean.enable_automation
    state: "on"
  - condition: time
    after: "07:00:00"
    before: "23:00:00"
```

### Templates

```yaml
action:
  - action: notify.notify
    data:
      message: >
        Temperature is {{ states('sensor.temperature') }}°C
```

### Delays

```yaml
action:
  - action: light.turn_on
    target:
      entity_id: light.hallway
  - delay:
      seconds: 30
  - action: light.turn_off
    target:
      entity_id: light.hallway
```

## Validation

YAML files should validate against Home Assistant schemas. Check syntax with:

```bash
# Home Assistant will validate configuration on startup
script/develop  # Start HA and check logs
```

Look for schema validation errors in Home Assistant logs.

## Staying Current

**YAML syntax evolves in Home Assistant:**

- **Always check** [current automation documentation](https://www.home-assistant.io/docs/automation/)
- **Review blueprint docs** at [Home Assistant Blueprints](https://www.home-assistant.io/docs/blueprint/)
- **Search for examples:** `site:www.home-assistant.io automation [trigger type]`
- Don't use deprecated syntax even if it still works

**When implementing services or blueprints:**

- Verify current [service schema patterns](https://developers.home-assistant.io/docs/dev_101_services/)
- Check the [developer blog](https://developers.home-assistant.io/blog/) for breaking changes
- Use official examples as reference, not assumptions
