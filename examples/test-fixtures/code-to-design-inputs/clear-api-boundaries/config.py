"""Application configuration constants."""
import os

# Server settings
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8080"))

# Feature flags
FEATURE_FHIR_EXPORT = os.getenv("FEATURE_FHIR_EXPORT", "true").lower() == "true"
ENABLE_AUDIT_LOG = True

# Timeouts
TIMEOUT_EHR_SECONDS = 30
MAX_RETRY_ATTEMPTS = 3
