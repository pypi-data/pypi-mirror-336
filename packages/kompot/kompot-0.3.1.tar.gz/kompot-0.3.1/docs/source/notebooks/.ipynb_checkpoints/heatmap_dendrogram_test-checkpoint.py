"""
Test script for the improved heatmap functionality with dendrograms at the bottom.
"""

import scanpy as sc
import numpy as np
import matplotlib.pyplot as plt
import kompot as kp

# Set matplotlib to non-interactive mode
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
plt.ioff()  # Turn off interactive mode

# Load your data (for this example, we'll use a built-in dataset)
adata = sc.datasets.pbmc3k_processed()

# Add simulated differential expression results to adata.var
np.random.seed(42)
n_genes = adata.n_vars

# Generate simulated log fold changes
lfc = np.random.normal(0, 1, n_genes)
adata.var["kompot_de_mean_lfc_conditionA_to_conditionB"] = lfc

# Generate simulated Mahalanobis distances
# Make some genes strongly significant (correlated with fold change)
mahalanobis = np.abs(lfc) * 2 + np.random.normal(0, 1, n_genes)
adata.var["kompot_de_mahalanobis"] = np.abs(mahalanobis)

# Create a condition column with exactly two conditions for diagonal split
n_cells = adata.n_obs
conditions = np.random.choice(['conditionA', 'conditionB'], size=n_cells)
adata.obs['condition'] = conditions

# Create a group column for cell types (we'll use louvain clusters as a substitute)
adata.obs['cell_type'] = adata.obs['louvain']

# Store the run info in adata.uns to simulate a real kompot run
adata.uns['kompot_de'] = {
    'run_history': [{
        'params': {
            'groupby': 'condition',
            'conditions': ['conditionA', 'conditionB'],
            'condition1': 'conditionA',
            'condition2': 'conditionB'
        },
        'field_names': {
            'mean_lfc_key': 'kompot_de_mean_lfc_conditionA_to_conditionB',
            'mahalanobis_key': 'kompot_de_mahalanobis'
        }
    }]
}

# Test 1: Diagonal split heatmap with clustering but no dendrograms (default)
print("Creating diagonal split heatmap with clustering but no dendrograms (default)...")
kp.plot.heatmap(
    adata,
    n_top_genes=15,
    groupby='cell_type',
    condition_column='condition',
    condition1_name='conditionA',
    condition2_name='conditionB',
    lfc_key="kompot_de_mean_lfc_conditionA_to_conditionB",
    score_key="kompot_de_mahalanobis",
    standard_scale='var',  # gene-wise z-scoring
    cmap='viridis',
    diagonal_split=True,
    cluster=True,  # Perform clustering
    dendrogram=False,  # Don't show dendrograms (default)
    title="Heatmap with Clustering (No Dendrograms)",
    save="test_heatmap_cluster_no_dendro.png"
)

# Test 2: Diagonal split heatmap with row dendrograms only
print("Creating diagonal split heatmap with row dendrograms only...")
kp.plot.heatmap(
    adata,
    n_top_genes=15,
    groupby='cell_type',
    condition_column='condition',
    condition1_name='conditionA',
    condition2_name='conditionB',
    lfc_key="kompot_de_mean_lfc_conditionA_to_conditionB",
    score_key="kompot_de_mahalanobis",
    standard_scale='var',
    cmap='viridis',
    diagonal_split=True,
    cluster=True,
    dendrogram=True,
    cluster_rows=True,
    cluster_cols=False,
    dendrogram_color="black",
    title="Heatmap with Row Dendrograms (Black)",
    save="test_heatmap_row_dendro.png"
)

# Test 3: Diagonal split heatmap with column dendrograms only
print("Creating diagonal split heatmap with column dendrograms only...")
kp.plot.heatmap(
    adata,
    n_top_genes=15,
    groupby='cell_type',
    condition_column='condition',
    condition1_name='conditionA',
    condition2_name='conditionB',
    lfc_key="kompot_de_mean_lfc_conditionA_to_conditionB",
    score_key="kompot_de_mahalanobis",
    standard_scale='var',
    cmap='viridis',
    diagonal_split=True,
    cluster=True,
    dendrogram=True,
    cluster_rows=False,
    cluster_cols=True,
    dendrogram_color="black",
    title="Heatmap with Column Dendrograms at Bottom (Black)",
    save="test_heatmap_col_dendro.png"
)

# Test 4: Diagonal split heatmap with both dendrograms
print("Creating diagonal split heatmap with both dendrograms...")
kp.plot.heatmap(
    adata,
    n_top_genes=15,
    groupby='cell_type',
    condition_column='condition',
    condition1_name='conditionA',
    condition2_name='conditionB',
    lfc_key="kompot_de_mean_lfc_conditionA_to_conditionB",
    score_key="kompot_de_mahalanobis",
    standard_scale='var',
    cmap='viridis',
    diagonal_split=True,
    cluster=True,
    dendrogram=True,
    cluster_rows=True,
    cluster_cols=True,
    dendrogram_color="black",
    title="Heatmap with Both Dendrograms (Black)",
    save="test_heatmap_both_dendro.png"
)

# Test 5: Diagonal split heatmap with both dendrograms in a different color
print("Creating diagonal split heatmap with both dendrograms in blue...")
kp.plot.heatmap(
    adata,
    n_top_genes=15,
    groupby='cell_type',
    condition_column='condition',
    condition1_name='conditionA',
    condition2_name='conditionB',
    lfc_key="kompot_de_mean_lfc_conditionA_to_conditionB",
    score_key="kompot_de_mahalanobis",
    standard_scale='var',
    cmap='viridis',
    diagonal_split=True,
    cluster=True,
    dendrogram=True,
    cluster_rows=True,
    cluster_cols=True,
    dendrogram_color="blue",
    title="Heatmap with Both Dendrograms (Blue)",
    save="test_heatmap_both_dendro_blue.png"
)

print("Dendrogram heatmap tests completed. Check the output images.")