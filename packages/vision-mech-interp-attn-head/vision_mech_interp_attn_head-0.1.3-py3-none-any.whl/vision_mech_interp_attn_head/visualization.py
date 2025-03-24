import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def plot_heatmap(file_path, baseline_loss, output_path):
    df = pd.read_excel(file_path)
    df['increase_percent'] = ((df['loss'] - baseline_loss) / baseline_loss) * 100
    heatmap_data = df.pivot(index="layer", columns="head", values="increase_percent")
    
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 16
    
    plt.figure(figsize=(12, 8))
    ax = sns.heatmap(
        heatmap_data,
        cmap="RdYlBu_r",
        annot=True,
        fmt=".2f",
        linewidths=0.5,
        cbar_kws={'label': 'Increase Percent (%)'},
    )
    
    ax.set_xticks(np.arange(heatmap_data.shape[1]) + 0.5)
    ax.set_xticklabels(np.arange(1, heatmap_data.shape[1] + 1))
    ax.set_yticks(np.arange(heatmap_data.shape[0]) + 0.5)
    ax.set_yticklabels(np.arange(1, heatmap_data.shape[0] + 1))
    
    plt.title("Layer vs Head Loss Increase Heatmap", fontsize=20, pad=20)
    plt.xlabel("Head", fontsize=18, labelpad=15)
    plt.ylabel("Layer", fontsize=18, labelpad=15)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()