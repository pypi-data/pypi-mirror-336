from typing import Dict, Optional

from rest_framework.request import Request

from nexus_auth.exceptions import NoActiveProviderError
from nexus_auth.providers.base import OAuth2IdentityProvider
from nexus_auth.providers.factory import providers
from nexus_auth.settings import nexus_settings


def get_oauth_provider(
    request: Request, provider_type: str
) -> Optional[OAuth2IdentityProvider]:
    """Get the OAuth provider object by provider type.

    Args:
        provider_type: Type of provider to get

    Returns:
        Optional[OAuth2IdentityProvider]: The active provider if found, None if no provider exists.

    Raises:
        NoActiveProviderError: If no active provider is found.
    """
    config = nexus_settings.get_provider_config(request=request)
    provider = config.get(provider_type)
    if not provider:
        raise NoActiveProviderError()

    config_kwargs = {k.lower(): v for k, v in provider.items()}

    return providers.get(
        provider_type,
        **config_kwargs,
    )


def load_provider_config(request: Request) -> Dict[str, Dict[str, str]]:
    """Load provider configuration.

    Args:
        request: HTTP request

    Returns:
        Dict[str, Dict[str, str]]: Provider configuration
    """
    return nexus_settings.providers_config()
