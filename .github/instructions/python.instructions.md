---
applyTo: "**/*.py"
---

# Python Code Instructions

**Applies to:** All Python files in the integration

## File Structure

### Module Organization

**Integration modules:**

- `__init__.py` - Platform setup with `async_setup_entry()`
- Individual files - One class per file when practical
- `const.py` - Module constants only (no logic)

**File size guidelines:**

- **Target:** 200-400 lines per file
- **Maximum:** ~500 lines before refactoring
- **Reason:** AI models have context limits - keep files manageable

**When a file grows too large:**

1. Extract helper functions to separate files
2. Move entity classes to individual files
3. Create subpackages for related functionality
4. Split constants into logical groups

**Example structure:**

```
sensor/
  __init__.py          # Setup and entity list (50 lines)
  air_quality.py       # Air quality sensor class (200 lines)
  temperature.py       # Temperature sensor class (150 lines)
  diagnostic.py        # Diagnostic sensors (180 lines)
  const.py             # Sensor-specific constants (30 lines)
```

**Naming:**

- Files: `snake_case.py`
- Classes: `PascalCase` prefixed with `IntegrationBlueprint`
- Functions/methods: `snake_case`
- Constants: `UPPER_SNAKE_CASE`

## Type Annotations

**Required for:**

- All function parameters
- All function return values
- Class attributes (when not obvious)

**Import from:**

- `from __future__ import annotations` (always first import)
- `typing` for complex types
- `collections.abc` for abstract base classes (prefer over `typing`)

**Example:**

```python
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

async def process_data(input_data: Mapping[str, Any]) -> dict[str, Any]:
    """Process input data."""
    ...
```

## Async Patterns

**All I/O operations must be async:**

- Network requests (aiohttp)
- File operations (aiofiles if needed)
- Database queries
- Any blocking operation

**Use:**

- `async def` for coroutines
- `await` for async calls
- `asyncio.gather()` for concurrent operations
- `asyncio.timeout()` for timeouts (not `async_timeout`)

**Never:**

- `time.sleep()` → use `await asyncio.sleep()`
- Synchronous HTTP libraries → use `aiohttp`
- Blocking operations in coordinator or entity code

## Imports

**Order (separated by blank lines):**

1. `from __future__ import annotations`
2. Standard library
3. Third-party packages
4. Home Assistant core
5. Local integration imports

**Home Assistant aliases:**

```python
import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.util import dt as dt_util
```

## Entity Classes

**Structure:**

```python
from homeassistant.components.sensor import SensorEntity

from ..const import DOMAIN
from ..coordinator import IntegrationBlueprintDataUpdateCoordinator
from ..entity import IntegrationBlueprintEntity

class IntegrationBlueprintSomeSensor(SensorEntity, IntegrationBlueprintEntity):
    """Some sensor class."""

    def __init__(
        self,
        coordinator: IntegrationBlueprintDataUpdateCoordinator,
    ) -> None:
        """Initialize sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_some_sensor"
        self._attr_name = "Some Sensor"
```

**Key points:**

- Inherit from both platform entity and `IntegrationBlueprintEntity`
- Set `_attr_unique_id` in `__init__`
- Use coordinator data, never direct API calls
- Handle unavailability via `_attr_available`

## Error Handling

**Use specific exceptions:**

```python
from ..exceptions import IntegrationBlueprintException, IntegrationBlueprintConnectionError

try:
    result = await self.coordinator.client.fetch_data()
except IntegrationBlueprintConnectionError as err:
    _LOGGER.error("Connection failed: %s", err)
    self._attr_available = False
```

**Log appropriately:**

- `_LOGGER.error()` - Errors that affect functionality
- `_LOGGER.warning()` - Recoverable issues
- `_LOGGER.debug()` - Detailed troubleshooting info

## Coordinator Pattern

**Always use the coordinator:**

```python
@property
def native_value(self) -> float | None:
    """Return sensor value."""
    return self.coordinator.data.temperature
```

**Never:**

```python
# DON'T DO THIS
async def async_update(self) -> None:
    """Fetch new state data."""
    self._value = await self.api_client.get_data()  # ❌ Wrong!
```

## Testing Considerations

**Note: Only write tests when explicitly requested by the developer.**

If you are asked to write tests for entities:

**Example test structure:**

```python
"""Test sensor platform."""

import pytest

from custom_components.ha_integration_domain.sensor import async_setup_entry

@pytest.mark.unit
async def test_sensor_setup(hass, config_entry, coordinator):
    """Test sensor platform setup."""
    # Test implementation
```

## Common Patterns

**Config entry data access:**

```python
entry_data: IntegrationBlueprintData = hass.data[DOMAIN][entry.entry_id]
coordinator = entry_data.coordinator
```

**Device info (in base entity):**

```python
@property
def device_info(self) -> DeviceInfo:
    """Return device information."""
    return DeviceInfo(
        identifiers={(DOMAIN, self.coordinator.config_entry.entry_id)},
        manufacturer="Manufacturer",
        model="Model",
        name="Device Name",
    )
```

## Validation

Before submitting code, ensure it passes:

```bash
script/type-check  # Pyright
script/lint        # Ruff (auto-fix enabled)
script/test        # pytest
```

**When validation fails:**

- Look up the specific error code in [Ruff rules](https://docs.astral.sh/ruff/rules/)
- Check [Pyright documentation](https://microsoft.github.io/pyright/) for type errors
- Search [Home Assistant docs](https://developers.home-assistant.io/) for pattern guidance
- Don't bypass checks - understand and fix the root cause

**Suppressing checks (use sparingly):**

When genuinely necessary (false positives, library issues):

```python
# Specific Ruff rule suppression
from plugin import register  # noqa: F401 - Side-effect import for plugin system

# Specific Pyright suppression
result = external_lib.method()  # type: ignore[attr-defined] - Library lacks type stubs

# Per-file suppression (top of file, rare cases only)
# ruff: noqa: E501 - URLs in docstrings exceed line length
```

**Never use blanket suppressions:**

- ❌ `# noqa` (no code)
- ❌ `# type: ignore` (no specific error)
- ❌ `# ruff: noqa` (entire file)

**Always:**

- Include specific error codes
- Add explanatory comments
- Prefer fixing over suppressing

## When Adding New Functionality

**Always verify current patterns:**

- Check [Home Assistant Developer Docs](https://developers.home-assistant.io/) for the latest API usage
- Review the [developer blog](https://developers.home-assistant.io/blog/) for recent deprecations or changes
- Search for similar implementations: `site:developers.home-assistant.io [feature type]`
- Home Assistant APIs evolve - don't rely solely on prior knowledge
