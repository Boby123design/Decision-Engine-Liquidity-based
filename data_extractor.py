import os
import re
import pandas as pd
import openpyxl

# 1. Paths setup
base_dir = r"C:\Models\Model_7"
excel_file = os.path.join(base_dir, "model_7 dataset.xlsx")
image_folder = os.path.join(base_dir, "dataset_images")
csv_output = os.path.join(base_dir, "cleaned_dataset.csv")

print("Data aur Images ko map kiya ja raha hai, please wait...")

try:
    # 2. Excel se Text Data Read karna (Columns B, C, D)
    # Header row 1 mein hai, data row 2 se start hota hai
    df = pd.read_excel(excel_file, usecols="B:D", names=["Trade_Type", "Result", "Type"])
    df = df.dropna(how='all') # Khali rows ko hata dena

    # 3. Images ko read aur sort karna
    # Taaki image1 pehli row ke saath map ho, image2 doosri ke saath
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.emf', '.wmf'))]
    
    def extract_number(filename):
        match = re.search(r'\d+', filename)
        return int(match.group()) if match else 0
        
    image_files.sort(key=extract_number)

    print(f"Excel mein total valid rows: {len(df)}")
    print(f"Folder mein total images: {len(image_files)}")

    # 4. Data ko combine karke CSV banana
    combined_data = []
    # Hum utni hi rows banayenge jitni images aur text match hote hain
    for i in range(min(len(df), len(image_files))):
        row_data = df.iloc[i].to_dict()
        # Image ka poora path add karna
        row_data["Image_Path"] = os.path.join(image_folder, image_files[i])
        combined_data.append(row_data)

    # DataFrame banakar columns ko arrange karna
    final_df = pd.DataFrame(combined_data)
    final_df = final_df[["Image_Path", "Trade_Type", "Result", "Type"]]
    
    # Text ko lowercase mein convert karna taaki model confuse na ho
    final_df["Trade_Type"] = final_df["Trade_Type"].astype(str).str.strip().str.lower()
    final_df["Result"] = final_df["Result"].astype(str).str.strip().str.lower()
    final_df["Type"] = final_df["Type"].astype(str).str.strip().str.lower()

    final_df.to_csv(csv_output, index=False)
    print(f"✅ Success! Data perfectly map ho gaya hai aur '{csv_output}' ready hai.")

except Exception as e:
    print(f"❌ Error aaya hai: {e}")