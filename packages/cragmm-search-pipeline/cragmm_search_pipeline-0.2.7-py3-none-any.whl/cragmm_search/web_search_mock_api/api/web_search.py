from typing import Union
import chromadb
import numpy as np
import torch
import transformers

def index_web_data(
    hf_path: str = "crag-mm-2025/web-search-index-public",
):
    """
    Load index data from Huggingface.

    Args:
        hf_path: Huggingface datasets containing search index

    Returns:
        chromadb.Collection: A ChromaDB collection containing the indexed data
    """
    try:
        from huggingface_hub import snapshot_download

        print("Loading web search data from Hugging Face...")
        dataset_local_path = snapshot_download(repo_id=hf_path, repo_type="dataset")

        client = chromadb.PersistentClient(path=dataset_local_path)
        collection = client.get_collection(name="web_search_embeddings")

        print(f"Successfully loaded collection with {collection.count()} entries")
        return collection

    except Exception as e:
        raise

        
def extract_features(
    model: torch.nn.Module,
    tokenizer: transformers.PreTrainedTokenizer,
    text: str,
    device: Union[torch.device, None] = None,
) -> np.ndarray:
    """
    Extract features from text using the model and tokenizer.

    Args:
        model: The embedding model
        tokenizer: The tokenizer
        text: The input text
        device: The device to run the model on

    Returns:
        numpy.ndarray: The extracted features
    """
    if device is None:
        device = model.device

    # Tokenize and prepare inputs
    inputs = tokenizer(
        text, return_tensors="pt", padding=True, truncation=True, max_length=512
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Extract features
    with torch.no_grad():
        outputs = model(**inputs)
        # Use mean pooling
        attention_mask = inputs["attention_mask"]
        features = mean_pooling(outputs.last_hidden_state, attention_mask)

    # Normalize features
    features = features / features.norm(dim=-1, keepdim=True)
    return features.cpu().numpy()


def mean_pooling(
    token_embeddings: torch.Tensor, attention_mask: torch.Tensor
) -> torch.Tensor:
    """
    Perform mean pooling on token embeddings using attention mask.

    Args:
        token_embeddings: Token embeddings from model
        attention_mask: Attention mask from tokenizer

    Returns:
        torch.Tensor: Mean pooled embeddings
    """
    input_mask_expanded = (
        attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    )
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
        input_mask_expanded.sum(1), min=1e-9
    )


def web_search(
    query_emb, collection: chromadb.Collection, top_n: int = 5
) -> list[tuple[int, float]]:
    """
    Search for similar web pages using query embedding.

    Args:
        query_emb: Query embedding
        collection: ChromaDB collection
        top_n: Number of results to return

    Returns:
        list[tuple[int, float]]: List of (index, score) tuples
    """
    # Ensure query_emb is in the right format
    if query_emb.ndim == 1:
        query_emb = query_emb.reshape(1, -1)

    # Normalize the embedding (ChromaDB doesn't do this automatically)
    norm = np.linalg.norm(query_emb)
    if norm > 0:
        query_emb = query_emb / norm

    # Query the collection
    results = collection.query(query_embeddings=query_emb.tolist(), n_results=top_n)

    assert results is not None, "No results found"

    # Extract and return indices and distances
    indices = [int(id) for id in results["ids"][0]]
    distances = (
        results["distances"][0]
        if "distances" in results and results["distances"]
        else [1.0] * len(indices)
    )

    # Convert distances to similarity scores (1 - distance)
    scores = [1.0 - d for d in distances]

    return list(zip(indices, scores))
