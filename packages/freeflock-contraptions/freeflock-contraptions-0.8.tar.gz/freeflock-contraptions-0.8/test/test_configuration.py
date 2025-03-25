import pytest


@pytest.mark.asyncio
async def test_collect_environment_variable(monkeypatch):
    monkeypatch.delenv("AZURE_KEY_VAULT_NAME", raising=False)
    monkeypatch.setenv("FREEFLOCK", "FREEFLOCK")
    from packages.freeflock_contraptions.configuration import collect
    result = collect("FREEFLOCK")
    assert result == "FREEFLOCK"


@pytest.mark.asyncio
async def test_collect_azure_keyvault(monkeypatch):
    # set env var AZURE_KEY_VAULT_NAME to an existing key vault with a secret named "FREEFLOCK" to run this test
    from packages.freeflock_contraptions.configuration import collect
    result = collect("FREEFLOCK")
    assert result == "FREEFLOCK"

@pytest.mark.asyncio
async def test_collect_azure_keyvault_caching(monkeypatch):
    # set env var AZURE_KEY_VAULT_NAME to an existing key vault with a secret named "FREEFLOCK" to run this test
    from packages.freeflock_contraptions.configuration import collect
    result = collect("FREEFLOCK")
    assert result == "FREEFLOCK"
    result = collect("FREEFLOCK")
    assert result == "FREEFLOCK"
