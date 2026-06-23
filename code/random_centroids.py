import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics import f1_score, cohen_kappa_score, matthews_corrcoef

MODEL_CONFIGS = [
    {
        "label": "Mixedbread large",
        "model_name": "mixedbread-ai/mxbai-embed-large-v1",
        "instruction": None,
        "task": None,
        "trust_remote_code": False,
    },
    {
        "label": "Nomic v1",
        "model_name": "nomic-ai/nomic-embed-text-v1",
        "instruction": None,
        "task": None,
        "trust_remote_code": True,
    },
    {
        "label": "Nomic v1",
        "model_name": "nomic-ai/nomic-embed-text-v1",
        "instruction": "classification: ",
        "task": None,
        "trust_remote_code": True,
    },
    {
        "label": "Jina small v2",
        "model_name": "jinaai/jina-embeddings-v2-small-en",
        "instruction": None,
        "task": None,
        "trust_remote_code": True,
    },
    {
        "label": "Jina base v2",
        "model_name": "jinaai/jina-embeddings-v2-base-en",
        "instruction": None,
        "task": None,
        "trust_remote_code": True,
    },
    {
        "label": "Jina v3",
        "model_name": "jinaai/jina-embeddings-v3",
        "instruction": None,
        "task": None,
        "trust_remote_code": True,
    },
    {
        "label": "Jina v3",
        "model_name": "jinaai/jina-embeddings-v3",
        "instruction": None,
        "task": "classification",
        "trust_remote_code": True,
    },
    {
        "label": "Jina v3",
        "model_name": "jinaai/jina-embeddings-v3",
        "instruction": None,
        "task": "text-matching",
        "trust_remote_code": True,
    },
    {
        "label": "Intfloat large instruct",
        "model_name": "intfloat/multilingual-e5-large-instruct",
        "instruction": None,
        "task": None,
        "trust_remote_code": False,
    },
    {
        "label": "Intfloat large instruct",
        "model_name": "intfloat/multilingual-e5-large-instruct",
        "instruction": "Instruct: Retrieve semantically similar text \nQuery: ",
        "task": None,
        "trust_remote_code": False,
    },
]

# Load the data
url = "https://zenodo.org/records/16912394/files/sources_v2.xlsx?download=1"

df_sources = pd.read_excel(url)
df_centroids = pd.read_excel('../data/centroids.xlsx')

# Update the code column
# Set updated_code to False if you want to use the original code
updated_code = True
if updated_code:
    df_sources.drop(columns=['code'], inplace=True)
    df_sources.rename(columns={'updated_code': 'code'}, inplace=True)

# Remove other (noise) labeled responses - for exhaustive coding
# Set exclude_other to False if you want to include the 'Other' responses
exclude_other = False

if exclude_other:
    df_sources = df_sources[df_sources["code"] != "O"]
    df_centroids = df_centroids[df_centroids["code"] != "O"]

centroid_size = len(df_centroids)

def create_centroids(df: pd.DataFrame,
                     code_col: str = "code",
                     emb_col: str = "embeddings",) -> tuple[np.ndarray, list]:
    """
    Compute one centroid per code by averaging row embeddings.

    Returns
    -------
    centroids : (C, D) array
        L2-normalized centroids stacked in the same order as `labels`.
    labels : list
        Sorted unique codes corresponding to rows in `centroids`.
    """
    if code_col not in df or emb_col not in df:
        raise KeyError(f"DataFrame must contain '{code_col}' and '{emb_col}' columns.")

    # Ensure deterministic order
    labels = sorted(df[code_col].unique().tolist())

    centroids: list[np.ndarray] = []
    for code in labels:
        # Stack all embeddings for this code
        embs = df.loc[df[code_col] == code, emb_col]
        # Support either arrays in .values or in Python lists
        stacked = np.vstack(embs)
        centroids.append(stacked.mean(axis=0))

    centroids_arr = np.asarray(centroids)

    return centroids_arr, labels

def predict_codes(embeddings: np.ndarray,
                  centroids: np.ndarray,
                  labels: list) -> list:
    """
    Assign each embedding the label of its most similar centroid (cosine).

    Parameters
    ----------
    embeddings : (N, D) array
    centroids  : (C, D) array (assumed L2-normalized row-wise)
    labels     : list of length C mapping centroid index -> code label
    """

    # Normalize so cosine similarity is dot product
    embeddings /= np.linalg.norm(embeddings, axis=1, keepdims=True)
    centroids /= np.linalg.norm(centroids, axis=1, keepdims=True)

    S = embeddings @ centroids.T  # (N, C) cosine similarities

    closest_arg = np.argmax(S, axis=1)
    return [labels[i] for i in closest_arg]

def compute_metrics(y_true: np.ndarray | list, y_pred: np.ndarray | list) -> dict[str, float]:
    """
    Compute agreement/quality metrics for categorical predictions.
    """
    return {
        "kappa": float(cohen_kappa_score(y_true, y_pred)),
        "f1_weighted": float(f1_score(y_true, y_pred, average="weighted")),
        "mcc": float(matthews_corrcoef(y_true, y_pred)),
    }

random_indecies = []
for i in range(100):
    random_indecies.append(np.random.choice(df_sources.index, size=centroid_size, replace=False))


results = []
for model_config in MODEL_CONFIGS:
    model = SentenceTransformer(
        model_config["model_name"],
        device="mps",
        trust_remote_code=model_config["trust_remote_code"],
    )

    encode_kwargs = {
        "normalize_embeddings": True,
        "show_progress_bar": True,
    }
    if model_config["instruction"]:
        encode_kwargs["prompt"] = model_config["instruction"]
    if model_config["task"]:
        encode_kwargs["task"] = model_config["task"]

    embeddings = model.encode(
        df_sources["response"].values.tolist(),
        **encode_kwargs,
    )

    df_sources["embeddings"] = list(embeddings)
 
    for i in range(100):
        random_centroids = df_sources.loc[random_indecies[i]]
        centroids, labels = create_centroids(random_centroids, code_col="code", emb_col="embeddings")
        pred = predict_codes(embeddings, centroids, labels)
        metrics = compute_metrics(df_sources["code"].tolist(), pred)
        results.append({
            "model + instruction/task": model_config["label"] + (f" + {model_config['instruction']}" if model_config["instruction"] else "") + (f" + {model_config['task']}" if model_config["task"] else ""),
            "sample": i + 1,
            "kappa": metrics["kappa"],
            "f1_weighted": metrics["f1_weighted"],
            "mcc": metrics["mcc"]
        })
df_results = pd.DataFrame(results)

rows = []
# i want unique models + prompt/task combinations, so i will group by model and then compute mean and std for each metric
for model_label, group in df_results.groupby("model + instruction/task"):
    mean_kappa = group["kappa"].mean()
    std_kappa = group["kappa"].std()
    mean_f1 = group["f1_weighted"].mean()
    std_f1 = group["f1_weighted"].std()
    mean_mcc = group["mcc"].mean()
    std_mcc = group["mcc"].std()
    rows.append({
        "model + instruction/task": model_label,
        "kappa": f"{mean_kappa:.4f} ± {std_kappa:.4f}",
        "f1_weighted": f"{mean_f1:.4f} ± {std_f1:.4f}",
        "mcc": f"{mean_mcc:.4f} ± {std_mcc:.4f}",
    })
df_summary = pd.DataFrame(rows)
print(df_summary)
df_centroids.to_csv('../data/results.csv', index=False)