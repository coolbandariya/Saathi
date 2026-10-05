from app.provider_adapters import SafeProviderFactory

def test_provider_factory_does_not_create_provider_without_secret():
    assert SafeProviderFactory.gemini(None,"gemini-3.8-flash") is None
