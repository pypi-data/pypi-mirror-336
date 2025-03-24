import torch
import torch.nn as nn
from transformers import ViTModel
from peft import LoraConfig, get_peft_model

class ViTForRegression(nn.Module):
    def __init__(self, pretrained_model_name="google/vit-base-patch16-224"):
        super(ViTForRegression, self).__init__()
        self.vit = ViTModel.from_pretrained(pretrained_model_name, attn_implementation="eager")
        
        # Apply LoRA for Parameter-Efficient Fine-Tuning
        lora_config = LoraConfig(
            r=8,  # Rank of the low-rank adaptation
            lora_alpha=16,  # Scaling factor
            target_modules=["query", "value"],  # Apply LoRA to specific layers
            lora_dropout=0.1,
            bias="none"
        )
        self.vit = get_peft_model(self.vit, lora_config)
        
        # Define the regression head
        self.regression_head = nn.Sequential(
            nn.Linear(self.vit.config.hidden_size, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 3)  # Output 3 values for regression
        )

    def forward(self, x):
        outputs = self.vit(pixel_values=x)
        cls_output = outputs.last_hidden_state[:, 0, :]
        regression_output = self.regression_head(cls_output)
        return regression_output