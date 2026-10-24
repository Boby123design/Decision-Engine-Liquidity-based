import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

# Apne banaye hue custom modules import karna
from dataset_loader import ForexDataset, transform, csv_file
from model_architecture import ForexMultiModalModel

# 1. Hyperparameters Setup
EPOCHS = 10         # Model 10 baar poore dataset ko dekhega
BATCH_SIZE = 4      # Ek baar mein 4 images process hongi (kyunki dataset 100 images ka hai)
LEARNING_RATE = 0.001

# Agar aapke paas NVIDIA GPU (CUDA) hai toh training fast hogi, warna CPU use hoga
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🚀 Training start ho rahi hai on: {device}")

# 2. Data Loaders aur Model initialize karna
dataset = ForexDataset(csv_file=csv_file, transform=transform)
dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

model = ForexMultiModalModel().to(device)
criterion = nn.CrossEntropyLoss() # Multi-class classification ke liye best loss function
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

print("\nModel seekhna shuru kar raha hai...\n")

# 3. Training Loop
for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0
    correct_predictions = 0
    total_predictions = 0
    
    for images, tabular, labels in dataloader:
        # Data ko RAM se CPU/GPU par bhejna
        images = images.to(device)
        tabular = tabular.to(device)
        labels = labels.to(device)
        
        # A. Forward Pass (Model ne predict kiya)
        outputs = model(images, tabular)
        loss = criterion(outputs, labels)
        
        # B. Backward Pass (Model ne apni galti sudhari)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        # C. Statistics calculate karna
        running_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        total_predictions += labels.size(0)
        correct_predictions += (predicted == labels).sum().item()
        
    # Har epoch ke baad update dena
    epoch_loss = running_loss / len(dataloader)
    epoch_acc = (correct_predictions / total_predictions) * 100
    
    print(f"Epoch [{epoch+1}/{EPOCHS}] -> Loss: {epoch_loss:.4f} | Accuracy: {epoch_acc:.2f}%")

# 4. Model save karna (Taaki baad mein platform ke liye use kar sakein)
save_path = r"C:\Models\Model_7\forex_model.pth"
torch.save(model.state_dict(), save_path)
print(f"\n✅ Training Complete! Trained model yahan save ho gaya hai: {save_path}")