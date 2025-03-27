import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"  # or "true" if you want to enable it

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import SpectralClustering
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer, util
import seaborn as sns
from sklearn.manifold import TSNE
from .ctg_api import ClinicalTrialsAPI
import os
from datetime import datetime

def get_candidate_embeddings(keyword: str, max_studies: int = 500):

    api = ClinicalTrialsAPI()
    if keyword == "":
        print(f"searching for {max_studies} studies without a keyword (general search)\n")
    else:
        print(f"searching for {max_studies} studies related to {keyword}...\n")
    df = api.search_to_dataframe_IDs(keyword, max_studies=max_studies)
    df["briefSummary"] = df["NCTId"].apply(lambda x: api.extract_brief_summary(x))
    corpus = df["briefSummary"].fillna("").tolist()
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(corpus, convert_to_tensor=True)
    
    # Convert embeddings to numpy array for checking NaNs
    emb_np = embeddings.cpu().numpy() if hasattr(embeddings, 'cpu') else np.array(embeddings)
    
    # Identify rows with NaNs
    nan_mask = np.isnan(emb_np).any(axis=1)
    if nan_mask.any():
        print(f"Found {nan_mask.sum()} studies with NaN embeddings. Filtering them out.\n")
        # Filter out those rows from both df and embeddings
        df = df.loc[~nan_mask].reset_index(drop=True)
        emb_np = emb_np[~nan_mask]
        # Optionally, convert back to tensor if needed:
        import torch
        embeddings = torch.tensor(emb_np)
    
    return df, embeddings, model

def get_top_similar_ids(query: str, keyword: str, candidate_pool_size: int = 500, top_n: int = 10, 
                        save_to_file: bool = True, filename: str = None):
    """
    Given a query description and a keyword for candidate filtering,
    computes the similarity between the query and the candidate studies,
    and returns the IDs (e.g., NCTId) of the top_n most similar studies.
    Also saves the IDs to a text file in the outputs directory.
    
    Args:
        query (str): The query text to find similar studies for.
        keyword (str): Keyword to filter candidate studies.
        candidate_pool_size (int): Maximum number of candidate studies to retrieve.
        top_n (int): Number of top similar studies to return.
        save_to_file (bool): Whether to save the results to a file.
        filename (str): Name of the output file. If None, a default name will be generated.
        
    Returns:
        List[str]: List of NCTIds for the top_n most similar studies.
    """
    print("Retrieving candidate studies...\n")
    df, embeddings, model = get_candidate_embeddings(keyword, max_studies=candidate_pool_size)
    
    # Compute the embedding for the query
    query_embedding = model.encode([query], convert_to_tensor=True)
    
    # Compute cosine similarity between the query and candidate embeddings
    similarities = util.pytorch_cos_sim(query_embedding, embeddings).cpu().numpy()[0]
    print("Computing similarities...\n")
    # Get indices of the top_n similar studies (sorted from most similar to least similar)
    top_indices = np.argsort(similarities)[::-1][:top_n]
    top_ids = df.iloc[top_indices]["NCTId"].tolist()
    
    # Save to file if requested
    if save_to_file:
        # Create outputs directory if it doesn't exist

        outputs_dir = os.path.join(os.getcwd(), 'outputs')
        os.makedirs(outputs_dir, exist_ok=True)

        #outputs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
        #os.makedirs(outputs_dir, exist_ok=True)
        
        # Generate filename if not provided
        if filename is None:
            # Create a sanitized version of the query for the filename
            sanitized_query = "".join(c if c.isalnum() else "_" for c in query[:30])
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"similar_studies_{sanitized_query}_{timestamp}.txt"
        
        # Save top IDs to text file
        filepath = os.path.join(outputs_dir, filename)
        with open(filepath, 'w') as f:
            f.write(f"Query: {query}\n")
            f.write(f"Keyword filter: {keyword if keyword else 'None'}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("Top similar study IDs:\n")
            for i, nct_id in enumerate(top_ids, 1):
                similarity = similarities[top_indices[i-1]]
                f.write(f"{i}. {nct_id} (Similarity: {similarity:.4f})\n")
                
        print(f"Top similar study IDs saved to: {filepath}\n")
    
    return top_ids

def plot_similarity_matrix(embeddings, subset_size: int = None, filename="similarity_matrix.png"):
    """
    Plots a heatmap of the cosine similarity matrix computed from the embeddings.
    Saves the figure to a directory inside clinicaltrials_interact called figures.
    
    Args:
        embeddings: BERT-based embeddings (torch tensor or numpy array).
        subset_size: If provided and less than the total number of studies,
                     a random subset of studies of this size will be used for plotting.
        filename: Name of the file to save the figure as.
    """
    # If subset_size is provided and less than total number of embeddings, select a random subset.
    if subset_size is not None:
        total = embeddings.shape[0] if hasattr(embeddings, 'shape') else len(embeddings)
        if total > subset_size:
            indices = np.random.choice(total, size=subset_size, replace=False)
            embeddings = embeddings[indices] if hasattr(embeddings, 'cpu') else np.array(embeddings)[indices]
    
    similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings).cpu().numpy()
    plt.figure(figsize=(10, 8))
    sns.heatmap(similarity_matrix, cmap="viridis")
    plt.title("Cosine Similarity Matrix for Brief Summaries (BERT-based)")
    plt.xlabel("Study Index")
    plt.ylabel("Study Index")
    
    # Create figures directory if it doesn't exist
    figures_dir = os.path.join(os.getcwd(), 'figures')
    os.makedirs(figures_dir, exist_ok=True)
    #os.makedirs(figures_dir, exist_ok=True)
    
    # Save the figure
    filepath = os.path.join(figures_dir, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"Similarity matrix saved to: {filepath}\n")
    
    # No plt.show() call to avoid displaying the plot

