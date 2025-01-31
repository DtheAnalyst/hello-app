import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Simple Data Dashboard")

# File Upload
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Data Preview")
    st.write(df.head())

    st.subheader('Data Summary')
    st.write(df.describe())

    # Filter Data
    st.subheader('Filter Data')
    columns = df.columns.tolist()
    
    selected_column = st.selectbox("Select column to filter by", columns)
    unique_values = df[selected_column].dropna().unique()
    selected_values = st.multiselect("Select values (multiple allowed)", unique_values)

    # Apply filter only if values are selected
    if selected_values:
        filtered_df = df[df[selected_column].isin(selected_values)]
    else:
        filtered_df = df  # Use full dataset if no filter applied

    st.write(filtered_df)

    # Identify numeric columns for y-axis selection
    numeric_columns = filtered_df.select_dtypes(include=['number']).columns.tolist()

    st.subheader("Plot Data")

    # X-axis: Can be categorical or numeric
    x_column = st.selectbox("Select x-axis column", columns)

    # Y-axis: Should be numeric
    if numeric_columns:
        y_column = st.selectbox("Select y-axis column", numeric_columns)
    else:
        st.error("No numeric columns available for plotting.")
        y_column = None

    if st.button("Generate Plot") and y_column:
        try:
            # Ensure x_column and y_column are properly formatted
            if pd.api.types.is_numeric_dtype(filtered_df[x_column]):
                x_data = filtered_df[x_column]
            else:
                x_data = filtered_df[x_column].astype(str)  # Convert categorical to string

            y_data = pd.to_numeric(filtered_df[y_column], errors='coerce')

            fig, ax = plt.subplots()
            ax.plot(x_data, y_data, marker='o', linestyle='-')
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            ax.set_title(f"{y_column} vs {x_column}")
            plt.xticks(rotation=45)  # Rotate labels if needed
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Error generating plot: {e}")

else:
    st.write("Waiting for file upload...")
