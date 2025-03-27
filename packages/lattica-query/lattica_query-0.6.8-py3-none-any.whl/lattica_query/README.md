# Lattica Query Client

A Python client library for securely executing AI inference with homomorphic encryption (HE) on Lattica's cloud platform.

## Overview

The `lattica_query` package provides a client-side interface for working with Lattica's homomorphic encryption system. It enables secure, private AI inference by allowing users to:

1. Generate encryption keys locally
2. Encrypt data with homomorphic encryption
3. Send encrypted data to Lattica's cloud service
4. Receive and decrypt computation results

With this library, sensitive data never leaves the client's environment in unencrypted form, ensuring privacy while leveraging cloud-based AI inference.

## Installation

```bash
pip install lattica-query
```

## Prerequisites

- Python 3.12
- PyTorch
- A valid Lattica query token

## Key Components

### QueryClient

The main client interface for interacting with Lattica's homomorphic encryption service.

```python
from lattica_query.lattica_query_client import QueryClient

# Initialize with your query token
client = QueryClient("your_query_token_here")
```

### Key Generation

Generate encryption keys for secure homomorphic operations:

```python
# Generate key pair and upload public key (returns context, secret_key, homomorphic_sequence)
context, secret_key, client_blocks = client.generate_key()

# Save secret key for future use
with open('my_secret_key.lsk', 'wb') as f:
    f.write(secret_key)
```

### Key Upload

The public key is automatically uploaded to Lattica's servers, when calling `generate_key()`.


### Encrypted Inference

Run queries on encrypted data:

```python
import torch

# Create plaintext tensor (your input data)
pt = torch.rand(10, dtype=torch.float64)

# Run query with homomorphic encryption
encrypted_result = client.run_query(context, secret_key, pt, client_blocks)

print(f"Encrypted result: {encrypted_result}")
```

## API Documentation

### QueryClient

- `__init__(query_token: str)` - Initialize the client with a Lattica query token
- `generate_key()` - Generate encryption keys for homomorphic operations and automatically upload the public key
- `run_query(context, secret_key, pt, client_blocks)` - Run homomorphically encrypted inference

### Worker API

Low-level API for direct communication with Lattica's worker service:

- `get_user_init_data()` - Retrieve context and client blocks
- `preprocess_pk()` - Preprocess the uploaded public key
- `apply_hom_pipeline(ct, block_index)` - Apply homomorphic operations
- `apply_clear(pt)` - Apply operations without encryption

## Security Considerations

- Store your secret key securely and never share it
- The public key can be safely uploaded to Lattica's servers
- All sensitive data is encrypted before leaving your environment

## License

Proprietary - © Lattica AI

---

For more information, visit [https://www.lattica.ai](https://www.lattica.ai)