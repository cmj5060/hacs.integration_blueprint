---
applyTo: "tests/**/*.py"
---

# Test Instructions

**Applies to:** `tests/` directory

## Test Structure

**Mirror integration structure:**

```text
tests/
  __init__.py
  conftest.py          # Shared fixtures
  test_init.py         # Integration setup tests
  test_config_flow.py  # Config flow tests
  sensor/
    test_init.py       # Sensor platform tests
    test_air_quality.py
  binary_sensor/
    test_connectivity.py
```

## File Organization

**Each test file:**

- Tests one module or feature
- Named `test_*.py`
- Contains related test functions
- Uses fixtures from `conftest.py`

## Markers

**Use pytest markers to categorize tests:**

```python
import pytest

@pytest.mark.unit
async def test_sensor_value(coordinator):
    """Test sensor returns correct value."""
    # Fast, isolated test

@pytest.mark.integration
async def test_coordinator_update(hass, coordinator):
    """Test coordinator data update."""
    # Test with Home Assistant and coordinator
```

**Available markers:**

- `@pytest.mark.unit` - Fast, isolated tests (no external dependencies)
- `@pytest.mark.integration` - Tests using coordinator, time service, etc.

## Common Fixtures

**From `conftest.py`:**

```python
async def test_example(hass, config_entry, coordinator):
    """Test using common fixtures.

    Args:
        hass: Home Assistant instance
        config_entry: Mock config entry
        coordinator: Data update coordinator
    """
    # Test implementation
```

**Standard fixtures:**

- `hass` - Mock Home Assistant instance
- `config_entry` - Mock ConfigEntry
- `coordinator` - IntegrationBlueprintDataUpdateCoordinator
- `mock_api_client` - Mocked API client

## Mocking

**Mock external API calls:**

```python
from unittest.mock import AsyncMock, patch

async def test_api_call(coordinator):
    """Test API call handling."""
    with patch.object(
        coordinator.client,
        "fetch_data",
        return_value={"temperature": 21.5},
    ):
        await coordinator.async_refresh()
        assert coordinator.data.temperature == 21.5
```

**Mock exceptions:**

```python
from custom_components.ha_integration_domain.exceptions import (
    IntegrationBlueprintConnectionError,
)

async def test_connection_error(coordinator):
    """Test handling of connection errors."""
    with patch.object(
        coordinator.client,
        "fetch_data",
        side_effect=IntegrationBlueprintConnectionError("Connection failed"),
    ):
        await coordinator.async_refresh()
        assert coordinator.last_update_success is False
```

## Entity Testing

**Test entity setup:**

```python
from custom_components.ha_integration_domain.sensor import async_setup_entry

@pytest.mark.unit
async def test_sensor_setup(hass, config_entry, coordinator):
    """Test sensor platform setup."""
    with patch(
        "custom_components.ha_integration_domain.sensor.IntegrationBlueprintDataUpdateCoordinator",
        return_value=coordinator,
    ):
        assert await async_setup_entry(hass, config_entry, AsyncMock())
```

**Test entity properties:**

```python
from custom_components.ha_integration_domain.sensor.air_quality import (
    IntegrationBlueprintAirQualitySensor,
)

@pytest.mark.unit
def test_sensor_properties(coordinator):
    """Test sensor properties."""
    sensor = IntegrationBlueprintAirQualitySensor(coordinator)

    assert sensor.unique_id is not None
    assert sensor.name is not None
    assert sensor.device_class is not None
```

**Test state updates:**

```python
@pytest.mark.integration
async def test_sensor_state_update(hass, coordinator):
    """Test sensor state updates with coordinator."""
    sensor = IntegrationBlueprintAirQualitySensor(coordinator)
    sensor.hass = hass

    # Initial state
    assert sensor.native_value is None

    # Update coordinator data
    coordinator.data.air_quality = 42
    await coordinator.async_refresh()

    # Check updated state
    assert sensor.native_value == 42
```

## Config Flow Testing

**Test user flow:**

```python
from custom_components.ha_integration_domain.config_flow_handler import (
    IntegrationBlueprintConfigFlowHandler,
)

async def test_user_flow(hass):
    """Test user config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": "user"},
    )

    assert result["type"] == "form"
    assert result["step_id"] == "user"
```

**Test validation:**

```python
async def test_invalid_input(hass):
    """Test handling of invalid user input."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": "user"},
        data={"host": ""},  # Invalid empty host
    )

    assert result["type"] == "form"
    assert "base" in result["errors"]
```

## Assertions

**Use descriptive assertions:**

```python
# ✅ Good
assert sensor.native_value == 21.5, "Temperature should be 21.5°C"
assert sensor.available is True, "Sensor should be available"

# ❌ Less helpful
assert sensor.native_value == 21.5
assert sensor.available
```

**Check multiple conditions:**

```python
def test_sensor_state(sensor):
    """Test sensor provides complete state."""
    assert sensor.native_value is not None
    assert sensor.native_unit_of_measurement == "°C"
    assert sensor.device_class == SensorDeviceClass.TEMPERATURE
    assert sensor.state_class == SensorStateClass.MEASUREMENT
```

## Running Tests

```bash
script/test                    # Run all tests
script/test -v                 # Verbose output
script/test --cov-html         # With coverage report
script/test tests/sensor/      # Specific directory
script/test -k test_sensor     # Tests matching pattern
script/test -m unit            # Only unit tests
```

## Best Practices

**Do:**

- Test both success and error cases
- Mock external dependencies (API calls, time)
- Use descriptive test names
- Keep tests focused (one thing per test)
- Use fixtures for common setup
- **Consult [pytest docs](https://docs.pytest.org/)** when exploring advanced patterns
- **Check [Home Assistant testing docs](https://developers.home-assistant.io/docs/development_testing)** for HA-specific patterns

**Don't:**

- Make actual network requests
- Use `time.sleep()` (use `async_fire_time_changed` instead)
- Test Home Assistant internals (trust the framework)
- Create overly complex test scenarios
- Skip testing error conditions
- Assume testing patterns without verifying current best practices

## Research When Needed

**When writing tests for new features:**

- Search [Home Assistant Core tests](https://github.com/home-assistant/core/tree/dev/tests/components) for similar integration examples
- Check [pytest documentation](https://docs.pytest.org/) for fixture and marker usage
- Review [Home Assistant testing guidelines](https://developers.home-assistant.io/docs/development_testing)
- Use `site:developers.home-assistant.io testing` to find official guidance

## Coverage

Aim for high test coverage, especially for:

- Core coordinator logic
- Config flow validation
- Error handling paths
- Entity state calculations

Check coverage with:

```bash
script/test --cov-html
# Open htmlcov/index.html in browser
```
