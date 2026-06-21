import plotly.express as px

def sales_trend_chart(df):

    fig = px.line(
        df,
        x="Order Date",
        y="Sales",
        title="Sales Trend"
    )

    return fig