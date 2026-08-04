from scipy import stats
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from database.repository import ReceiptRepository
import plotly.io as pio

pio.templates.default = "plotly_white"


def dashboard_page():

    st.title("📊 Dashboard")

    repo = ReceiptRepository()

    total_receipts = repo.get_total_receipts()
    total_amount = repo.get_total_amount()
    total_stores = repo.get_total_stores()
    total_items = repo.get_total_items()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container(border=True):
            st.metric(
                "Receipts",
                total_receipts
            )

    with col2:
        with st.container(border=True):
            st.metric(
                "Total Spent",
                f"₹ {total_amount:.2f}"
            )

    with col3:
        with st.container(border=True):
            st.metric(
                "Stores",
                total_stores
            )

    with col4:
        with st.container(border=True):
            st.metric(
                "Items",
                total_items
            )

    distribution = repo.get_receipt_type_distribution()
    top_stores = repo.get_top_stores()

    left, right = st.columns(2)

    # ==================================================
    # Receipt Type Distribution
    # ==================================================

    with left:
        with st.container(border=True):

            st.subheader("📊 Receipt Type Distribution")

            receipt_df = pd.DataFrame(
                distribution,
                columns=[
                    "Receipt Type",
                    "Count"
                ]
            )

            fig = px.pie(
                receipt_df,
                names="Receipt Type",
                values="Count",
                hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Set2
            )

            fig.update_layout(
                height=350,
                margin=dict(
                    l=20,
                    r=20,
                    t=30,
                    b=20
                )
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

    # ==================================================
    # Top Stores
    # ==================================================

    with right:
        with st.container(border=True):

            st.subheader("🏪 Top Stores")

            store_df = pd.DataFrame(
                top_stores,
                columns=[
                    "Store",
                    "Receipts",
                    "Total"
                ]
            )

            fig = px.bar(
                store_df,
                x="Receipts",
                y="Store",
                orientation="h",
                color="Receipts",
                color_continuous_scale="Blues"
            )

            fig.update_layout(
                height=350,
                showlegend=False,
                margin=dict(
                    l=20,
                    r=20,
                    t=30,
                    b=20
                ),
                yaxis=dict(
                    categoryorder="total ascending"
                )
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

    # ==================================================
    # Most Purchased Items
    # ==================================================
    most_purchased_items = repo.get_top_items()

    with left:

        with st.container(border=True):

            st.subheader("🛒 Most Purchased Items")

            item_df = pd.DataFrame(
                most_purchased_items,
                columns=[
                    "Item",
                    "Quantity"
                ]
            )

            fig = px.bar(
                item_df,
                x="Quantity",
                y="Item",
                orientation="h",
                color="Quantity",
                color_continuous_scale="Greens"
            )

            fig.update_layout(
                height=320,
                showlegend=False,
                margin=dict(
                    l=20,
                    r=20,
                    t=20,
                    b=20
                ),
                yaxis=dict(
                    categoryorder="total ascending"
                )
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

    # ==================================================
    # Monthly Spending
    # ==================================================
        
    monthly_spending = repo.get_monthly_spending()

    with right:

        with st.container(border=True):

            st.subheader("📅 Monthly Spending")

            monthly_df = pd.DataFrame(
                monthly_spending,
                columns=[
                    "Month",
                    "Amount"
                ]
            )

            fig = px.line(
                monthly_df,
                x="Month",
                y="Amount",
                markers=True
            )

            fig.update_layout(
                height=320,
                margin=dict(
                    l=20,
                    r=20,
                    t=20,
                    b=20
                )
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

    repo.close()