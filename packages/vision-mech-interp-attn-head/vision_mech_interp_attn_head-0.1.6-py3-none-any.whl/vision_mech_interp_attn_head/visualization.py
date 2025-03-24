import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def plot_heatmap(file_path, baseline_loss, output_path):
    # Read the CSV file
    df = pd.read_csv(file_path)  # Use pd.read_csv for CSV files
    
    # Calculate the increase percent for each loss value
    df['increase_percent'] = ((df['loss'] - baseline_loss) / baseline_loss) * 100
    
    # Pivot the DataFrame to create a matrix for the heatmap
    heatmap_data = df.pivot(index="layer", columns="head", values="increase_percent")
    
    # Set the font to Times New Roman and size to 16
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 16
    
    # Create the heatmap with reversed colormap
    plt.figure(figsize=(12, 8))
    ax = sns.heatmap(
        heatmap_data,
        cmap="RdYlBu_r",  # Reversed colormap (blue for lower values, red for higher values)
        annot=True,       # Annotate cells with values (set to True to show increase percent)
        fmt=".2f",        # Format annotations to 2 decimal places
        linewidths=0.5,   # Add lines between cells
        cbar_kws={'label': 'Increase Percent (%)'},  # Add a label to the colorbar
    )
    
    # Adjust the x-axis and y-axis tick labels to start from 1 instead of 0
    ax.set_xticks(np.arange(heatmap_data.shape[1]) + 0.5)  # Center the ticks
    ax.set_xticklabels(np.arange(1, heatmap_data.shape[1] + 1))  # Start labels from 1
    ax.set_yticks(np.arange(heatmap_data.shape[0]) + 0.5)  # Center the ticks
    ax.set_yticklabels(np.arange(1, heatmap_data.shape[0] + 1))  # Start labels from 1
    
    # Add title and labels
    plt.title("Layer vs Head Loss Increase Heatmap", fontsize=20, pad=20)
    plt.xlabel("Head", fontsize=18, labelpad=15)
    plt.ylabel("Layer", fontsize=18, labelpad=15)
    
    # Adjust layout for better appearance
    plt.tight_layout()
    
    # Save the figure to the specified path
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    
    # Close the plot to free up memory
    plt.close()