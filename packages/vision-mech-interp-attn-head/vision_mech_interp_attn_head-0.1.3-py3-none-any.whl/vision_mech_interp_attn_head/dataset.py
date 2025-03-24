import os
from torch.utils.data import Dataset
from torchvision import transforms
from PIL import Image
import torch

class SpectrogramDataset(Dataset):
    def __init__(self, data_dir, indices, labels, transform=None):
        self.data_dir = data_dir
        self.indices = indices
        self.labels = labels
        self.transform = transform or transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, idx):
        actual_idx = self.indices[idx]
        img_path = os.path.join(self.data_dir, f"spectrogram_{actual_idx + 1}.png")
        try:
            img = Image.open(img_path).convert("RGB")  # Convert to RGB (ViT expects 3 channels)
            img = self.transform(img)  # Apply transform to convert to tensor
            label = torch.tensor(self.labels[actual_idx], dtype=torch.float32)
            return img, label
        except Exception as e:
            print(f"Error loading image {img_path}: {e}")
            # Return a dummy image and label
            dummy_img = torch.zeros(3, 224, 224)
            dummy_label = torch.zeros(3)
            return dummy_img, dummy_label