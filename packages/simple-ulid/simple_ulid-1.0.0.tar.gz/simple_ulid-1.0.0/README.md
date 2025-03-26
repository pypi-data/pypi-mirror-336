# ULID

This library provides a single function to generate a `ULID` (_Universally Unique Lexicographically Sortable Identifier_).

## Installation
`pip install simple-ulid`

## Usage

### Generating a ULID

```python
import ulid


print(ulid.new())
```

### Using ULID in a Django Model as Primary Key

```python
import ulid
from django.db import models

class BaseForm(models.Model):
    id = models.CharField(primary_key=True, default=ulid.new, editable=False, max_length=26)
```
