import requests
import time
import pandas as pd
from typing import List, Dict, Optional, Union
from datetime import datetime

class ClinicalTrialsAPI:
    """Class to interact with ClinicalTrials.gov API v2"""
    
    def __init__(self):
        self.base_url = 'https://clinicaltrials.gov/api/v2/studies'
        
    def query_studies(
        self,
        search_expr: str,
        fields: Optional[List[str]] = None,
        max_studies: int = 100,
        format: str = 'json',
        page_token: Optional[str] = None
    ) -> Dict:
        """
        Query ClinicalTrials.gov API for studies matching criteria
        
        Args:
            search_expr (str): Search expression (e.g. 'cancer AND phase=1')
            fields (List[str], optional): Specific fields to return
            max_studies (int): Maximum number of studies to return
            format (str): Response format ('json' or 'csv')
            page_token (str, optional): Token for pagination
            
        Returns:
            Dict: JSON response containing study data
        """
        if fields is None:
            fields = [
                'NCTId',
                'BriefTitle', 
                'Condition',
                'Phase',
                'StartDate',
                'CompletionDate',
                'EnrollmentCount',
                'OverallStatus'
            ]

        params = {
            'format': format,
            'query.term': search_expr,
            'pageSize': max_studies,
            'fields': ','.join(fields)
        }

        # Add page token if provided
        if page_token:
            params['pageToken'] = page_token

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response content: {e.response.text[:500]}")
            raise

    def get_study_details(self, nct_id: str) -> Dict:
        """
        Get detailed information for a specific study
        
        Args:
            nct_id (str): NCT ID of the study
            
        Returns:
            Dict: Detailed study information
        """
        url = f"{self.base_url}/{nct_id}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving study {nct_id}: {e}")
            raise

    def search_to_dataframe(
        self,
        search_expr: str,
        max_studies: int = 100
    ) -> pd.DataFrame:
        """
        Search studies and return results as a pandas DataFrame
        
        Args:
            search_expr (str): Search expression
            max_studies (int): Maximum number of studies to return
            
        Returns:
            pd.DataFrame: Study results as a DataFrame
        """
        results = self.query_studies(search_expr, max_studies=max_studies)
        if 'studies' in results:
            return pd.DataFrame(results['studies'])
        else:
            print("No studies found or unexpected response format")
            return pd.DataFrame()
    def extract_nctid(self,study):
        if isinstance(study, dict):
            return study.get("identificationModule", {}).get("nctId", "")
        return ""
    
    def search_to_dataframe_IDs(
        self,
        search_expr: str,
        max_studies: int = 100
    ) -> pd.DataFrame:
        """
        Search studies and return a pandas DataFrame containing only the nctId for each study.
        
        Args:
            search_expr (str): Search expression.
            max_studies (int): Maximum number of studies to return.
            
        Returns:
            pd.DataFrame: A DataFrame with a single column 'nctId' listing the study identifiers.
        """
        df_results = self.search_to_dataframe(search_expr, max_studies)
        df_results["NCTId"] = df_results["protocolSection"].apply(lambda x: self.extract_nctid(x))
        return (df_results)


    # Define a helper function to extract the brief summary from a trial record
    def extract_brief_summary(self, NCTId: str) -> str:
        """
        Given the protocolSection dictionary from a trial, extract the brief summary.
        """
        test_study_details = self.get_study_details(NCTId)
        test_brief_summary = test_study_details.get("protocolSection", {}) \
                             .get("descriptionModule", {}) \
                             .get("briefSummary")
        return(test_brief_summary)


# Usage example:
if __name__ == "__main__":
    api = ClinicalTrialsAPI()
    
    # Example search
    try:
        results = api.search_to_dataframe("covid-19 AND vaccine", max_studies=5)
        print("\nExample search results:")
        print(results)
        
    except Exception as e:
        print(f"Error in example search: {e}")

def fetch_all_studies():
    base_url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "format": "json",
        "pageSize": 1000,
        "fields": (
            "NCTId,"
            "BriefTitle,"
            "OfficialTitle,"
            "OverallStatus,"
            "LastUpdatePostDate,"
            "StudyType,"
            "Phase,"
            "EnrollmentCount,"
            "StartDate,"
            "CompletionDate,"
            "LeadSponsorName,"
            "BriefSummary,"
            "DetailedDescription,"
            "Condition,"
            "EligibilityCriteria,"
            "Gender,"
            "MinimumAge,"
            "MaximumAge,"
            "HealthyVolunteers,"
            "LocationFacility,"
            "LocationCity,"
            "LocationState,"
            "LocationCountry,"
            "InterventionType,"
            "InterventionName"),
        "countTotal": "true"  # Changed to string
    }
    
    all_studies = []
    next_page_token = None
    
    while True:
        if next_page_token:
            params["pageToken"] = next_page_token
            
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            print(response)
            data = response.json()
            studies = data.get("studies", [])
            all_studies.extend(studies)
            
            # Print progress with timestamp
            print(f"{datetime.now().strftime('%H:%M:%S')} - Downloaded {len(all_studies)} studies")
            
            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break
                
            time.sleep(0.5)  # Add small delay between requests
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            print(f"URL that caused error: {response.url}")
            break
            
    return all_studies