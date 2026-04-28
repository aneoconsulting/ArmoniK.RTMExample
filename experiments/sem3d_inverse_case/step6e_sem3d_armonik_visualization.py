import os
import pandas as pd
import matplotlib.pyplot as plt


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")

csv_path = os.path.join(RESULTS_DIR, "sem3d_armonik_trace_misfits.csv")

top10_plot_path = os.path.join(RESULTS_DIR, "sem3d_top10_station_misfit.png")
distribution_plot_path = os.path.join(RESULTS_DIR, "sem3d_misfit_distribution.png")
summary_plot_path = os.path.join(RESULTS_DIR, "sem3d_armonik_misfit_summary.png")


def main():
    print("Reading:", csv_path)

    df = pd.read_csv(csv_path)
    df = df[df["status"] == "OK"].copy()
    df["misfit"] = pd.to_numeric(df["misfit"], errors="coerce")
    df = df.dropna(subset=["misfit"])
    df = df.sort_values("misfit")

    print(f"Number of valid traces = {len(df)}")
    print("\nTop 10:")
    print(df.head(10))

    top10 = df.head(10).copy()
    top10["label"] = top10["h5_file"] + " | " + top10["station"]

    plt.figure(figsize=(10, 6))
    plt.barh(top10["label"], top10["misfit"])
    plt.xlabel("Misfit")
    plt.ylabel("Station")
    plt.title("Top 10 closest SEM3D station traces")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(top10_plot_path, dpi=200)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.hist(df["misfit"], bins=30)
    plt.xlabel("Misfit")
    plt.ylabel("Number of station traces")
    plt.title("Distribution of SEM3D station misfits")
    plt.tight_layout()
    plt.savefig(distribution_plot_path, dpi=200)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(range(len(df)), df["misfit"].values, marker="o", linewidth=1)
    plt.xlabel("Station rank after sorting")
    plt.ylabel("Misfit")
    plt.title("Sorted SEM3D station misfits")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(summary_plot_path, dpi=200)
    plt.close()

    print("\nSaved plots:")
    print(top10_plot_path)
    print(distribution_plot_path)
    print(summary_plot_path)


if __name__ == "__main__":
    main()