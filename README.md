# COST

# Classifying open-ended survey responses with text embeddings

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)


## Description


------------


### Table of contents
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation

```bash
git clone https://github.com/halvorty/COST.git
pip install -r requirements.txt
```


## Usage

The embedding models we have used

<table>
  <thead>
    <tr>
      <th>Model</th>
      <th>HF Model Name</th>
      <th>No. of Parameters</th>
      <th>No. of Dimensions</th>
      <th>Max Tokens</th>
      <th>Prompt / LoRA Rank Adapter</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1"><b>Mixedbread large</b></a></td>
      <td><code>mixedbread-ai/mxbai-embed-large-v1</code></td>
      <td align="right">335M</td>
      <td align="right">1024</td>
      <td align="right">512</td>
      <td>None</td>
    </tr>
    <tr>
      <td><a href="https://huggingface.co/nomic-ai/nomic-embed-text-v1"><b>Nomic v1</b></a></td>
      <td><code>nomic-ai/nomic-embed-text-v1</code></td>
      <td align="right">137M</td>
      <td align="right">768</td>
      <td align="right">8192</td>
      <td>None / Classification</td>
    </tr>
    <tr>
      <td><a href="https://huggingface.co/jinaai/jina-embeddings-v2-small-en"><b>Jina small v2</b></a></td>
      <td><code>jinaai/jina-embeddings-v2-small-en</code></td>
      <td align="right">32.7M</td>
      <td align="right">512</td>
      <td align="right">8192</td>
      <td>None</td>
    </tr>
    <tr>
      <td><a href="https://huggingface.co/jinaai/jina-embeddings-v2-base-en"><b>Jina base v2</b></a></td>
      <td><code>jinaai/jina-embeddings-v2-base-en</code></td>
      <td align="right">137M</td>
      <td align="right">768</td>
      <td align="right">8192</td>
      <td>None</td>
    </tr>
    <tr>
      <td><a href="https://huggingface.co/jinaai/jina-embeddings-v3"><b>Jina v3</b></a></td>
      <td><code>jinaai/jina-embeddings-v3</code></td>
      <td align="right">572M</td>
      <td align="right">1024</td>
      <td align="right">8192</td>
      <td>None / Classification / STS</td>
    </tr>
    <tr>
      <td><a href="https://huggingface.co/intfloat/multilingual-e5-large-instruct"><b>Infloat large instruct</b></a></td>
      <td><code>intfloat/multilingual-e5-large-instruct</code></td>
      <td align="right">560M</td>
      <td align="right">1024</td>
      <td align="right">512</td>
      <td>None / STS</td>
    </tr>
  </tbody>
</table>

We followed what the embedding model providers listed as how to use the models with prompts, and task. Task refers to the usage of a LORA adapter which is a option for Jina v3. 



## License

This project is licensed under the [MIT License](LICENSE).

## Contact

Any and all questions can be sent to either: 

halvorty@uio.no
markusfk@uio.no
jonastm@uio.no






