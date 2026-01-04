import os
import pandas as pd
import numpy as np
from itertools import combinations
from pathlib import Path

HASH_CSV = "../hashes/hashes.csv"
RESULTS_DIR = "../results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def load_hashes():
    print("\nLoading hashes.csv ...")

    # CSV has no headers → assign manually
    df = pd.read_csv(HASH_CSV, header=None, names=["filename", "hash"])

    print(f"Total rows loaded = {len(df)}")

    # Drop empty / NaN
    df = df.dropna()

    # Ensure filename string
    df["filename"] = df["filename"].astype(str)

    # Convert scientific notation → integer hash
    df["hash"] = df["hash"].astype(str).apply(lambda x: int(float(x)))

    print(f"Valid rows after cleaning = {len(df)}")

    return df


def hamming_distance(h1, h2):
    return bin(h1 ^ h2).count("1") / 64.0


def get_base_name(name):
    """
    Extract unique image identity
    ORIG_xxxx   and   VAR_xxxx   belong to same family
    """

    parts = name.split("_")

    if len(parts) < 2:
        return name

    return parts[1]   # stable patient / scan id


def auto_analysis(df):
    records = []

    groups = {}

    # Group variations of same image
    for _, row in df.iterrows():
        fname = row["filename"]
        hid = row["hash"]

        base = get_base_name(fname)

        groups.setdefault(base, []).append((fname, hid))

    print(f"\nDetected {len(groups)} image groups\n")

    # ---- PER-IMAGE ROBUSTNESS ----
    print("Computing robustness within same-image variations...")

    per_image_scores = []

    for gid, items in groups.items():

        if len(items) < 2:
            continue

        pair_scores = []

        for (f1,h1),(f2,h2) in combinations(items,2):
            hd = hamming_distance(h1,h2)
            pair_scores.append(1-hd)

            records.append(["same-image", f1,f2,hd,1-hd])

        if pair_scores:
            per_image_scores.append([gid, np.mean(pair_scores)])

    df_robust = pd.DataFrame(per_image_scores,
        columns=["image_id","avg_robustness"])

    df_robust.to_csv(f"{RESULTS_DIR}/per_image_robustness.csv", index=False)


    # ---- DISCRIMINATION BETWEEN DIFFERENT IMAGES ----
    print("Computing discrimination across different images...")

    samples = list(groups.keys())
    diff_scores = []

    for i in range(len(samples)):
        for j in range(i+1,len(samples)):

            a = groups[samples[i]][0][1]
            b = groups[samples[j]][0][1]

            hd = hamming_distance(a,b)

            diff_scores.append(1-hd)

            records.append(["different-image",
                            groups[samples[i]][0][0],
                            groups[samples[j]][0][0],
                            hd,1-hd])

    df_diff = pd.DataFrame(diff_scores, columns=["similarity"])
    df_diff.to_csv(f"{RESULTS_DIR}/discrimination_scores.csv", index=False)


    # ---- MASTER REPORT ----
    df_all = pd.DataFrame(records,
        columns=[
            "pair_type",
            "image_A",
            "image_B",
            "hamming_distance",
            "similarity"
        ])

    df_all.to_csv(f"{RESULTS_DIR}/similarity_pairs.csv", index=False)

    print("\n✔ Auto-Analysis Completed")
    print(" Saved:")
    print("  → per_image_robustness.csv")
    print("  → discrimination_scores.csv")
    print("  → similarity_pairs.csv")


if __name__ == "__main__":
    df = load_hashes()
    auto_analysis(df)