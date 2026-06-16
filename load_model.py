import zipfile

with zipfile.ZipFile("arabert_trained.zip", "r") as zip_ref:
    zip_ref.extractall("arabert_trained")

print("Model extracted successfully!")