# training_metrics.py
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import os

# Create dummy dataset (replace with your real one)
X_train = torch.randn(500, 10)
y_train = torch.randint(0, 8, (500,))
X_val = torch.randn(100, 10)
y_val = torch.randint(0, 8, (100,))
train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=32, shuffle=True)
val_loader = DataLoader(TensorDataset(X_val, y_val), batch_size=32)

class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self)._init_()
        self.model = nn.Sequential(
            nn.Linear(10, 64),
            nn.ReLU(),
            nn.Linear(64, 8)
        )

    def forward(self, x):
        return self.model(x)

def train_and_save_plots():
    model = SimpleNN()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    num_epochs = 50
    train_loss = []
    val_loss = []
    train_accuracy = []
    val_accuracy = []
    precision_scores = []
    recall_scores = []
    f1_scores = []

    for epoch in range(num_epochs):
        model.train()
        epoch_train_loss, all_preds, all_labels = 0, [], []

        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            epoch_train_loss += loss.item()
            preds = torch.argmax(outputs, dim=1)
            all_preds += preds.tolist()
            all_labels += labels.tolist()

        train_loss.append(epoch_train_loss / len(train_loader))
        train_accuracy.append(accuracy_score(all_labels, all_preds))

        model.eval()
        val_preds, val_labels = [], []
        val_epoch_loss = 0

        with torch.no_grad():
            for inputs, labels in val_loader:
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                val_epoch_loss += loss.item()
                preds = torch.argmax(outputs, dim=1)
                val_preds += preds.tolist()
                val_labels += labels.tolist()

        val_loss.append(val_epoch_loss / len(val_loader))
        val_accuracy.append(accuracy_score(val_labels, val_preds))
        precision_scores.append(precision_score(val_labels, val_preds, average='macro', zero_division=0))
        recall_scores.append(recall_score(val_labels, val_preds, average='macro', zero_division=0))
        f1_scores.append(f1_score(val_labels, val_preds, average='macro', zero_division=0))

    # Save plots to static folder
    os.makedirs("static/plots", exist_ok=True)
    x = range(num_epochs)

    # Loss Plot
    plt.figure()
    plt.plot(x, train_loss, label="Train Loss")
    plt.plot(x, val_loss, label="Val Loss")
    plt.title("Loss")
    plt.legend()
    plt.savefig("static/plots/loss.png")
    plt.close()

    # Accuracy Plot
    plt.figure()
    plt.plot(x, train_accuracy, label="Train Accuracy")
    plt.plot(x, val_accuracy, label="Val Accuracy")
    plt.title("Accuracy")
    plt.legend()
    plt.savefig("static/plots/accuracy.png")
    plt.close()

    # Precision/Recall/F1 Plot
    plt.figure()
    plt.plot(x, precision_scores, label="Precision")
    plt.plot(x, recall_scores, label="Recall")
    plt.plot(x, f1_scores, label="F1 Score")
    plt.title("Precision / Recall / F1")
    plt.legend()
    plt.savefig("static/plots/metrics.png")
    plt.close()
