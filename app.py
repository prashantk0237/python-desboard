from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

import os

print("Current Directory:", os.getcwd())
print("Files:", os.listdir())
print("Data Folder Exists:", os.path.exists("data"))


from pathlib import Path

csv_path = Path("data") / "shopify_sales_dataset_ml_eda_clean.csv"

print("CSV Exists:", csv_path.exists())

df = pd.read_csv(csv_path)

# Load Data
#df = pd.read_csv("data\shopify_sales_dataset_ml_eda_clean.csv")

df["order_date"] = pd.to_datetime(df["order_date"])

# KPIs
total_revenue = round(df["revenue"].sum(), 2)
total_profit = round(df["profit"].sum(), 2)
total_orders = df["order_id"].nunique()
total_customers = df["customer_id"].nunique()

# Monthly Revenue
monthly_revenue = (
    df.groupby(["order_year", "order_month"])["revenue"]
    .sum()
    .reset_index()
)

month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

monthly_revenue["order_month"] = pd.Categorical(
    monthly_revenue["order_month"],
    categories=month_order,
    ordered=True
)

monthly_revenue = monthly_revenue.sort_values(
    ["order_year", "order_month"]
)

fig_monthly = px.line(
    monthly_revenue,
    x="order_month",
    y="revenue",
    color="order_year",
    markers=True,
    title="Monthly Revenue Trend"
)

fig_category = px.bar(
    df.groupby("product_category")["revenue"]
      .sum()
      .reset_index(),
    x="product_category",
    y="revenue",
    title="Revenue by Category"
)

fig_country = px.bar(
    df.groupby("customer_country")["revenue"]
      .sum()
      .reset_index(),
    x="customer_country",
    y="revenue",
    title="Revenue by Country"
)


fig_country = px.bar(
    df.groupby("customer_country")["revenue"]
      .sum()
      .reset_index(),
    x="customer_country",
    y="revenue",
    title="Revenue by Country"
)


app = Dash(__name__)
server = app.server

app.layout = html.Div([

    # Header
    html.Div([
        html.H1("📊 Shopify Sales Dashboard", className="dashboard-title"),
        html.P(
            "Revenue • Profit • Customer • Product Analytics",
            className="dashboard-subtitle"
        )
    ], className="header"),

    # KPI Cards
    html.Div([

        html.Div([
            html.P("💰 Total Revenue", className="kpi-label"),
            html.H2(f"${total_revenue:,.0f}", className="kpi-value")
        ], className="card revenue"),

        html.Div([
            html.P("📈 Total Profit", className="kpi-label"),
            html.H2(f"${total_profit:,.0f}", className="kpi-value")
        ], className="card profit"),

        html.Div([
            html.P("🛒 Total Orders", className="kpi-label"),
            html.H2(f"{total_orders:,}", className="kpi-value")
        ], className="card orders"),

        html.Div([
            html.P("👥 Customers", className="kpi-label"),
            html.H2(f"{total_customers:,}", className="kpi-value")
        ], className="card customers"),

    ], className="kpi-row"),

    # Charts Row 1
    html.Div([

        html.Div([
            dcc.Graph(
                figure=fig_monthly,
                config={"displayModeBar": False}
            )
        ], className="graph-card"),

        html.Div([
            dcc.Graph(
                figure=fig_category,
                config={"displayModeBar": False}
            )
        ], className="graph-card")

    ], className="graph-row"),
    html.Div([
            dcc.Graph(
                figure=fig_country,
                config={"displayModeBar": False}
            )
        ], className="graph-card"),
    html.Div([
            dcc.Graph(
                figure=fig_country,
                config={"displayModeBar": False}
            )
        ], className="graph-card")
     
    

], className="main-container")
if __name__ == "__main__":
    app.run(debug=True)