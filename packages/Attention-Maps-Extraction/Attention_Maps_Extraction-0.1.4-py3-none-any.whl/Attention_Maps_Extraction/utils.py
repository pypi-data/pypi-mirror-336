import os
import pandas as pd
from torch.utils.data import DataLoader
from torchvision import transforms
from .dataset import SpectrogramDataset

def load_data(data_dir, csv_path, transform=None):
    df = pd.read_csv(csv_path)
    labels = df[["Chirp_Start_Time", "Chirp_Start_Freq", "Chirp_End_Freq"]].values
    indices = df.index.values
    dataset = SpectrogramDataset(data_dir, indices, labels, transform=transform)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=False)
    return dataloader