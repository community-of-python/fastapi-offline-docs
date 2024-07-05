# fastapi-offline-docs

This package enables "offline mode" for FastAPI (in other words lets you avoid loading assets from CDN).

# Installation

```sh
poetry add fastapi-offline-docs
```

# Usage

Before:

```python
import fastapi

app = fastapi.FastAPI(docs_url="path/to/doc", redoc_url="path/to/redoc")
```

After:

```python
import fastapi
from fastapi_offline_docs import enable_offline_docs

app = fastapi.FastAPI(docs_url="path/to/doc", redoc_url="path/to/redoc")
enable_offline_docs(app)
```

Now, the assets for API docs are served locally, not from CDN.

See also: [litestar-offline-docs](https://github.com/community-of-python/litestar-offline-docs).
