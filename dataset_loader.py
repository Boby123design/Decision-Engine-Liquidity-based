import os
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
from sklearn.preprocessing import LabelEncoder

# 1. Paths Setup
base_dir = r"C:\Models\Model_7"
csv_file = os.path.join(base_dir, "cleaned_dataset.csv")

class ForexDataset(Dataset):
    def __init__(self, csv_file, transform=None):
        self.data = pd.read_csv(csv_file)
        self.transform = transform
        
        # 2. Text ko Numbers mein convert karna (Encoding)
        self.le_trade_type = LabelEncoder()
        self.le_type = LabelEncoder()
        self.le_result = LabelEncoder()
        
        # 'blind', 'good', 'best' -> 0, 1, 2
        self.data['Trade_Type_Enc'] = self.le_trade_type.fit_transform(self.data['Trade_Type'])
        # 'buy', 'sell' -> 0, 1
        self.data['Type_Enc'] = self.le_type.fit_transform(self.data['Type'])
        # 'tp', 'sl', 'ctc' -> 0, 1, 2
        self.data['Result_Enc'] = self.le_result.fit_transform(self.data['Result'])
        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        # A. Image Load aur Transform karna
        img_path = self.data.iloc[idx]['Image_Path']
        # Image ko RGB format mein open karna
        image = Image.open(img_path).convert('RGB') 
        
        if self.transform:
            image = self.transform(image)
            
        # B. Tabular Features aur Label Load karna
        tabular_features = torch.tensor([
            self.data.iloc[idx]['Trade_Type_Enc'],
            self.data.iloc[idx]['Type_Enc']
        ], dtype=torch.float32)
        
        label = torch.tensor(self.data.iloc[idx]['Result_Enc'], dtype=torch.long)
        
        return image, tabular_features, label

# 3. Image Transformations (Resize aur Normalize)
transform = transforms.Compose([
    transforms.Resize((224, 224)), # Standard CNN input size
    transforms.ToTensor(),         # Image ko PyTorch Tensor mein badalna
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# 4. Dataset aur DataLoader ko test karna
if __name__ == "__main__":
    print("Dataset Loader initialize ho raha hai...")
    dataset = ForexDataset(csv_file=csv_file, transform=transform)
    dataloader = DataLoader(dataset, batch_size=4, shuffle=True)
    
    # Ek batch nikaal kar check karte hain
    images, tabular, labels = next(iter(dataloader))
    
    print("\n✅ Dataset Successfully Loaded!")
    print(f"Images Batch Shape: {images.shape} -> (Batch_Size, Channels, Height, Width)")
    print(f"Tabular Features Shape: {tabular.shape} -> (Batch_Size, Num_Features)")
    print(f"Labels Batch: {labels} -> 0/1/2 for CTC/SL/TP (alphabetical order)")
    
    # Mapping dikhana taaki future mein condition lagane mein aasaani ho
    print("\nEncoding Mapping:")
    print("Result Map:", dict(zip(dataset.le_result.classes_, dataset.le_result.transform(dataset.le_result.classes_))))