# Transformers_IPFS

Load models directly from IPFS for Hugging Face Transformers.

## Features

- 🌐 Direct integration with local IPFS nodes (preferred method)
- 🔄 Automatic fallback to IPFS gateways when local node isn't available
- 🔍 Simple URI format: `ipfs://CID` for easy model sharing
- ⚡ Zero configuration required - works automatically once installed
- 🧩 Compatible with any version of Transformers

## Installation

```bash
pip install transformers-ipfs
transformers-ipfs activate
```

Once installed and activated, the `transformers_ipfs` integration will be loaded automatically whenever you use Python.

## Usage

- [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/alexbakers/transformers_ipfs/blob/main/examples/colab/transformers_ipfs_example.ipynb)
- 🤗 [Demo Space](https://huggingface.co/spaces/alexbakers/transformers_ipfs)

Use the Transformers library with IPFS model URIs:

```python
from transformers import AutoModel, AutoTokenizer

# Load a model directly from IPFS
tokenizer = AutoTokenizer.from_pretrained("ipfs://bafybeichqdarufyutqc7yd43k77fkxbmeuhhetbihd3g32ghcqvijp6fxi")
# Equivalent HuggingFace model: "riturajpandey739/gpt2-sentiment-analysis-tweets"
model = AutoModel.from_pretrained("ipfs://bafybeichqdarufyutqc7yd43k77fkxbmeuhhetbihd3g32ghcqvijp6fxi")
```

## IPFS Node Connectivity

The `transformers_ipfs` package prioritizes connectivity in the following order:

1. **Local IPFS Node** (Recommended): If you have an IPFS daemon running locally (`ipfs daemon`),
   the package will automatically detect and use it. This method:

   - Is much faster for repeated downloads
   - More reliably loads complex model directories with multiple files
   - Contributes to the IPFS network by providing content to others

2. **IPFS Gateway** (Fallback): If a local node isn't available, the package will fall back to
   public gateways. This method:
   - Works without installing IPFS
   - May be less reliable for complex model directories
   - Downloads can be interrupted more easily

## Command Line Interface

```bash
# Activate the auto-loading
transformers-ipfs activate

# Check if the integration is active
transformers-ipfs status

# Test the integration
transformers-ipfs test

# Deactivate the integration
transformers-ipfs deactivate
```

## Dependencies

- Python 3.7+
- transformers

## License

MIT
