import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="F1 2025 Analytics Dashboard",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: white;
        color: black;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111116;
        border-right: 1px solid #29292f;
    }

    /* Main title */
    .main-title {
        font-size: 48px;
        font-weight: 800;
        color: #e10600;
        margin-bottom: 0px;
    }

    .subtitle {
        color: #b8b8bd;
        font-size: 18px;
        margin-bottom: 30px;
    }

    /* KPI cards */
    .metric-card {
        background: linear-gradient(135deg, #17171d, #0f0f13);
        border: 1px solid #292930;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.25);
    }

    .metric-title {
        color: #a6a6ad;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .metric-value {
        color: black;
        font-size: 30px;
        font-weight: 700;
    }

    /* Section headings */
    h2, h3 {
        color: black !important;
    }

    /* Divider */
    hr {
        border-color: #2a2a30;
    }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("F1_2025_GP.csv")

    # Remove unwanted index column
    if "Unnamed: 0" in df.columns:
        df = df.drop("Unnamed: 0", axis=1)

    # Rename driver
    df["FullName"] = df["FullName"].replace(
        "Andrea Kimi Antonelli",
        "Kimi Antonelli"
    )

    return df


df = load_data()


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">🏎️ F1 2025 ANALYTICS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Formula 1 Season Performance & Championship Dashboard</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.title("🏁 Dashboard Controls")

st.sidebar.markdown("---")

drivers = sorted(df["FullName"].dropna().unique())
teams = sorted(df["TeamName"].dropna().unique())
venues = sorted(df["Venue"].dropna().unique())

selected_team = st.sidebar.selectbox(
    "Select Team",
    ["All Teams"] + teams
)

selected_venue = st.sidebar.selectbox(
    "Select Grand Prix",
    ["All Races"] + venues
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Use the controls above to explore the 2025 F1 season."
)


# ---------------------------------------------------------
# FILTER DATA
# ---------------------------------------------------------

filtered_df = df.copy()

if selected_team != "All Teams":
    filtered_df = filtered_df[
        filtered_df["TeamName"] == selected_team
    ]

if selected_venue != "All Races":
    filtered_df = filtered_df[
        filtered_df["Venue"] == selected_venue
    ]


# ---------------------------------------------------------
# KPI SECTION
# ---------------------------------------------------------

total_points = filtered_df["Points"].sum()
total_laps = filtered_df["Laps"].sum()
total_drivers = filtered_df["FullName"].nunique()
total_teams = filtered_df["TeamName"].nunique()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Total Points</div>
            <div class="metric-value">{total_points:.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Total Laps</div>
            <div class="metric-value">{total_laps:.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Drivers</div>
            <div class="metric-value">{total_drivers}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Teams</div>
            <div class="metric-value">{total_teams}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("---")


# =========================================================
# CHAMPIONSHIP STANDINGS
# =========================================================

st.header("🏆 Championship Standings")

col1, col2 = st.columns(2)


# ---------------------------------------------------------
# DRIVER STANDINGS
# ---------------------------------------------------------

with col1:

    driver_points = (
        filtered_df
        .groupby("FullName")["Points"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    driver_points.columns = ["Driver", "Points"]

    fig, ax = plt.subplots(figsize=(10, 7))

    sns.barplot(
        data=driver_points,
        x="Points",
        y="Driver",
        palette="Reds_r",
        ax=ax
    )

    ax.set_title(
        "Driver Championship",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel("Points")
    ax.set_ylabel("")

    fig.patch.set_facecolor("#0b0b0f")
    ax.set_facecolor("#0b0b0f")

    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white")
    ax.title.set_color("white")

    for spine in ax.spines.values():
        spine.set_visible(False)

    st.pyplot(fig, use_container_width=True)


# ---------------------------------------------------------
# TEAM STANDINGS
# ---------------------------------------------------------

with col2:

    team_points = (
        filtered_df
        .groupby("TeamName")["Points"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    team_points.columns = ["Team", "Points"]

    fig, ax = plt.subplots(figsize=(10, 7))

    sns.barplot(
        data=team_points,
        x="Points",
        y="Team",
        palette="Reds_r",
        ax=ax
    )

    ax.set_title(
        "Constructor Championship",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel("Points")
    ax.set_ylabel("")

    fig.patch.set_facecolor("#0b0b0f")
    ax.set_facecolor("#0b0b0f")

    ax.tick_params(colors="white")

    for spine in ax.spines.values():
        spine.set_visible(False)

    st.pyplot(fig, use_container_width=True)


# =========================================================
# DRIVER VS DRIVER
# =========================================================

st.markdown("---")

st.header("⚔️ Driver vs Driver")

d1, d2 = st.columns(2)

with d1:
    driver1 = st.selectbox(
        "Driver 1",
        drivers,
        index=0
    )

with d2:
    driver2 = st.selectbox(
        "Driver 2",
        drivers,
        index=1 if len(drivers) > 1 else 0
    )


driver1_df = df[df["FullName"] == driver1]
driver2_df = df[df["FullName"] == driver2]


# ---------------------------------------------------------
# DRIVER KPIs
# ---------------------------------------------------------

p1 = driver1_df["Points"].sum()
p2 = driver2_df["Points"].sum()

avg1 = driver1_df["Position"].mean()
avg2 = driver2_df["Position"].mean()

x1, x2, x3, x4 = st.columns(4)

with x1:
    st.metric(
        f"{driver1} Points",
        f"{p1:.0f}"
    )

with x2:
    st.metric(
        f"{driver2} Points",
        f"{p2:.0f}"
    )

with x3:
    st.metric(
        f"{driver1} Avg Position",
        f"{avg1:.2f}"
    )

with x4:
    st.metric(
        f"{driver2} Avg Position",
        f"{avg2:.2f}"
    )


# ---------------------------------------------------------
# DRIVER POINTS GRAPH
# ---------------------------------------------------------

fig, ax = plt.subplots(figsize=(15, 6))

sns.lineplot(
    data=driver1_df,
    x="Venue",
    y="Points",
    marker="o",
    linewidth=3,
    color="#e10600",
    label=driver1,
    ax=ax
)

sns.lineplot(
    data=driver2_df,
    x="Venue",
    y="Points",
    marker="o",
    linewidth=3,
    color="#ffffff",
    label=driver2,
    ax=ax
)

ax.set_title(
    "Race-by-Race Points Comparison",
    fontsize=17,
    fontweight="bold"
)

ax.set_xlabel("Grand Prix")
ax.set_ylabel("Points")

plt.xticks(rotation=60)

fig.patch.set_facecolor("#0b0b0f")
ax.set_facecolor("#0b0b0f")

ax.tick_params(colors="white")

for spine in ax.spines.values():
    spine.set_visible(False)

legend = ax.legend()
legend.get_frame().set_facecolor("#17171d")
legend.get_frame().set_edgecolor("#292930")

st.pyplot(fig, use_container_width=True)


# =========================================================
# TEAM DRIVER COMPARISON
# =========================================================

st.markdown("---")

st.header("👥 Team Driver Performance")

selected_team_chart = st.selectbox(
    "Choose a team",
    teams,
    key="team_driver_chart"
)

team_df = df[df["TeamName"] == selected_team_chart]

team_driver_points = (
    team_df
    .groupby("FullName")["Points"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig, ax = plt.subplots(figsize=(12, 5))

sns.barplot(
    data=team_driver_points,
    x="FullName",
    y="Points",
    palette="Reds_r",
    ax=ax
)

ax.set_title(
    f"{selected_team_chart} - Driver Points",
    fontsize=16,
    fontweight="bold"
)

ax.set_xlabel("")
ax.set_ylabel("Points")

plt.xticks(rotation=30)

fig.patch.set_facecolor("#0b0b0f")
ax.set_facecolor("#0b0b0f")

ax.tick_params(colors="white")

for spine in ax.spines.values():
    spine.set_visible(False)

st.pyplot(fig, use_container_width=True)


# =========================================================
# POSITION ANALYSIS
# =========================================================

st.markdown("---")

st.header("📊 Race Position Analysis")

col1, col2 = st.columns(2)


# ---------------------------------------------------------
# POSITION DISTRIBUTION
# ---------------------------------------------------------

with col1:

    selected_driver_position = st.selectbox(
        "Select driver",
        drivers,
        key="position_driver"
    )

    pos_df = df[
        df["FullName"] == selected_driver_position
    ].copy()

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.histplot(
        pos_df["Position"],
        bins=10,
        kde=True,
        color="#e10600",
        ax=ax
    )

    ax.set_title(
        f"{selected_driver_position} - Finishing Position Distribution"
    )

    ax.set_xlabel("Finishing Position")
    ax.set_ylabel("Number of Races")

    fig.patch.set_facecolor("#0b0b0f")
    ax.set_facecolor("#0b0b0f")

    ax.tick_params(colors="white")

    st.pyplot(fig, use_container_width=True)


# ---------------------------------------------------------
# POSITION BY RACE
# ---------------------------------------------------------

with col2:

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.lineplot(
        data=pos_df,
        x="Venue",
        y="Position",
        marker="o",
        linewidth=3,
        color="#e10600",
        ax=ax
    )

    ax.invert_yaxis()

    ax.set_title(
        f"{selected_driver_position} - Finishing Positions"
    )

    ax.set_xlabel("Grand Prix")
    ax.set_ylabel("Position")

    plt.xticks(rotation=60)

    fig.patch.set_facecolor("#0b0b0f")
    ax.set_facecolor("#0b0b0f")

    ax.tick_params(colors="white")

    st.pyplot(fig, use_container_width=True)


# =========================================================
# RACE STATUS ANALYSIS
# =========================================================

st.markdown("---")

st.header("🏁 Race Status Analysis")

status_count = (
    filtered_df["Status"]
    .value_counts()
    .reset_index()
)

status_count.columns = ["Status", "Count"]


fig, ax = plt.subplots(figsize=(12, 5))

sns.barplot(
    data=status_count,
    x="Status",
    y="Count",
    palette="Reds_r",
    ax=ax
)

ax.set_title(
    "Race Finish / Status Distribution",
    fontsize=16,
    fontweight="bold"
)

ax.set_xlabel("")
ax.set_ylabel("Number of Entries")

plt.xticks(rotation=45)

fig.patch.set_facecolor("#0b0b0f")
ax.set_facecolor("#0b0b0f")

ax.tick_params(colors="white")

for spine in ax.spines.values():
    spine.set_visible(False)

st.pyplot(fig, use_container_width=True)


# =========================================================
# LAPS ANALYSIS
# =========================================================

st.markdown("---")

st.header("🔄 Lap Performance")

lap_df = (
    filtered_df
    .groupby("FullName")["Laps"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig, ax = plt.subplots(figsize=(12, 7))

sns.barplot(
    data=lap_df,
    x="Laps",
    y="FullName",
    palette="Reds_r",
    ax=ax
)

ax.set_title(
    "Total Laps Completed by Driver",
    fontsize=16,
    fontweight="bold"
)

ax.set_xlabel("Total Laps")
ax.set_ylabel("")

fig.patch.set_facecolor("#0b0b0f")
ax.set_facecolor("#0b0b0f")

ax.tick_params(colors="white")

for spine in ax.spines.values():
    spine.set_visible(False)

st.pyplot(fig, use_container_width=True)


# =========================================================
# RAW DATA
# =========================================================

st.markdown("---")

with st.expander("🔎 View Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=500
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style='text-align:center; color:#777;'>
        🏎️ F1 2025 Analytics Dashboard<br>
        Built with Python, Pandas, Seaborn, Matplotlib & Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
