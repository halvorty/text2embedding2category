# COST

# Classifying open-ended survey responses with text embeddings

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Description

This repository is published in relation to the paper *Classifying open-ended survey responses with text embeddings* by 
Jonas Timmann Mjaaland, Halvor Tyseng, Markus Fleten Kreutzer, Rebeckah K. Fussell, Gina Passante, N.G. Holmes, Anders Malthe-Sørenssen, and Tor Ole B. Odden. 

---

There are three notebooks that present our main findings <br>
### [data_audit.ipynb](data_audit.ipynb)
This notebook introduces the concept of detecting inconsistencies and edge cases. A text embedding model is used to embed all the text in the data. Then we identify text with high similarity that has been coded differently. We qualitatively set a cutoff and present pairs of inconsistently coded text to a qualitative researcher with domain knowledge of the classification task. 

### [defsscute.ipynb](defsscute.ipynb)
In defsscute.ipynb we present our five-step method to perform *Deductive Few-Shot Survey Classification Using Text Embedding* — DeFSSCUTE. This notebook can be used to reproduce the results presented in the article by varying model, prompt, task, and dataset. 

### [finetune.ipynb](finetune.ipynb)  
DeFSSCUTE performs well out of the box for selective coding, for our example dataset. When including noisy responses (an "Other" category), performance drops. We find that fine-tuning the embedding models following the guide of [sentence-transformers](https://sbert.net/docs/sentence_transformer/training_overview.html) on only a few responses improves performance. The notebook presents the steps needed to fine-tune a model, and the fine-tuned model is then saved into the folder [finetuned_models](finetuned_models/). Thereafter, the model can be substituted into the defsscute notebook to check the results. 

### Table of contents
- [Installation](#installation)
- [Embedding models](#Embedding_models)
- [Contributing](#contributing)
- [Data](#Data)
- [License](#license)
- [Contact](#contact)

## Installation

**Python version recommended:** Python 3.9+

```bash
git clone https://github.com/halvorty/COST.git
pip install -r requirements.txt
```


## Embedding models

The embedding models we have used are: 

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

We followed what the embedding model providers listed as how to use the models with prompts and tasks. "Task" refers to the usage of a LoRA adapter, which is an option for Jina v3.


## Contributing

## Data

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

Any and all questions can be sent to either: 

halvorty@uio.no
markusfk@uio.no
jonastm@uio.no









