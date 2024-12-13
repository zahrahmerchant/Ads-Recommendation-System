from typing import List, Dict
from .embeddings import EmbeddingGenerator
from .qdrant_setup import QdrantManager
from .data_loader import DataLoader

class RecommendationEngine:
    def __init__(self, data_path: str):
        """Initialize the recommendation engine components."""
        self.data_loader = DataLoader(data_path)
        self.embedding_generator = EmbeddingGenerator()
        self.qdrant_manager = QdrantManager()
        self.initialized = False

    def initialize(self):
        """Initialize the recommendation system with data."""
        if not self.initialized:
            # Load and process data
            ads = self.data_loader.get_all_ads()
            processed_ads = self.embedding_generator.prepare_ad_embeddings(ads)
            
            # Setup Qdrant
            self.qdrant_manager.create_collection()
            self.qdrant_manager.upload_ads(processed_ads)
            
            self.initialized = True

    def get_recommendations(self, user_query: str, num_recommendations: int = 5) -> List[Dict]:
        """Get ad recommendations based on user query."""
        if not self.initialized:
            self.initialize()

        # Generate embedding for user query
        query_embedding = self.embedding_generator.generate_embedding(user_query)
        
        # Get similar ads
        recommendations = self.qdrant_manager.search_similar_ads(
            query_embedding,
            limit=num_recommendations
        )
        
        return recommendations

    def get_recommendations_by_category(self, category: str, num_recommendations: int = 5) -> List[Dict]:
        """Get recommendations filtered by category."""
        if not self.initialized:
            self.initialize()

        # Use the category as the query
        recommendations = self.get_recommendations(category, num_recommendations)
        
        # Filter by matching category
        return [rec for rec in recommendations if rec['category'].lower() == category.lower()]
