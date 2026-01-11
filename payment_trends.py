import pandas as pd
import matplotlib.pyplot as plt

def payment_trends(df):
    df["year"] = pd.to_datetime(df["order_date"]).dt.year
    pivot = df.pivot_table(values="final_amount_inr",
                           index="year",
                           columns="payment_method",
                           aggfunc="sum")

    pivot.plot(kind="area", stacked=True, figsize=(12,6))
    plt.title("Payment Method Evolution")
    plt.savefig("eda_outputs/payment_trends.png")
    plt.close()
