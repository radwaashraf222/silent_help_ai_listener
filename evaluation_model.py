import pandas as pd
from arabert_model import predict

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

import matplotlib.pyplot as plt
import seaborn as sns

# on dataset 
df = pd.read_csv("data/dataset_20k_clean (2).csv")

y_true = []
y_pred = []

for _, row in df.iterrows():
    text = str(row["text"])
    true_label = int(row["label"])

    predicted_label, confidence = predict(text)

    y_true.append(true_label)
    y_pred.append(predicted_label)

# Metrics
acc = accuracy_score(y_true, y_pred)
prec = precision_score(y_true, y_pred)
rec = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

print("\n📊 === Evaluation Results ===")
print(f"Accuracy  = {acc:.4f} ({acc*100:.2f}%)")
print(f"Precision = {prec:.4f} ({prec*100:.2f}%)")
print(f"Recall    = {rec:.4f} ({rec*100:.2f}%)")
print(f"F1 Score  = {f1:.4f} ({f1*100:.2f}%)")

print("\n📋 Classification Report:\n")
print(classification_report(y_true, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_true, y_pred)

plt.figure(figsize=(6,5))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    xticklabels=["Safe", "Danger"],
    yticklabels=["Safe", "Danger"]
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("AraBERT Confusion Matrix")

plt.savefig("arabert_confusion_matrix.png")
plt.show()

