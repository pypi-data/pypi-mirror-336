from typing import List, Dict, Optional, Union
from datetime import datetime, timedelta
import requests
import time
import pandas as pd
import plotly.express as px
import plotly.io as pio
import re
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
            
            # Extract phase information
            phases = study_details.get('protocolSection', {}).get(
                'designModule', {}).get('phases', [])
            phase_str = ", ".join(phases) if phases else "Not specified"
            
            # Create phase indicator flags
            phase_1 = False
            phase_2 = False
            phase_3 = False
            phase_4 = False
            
            # Check for each phase in the phases list
            for phase in phases:
                if re.search(r'1', phase):
                    phase_1 = True
                if re.search(r'2', phase):
                    phase_2 = True
                if re.search(r'3', phase):
                    phase_3 = True
                if re.search(r'4', phase):
                    phase_4 = True
            
            # Extract study type
            study_type = study_details.get('protocolSection', {}).get(
                'designModule', {}).get('studyType', '')
                
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
                    'phase': phase_str,  # Keep original phase string
                    'phase_1': phase_1,  # Add phase indicator columns
                    'phase_2': phase_2,
                    'phase_3': phase_3,
                    'phase_4': phase_4,
                    'study_type': study_type
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
                                         title=None, save_path=None, color_by='nct_id', 
                                         filter_country=None, mapbox_style="open-street-map", height=800):
    """
    Create an interactive map of clinical trial locations with better phase filtering.
    Color points by NCT ID to distinguish different trials.
    """
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    
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
    all_locations = locations_df.dropna(subset=['latitude', 'longitude']).copy()
    if len(all_locations) == 0:
        print("Error: No valid coordinates found in the location data")
        return None
    
    # Set initial filtered data (may be updated by user controls)
    valid_locations = all_locations.copy()
    if filter_country:
        valid_locations = valid_locations[valid_locations['country'] == filter_country]
        if len(valid_locations) == 0:
            print(f"No locations found in {filter_country}")
            filter_country = None
            valid_locations = all_locations.copy()
    
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
    
    # Create phase-specific dataframes - THIS IS THE KEY IMPROVEMENT
    phase_1_df = valid_locations[valid_locations['phase_1'] == True].copy()
    phase_2_df = valid_locations[valid_locations['phase_2'] == True].copy()
    phase_3_df = valid_locations[valid_locations['phase_3'] == True].copy()
    phase_4_df = valid_locations[valid_locations['phase_4'] == True].copy()
    
    # Create sets of the NCT IDs for each phase
    phase_1_ncts = set(phase_1_df['nct_id'].unique())
    phase_2_ncts = set(phase_2_df['nct_id'].unique())
    phase_3_ncts = set(phase_3_df['nct_id'].unique())
    phase_4_ncts = set(phase_4_df['nct_id'].unique())
    
    # Prepare hover text information
    valid_locations['hover_text'] = valid_locations.apply(
        lambda row: f"<b>NCT ID:</b> {row['nct_id']}<br>" +
                   f"<b>Title:</b> {row['brief_title']}<br>" +
                   f"<b>Facility:</b> {row['facility']}<br>" +
                   f"<b>Location:</b> {row['city']}, {row['state'] if pd.notna(row['state']) else ''}, {row['country']}<br>" +
                   f"<b>Phase:</b> {row['phase']}<br>" +
                   (f"<b>Status:</b> {row['status']}<br>" if 'status' in row and pd.notna(row['status']) else ""),
        axis=1
    )
    
    # Apply the same hover text to phase-specific dataframes
    phase_1_df['hover_text'] = phase_1_df.apply(
        lambda row: f"<b>NCT ID:</b> {row['nct_id']}<br>" +
                   f"<b>Title:</b> {row['brief_title']}<br>" +
                   f"<b>Facility:</b> {row['facility']}<br>" +
                   f"<b>Location:</b> {row['city']}, {row['state'] if pd.notna(row['state']) else ''}, {row['country']}<br>" +
                   f"<b>Phase:</b> {row['phase']}<br>" +
                   (f"<b>Status:</b> {row['status']}<br>" if 'status' in row and pd.notna(row['status']) else ""),
        axis=1
    )
    
    phase_2_df['hover_text'] = phase_2_df.apply(
        lambda row: f"<b>NCT ID:</b> {row['nct_id']}<br>" +
                   f"<b>Title:</b> {row['brief_title']}<br>" +
                   f"<b>Facility:</b> {row['facility']}<br>" +
                   f"<b>Location:</b> {row['city']}, {row['state'] if pd.notna(row['state']) else ''}, {row['country']}<br>" +
                   f"<b>Phase:</b> {row['phase']}<br>" +
                   (f"<b>Status:</b> {row['status']}<br>" if 'status' in row and pd.notna(row['status']) else ""),
        axis=1
    )
    
    phase_3_df['hover_text'] = phase_3_df.apply(
        lambda row: f"<b>NCT ID:</b> {row['nct_id']}<br>" +
                   f"<b>Title:</b> {row['brief_title']}<br>" +
                   f"<b>Facility:</b> {row['facility']}<br>" +
                   f"<b>Location:</b> {row['city']}, {row['state'] if pd.notna(row['state']) else ''}, {row['country']}<br>" +
                   f"<b>Phase:</b> {row['phase']}<br>" +
                   (f"<b>Status:</b> {row['status']}<br>" if 'status' in row and pd.notna(row['status']) else ""),
        axis=1
    )
    
    phase_4_df['hover_text'] = phase_4_df.apply(
        lambda row: f"<b>NCT ID:</b> {row['nct_id']}<br>" +
                   f"<b>Title:</b> {row['brief_title']}<br>" +
                   f"<b>Facility:</b> {row['facility']}<br>" +
                   f"<b>Location:</b> {row['city']}, {row['state'] if pd.notna(row['state']) else ''}, {row['country']}<br>" +
                   f"<b>Phase:</b> {row['phase']}<br>" +
                   (f"<b>Status:</b> {row['status']}<br>" if 'status' in row and pd.notna(row['status']) else ""),
        axis=1
    )
    
    # Create the main figure - we'll build separate figures for each phase
    fig = go.Figure()
    
    # Add main scattermapbox trace for all locations
    fig.add_trace(
        go.Scattermapbox(
            lat=valid_locations['latitude'],
            lon=valid_locations['longitude'],
            mode='markers',
            marker=dict(
                size=8,
                opacity=0.7,
                color=valid_locations['nct_id'].astype('category').cat.codes,
                colorscale='viridis',  # Changed to a valid colorscale
                showscale=False,
            ),
            text=valid_locations['hover_text'],
            hoverinfo='text',
            name='All Locations',
            legendgroup='all',
            showlegend=False,
            visible=True
        )
    )
    
    # Add a trace for Phase 1 studies
    fig.add_trace(
        go.Scattermapbox(
            lat=phase_1_df['latitude'],
            lon=phase_1_df['longitude'],
            mode='markers',
            marker=dict(
                size=8,
                opacity=0.7,
                color=phase_1_df['nct_id'].astype('category').cat.codes,
                colorscale='viridis',
                showscale=False,
            ),
            text=phase_1_df['hover_text'],
            hoverinfo='text',
            name='Phase 1 Locations',
            legendgroup='phase1',
            showlegend=False,
            visible=False  # Initially hidden
        )
    )
    
    # Add a trace for Phase 2 studies
    fig.add_trace(
        go.Scattermapbox(
            lat=phase_2_df['latitude'],
            lon=phase_2_df['longitude'],
            mode='markers',
            marker=dict(
                size=8,
                opacity=0.7,
                color=phase_2_df['nct_id'].astype('category').cat.codes,
                colorscale='viridis',
                showscale=False,
            ),
            text=phase_2_df['hover_text'],
            hoverinfo='text',
            name='Phase 2 Locations',
            legendgroup='phase2',
            showlegend=False,
            visible=False  # Initially hidden
        )
    )
    
    # Add a trace for Phase 3 studies
    fig.add_trace(
        go.Scattermapbox(
            lat=phase_3_df['latitude'],
            lon=phase_3_df['longitude'],
            mode='markers',
            marker=dict(
                size=8,
                opacity=0.7,
                color=phase_3_df['nct_id'].astype('category').cat.codes,
                colorscale='viridis',
                showscale=False,
            ),
            text=phase_3_df['hover_text'],
            hoverinfo='text',
            name='Phase 3 Locations',
            legendgroup='phase3',
            showlegend=False,
            visible=False  # Initially hidden
        )
    )
    
    # Add a trace for Phase 4 studies
    fig.add_trace(
        go.Scattermapbox(
            lat=phase_4_df['latitude'],
            lon=phase_4_df['longitude'],
            mode='markers',
            marker=dict(
                size=8,
                opacity=0.7,
                color=phase_4_df['nct_id'].astype('category').cat.codes,
                colorscale='viridis',
                showscale=False,
            ),
            text=phase_4_df['hover_text'],
            hoverinfo='text',
            name='Phase 4 Locations',
            legendgroup='phase4',
            showlegend=False,
            visible=False  # Initially hidden
        )
    )
    
    # Set up the mapbox layout
    fig.update_layout(
        mapbox=dict(
            style=mapbox_style,
            center=dict(
                lat=valid_locations['latitude'].mean(),
                lon=valid_locations['longitude'].mean()
            ),
            zoom=1 if not filter_country else 4
        ),
        margin={"r": 0, "t": 50, "l": 0, "b": 10},
    )
    
    # Add statistics and title
    countries = sorted(all_locations['country'].unique())
    
    # Create arrays to control which traces are visible for each filter
    # Index 0: All locations (always the first trace)
    # Index 1: Phase 1
    # Index 2: Phase 2
    # Index 3: Phase 3
    # Index 4: Phase 4
    all_visible = [True, False, False, False, False]
    phase_1_visible = [False, True, False, False, False]
    phase_2_visible = [False, False, True, False, False]
    phase_3_visible = [False, False, False, True, False]
    phase_4_visible = [False, False, False, False, True]
    
    # Create filter controls section with filter buttons
    annotations = [
        # Title
        dict(
            x=0.5,
            y=1.05,
            xref="paper",
            yref="paper",
            text=full_title,
            showarrow=False,
            font=dict(size=16),
            align="center"
        ),
        # Filter section title
        dict(
            x=1.0,
            y=0.95,
            xref="paper",
            yref="paper",
            text="<b>Filter Options</b>",
            showarrow=False,
            font=dict(size=14),
            align="left",
            bgcolor="rgba(255, 255, 255, 0.8)",
            borderpad=4
        ),
        # Statistics
        dict(
            x=1.0,
            y=0.35,
            xref="paper",
            yref="paper",
            text=f"<b>Statistics</b><br>" +
                 f"Total Trials: {valid_locations['nct_id'].nunique()}<br>" +
                 f"Total Locations: {len(valid_locations)}<br>" +
                 f"Countries: {len(countries)}<br>" +
                 f"Phase 1 Trials: {len(phase_1_ncts)}<br>" +
                 f"Phase 2 Trials: {len(phase_2_ncts)}<br>" +
                 f"Phase 3 Trials: {len(phase_3_ncts)}<br>" +
                 f"Phase 4 Trials: {len(phase_4_ncts)}",
            showarrow=False,
            font=dict(size=12),
            align="left",
            bgcolor="rgba(255, 255, 255, 0.8)",
            borderpad=4
        ),
    ]
    
    # Update layout with buttons for filtering
    fig.update_layout(
        height=height,
        annotations=annotations,
        updatemenus=[
            # Phase filter buttons
            dict(
                buttons=[
                    dict(
                        args=[{"visible": all_visible}],
                        label="All Phases",
                        method="update"
                    ),
                    dict(
                        args=[{"visible": phase_1_visible}],
                        label=f"Phase 1 ({len(phase_1_ncts)} trials)",
                        method="update"
                    ),
                    dict(
                        args=[{"visible": phase_2_visible}],
                        label=f"Phase 2 ({len(phase_2_ncts)} trials)",
                        method="update"
                    ),
                    dict(
                        args=[{"visible": phase_3_visible}],
                        label=f"Phase 3 ({len(phase_3_ncts)} trials)",
                        method="update"
                    ),
                    dict(
                        args=[{"visible": phase_4_visible}],
                        label=f"Phase 4 ({len(phase_4_ncts)} trials)",
                        method="update"
                    ),
                ],
                direction="down",
                showactive=True,
                x=1.0,
                xanchor="right",
                y=0.85,
                yanchor="top",
                bgcolor="rgba(255, 255, 255, 0.8)",
                bordercolor="rgba(0, 0, 0, 0.4)",
                font=dict(size=12)
            ),
        ]
    )
    
    # Save to HTML if a path is provided
    if save_path:
        if not save_path.endswith('.html'):
            save_path += '.html'
        fig.write_html(
            save_path,
            full_html=True,
            include_plotlyjs='cdn',
            config={"displayModeBar": True, "scrollZoom": True}
        )
        print(f"Interactive map saved to {save_path}")
    
    return fig

# # Example usage:
if __name__ == "__main__":
    api = ClinicalTrialsAPI()

    fetch_recently_updated_trials(days_ago=1, from_date=None, to_date=None,include_summary=False).head(n=100)
    
    # Example 1: Get locations for a search query
    # cancer_trial_locations = get_trial_locations(
    #     api, 
    #     search_expr="cancer AND recruiting",
    #     max_studies=20
    # )
    
    
    # print("\nDistribution of trial locations by country:")
    # print(cancer_trial_locations["country"])
    
    # # Try to import required libraries, with helpful error messages if they're missing
    # try:
    #     import plotly.express as px
    # except ImportError:
    #     print("This function requires plotly. Install with:\npip install plotly")
    #     exit(1)
    
    # api = ClinicalTrialsAPI()
    
    # # Example 1: Search expression
    # print("\nExample 1: Visualizing locations for cancer trials")
    # fig1 = visualize_trial_locations_interactive(
    #     api,
    #     search_expr="cancer AND recruiting",
    #     max_studies=50,
    #     title="Global Distribution of Cancer Trial Locations",
    #     save_path="cancer_trials_global_interactive.html"
    # )





