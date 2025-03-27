import requests
import time
import pandas as pd
from typing import List, Dict, Optional, Union
from datetime import datetime, timedelta
import plotly.express as px
import plotly.io as pio

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



def fetch_recently_updated_trials(days_ago=30, from_date=None, to_date=None,include_summary=False):
    """
    Fetches clinical trials updated within a specified date range.
    
    Args:
        days_ago (int): Number of days to look back from today. Default is 30.
                        Only used if from_date and to_date are not provided.
        from_date (str): Start date in 'YYYY-MM-DD' format.
        to_date (str): End date in 'YYYY-MM-DD' format.
        include_summary (bool): Whether to include the brief summary in the results.
    Returns:
        pd.DataFrame: DataFrame containing the retrieved studies.
    """
    # Determine the date range
    if from_date and to_date:
        # Use the provided date range
        start_date = from_date
        end_date = to_date
    else:
        # Calculate date range from days_ago
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
    
    base_url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "format": "json",
        "pageSize": 1000,
        # Use the range query syntax for LastUpdatePostDate
        "query.term": f"AREA[LastUpdatePostDate]RANGE[{start_date},{end_date}]",
        "countTotal": "true"
    }
    
    all_studies = []
    next_page_token = None
    
    while True:
        if next_page_token:
            params["pageToken"] = next_page_token
            
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            studies = data.get("studies", [])
            all_studies.extend(studies)
            
            print(f"Downloaded {len(all_studies)} studies updated between {start_date} and {end_date}")
            
            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break
                
            time.sleep(0.1)  # Be nice to the API
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            break
    df = pd.DataFrame(all_studies)
    
    # Extract nctId and lastUpdatePostDateStruct from protocolSection
    df['nctId'] = df['protocolSection'].apply(lambda x: x.get('identificationModule', {}).get('nctId'))
    df['lastUpdatePostDateStruct'] = df['protocolSection'].apply(
        lambda x: x.get('statusModule', {}).get('lastUpdatePostDateStruct', {}).get('date')
    )
    # Extract brief summary if requested
    if include_summary:
        df['briefSummary'] = df['protocolSection'].apply(
            lambda x: x.get('descriptionModule', {}).get('briefSummary', '')
        )
        return df[['nctId', 'lastUpdatePostDateStruct', 'briefSummary']]
    # Keep only the extracted columns
    return df[['nctId', 'lastUpdatePostDateStruct']]

def get_trial_locations(api, search_expr=None, nct_id_list=None, max_studies=100):
    """
    Get locations for clinical trials based on either a search expression or a list of NCT IDs.
    
    Args:
        api (ClinicalTrialsAPI): Instance of the ClinicalTrialsAPI class
        search_expr (str, optional): Search expression to find trials
        nct_id_list (List[str], optional): List of NCT IDs to retrieve
        max_studies (int): Maximum number of studies to retrieve if using search_expr
        
    Returns:
        pd.DataFrame: DataFrame with trial locations, each row representing one location
    """
    # Validate inputs
    if search_expr is None and nct_id_list is None:
        raise ValueError("Either search_expr or nct_id_list must be provided")
    
    # Get trial IDs from search expression if provided
    if search_expr is not None:
        results = api.search_to_dataframe(search_expr, max_studies=max_studies)
        if 'protocolSection' not in results.columns:
            print("No studies found matching the search criteria")
            return pd.DataFrame()
            
        # Extract NCT IDs from search results
        nct_ids = []
        for _, row in results.iterrows():
            try:
                nct_id = row['protocolSection'].get('identificationModule', {}).get('nctId')
                if nct_id:
                    nct_ids.append(nct_id)
            except:
                continue
    else:
        # Use provided NCT IDs
        nct_ids = nct_id_list
    
    # Get location data for each trial
    all_locations = []
    
    for i, nct_id in enumerate(nct_ids):
        if i % 10 == 0:
            print(f"Processing trial {i+1}/{len(nct_ids)}: {nct_id}")
            
        try:
            # Get study details
            study_details = api.get_study_details(nct_id)
            
            # Extract location information
            locations = study_details.get('protocolSection', {}).get(
                'contactsLocationsModule', {}).get('locations', [])
            
            if not locations:
                continue
                
            # Capture brief title for context
            brief_title = study_details.get('protocolSection', {}).get(
                'identificationModule', {}).get('briefTitle', '')
                
            # Extract relevant fields from each location
            for location in locations:
                location_data = {
                    'nct_id': nct_id,
                    'brief_title': brief_title,
                    'facility': location.get('facility', ''),
                    'city': location.get('city', ''),
                    'state': location.get('state', ''),
                    'zip': location.get('zip', ''),
                    'country': location.get('country', ''),
                    'status': location.get('status', ''),
                }
                
                # Add geo coordinates if available
                if 'geoPoint' in location:
                    location_data['latitude'] = location.get('geoPoint', {}).get('lat')
                    location_data['longitude'] = location.get('geoPoint', {}).get('lon')
                
                all_locations.append(location_data)
            
            # Be nice to the API
            time.sleep(0.1)
                
        except Exception as e:
            print(f"Error processing trial {nct_id}: {e}")
            continue
    
    # Create DataFrame from collected data
    locations_df = pd.DataFrame(all_locations)
    
    print(f"\nRetrieved {len(locations_df)} locations from {len(set(locations_df['nct_id']))} trials")
    
    return locations_df

