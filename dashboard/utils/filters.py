import streamlit as st


def sidebar_filters(df):

    st.sidebar.title("Dashboard Filters")

    # Country
    countries = sorted(df["Country"].unique())

    selected_country = st.sidebar.multiselect(
        "Country",
        countries,
        default=countries
    )

    # Category
    categories = sorted(df["Category"].unique())

    selected_category = st.sidebar.multiselect(
        "Category",
        categories,
        default=categories
    )

    # Sub Category
    subcategories = sorted(df["Sub_Category"].unique())

    selected_subcategory = st.sidebar.multiselect(
        "Sub Category",
        subcategories,
        default=subcategories
    )

    # Season
    seasons = sorted(df["Season"].unique())

    selected_season = st.sidebar.multiselect(
        "Season",
        seasons,
        default=seasons
    )

    # Apply Filters
    filtered_df = df[
        (df["Country"].isin(selected_country))
        &
        (df["Category"].isin(selected_category))
        &
        (df["Sub_Category"].isin(selected_subcategory))
        &
        (df["Season"].isin(selected_season))
    ]

    # Sidebar Summary
    st.sidebar.markdown("---")

    st.sidebar.subheader("Dataset Summary")

    st.sidebar.write(f"Rows: {len(filtered_df):,}")
    st.sidebar.write(f"Countries: {filtered_df['Country'].nunique()}")
    st.sidebar.write(f"Products: {filtered_df['Product_Name'].nunique()}")
    st.sidebar.write(f"Categories: {filtered_df['Category'].nunique()}")

    # Download Button
    csv = filtered_df.to_csv(index=False)

    st.sidebar.download_button(
        label="📥 Download Filtered Data",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv"
    )

    # Reset Button
    if st.sidebar.button("🔄 Reset Filters"):
        st.rerun()

    return filtered_df