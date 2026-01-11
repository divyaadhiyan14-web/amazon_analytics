import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def seasonality(df):
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["month"] = df["order_date"].dt.month
    df["year"] = df["order_date"].dt.year

    pivot = df.pivot_table(values="final_amount_inr",
                           index="month",
                           columns="year",
                           aggfunc="sum")

    plt.figure(figsize=(14,7))
    sns.heatmap(pivot, cmap="YlOrRd")
    plt.title("Monthly Sales Heatmap")
    plt.savefig("eda_outputs/seasonality_heatmap.png")
    plt.close()
