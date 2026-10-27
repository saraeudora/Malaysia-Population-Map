
import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np


# Generate sample population and GDP data
def generate_data(min_population, max_population):
    states = [
        "Johor", "Kedah", "Kelantan", "Melaka",
        "Negeri Sembilan", "Pahang", "Penang", "Perak",
        "Perlis", "Sabah", "Sarawak", "Selangor",
        "Terengganu", "Kuala Lumpur", "Labuan", "Putrajaya"
    ]

    population = np.random.randint(
        min_population,
        max_population + 1,
        size=len(states)
    )

    gdp = np.random.randint(10000, 100000, size=len(states))

    return pd.DataFrame({
        "State": states,
        "Population": population,
        "GDP": gdp
    })


# Load Malaysia map from the same folder as this script
@st.cache_data
def load_map():
    return gpd.read_file("my.json")


# Plot the choropleth map
def plot_map(malaysia_map, data, selected_metric, selected_color):
    m = folium.Map(
        location=[4.2105, 101.9758],
        zoom_start=6
    )

    folium.Choropleth(
        geo_data=malaysia_map.__geo_interface__,
        name=f"{selected_metric} Distribution",
        data=data,
        columns=["State", selected_metric],
        key_on="feature.properties.name",
        fill_color=selected_color,
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f"{selected_metric} Distribution",
        nan_fill_color="lightgrey"
    ).add_to(m)

    folium.LayerControl().add_to(m)

    return m


# Main Streamlit application
def main():
    st.title("Malaysia Population and GDP Distribution Map")

    st.write(
        "Explore how different data values and colour schemes "
        "affect the map of Malaysia."
    )

    # Sidebar settings
    st.sidebar.header("Map Settings")

    min_population = st.sidebar.number_input(
        "Minimum population",
        min_value=1,
        max_value=10000000,
        value=1000000,
        step=500000
    )

    max_population = st.sidebar.number_input(
        "Maximum population",
        min_value=2,
        max_value=20000000,
        value=10000000,
        step=500000
    )

    if min_population >= max_population:
        st.error("Maximum population must be greater than minimum.")
        return

    selected_metric = st.sidebar.selectbox(
        "Select dataset",
        ["Population", "GDP"]
    )

    selected_color = st.sidebar.selectbox(
        "Select map colour",
        ["YlOrRd", "BuGn", "Blues", "Greens"]
    )

    # Generate data
    if (
        "data" not in st.session_state
        or st.sidebar.button("Generate New Data")
    ):
        st.session_state["data"] = generate_data(
            int(min_population),
            int(max_population)
        )

    data = st.session_state["data"]

    # Display selected data
    st.subheader(f"Sample {selected_metric} Data")
    st.dataframe(
        data[["State", selected_metric]],
        use_container_width=True
    )

    # Display map
    try:
        malaysia_map = load_map()

        st.subheader(f"{selected_metric} Distribution Map")

        folium_map = plot_map(
            malaysia_map,
            data,
            selected_metric,
            selected_color
        )

        st_folium(
            folium_map,
            width=None,
            height=600,
            key="malaysia_map"
        )

    except Exception as e:
        st.error(f"Unable to load or display the map: {e}")
        st.info(
            "Ensure my.json is in the same folder as this script. "
            "The map's state names must match the State column, "
            "and its GeoJSON features must contain "
            "properties.name."
        )


if __name__ == "__main__":
    main()
