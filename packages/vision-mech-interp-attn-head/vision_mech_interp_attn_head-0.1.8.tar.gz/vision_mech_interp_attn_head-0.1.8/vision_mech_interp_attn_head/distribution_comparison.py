import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def compare_distributions(combined_csv_path, baseline_excel_path, output_plot_path):
    combined_df = pd.read_csv(combined_csv_path)
    baseline_df = pd.read_csv(baseline_excel_path)
    baseline_data = baseline_df['Chirp_Start_Time_Pred']
    
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 22
    
    fig, axes = plt.subplots(3, 4, figsize=(24, 18))
    fig.suptitle('Distribution Comparison: Layer Heads vs Baseline', fontsize=20, y=1.02)
    
    colors = plt.cm.tab20(np.linspace(0, 1, 12))
    
    for layer in range(1, 13):
        ax = axes[(layer - 1) // 4, (layer - 1) % 4]
        ax.hist(baseline_data.dropna(), bins=30, alpha=0.3, color='gray', label='BL', edgecolor='black', linewidth=0.5)
        
        for head in range(1, 13):
            column_name = f"layer {layer} - head {head}"
            if column_name in combined_df.columns:
                ax.hist(combined_df[column_name].dropna(), bins=30, alpha=0.7, color=colors[head - 1], label=f'H{head}', edgecolor='black', linewidth=0.5)
        
        ax.set_title(f'Layer {layer}', fontsize=28)
        ax.set_xlabel('Chirp Start Time Raw Predictions', fontsize=22)
        ax.set_ylabel('Frequency', fontsize=26)
        ax.legend(loc='upper right', fontsize=12, ncol=1)
    
    plt.tight_layout()
    plt.savefig(output_plot_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Layer head distribution grid saved to: {output_plot_path}")