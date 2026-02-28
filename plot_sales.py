import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# --- Stub Data ---
def get_sales_data():
    """Returns stubbed recent sales data for the last 30 days."""
    base_date = datetime(2026, 1, 30)
    data = [
        {"date": base_date - timedelta(days=29), "product": "Laptops",     "revenue": 12400, "units": 31},
        {"date": base_date - timedelta(days=26), "product": "Monitors",    "revenue":  8200, "units": 41},
        {"date": base_date - timedelta(days=24), "product": "Laptops",     "revenue": 15600, "units": 39},
        {"date": base_date - timedelta(days=22), "product": "Keyboards",   "revenue":  3100, "units": 62},
        {"date": base_date - timedelta(days=20), "product": "Monitors",    "revenue":  9800, "units": 49},
        {"date": base_date - timedelta(days=18), "product": "Laptops",     "revenue": 18200, "units": 46},
        {"date": base_date - timedelta(days=15), "product": "Keyboards",   "revenue":  4500, "units": 90},
        {"date": base_date - timedelta(days=13), "product": "Monitors",    "revenue": 11300, "units": 57},
        {"date": base_date - timedelta(days=11), "product": "Laptops",     "revenue": 21000, "units": 53},
        {"date": base_date - timedelta(days=9),  "product": "Keyboards",   "revenue":  5200, "units": 104},
        {"date": base_date - timedelta(days=7),  "product": "Monitors",    "revenue": 13700, "units": 69},
        {"date": base_date - timedelta(days=5),  "product": "Laptops",     "revenue": 19500, "units": 49},
        {"date": base_date - timedelta(days=3),  "product": "Keyboards",   "revenue":  6100, "units": 122},
        {"date": base_date - timedelta(days=1),  "product": "Monitors",    "revenue": 15200, "units": 76},
        {"date": base_date,                      "product": "Laptops",     "revenue": 23800, "units": 60},
    ]
    return data


def group_by_product(data):
    """Groups data by product, returning sorted dates, revenues, and units."""
    products = {}
    for row in data:
        p = row["product"]
        if p not in products:
            products[p] = {"dates": [], "revenue": [], "units": []}
        products[p]["dates"].append(row["date"])
        products[p]["revenue"].append(row["revenue"])
        products[p]["units"].append(row["units"])
    return products


def plot_sales(data):
    products = group_by_product(data)
    colors = {"Laptops": "#4C72B0", "Monitors": "#DD8452", "Keyboards": "#55A868"}

    fig, axes = plt.subplots(2, 1, figsize=(12, 9), sharex=True)
    fig.suptitle("Recent Sales Data — Last 30 Days", fontsize=16, fontweight="bold", y=0.98)

    # --- Top chart: Revenue ---
    ax1 = axes[0]
    for product, series in products.items():
        ax1.plot(
            series["dates"], series["revenue"],
            marker="o", linewidth=2, markersize=6,
            color=colors.get(product), label=product,
        )
    ax1.set_ylabel("Revenue (USD)", fontsize=12)
    ax1.set_title("Revenue by Product", fontsize=13)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax1.legend(title="Product", fontsize=10)
    ax1.grid(True, linestyle="--", alpha=0.5)

    # --- Bottom chart: Units Sold ---
    ax2 = axes[1]
    for product, series in products.items():
        ax2.bar(
            series["dates"], series["units"],
            width=1.5, color=colors.get(product), label=product, alpha=0.8,
        )
    ax2.set_ylabel("Units Sold", fontsize=12)
    ax2.set_title("Units Sold by Product", fontsize=13)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax2.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    ax2.legend(title="Product", fontsize=10)
    ax2.grid(True, linestyle="--", alpha=0.5, axis="y")

    fig.autofmt_xdate(rotation=30)
    plt.tight_layout()
    plt.savefig("sales_plot.png", dpi=150, bbox_inches="tight")
    print("Plot saved to sales_plot.png")
    plt.show()


if __name__ == "__main__":
    sales_data = get_sales_data()
    plot_sales(sales_data)
