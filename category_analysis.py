import matplotlib.pyplot as plt

def category_analysis(df):
    category_rev = df.groupby("category")["final_amount_inr"].sum()

    category_rev.sort_values().plot(kind="barh", figsize=(10,6))
    plt.title("Revenue by Category")
    plt.savefig("eda_outputs/category_revenue.png")
    plt.close()