def perform_spectral_clustering(embeddings, n_clusters=3):
    """
    Performs spectral clustering on the embeddings using a precomputed cosine similarity matrix.
    
    Returns:
        labels (np.ndarray): Cluster labels for each study.
        similarity_matrix (np.ndarray): The computed cosine similarity matrix.
    """
    similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings).cpu().numpy()
    #similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings).cpu().numpy()
    similarity_matrix[similarity_matrix < 0] = 0    
    clustering = SpectralClustering(n_clusters=n_clusters, affinity="precomputed", random_state=42)
    labels = clustering.fit_predict(similarity_matrix)
    return labels, similarity_matrix

def plot_clusters(embeddings, labels, perplexity=30, max_iter=1000, filename="clusters.png", keyword = None):
    """
    Reduces high-dimensional embeddings to 2D using t-SNE and plots the clusters.
    Saves the figure to a directory inside clinicaltrials_interact called figures.
    
    Args:
        embeddings: High-dimensional embeddings (torch tensor or numpy array).
        labels: Cluster labels (array-like).
        perplexity: t-SNE perplexity parameter.
        max_iter: Number of iterations for t-SNE.
        filename: Name of the file to save the figure as.
    """
    # Convert embeddings to numpy array if they are torch tensors.
    if hasattr(embeddings, 'cpu'):
        embeddings_np = embeddings.cpu().numpy()
    else:
        embeddings_np = np.array(embeddings)
    
    tsne = TSNE(n_components=2, perplexity=perplexity, max_iter=max_iter, random_state=42)
    embeddings_2d = tsne.fit_transform(embeddings_np)
    
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], c=labels, cmap="viridis", alpha=0.7)
    plt.title("t-SNE Visualization of Clusters")
    plt.xlabel("t-SNE Dimension 1")
    plt.ylabel("t-SNE Dimension 2")
    plt.colorbar(scatter, label="Cluster Label")
    
    # Create figures directory if it doesn't exist

    figures_dir = os.path.join(os.getcwd(), 'figures')
    os.makedirs(figures_dir, exist_ok=True)
    
    # Save the figure
    filepath = os.path.join(figures_dir, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"cluster visualization for {keyword} saved to: {filepath}\n")
    
    #plt.show()

def plot_index_to_id_mapping(df, subset_size: int = 50, filename="index_to_id_mapping.png"):
    """
    Plots a table mapping study indices (used in plots) to their corresponding study IDs.
    Saves the figure to a directory inside clinicaltrials_interact called figures.
    
    Args:
        df (pd.DataFrame): DataFrame containing the candidate studies with a 'NCTId' column.
        subset_size (int): Number of studies to include in the mapping table.
        filename (str): Name of the file to save the figure as.
    """
    # If the DataFrame is larger than the subset_size, select the first subset_size studies
    if len(df) > subset_size:
        mapping_df = df.iloc[:subset_size][["NCTId"]].copy()
    else:
        mapping_df = df[["NCTId"]].copy()
    
    mapping_df.reset_index(inplace=True)
    mapping_df.rename(columns={'index': 'Study Index', 'NCTId': 'Study ID'}, inplace=True)
    
    fig, ax = plt.subplots(figsize=(10, len(mapping_df) * 0.3 + 1))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=mapping_df.values, colLabels=mapping_df.columns, loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    plt.title("Mapping of Study Index to Study ID")
    
    # Create figures directory if it doesn't exist

    figures_dir = os.path.join(os.getcwd(), 'figures')
    os.makedirs(figures_dir, exist_ok=True)
    
    # Save the figure
    filepath = os.path.join(figures_dir, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"plot_index_to_id_mapping saved to: {filepath} \n")
    print("Use this mapping to understand which studies are most similar to each other.\n")
    
    # No plt.show() call to avoid displaying the plot

