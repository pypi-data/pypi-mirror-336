import pandas as pd
import os
from .evaluation import evaluate_model

def perform_ablation_analysis(model, dataloader, output_dir):
    # Perform ablation analysis
    results = []
    num_layers = len(model.vit.encoder.layer)
    num_heads = model.vit.config.num_attention_heads

    for layer in range(num_layers):
        for head in range(num_heads):
            print(f"Zeroing out layer {layer}, head {head}...")
            loss, predictions, targets = evaluate_model(model, dataloader, zero_out_layer=layer, zero_out_head=head)
        
            # Save results for ablation analysis
            results.append({
                "layer": layer,
                "head": head,
                "loss": loss
            })
        
            # Save predictions and ground truth for this scenario
            scenario_results = pd.DataFrame({
                "Chirp_Start_Time_Pred": predictions[:, 0],
                "Chirp_Start_Freq_Pred": predictions[:, 1],
                "Chirp_End_Freq_Pred": predictions[:, 2]
            })
        
            # Save to CSV
            scenario_csv_path = os.path.join(output_dir, f"scenario_layer_{layer}_head_{head}.csv")
            scenario_results.to_csv(scenario_csv_path, index=False)
            print(f"Saved predictions and ground truth for layer {layer}, head {head} to {scenario_csv_path}")

    # Save ablation results to a CSV file
    results_df = pd.DataFrame(results)
    results_csv_path = os.path.join(output_dir, "ablation_results.csv")
    results_df.to_csv(results_csv_path, index=False)
    print(f"Saved ablation results to {results_csv_path}")