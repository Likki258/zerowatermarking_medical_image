import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

RESULTS_DIR = "../results"
robust_path = os.path.join(RESULTS_DIR, "per_image_robustness.csv")
disc_path = os.path.join(RESULTS_DIR, "discrimination_scores.csv")
pairs_path = os.path.join(RESULTS_DIR, "similarity_pairs.csv")

print("\nLoading evaluation CSV files...")

robust_df = pd.read_csv(robust_path)
disc_df = pd.read_csv(disc_path)
pairs_df = pd.read_csv(pairs_path)

print("Files loaded successfully 👍\n")

print("Detected columns in robustness file:")
print(list(robust_df.columns))

# ---- AUTO MAP COLUMN NAMES ----
IMAGE_COLS = ["image", "image_id", "filename"]
ROBUST_COLS = ["mean_robustness", "avg_robustness", "robustness"]

image_col = next((c for c in IMAGE_COLS if c in robust_df.columns), None)
robust_col = next((c for c in ROBUST_COLS if c in robust_df.columns), None)

if image_col is None or robust_col is None:
    raise ValueError("\n❌ Could not detect column names.\n"
                     "Open CSV and confirm column headers.\n")

robust_df = robust_df[[image_col, robust_col]]
robust_df.columns = ["image", "robustness"]

print("\nMapped column names -> OK")
print(robust_df.head())

# ==============================
# 1️⃣ ROBUSTNESS BAR GRAPH
# ==============================
plt.figure(figsize=(14,6))
sns.barplot(
    x="image",
    y="robustness",
    data=robust_df.sort_values("robustness", ascending=False).head(25)
)
plt.xticks(rotation=90)
plt.title("Top 25 Most Robust Medical Images")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "graph_top_robust_images.png"))
print("Saved: graph_top_robust_images.png")

# ==============================
# 2️⃣ HAMMING DISTANCE DISTRIBUTION
# ==============================
plt.figure(figsize=(10,5))
sns.histplot(pairs_df["hamming_distance"], bins=40)
plt.title("Hamming Distance Distribution")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "graph_hamming_distribution.png"))
print("Saved: graph_hamming_distribution.png")

# ==============================
# 3️⃣ ROBUST vs DIFFERENT IMAGE SCORE COMPARISON
# ==============================
plt.figure(figsize=(10,5))
sns.boxplot(
    x="pair_type",
    y="similarity",
    data=pairs_df.replace({"same-image": "Robustness", "diff-image": "Discrimination"})
)

plt.title("Robustness vs Discrimination Similarity Scores")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "graph_robust_vs_discrimination.png"))
print("Saved: graph_robust_vs_discrimination.png")

print("\n🎯 Research graphs generated successfully\n")