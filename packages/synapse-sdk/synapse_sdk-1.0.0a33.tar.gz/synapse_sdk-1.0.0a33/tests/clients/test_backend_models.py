import pytest
from pydantic import ValidationError

from synapse_sdk.clients.backend.models import Storage, StorageCategory, StorageProvider


def test_storage_model_validation_success():
    storage_response = {
        'id': 1,
        'name': 'test_storage',
        'category': 'internal',
        'provider': 'file_system',
        'configuration': {},
        'is_default': True,
    }
    storage = Storage(**storage_response)
    assert storage.id == 1


def test_storage_model_validation_failed_with_invalid_category():
    storage_response = {
        'id': 1,
        'name': 'test_storage',
        'category': 'invalid_data',
        'provider': 'file_system',
        'configuration': {},
        'is_default': True,
    }
    with pytest.raises(ValidationError) as exc_info:
        Storage(**storage_response)
    assert 'category' in str(exc_info.value)


def test_storage_model_validation_failed_with_invalid_provider():
    storage_response = {
        'id': 1,
        'name': 'test_storage',
        'category': 'internal',
        'provider': 'invalid_provider',
        'configuration': {},
        'is_default': True,
    }
    with pytest.raises(ValidationError) as exc_info:
        Storage(**storage_response)
    assert 'provider' in str(exc_info.value)


def test_storage_model_validation_failed_with_missing_field():
    storage_response = {
        'id': 1,
        'name': 'test_storage',
        'category': 'internal',
        'provider': 'file_system',
        'is_default': True,
        # Missing configuration field
    }
    with pytest.raises(ValidationError):
        Storage(**storage_response)


def test_storage_model_enum_values():
    # Test that valid enum values work correctly
    for category in StorageCategory:
        for provider in StorageProvider:
            storage = Storage(
                id=1,
                name='test_storage',
                category=category,
                provider=provider,
                configuration={},
                is_default=True,
            )
            assert storage.category == category
            assert storage.provider == provider
