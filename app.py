import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import fastf1

# Page settings
st.set_page_config(
    page_title="F1 Race Analysis",
    page_icon="🏎️",
    layout="wide"
)

st.title("🏎️ Formula 1 Race Analysis")
st.write("Select a Grand Prix to see the driver points.")

# FastF1 cache
@st.cache_data
def get_race_data():

    # Get 2025 event schedule
    schedule = fastf1.get_event_schedule(2025)

    # Race names
    races = schedule["EventName"].tolist()

    final = pd.DataFrame(
        columns=[
            "TeamName",
            "FullName",
            "Position",
            "Time",
            "Status",
            "Points",
            "Laps",
            "Venue"
        ]
    )

    # Get race results
    for race in races:

        try:
            session = fastf1.get_session(2025, race, "R")
            session.load()

            results = session.results

            results = results[
                [
                    "TeamName",
                    "FullName",
                    "Position",
                    "Time",
                    "Status",
                    "Points",
                    "Laps"
                ]
            ].copy()

            results["Venue"] = race

            final = pd.concat(
                [final, results],
                ignore_index=True
            )

        except Exception as error:
            st.warning(f"Could not load {race}")

    return final


# Load data
with st.spinner("Loading F1 race data..."):
    final = get_race_data()


# Check if data exists
if not final.empty:

    # Dropdown
    venues = final["Venue"].unique()

    selected_venue = st.selectbox(
        "🏁 Select Grand Prix",
        venues
    )

    # Filter selected race
    p = final[final["Venue"] == selected_venue].copy()

    # Sort by points
    p = p.sort_values("Points", ascending=False)

    st.subheader(f"🏆 {selected_venue}")

    # Display results
    st.dataframe(
        p[
            [
                "FullName",
                "TeamName",
                "Position",
                "Points",
                "Laps",
                "Status"
            ]
        ],
        use_container_width=True
    )

    # Bar chart
    st.subheader("Driver Points")

    fig, ax = plt.subplots(figsize=(12, 6))

    sb.barplot(
        data=p,
        x="FullName",
        y="Points",
        ax=ax
    )

    ax.set_xlabel("Driver")
    ax.set_ylabel("Points")
    ax.tick_params(axis="x", rotation=90)

    plt.tight_layout()

    st.pyplot(fig)

else:
    st.error("No race data found.")
