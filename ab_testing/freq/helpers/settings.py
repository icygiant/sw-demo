import seaborn as sns
import matplotlib.pyplot as plt

def apply_settings():

    sns.set_theme(
        style="darkgrid",
        palette="magma"
    )

    plt.rcParams.update({
        "axes.titlesize": 18,
        "axes.labelsize": 14,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "legend.fontsize": 12,
        "figure.titlesize": 20,
    })

    custom_palette = ["#4E79A7", "#F28E2B"]
    sns.set_palette(custom_palette)

if __name__ == "__main__":
    apply_settings()
