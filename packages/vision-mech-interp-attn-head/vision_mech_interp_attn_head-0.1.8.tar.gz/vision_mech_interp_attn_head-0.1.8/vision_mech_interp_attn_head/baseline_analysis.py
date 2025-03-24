import os
import pandas as pd
from .evaluation import evaluate_model

def perform_baseline_analysis(model, dataloader, output_dir):
    """
    Perform baseline analysis without zeroing out any attention heads.
    Save predictions and ablation results to CSV files.
    """
    print("Performing analysis without zeroing out any heads...")
    
    # Evaluate the model
    loss, predictions, targets = evaluate_model(model, dataloader)

    # Save results for ablation analysis
    results = [{
        "layer": "all",
        "head": "all",
        "loss": loss
    }]

    # Save predictions and ground truth
    scenario_results = pd.DataFrame({
        "Chirp_Start_Time_Pred": predictions[:, 0],
        "Chirp_Start_Freq_Pred": predictions[:, 1],
        "Chirp_End_Freq_Pred": predictions[:, 2]
    })

    # Save to CSV
    scenario_csv_path = os.path.join(output_dir, "baseline.csv")
    scenario_results.to_csv(scenario_csv_path, index=False)
    print(f"Saved predictions and ground truth for all heads to {scenario_csv_path}")

    # Save ablation results to a CSV file
    results_df = pd.DataFrame(results)
    results_csv_path = os.path.join(output_dir, "baseline_ablation_results.csv")
    results_df.to_csv(results_csv_path, index=False)
    print(f"Saved ablation results to {results_csv_path}")