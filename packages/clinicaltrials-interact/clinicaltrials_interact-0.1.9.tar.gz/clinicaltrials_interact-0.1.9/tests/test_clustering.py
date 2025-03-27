# tests/test_clustering.py

import pytest
import pandas as pd
import numpy as np
from clinicaltrials_interact.clustering import get_candidate_embeddings

def test_get_candidate_embeddings():
    # Use a small number of studies for faster tests.
    df, embeddings, model = get_candidate_embeddings("leukemia", max_studies=5)
    
    # Check that the returned dataframe is a Pandas DataFrame and not empty.
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    # Check that embeddings are returned and that their count matches df.
    # Depending on your setup, embeddings might be a torch tensor.
    if hasattr(embeddings, 'cpu'):
        emb_np = embeddings.cpu().numpy()
    else:
        emb_np = np.array(embeddings)
        
    assert emb_np.shape[0] == len(df)
    
    # Optionally, check that the model is an instance of SentenceTransformer
    from sentence_transformers import SentenceTransformer
    assert isinstance(model, SentenceTransformer)

    