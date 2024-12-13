import streamlit as st
from src.recommendation_engine import RecommendationEngine
import os

def main():
    st.set_page_config(
        page_title="Ad Recommendation System",
        page_icon="🎯",
        layout="wide"
    )

    st.title("🎯 Smart Ad Recommendation System")
    st.write("Get personalized ad recommendations based on your interests!")

    # Initialize recommendation engine
    data_path = os.path.join("data", "realistic_ads_dataset.json")
    try:
        engine = RecommendationEngine(data_path)
        # Initialize the engine right away to catch any startup errors
        engine.initialize()
    except Exception as e:
        st.error(f"Failed to initialize recommendation engine: {str(e)}")
        st.stop()
        return

    # User input section
    st.subheader("What are you interested in?")
    user_query = st.text_input(
        "Describe your interests or preferences",
        placeholder="e.g., gaming laptops, outdoor sports equipment, healthy cooking..."
    )

    col1, col2 = st.columns(2)
    with col1:
        num_recommendations = st.slider(
            "Number of recommendations",
            min_value=1,
            max_value=10,
            value=5
        )

    # Get recommendations button
    if st.button("Get Recommendations", type="primary"):
        if user_query:
            with st.spinner("Finding the best ads for you..."):
                try:
                    recommendations = engine.get_recommendations(
                        user_query,
                        num_recommendations=num_recommendations
                    )
                    
                    if not recommendations:
                        st.warning("No recommendations found for your query. Try different keywords!")
                        st.stop()
                        
                    # Display recommendations
                    st.subheader("📢 Recommended Ads")
                    for i, ad in enumerate(recommendations, 1):
                        with st.container():
                            st.markdown(f"### {i}. {ad['tagline']}")
                            st.markdown(f"**Ad Details:**")
                            st.markdown(ad['text'])
                            if ad['image_url']:
                                st.image(ad['image_url'], caption="Ad Image")
                            st.markdown(f"[Click here to learn more]({ad['link']})")
                            st.divider()
                except Exception as e:
                    st.error(f"Error getting recommendations: {str(e)}")
        else:
            st.warning("Please enter your interests to get recommendations.")

    # Sidebar with additional information
    with st.sidebar:
        st.header("About")
        st.write("""
        This recommendation system uses advanced AI to match your interests
        with relevant advertisements. It analyzes the semantic meaning of your
        query to find the most relevant ads from our database.
        """)
        
        st.header("Tips")
        st.write("""
        - Be specific about your interests
        - Try different variations of your query
        - Adjust the number of recommendations
        """)

if __name__ == "__main__":
    main()
