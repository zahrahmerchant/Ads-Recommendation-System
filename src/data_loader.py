import json
import pandas as pd
from typing import List, Dict, Optional, Any, Union

class DataLoader:
    def __init__(self, file_path: str) -> None:
        """Initialize the DataLoader with the path to the JSON file."""
        self.file_path: str = file_path
        self.data: Optional[pd.DataFrame] = None

    def load_data(self) -> pd.DataFrame:
        """Load the advertisement data from JSON file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data: List[Dict] = json.load(file)
                
            # Validate data structure
            if not isinstance(data, list) or not all(isinstance(ad, dict) for ad in data):
                raise ValueError("JSON data must be a list of dictionaries")
                
            # Validate required fields in each advertisement
            required_fields = {'ad_id', 'image_url', 'link', 'tagline', 'text'}
            for ad in data:
                missing_fields = required_fields - set(ad.keys())
                if missing_fields:
                    raise ValueError(f"Advertisement missing required fields: {missing_fields}")
                
            self.data = pd.DataFrame(data)
            return self.data
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file not found at: {self.file_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in file: {self.file_path}")
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")

    def get_ad_by_id(self, ad_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Retrieve a specific advertisement by its ID.
        
        Args:
            ad_id: The ID of the advertisement (can be integer or string)
            
        Returns:
            Optional[Dict[str, Any]]: Advertisement data if found, None otherwise
        """
        if self.data is None:
            self.load_data()
        
        if self.data is None:
            raise ValueError("Failed to load advertisement data")
            
        if 'ad_id' not in self.data.columns:
            raise ValueError("'ad_id' column not found in the data")
        
        # Convert ad_id to int if it's a string and looks like a number
        if isinstance(ad_id, str) and ad_id.isdigit():
            ad_id = int(ad_id)
            
        ad: pd.DataFrame = self.data.loc[self.data['ad_id'] == ad_id]
        if ad.empty:
            return None
        return ad.iloc[0].to_dict()

    def get_all_ads(self) -> List[Dict[str, Any]]:
        """Return all advertisements as a list of dictionaries."""
        if self.data is None:
            self.load_data()
        if self.data is None:
            raise ValueError("Failed to load advertisement data")
        return self.data.to_dict('records')
