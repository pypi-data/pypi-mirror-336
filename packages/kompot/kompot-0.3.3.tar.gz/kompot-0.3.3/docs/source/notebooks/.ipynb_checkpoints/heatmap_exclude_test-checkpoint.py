"""
Example demonstrating how to use the exclude_groups parameter in Kompot's heatmap plotting.

This example shows how to create heatmaps while excluding specific groups.
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
# In a real scenario, you would load your own data with sc.read() or similar
adata = sc.datasets.pbmc3k_processed()

# Add simulated differential expression results to adata.var
# In a real scenario, these would be the results from running kompot.compute_differential_expression
np.random.seed(42)
n_genes = adata.n_vars

# Generate simulated log fold changes
lfc = np.random.normal(0, 1, n_genes)
adata.var["kompot_de_mean_lfc_groupA_to_groupB"] = lfc

# Generate simulated Mahalanobis distances
# Make some genes strongly significant (correlated with fold change)
mahalanobis = np.abs(lfc) * 2 + np.random.normal(0, 1, n_genes)
adata.var["kompot_de_mahalanobis"] = np.abs(mahalanobis)

# For this example, we'll create a random grouping of cells
# In a real scenario, this would be your experimental groups or conditions
n_cells = adata.n_obs
groups = np.random.choice(['groupA', 'groupB', 'groupC', 'groupD', 'groupE'], size=n_cells)
adata.obs['group'] = groups

# Create conditions for diagonal split examples
conditions = np.random.choice(['conditionA', 'conditionB'], size=n_cells)
adata.obs['condition'] = conditions

# Store run info in adata.uns to simulate real kompot run
adata.uns['kompot_de'] = {
    'run_history': [{
        'params': {
            'groupby': 'condition',
            'conditions': ['conditionA', 'conditionB'],
            'condition1': 'conditionA',
            'condition2': 'conditionB'
        },
        'field_names': {
            'mean_lfc_key': 'kompot_de_mean_lfc_groupA_to_groupB',
            'mahalanobis_key': 'kompot_de_mahalanobis'
        }
    }]
}

# Create a standard heatmap with all groups
fig1, ax1 = plt.subplots(figsize=(12, 10))
kp.plot.heatmap(
    adata,
    n_top_genes=15,
    groupby='group',
    standard_scale='var',
    cmap='viridis',
    diagonal_split=False,
    title='Standard Heatmap - All Groups',
    ax=ax1,
    return_fig=True
)
fig1.tight_layout()
fig1.savefig("heatmap_all_groups.png")
plt.close(fig1)

# Create a heatmap excluding a single group (as string)
fig2, ax2 = plt.subplots(figsize=(12, 10))
kp.plot.heatmap(
    adata,
    n_top_genes=15,
    groupby='group',
    standard_scale='var',
    cmap='viridis',
    diagonal_split=False,
    exclude_groups='groupA',  # Exclude a single group as string
    title='Heatmap - Excluding groupA',
    ax=ax2,
    return_fig=True
)
fig2.tight_layout()
fig2.savefig("heatmap_exclude_one_group.png")
plt.close(fig2)

# Create a heatmap excluding multiple groups (as list)
fig3, ax3 = plt.subplots(figsize=(12, 10))
kp.plot.heatmap(
    adata,
    n_top_genes=15,
    groupby='group',
    standard_scale='var',
    cmap='viridis',
    diagonal_split=False,
    exclude_groups=['groupA', 'groupB'],  # Exclude multiple groups as list
    title='Heatmap - Excluding groupA and groupB',
    ax=ax3,
    return_fig=True
)
fig3.tight_layout()
fig3.savefig("heatmap_exclude_multiple_groups.png")
plt.close(fig3)

# Create a heatmap excluding a non-existent group (should show warning)
fig5, ax5 = plt.subplots(figsize=(12, 10))
kp.plot.heatmap(
    adata,
    n_top_genes=15,
    groupby='group',
    standard_scale='var',
    cmap='viridis',
    diagonal_split=False,
    exclude_groups=['non_existent_group', 'groupA'],  # Include a non-existent group
    title='Heatmap - Excluding non-existent group and groupA',
    ax=ax5,
    return_fig=True
)
fig5.tight_layout()
fig5.savefig("heatmap_exclude_nonexistent_group.png")
plt.close(fig5)

# Create a diagonal split heatmap excluding a group
fig4, ax4 = plt.subplots(figsize=(12, 10))
kp.plot.heatmap(
    adata,
    n_top_genes=15,
    groupby='group',
    condition_column='condition',
    standard_scale='var',
    cmap='RdBu_r',
    diagonal_split=True,  # Enable diagonal split
    exclude_groups='groupC',  # Exclude a single group
    title='Diagonal Split Heatmap - Excluding groupC',
    ax=ax4,
    return_fig=True
)
# Don't use tight_layout() for diagonal split, manually adjust spacing
fig4.subplots_adjust(right=0.85)  # Make room for colorbar and legend
fig4.savefig("diagonal_heatmap_exclude_group.png", bbox_inches='tight')
plt.close(fig4)

# Create a diagonal split heatmap excluding a non-existent group
fig6, ax6 = plt.subplots(figsize=(12, 10))
kp.plot.heatmap(
    adata,
    n_top_genes=15,
    groupby='group',
    condition_column='condition',
    standard_scale='var',
    cmap='RdBu_r',
    diagonal_split=True,  # Enable diagonal split
    exclude_groups=['non_existent_group', 'groupC'],  # Include a non-existent group
    title='Diagonal Split Heatmap - Excluding non-existent group and groupC',
    ax=ax6,
    return_fig=True
)
# Don't use tight_layout() for diagonal split, manually adjust spacing
fig6.subplots_adjust(right=0.85)  # Make room for colorbar and legend
fig6.savefig("diagonal_heatmap_exclude_nonexistent_group.png", bbox_inches='tight')
plt.close(fig6)

print("Heatmap examples with group exclusion created successfully!")