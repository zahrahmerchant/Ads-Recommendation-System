# Ads Recommendation System

This project implements an AI-powered advertisement recommendation system that suggests relevant ads based on user preferences. The system uses advanced embedding techniques and similarity search to provide personalized ad recommendations.

## Features

- Load and process advertisement data
- Generate embeddings for ad content
- Similarity-based recommendation engine
- Interactive Streamlit web interface
- Qdrant vector database integration

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ads-recommendation-system.git
cd ads-recommendation-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run main.py
```

## Project Structure

```
ads-recommendation-system/
│
├── data/                      # Dataset directory
├── src/                      # Source code
├── requirements.txt          # Project dependencies
├── README.md                 # Project documentation
├── .gitignore               # Git ignore rules
└── main.py                  # Main Streamlit application
```

## Usage

1. The system loads advertisement data from the provided JSON dataset
2. Users can input their preferences or interests
3. The system returns relevant ad recommendations based on the input

## License

MIT License
