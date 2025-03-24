import torch
import numpy as np

def evaluate_model(model, dataloader, zero_out_layer=None, zero_out_head=None):
    model.eval()
    total_loss = 0.0
    criterion = torch.nn.MSELoss()
    total_samples = 0
    
    all_predictions = []
    all_targets = []
    
    with torch.no_grad():
        for batch in dataloader:
            inputs, targets = batch
            inputs, targets = inputs.to(model.device), targets.to(model.device)  # Move data to device
            outputs = model(inputs, zero_out_layer, zero_out_head)
            loss = criterion(outputs, targets)
            total_loss += loss.item()
            total_samples += inputs.size(0)
            
            all_predictions.extend(outputs.cpu().numpy())
            all_targets.extend(targets.cpu().numpy())
    
    print(f"Total images processed: {total_samples}")
    return total_loss / len(dataloader), np.array(all_predictions), np.array(all_targets)