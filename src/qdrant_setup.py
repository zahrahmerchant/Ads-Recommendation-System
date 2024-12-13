from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import numpy as np
from typing import List, Dict, Union

class QdrantManager:
    def __init__(self, collection_name: str = "ads_collection"):
        """Initialize Qdrant client and setup collection."""
        self.client = QdrantClient(":memory:")  # Using in-memory storage for demonstration
        self.collection_name = collection_name
        self.vector_size = 384  # Size for 'all-MiniLM-L6-v2' embeddings

    def create_collection(self):
        """Create a new collection for storing ad embeddings."""
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE)
        )

    def upload_ads(self, ads: List[Dict]):
        """Upload ads with their embeddings to Qdrant."""
        points = []
        for i, ad in enumerate(ads):
            points.append(PointStruct(
                id=i,
                vector=ad['embedding'].tolist(),
                payload={
                    'ad_id': ad['ad_id'],
                    'tagline': ad['tagline'],
                    'text': ad['text'],
                    'image_url': ad['image_url'],
                    'link': ad['link']
                }
            ))
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def search_similar_ads(self, query_vector: np.ndarray, limit: int = 5) -> List[Dict | None]:
        """Search for similar ads based on a query vector."""
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector.tolist(),
            limit=limit
        )
        return [hit.payload for hit in search_result]
