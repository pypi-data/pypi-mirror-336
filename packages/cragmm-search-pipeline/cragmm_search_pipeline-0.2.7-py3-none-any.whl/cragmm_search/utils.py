from typing import Any

import chromadb
import numpy as np


def add_embeddings_to_collection(
    collection, all_embeddings, max_batch_size=5000
) -> chromadb.Collection:
    # Note - Adjust max_batch_size to avoid OOM errors
    # Add embeddings to collection
    for i in range(0, len(all_embeddings), max_batch_size):
        batch_embeddings = all_embeddings[i : i + max_batch_size]
        batch_ids = [str(j) for j in range(i, i + len(batch_embeddings))]
        collection.add(embeddings=batch_embeddings.tolist(), ids=batch_ids)

    return collection


def maybe_list(x: Any) -> list[Any]:
    if isinstance(x, list):
        return x
    else:
        return [x]