def plot_general_tsne_clusters(max_studies: int = 500, n_clusters: int = 3, perplexity=30, max_iter=1000):
    """
    Retrieves a general candidate pool (using no keyword), computes embeddings,
    performs spectral clustering, and plots t-SNE clusters.
    
    This function is intended to reveal broad subjects or keywords represented by the studies.
    """
    # Use an empty keyword for a general search
    df, embeddings, model = get_candidate_embeddings("", max_studies=max_studies)
    labels, sim_matrix = perform_spectral_clustering(embeddings, n_clusters=n_clusters)
    plot_clusters(embeddings, labels, perplexity=perplexity, max_iter=max_iter)
    return df, embeddings, labels

def extract_cluster_keywords(df: pd.DataFrame, cluster_labels: np.ndarray, top_n: int = 10) -> dict:
    """
    Extracts keywords for each cluster using TF-IDF.
    
    Args:
        df (pd.DataFrame): DataFrame containing the studies with a 'briefSummary' column.
        cluster_labels (np.ndarray): Array of cluster labels corresponding to each study.
        top_n (int): Number of top keywords to extract per cluster.
        
    Returns:
        dict: A dictionary where keys are cluster labels and values are lists of keywords.
    """
    df = df.copy()
    df["cluster"] = cluster_labels
    cluster_keywords = {}
    
    # Create a custom stop words list (ensure it's a list, not a set)
    from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
    custom_stop_words = list(ENGLISH_STOP_WORDS)
    custom_stop_words.extend(["intervention","purpose","study", "health","patients", "treatment", "group", "clinical", "trial", "investigators"])
    
    # Loop over each unique cluster
    for cluster in df["cluster"].unique():
        # Combine all brief summaries in the cluster into one text document
        cluster_text = " ".join(df[df["cluster"] == cluster]["briefSummary"].fillna("").tolist())
        
        # When the corpus is just one document, don't apply a max_df filter less than 1.0.
        vectorizer = TfidfVectorizer(stop_words=custom_stop_words, max_df=1.0, max_features=1000)
        tfidf_matrix = vectorizer.fit_transform([cluster_text])
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.toarray()[0]
        
        # Get the indices of the top_n scores
        top_indices = scores.argsort()[::-1][:top_n]
        keywords = [feature_names[i] for i in top_indices]
        cluster_keywords[cluster] = keywords
        
    return cluster_keywords

def print_cluster_keywords(filename="cluster_keywords.txt"):
    """
    Performs clustering and extracts keywords for each cluster.
    Prints the keywords to console and saves them to a text file in the outputs directory.
    
    Args:
        filename (str): Name of the file to save the keywords to.
    """
    df, embeddings, labels = plot_general_tsne_clusters(max_studies=500, n_clusters=5)
    keywords_per_cluster = extract_cluster_keywords(df, labels, top_n=10)
    
    # Create outputs directory if it doesn't exist


    outputs_dir = os.path.join(os.getcwd(), 'outputs')
    os.makedirs(outputs_dir, exist_ok=True)
    
    # Save keywords to text file
    filepath = os.path.join(outputs_dir, filename)
    with open(filepath, 'w') as f:
        for cluster, keywords in keywords_per_cluster.items():
            cluster_line = f"Cluster {cluster}: {keywords}"
            f.write(cluster_line + '\n')
            print(cluster_line)
    
    print(f"Cluster keywords saved to: {filepath}\n")
    return keywords_per_cluster

if __name__ == "__main__":
    
    # 1a. Retrieve candidate studies related to "leukemia" and compute embeddings.
    df, embeddings, model = get_candidate_embeddings("leukemia", max_studies=100)
    
    # 1b. Plot the cosine similarity matrix for a subset (e.g., 50 studies) of the candidate pool.
    plot_similarity_matrix(embeddings, subset_size=50)

    # 1c. Output the index to id mapping to understand which studies are most to each other. 
    plot_index_to_id_mapping(df, subset_size=50)

    # 1d. Perform spectral clustering on the embeddings.
    labels, sim_matrix = perform_spectral_clustering(embeddings, n_clusters=3)
    
    # 1e. Visualize the clusters with a t-SNE plot.
    plot_clusters(embeddings, labels, filename="leukemia_clusters.png", keyword = "leukemia")
    
    # Second usage below

    # 2a. For a given query, return the IDs of the top 10 most similar studies.
    query = "A study about heart attacks"
    top_similar_ids = get_top_similar_ids(query, "", candidate_pool_size=500, top_n=10)
    print(f"Top similar study IDs related to your query: {top_similar_ids}\n")


    # Third usage below

    # 3. Perform general clustering and extract keywords for each cluster.
    # Takes the top 500 or so studies and clusters them into 5 clusters. 
    # returns the keywords for each cluster
    print_cluster_keywords()
