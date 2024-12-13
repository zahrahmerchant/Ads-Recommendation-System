from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
import torch

class EmbeddingGenerator:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """Initialize the embedding generator with a specific model."""
        self.model = SentenceTransformer(model_name)

    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for a single text."""
        embedding = self.model.encode(text)
        if isinstance(embedding, torch.Tensor):
            embedding = embedding.cpu().numpy()
        return np.asarray(embedding)

    def generate_batch_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a batch of texts."""
        embeddings = self.model.encode(texts)
        if isinstance(embeddings, torch.Tensor):
            embeddings = embeddings.cpu().numpy()
        return np.asarray(embeddings)

    def prepare_ad_embeddings(self, ads: List[Dict]) -> List[Dict]:
        """Prepare embeddings for advertisements combining tagline and text."""
        processed_ads = []
        for ad in ads:
            try:
                combined_text = f"{ad['tagline']} {ad['text']}"
                embedding = self.generate_embedding(combined_text)
                ad['embedding'] = embedding
                processed_ads.append(ad)
            except KeyError as e:
                raise KeyError(f"Missing required field in ad: {e}. Each ad must contain 'tagline' and 'text' fields.")
        return processed_ads
