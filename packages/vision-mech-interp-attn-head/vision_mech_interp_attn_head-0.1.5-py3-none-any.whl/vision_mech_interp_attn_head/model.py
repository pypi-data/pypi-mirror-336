import torch
import torch.nn as nn
from transformers import ViTModel
from peft import LoraConfig, get_peft_model

class ViTForRegression(nn.Module):
    def __init__(self, pretrained_model_name="google/vit-base-patch16-224"):
        super(ViTForRegression, self).__init__()
        self.vit = ViTModel.from_pretrained(pretrained_model_name)
        
        lora_config = LoraConfig(
            r=8,
            lora_alpha=16,
            target_modules=["query", "value"],
            lora_dropout=0.1,
            bias="none"
        )
        self.vit = get_peft_model(self.vit, lora_config)
        
        self.regression_head = nn.Sequential(
            nn.Linear(self.vit.config.hidden_size, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 3)
        )
        
        # Add device attribute
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.to(self.device)  # Move the model to the appropriate device
    
    def forward(self, x, zero_out_layer=None, zero_out_head=None):
        # Move input tensor to the correct device
        x = x.to(self.device)
        
        # Pass input through ViT
        outputs = self.vit(pixel_values=x)
        
        # Zero out specific attention head if specified
        if zero_out_layer is not None and zero_out_head is not None:
            with torch.no_grad():
                for i, layer in enumerate(self.vit.encoder.layer):
                    if i == zero_out_layer:
                        # Zero out the specified attention head
                        layer.attention.attention.key.weight[zero_out_head, :] = 0
                        layer.attention.attention.value.weight[zero_out_head, :] = 0
                        layer.attention.attention.query.weight[zero_out_head, :] = 0
        
        # Use the [CLS] token representation for regression
        cls_output = outputs.last_hidden_state[:, 0, :]
        regression_output = self.regression_head(cls_output)
        return regression_output