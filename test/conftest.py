import os
import sys
import types

# Set required environment variables for module imports
os.environ.setdefault("CWA_AUTH_TOKEN", "test-token")
os.environ.setdefault("GCS_BUCKET", "test-bucket")
os.environ.setdefault("GCP_PROJECT_ID", "test-project")

# Provide a minimal stub for google.cloud.storage used in backgroud_task
if 'google.cloud.storage' not in sys.modules:
    google = types.ModuleType("google")
    cloud = types.ModuleType("cloud")
    storage = types.ModuleType("storage")

    class DummyBlob:
        def upload_from_string(self, data):
            pass

    class DummyBucket:
        def blob(self, name):
            return DummyBlob()

    class DummyClient:
        def __init__(self, *args, **kwargs):
            pass

        def bucket(self, name):
            return DummyBucket()

    storage.Client = DummyClient
    cloud.storage = storage
    google.cloud = cloud

    sys.modules['google'] = google
    sys.modules['google.cloud'] = cloud
    sys.modules['google.cloud.storage'] = storage