def visualize_trial_locations_interactive(api, search_expr=None, nct_id_list=None, max_studies=100, 
                                         title=None, save_path=None, color_by='country', 
                                         filter_country=None, mapbox_style="open-street-map", height=800):
    """
    Create an interactive map of clinical trial locations using Plotly.
    
    Args:
        api (ClinicalTrialsAPI): Instance of the ClinicalTrialsAPI class
        search_expr (str, optional): Search expression to find trials
        nct_id_list (List[str], optional): List of NCT IDs to retrieve
        max_studies (int): Maximum number of studies to retrieve if using search_expr
        title (str, optional): Title for the map
        save_path (str, optional): Path to save the map as HTML
        color_by (str): Column to use for color-coding (default: 'country')
        filter_country (str, optional): Filter to show only trials in this country
        mapbox_style (str): Style of the map ('open-street-map', 'carto-positron', etc.)
        height (int): Height of the map in pixels
        
    Returns:
        plotly.graph_objects.Figure: Interactive map figure
    """
    
    
    # Get locations data from search expression or NCT ID list
    locations_df = get_trial_locations(api, search_expr, nct_id_list, max_studies)
    
    # Check if we got any data
    if locations_df.empty:
        print("No location data found. Please check your search criteria.")
        return None
    
    # Check if required columns exist
    if 'latitude' not in locations_df.columns or 'longitude' not in locations_df.columns:
        print("Error: Location data must contain latitude and longitude columns")
        print("Available columns:", locations_df.columns.tolist())
        return None
    
    # Remove rows with missing coordinates
    valid_locations = locations_df.dropna(subset=['latitude', 'longitude']).copy()
    if len(valid_locations) == 0:
        print("Error: No valid coordinates found in the location data")
        return None
    
    # Filter by country if specified
    if filter_country:
        valid_locations = valid_locations[valid_locations['country'] == filter_country]
        if len(valid_locations) == 0:
            print(f"No locations found in {filter_country}")
            return None
    
    # Prepare hover text information
    valid_locations['hover_text'] = valid_locations.apply(
        lambda row: f"<b>NCT ID:</b> {row['nct_id']}<br>" +
                    f"<b>Title:</b> {row['brief_title']}<br>" +
                    f"<b>Facility:</b> {row['facility']}<br>" +
                    f"<b>Location:</b> {row['city']}, {row['state'] if pd.notna(row['state']) else ''}, {row['country']}<br>" +
                    (f"<b>Status:</b> {row['status']}<br>" if 'status' in row and pd.notna(row['status']) else ""),
        axis=1
    )
    
    # Set map title
    if title is None:
        trial_count = valid_locations['nct_id'].nunique()
        search_info = f"'{search_expr}'" if search_expr else f"{len(nct_id_list)} specified NCT IDs"
        title = f"Clinical Trial Locations for {search_info}"
        subtitle = f"{len(valid_locations)} locations across {trial_count} trials"
        full_title = f"{title}<br><sup>{subtitle}</sup>"
    else:
        full_title = title
    
    # Check if color_by column exists
    if color_by not in valid_locations.columns:
        print(f"Warning: '{color_by}' column not found, using 'country' for coloring")
        color_by = 'country' if 'country' in valid_locations.columns else None
    
    # Create the map
    if color_by:
        fig = px.scatter_mapbox(
            valid_locations,
            lat="latitude",
            lon="longitude",
            color=color_by,
            hover_name="facility",
            hover_data=None,  # Don't show any columns in hover automatically
            custom_data=["nct_id", "brief_title", "facility", "city", "state", "country"],
            color_discrete_sequence=px.colors.qualitative.Bold,
            zoom=1 if not filter_country else 3,
            height=height,
            title=full_title,
            opacity=0.7,
            size_max=10,
            category_orders={color_by: sorted(valid_locations[color_by].unique())}
        )
    else:
        fig = px.scatter_mapbox(
            valid_locations,
            lat="latitude",
            lon="longitude",
            hover_name="facility",
            hover_data=None,
            custom_data=["nct_id", "brief_title", "facility", "city", "state", "country"],
            zoom=1 if not filter_country else 3,
            height=height,
            title=full_title,
            opacity=0.7
        )
    
    # Update hover template to show detailed information
    fig.update_traces(
        hovertemplate="%{customdata[2]}<br>" +
                      "<b>NCT ID:</b> %{customdata[0]}<br>" +
                      "<b>Title:</b> %{customdata[1]}<br>" +
                      "<b>Location:</b> %{customdata[3]}, %{customdata[4]}, %{customdata[5]}<extra></extra>"
    )
    
    # Set the mapbox style
    fig.update_layout(
        mapbox_style=mapbox_style,
        mapbox=dict(
            center=dict(
                lat=valid_locations['latitude'].mean(),
                lon=valid_locations['longitude'].mean()
            ),
            zoom=1 if not filter_country else 4
        ),
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        title={
            'text': full_title,
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    
    # Center on US if filtering for US
    if filter_country == 'United States':
        fig.update_layout(
            mapbox=dict(
                center=dict(lat=39.5, lon=-98.5),
                zoom=3
            )
        )
    
    # Save to HTML if a path is provided
    if save_path:
        if not save_path.endswith('.html'):
            save_path += '.html'
        fig.write_html(save_path)
        print(f"Interactive map saved to {save_path}")
    
    return fig

# # Example usage:
# if __name__ == "__main__":
#     api = ClinicalTrialsAPI()
    
#     # Example 1: Get locations for a search query
#     cancer_trial_locations = get_trial_locations(
#         api, 
#         search_expr="cancer AND recruiting",
#         max_studies=20
#     )
    
    
#     print("\nDistribution of trial locations by country:")
#     print(cancer_trial_locations.head(10))
    
#     # Try to import required libraries, with helpful error messages if they're missing
#     try:
#         import plotly.express as px
#     except ImportError:
#         print("This function requires plotly. Install with:\npip install plotly")
#         exit(1)
    
#     api = ClinicalTrialsAPI()
    
#     # Example 1: Search expression
#     print("\nExample 1: Visualizing locations for cancer trials")
#     fig1 = visualize_trial_locations_interactive(
#         api,
#         search_expr="cancer AND recruiting",
#         max_studies=50,
#         title="Global Distribution of Cancer Trial Locations",
#         save_path="cancer_trials_global_interactive.html"
#     )





