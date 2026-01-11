import pandas as pd
import matplotlib.pyplot as plt

def revenue_trend(df):
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["year"] = df["order_date"].dt.year

    yearly = df.groupby("year")["final_amount_inr"].sum().reset_index()

    yearly["growth_%"] = yearly["final_amount_inr"].pct_change() * 100

    plt.figure(figsize=(12,6))
    plt.plot(yearly["year"], yearly["final_amount_inr"], marker="o")
    plt.title("Amazon India Revenue Trend (2015–2025)")
    plt.xlabel("Year")
    plt.ylabel("Revenue (INR)")
    plt.grid(True)

    for i in range(1, len(yearly)):
        plt.text(yearly["year"][i], yearly["final_amount_inr"][i],
                 f"{yearly['growth_%'][i]:.1f}%", fontsize=9)

    plt.savefig("eda_outputs/revenue_trend.png")
    plt.close()
