import torch
import torch.nn as nn
import torchvision.models as models

class ForexMultiModalModel(nn.Module):
    def __init__(self, num_tabular_features=2, num_classes=3):
        super(ForexMultiModalModel, self).__init__()
        
        # 1. Vision Branch (Data Bus for Images)
        # Hum ResNet-18 use kar rahe hain
        self.cnn = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        # ResNet ki aakhri layer hata rahe hain, humein sirf features (512 numbers) chahiye
        self.cnn.fc = nn.Identity() 
        
        # 2. Tabular Branch (Control Bus for Text Data)
        # Trade_Type aur Type ko process karne ke liye chhota sa network
        self.tabular_fc = nn.Sequential(
            nn.Linear(num_tabular_features, 16),
            nn.ReLU(),
            nn.Linear(16, 16),
            nn.ReLU()
        )
        
        # 3. Fusion Branch (ALU - Combining both)
        # ResNet se 512 features + Tabular se 16 features = Total 528 features
        self.classifier = nn.Sequential(
            nn.Linear(512 + 16, 128),
            nn.ReLU(),
            nn.Dropout(0.3), # Model ko jyada ratne (overfit) se rokne ke liye
            nn.Linear(128, num_classes)
        )

    def forward(self, image, tabular):
        # A. Image se features nikalo
        img_features = self.cnn(image)
        
        # B. Tabular data se features nikalo
        tab_features = self.tabular_fc(tabular)
        
        # C. Dono features ko ek saath jod do (Concatenate)
        combined = torch.cat((img_features, tab_features), dim=1)
        
        # D. Final prediction (3 classes: CTC, SL, TP)
        output = self.classifier(combined)
        return output

# Test block: Check karne ke liye ki architecture sahi se kaam kar raha hai
if __name__ == "__main__":
    print("Model Architecture initialize ho raha hai...")
    
    # Model ko call karna
    model = ForexMultiModalModel()
    
    # Dummy data banakar model mein pass karna (Jaise DataLoader ne diya tha)
    dummy_images = torch.randn(4, 3, 224, 224) # 4 images ka ek batch
    dummy_tabular = torch.randn(4, 2)          # 4 tabular records ka batch
    
    # Model se output nikalna
    output = model(dummy_images, dummy_tabular)
    
    print("\n✅ Model Architecture Successfully Build!")
    print(f"Output Shape: {output.shape} -> (Batch_Size, Num_Classes)")
    print("Har image ke liye 3 raw scores (logits) generate ho rahe hain:")
    print(output)