import streamlit as st
import pandas as pd
import plotly as px

st.set_page_config(page_title="Skycity Restaurants & Bars", layout="wide", page_icon="🍽️")


st.header(" _ ")
st.header("This is SkyCity restaurants & bars dataset ")
df=pd.read_csv("Skycity restaurants & bars.csv")
df

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .block-container { padding-top: 1.5rem; }
    .kpi-card {
        background: linear-gradient(135deg, #1e2130, #252a3a);
        border: 1px solid #2e3450;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
    }
    .kpi-label { color: #8b9cc8; font-size: 13px; font-weight: 500; margin-bottom: 4px; }
    .kpi-value { color: #ffffff; font-size: 26px; font-weight: 700; }
    .kpi-delta-pos { color: #22c55e; font-size: 12px; }
    .kpi-delta-neg { color: #ef4444; font-size: 12px; }
    .section-header {
        color: #c9d3f0;
        font-size: 20px;
        font-weight: 600;
        margin: 28px 0 12px 0;
        padding-bottom: 6px;
        border-bottom: 2px solid #2e3450;
    }
    .tab-subheader {
        color: #a0aec0;
        font-size: 15px;
        font-weight: 500;
        margin: 16px 0 6px 0;
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e2130, #252a3a);
        border: 1px solid #2e3450;
        border-radius: 10px;
        padding: 12px 16px;
    }
</style>
""", unsafe_allow_html=True)

PALETTE = ["#6366f1", "#22d3ee", "#f59e0b", "#10b981", "#f43f5e", "#a78bfa", "#34d399", "#fb923c"]
CHANNEL_COLORS = {"InStore": "#6366f1", "UberEats": "#22d3ee", "DoorDash": "#f59e0b", "SelfDelivery": "#10b981"}
CHANNEL_LABELS = {
    "InStoreOrders": "In-Store", "UberEatsOrders": "UberEats",
    "DoorDashOrders": "DoorDash", "SelfDeliveryOrders": "Self-Delivery"
}

def plotly_defaults(fig, height=380):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c9d3f0", family="Inter, sans-serif", size=12),
        margin=dict(l=10, r=10, t=40, b=10),
        height=height,
        legend=dict(
            bgcolor="rgba(30,33,48,0.8)",
            bordercolor="#2e3450",
            borderwidth=1,
            font=dict(size=11)
        ),
        xaxis=dict(gridcolor="#1e2234", linecolor="#2e3450", tickfont=dict(size=11)),
        yaxis=dict(gridcolor="#1e2234", linecolor="#2e3450", tickfont=dict(size=11)),
    )
    return fig

# ─── Load data ────────────────────────────────────────────────────────────────
st.title("🍽️  Skycity Restaurant & Bar  —  Analytics Dashboard")

try:
    df = pd.read_csv("Skycity restaurants & bars.csv")
except FileNotFoundError:
    st.error("⚠️  `Skycity restaurants & bars.csv` not found. Place it in the same folder as this script.")
    st.stop()

# ─── Derived columns ──────────────────────────────────────────────────────────
df["TotalOrders"] = df[["InStoreOrders","UberEatsOrders","DoorDashOrders","SelfDeliveryOrders"]].sum(axis=1)
df["InStoreShare_calc"]  = df["InStoreOrders"]  / df["TotalOrders"]
df["UE_share_calc"]      = df["UberEatsOrders"] / df["TotalOrders"]
df["DD_share_calc"]      = df["DoorDashOrders"] / df["TotalOrders"]
df["SD_share_calc"]      = df["SelfDeliveryOrders"] / df["TotalOrders"]
df["TotalRevenue"]       = df[["InStoreRevenue","UberEatsRevenue","DoorDashRevenue","SelfDeliveryRevenue"]].sum(axis=1)
df["TotalNetProfit"]     = df[["InStoreNetProfit","UberEatsNetProfit","DoorDashNetProfit","SelfDeliveryNetProfit"]].sum(axis=1)
df["ShareSum"] = df[["InStoreShare","UE_share","DD_share","SD_share"]].sum(axis=1)
df["MaxChannelShare"] = df[["InStoreShare","UE_share","DD_share","SD_share"]].max(axis=1)
df["DependencyLevel"] = df["MaxChannelShare"].apply(
    lambda x: "High Dependency" if x > 0.7 else ("Moderate" if x > 0.5 else "Diversified")
)

# ─── Sidebar ──────────────────────────────────────────────────────────────────



st.sidebar.image("https://img.icons8.com/fluency/96/restaurant.png", width=60)
st.sidebar.markdown("## 🔍 Filters")
subregion  = st.sidebar.multiselect("Subregion",  sorted(df["Subregion"].unique()))
cuisine    = st.sidebar.multiselect("Cuisine",    sorted(df["CuisineType"].unique()))
segment    = st.sidebar.multiselect("Segment",    sorted(df["Segment"].unique()))
channel_type = st.sidebar.radio("Channel Focus", ["All", "In-Store Only", "Delivery Only"])

fdf = df.copy()
if subregion: fdf = fdf[fdf["Subregion"].isin(subregion)]
if cuisine:   fdf = fdf[fdf["CuisineType"].isin(cuisine)]
if segment:   fdf = fdf[fdf["Segment"].isin(segment)]
if not fdf.empty:
    fdf["TotalOrders"]    = fdf[["InStoreOrders","UberEatsOrders","DoorDashOrders","SelfDeliveryOrders"]].sum(axis=1)
    fdf["TotalRevenue"]   = fdf[["InStoreRevenue","UberEatsRevenue","DoorDashRevenue","SelfDeliveryRevenue"]].sum(axis=1)
    fdf["TotalNetProfit"] = fdf[["InStoreNetProfit","UberEatsNetProfit","DoorDashNetProfit","SelfDeliveryNetProfit"]].sum(axis=1)

    if channel_type == "In-Store Only":
        fdf = fdf[fdf["InStoreShare_calc"] > 0.5]  # majority in-store
    elif channel_type == "Delivery Only":
        fdf = fdf[fdf["InStoreShare_calc"] <= 0.5]  # majority delivery

# ─── KPIs ─────────────────────────────────────────────────────────────────────
def kpis(d):
    rev     = d["TotalRevenue"].sum()
    orders  = d["TotalOrders"].sum()
    profit  = d["TotalNetProfit"].sum()
    margin  = profit / rev * 100 if rev else 0
    aov     = rev / orders if orders else 0
    growth  = d["GrowthFactor"].mean()
    n       = len(d)
    ch      = d[["InStoreOrders","UberEatsOrders","DoorDashOrders","SelfDeliveryOrders"]].sum().idxmax()
    ch_lbl  = CHANNEL_LABELS.get(ch, ch)
    return dict(rev=rev, orders=orders, profit=profit, margin=margin, aov=aov, growth=growth, n=n, top_channel=ch_lbl)

k  = kpis(fdf if not fdf.empty else df)
k0 = kpis(df)

def delta_str(v, v0, fmt=".2f"):
    d = v - v0
    sign = "▲" if d >= 0 else "▼"
    color = "kpi-delta-pos" if d >= 0 else "kpi-delta-neg"
    return f'<span class="{color}">{sign} {abs(d):{fmt}}</span>'

st.markdown('<div class="section-header">📊 Key Performance Indicators</div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5, c6 = st.columns(6)
metrics = [
    (c1, "💰 Total Revenue",       f"${k['rev']:,.0f}",         delta_str(k['rev'], k0['rev'], ",.0f")),
    (c2, "🛒 Total Orders",        f"{k['orders']:,.0f}",       delta_str(k['orders'], k0['orders'], ",.0f")),
    (c3, "📈 Net Profit",          f"${k['profit']:,.0f}",      delta_str(k['profit'], k0['profit'], ",.0f")),
    (c4, "🎯 Profit Margin",       f"{k['margin']:.1f}%",       delta_str(k['margin'], k0['margin'], ".1f")),
    (c5, "🧾 Avg Order Value",     f"${k['aov']:.2f}",          delta_str(k['aov'], k0['aov'])),
    (c6, "🏆 Top Channel",         k['top_channel'],                 ""),
]
for col, label, val, delta in metrics:
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{val}</div>
            <div>{delta}</div>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  TAB LAYOUT
# ═══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs(["📦 Channel Analysis", "🌍 Geographic Analysis", "🍜 Cuisine & Segment", "🔬 Forecasting & Validation"])
# ──────────────── TAB 1: Channel Analysis ─────────────────────────────────────
with tab1:

    # 1. Total Orders by Channel — Funnel
    st.markdown('<div class="section-header">1. Total Orders by Channel</div>', unsafe_allow_html=True)
    st.caption("Shows total orders from each channel. ")

    channel_totals = fdf[["InStoreOrders","UberEatsOrders","DoorDashOrders","SelfDeliveryOrders"]].sum().reset_index()
    channel_totals.columns = ["Channel", "Orders"]
    channel_totals["Channel"] = channel_totals["Channel"].map(CHANNEL_LABELS)
    channel_totals = channel_totals.sort_values("Orders", ascending=False)

    fig = px.bar(channel_totals, x="Channel", y="Orders", color="Channel",
                 color_discrete_sequence=PALETTE, text="Orders",
                 title="Total Orders by Channel")
    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside", marker_line_width=0)
    fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Orders")
    st.plotly_chart(plotly_defaults(fig), use_container_width=True)

    st.caption("Insight: Identifies the most used ordering channel and overall customer preference.")


    

    # 2. Average Order Share — Donut + Bar side by side
    st.markdown('<div class="section-header">2. Average Order Share by Channel</div>', unsafe_allow_html=True)
    left, right = st.columns(2)
    share_vals = {
        "In-Store":      fdf["InStoreShare_calc"].mean() if not fdf.empty else df["InStoreShare_calc"].mean(),
        "UberEats":      fdf["UE_share_calc"].mean()     if not fdf.empty else df["UE_share_calc"].mean(),
        "DoorDash":      fdf["DD_share_calc"].mean()     if not fdf.empty else df["DD_share_calc"].mean(),
        "Self-Delivery": fdf["SD_share_calc"].mean()     if not fdf.empty else df["SD_share_calc"].mean(),
    }
    share_df = pd.DataFrame(list(share_vals.items()), columns=["Channel", "Share"])
    with left:
        fig = px.pie(share_df, names="Channel", values="Share", hole=0.55,
                     color_discrete_sequence=PALETTE,
                     title="Share Distribution (Donut)")
        st.caption("Description: Donut + bar chart showing % share of each channel.")

        fig.update_traces(textposition="outside", textinfo="percent+label",
                          hovertemplate="%{label}: %{percent}")
        st.plotly_chart(plotly_defaults(fig), use_container_width=True)

    with right:
        fig = px.bar(share_df.sort_values("Share", ascending=True),
                     x="Share", y="Channel", orientation="h",
                     color="Channel", color_discrete_sequence=PALETTE,
                     text="Share", title="Average Share (Horizontal Bar)")
        fig.update_traces(texttemplate="%{text:.1%}", textposition="outside", marker_line_width=0)
        fig.update_layout(showlegend=False, xaxis_tickformat=".0%")
        st.plotly_chart(plotly_defaults(fig), use_container_width=True)
        st.caption("Insight: Highlights channel importance and detects over-dependence on one channel.")


    # 3. Dependency Level
    st.markdown('<div class="section-header">3. Channel Dependency Distribution</div>', unsafe_allow_html=True)
    st.caption("Description: Categorizes restaurants as Diversified, Moderate, or High Dependency.")
    dep_order = ["Diversified", "Moderate", "High Dependency"]
    dep_colors = {"Diversified": "#10b981", "Moderate": "#f59e0b", "High Dependency": "#ef4444"}
    dep_counts = fdf["DependencyLevel"].value_counts().reindex(dep_order, fill_value=0).reset_index()
    dep_counts.columns = ["Level", "Count"]

    fig = px.bar(dep_counts, x="Level", y="Count", color="Level",
                 color_discrete_map=dep_colors, text="Count",
                 title="Channel Dependency Level Across Restaurants")
    fig.update_traces(textposition="outside", marker_line_width=0)
    fig.update_layout(showlegend=False)
    st.plotly_chart(plotly_defaults(fig), use_container_width=True)
    st.caption("Insight: Reveals risk level — high dependency means business vulnerability.")

# ──────────────── TAB 2: Geographic Analysis ──────────────────────────────────
with tab2:

    # 3. Channel Distribution by Subregion — Grouped bar
    st.markdown('<div class="section-header">1. Channel Distribution by Subregion</div>', unsafe_allow_html=True)
    st.caption("Description: Orders split by channel across regions.")

    geo_ch = fdf.groupby("Subregion")[["InStoreOrders","UberEatsOrders","DoorDashOrders","SelfDeliveryOrders"]].sum().reset_index()
    geo_melt = geo_ch.melt(id_vars="Subregion", var_name="Channel", value_name="Orders")
    geo_melt["Channel"] = geo_melt["Channel"].map(CHANNEL_LABELS)

    fig = px.bar(geo_melt, x="Subregion", y="Orders", color="Channel",
                 barmode="group", color_discrete_sequence=PALETTE,
                 title="Orders by Subregion and Channel")
    fig.update_layout(xaxis_title="", yaxis_title="Orders")
    st.plotly_chart(plotly_defaults(fig, height=420), use_container_width=True)

    st.caption("Insight: Shows regional ordering behavior (delivery vs dine-in).")

    # Channel share (stacked 100%)
    st.markdown('<div class="section-header">2. Channel Share by Subregion (100% Stacked)</div>', unsafe_allow_html=True)
    st.caption("Description: 100% stacked chart of channel proportions.")
    geo_share = geo_ch.copy()
    for col in ["InStoreOrders","UberEatsOrders","DoorDashOrders","SelfDeliveryOrders"]:
        geo_share[col] = geo_share[col] / geo_share[["InStoreOrders","UberEatsOrders","DoorDashOrders","SelfDeliveryOrders"]].sum(axis=1)
    geo_share_melt = geo_share.melt(id_vars="Subregion", var_name="Channel", value_name="Share")
    geo_share_melt["Channel"] = geo_share_melt["Channel"].map(CHANNEL_LABELS)

    fig = px.bar(geo_share_melt, x="Subregion", y="Share", color="Channel",
                 barmode="relative", color_discrete_sequence=PALETTE,
                 title="Proportional Channel Share per Subregion")
    fig.update_layout(yaxis_tickformat=".0%", xaxis_title="", yaxis_title="Share")
    st.plotly_chart(plotly_defaults(fig, height=420), use_container_width=True)
    st.caption("Insight: Compares channel preference across locations.")

    # Net Profit by Subregion
    st.markdown('<div class="section-header">3. Net Profit by Subregion</div>', unsafe_allow_html=True)
    st.caption("Description: Average profit by channel and region.")

    profit_geo = fdf.groupby("Subregion")[["InStoreNetProfit","UberEatsNetProfit","DoorDashNetProfit","SelfDeliveryNetProfit"]].mean().reset_index()
    profit_melt = profit_geo.melt(id_vars="Subregion", var_name="Channel", value_name="NetProfit")
    profit_melt["Channel"] = profit_melt["Channel"].str.replace("NetProfit","").str.replace("InStore","In-Store").str.replace("SelfDelivery","Self-Delivery")

    fig = px.bar(profit_melt, x="Subregion", y="NetProfit", color="Channel",
                 barmode="group", color_discrete_sequence=PALETTE,
                 title="Average Net Profit by Channel & Subregion")
    fig.update_layout(xaxis_title="", yaxis_title="Avg Net Profit ($)")
    st.plotly_chart(plotly_defaults(fig, height=420), use_container_width=True)
    st.caption("Insight: Identifies most profitable channels geographically.")

# ──────────────── TAB 3: Cuisine & Segment ────────────────────────────────────
with tab3:

    # 1. Channel mix by Cuisine
    st.markdown('<div class="section-header">1. Average Channel Mix by Cuisine Type</div>', unsafe_allow_html=True)
    st.caption("Description: Channel usage across cuisine types. ")

    cuisine_mix = fdf.groupby("CuisineType")[["InStoreShare_calc","UE_share_calc","DD_share_calc","SD_share_calc"]].mean().reset_index()
    cuisine_melt = cuisine_mix.melt(id_vars="CuisineType", var_name="Channel", value_name="Share")
    cuisine_melt["Channel"] = cuisine_melt["Channel"].map({
        "InStoreShare_calc": "In-Store", "UE_share_calc": "UberEats",
        "DD_share_calc": "DoorDash", "SD_share_calc": "Self-Delivery"
    })

    fig = px.bar(cuisine_melt, x="CuisineType", y="Share", color="Channel",
                 barmode="relative", color_discrete_sequence=PALETTE,
                 title="Channel Share Mix by Cuisine Type (100% Stacked)")
    fig.update_layout(yaxis_tickformat=".0%", xaxis_title="", yaxis_title="Average Share")
    st.plotly_chart(plotly_defaults(fig, height=420), use_container_width=True)
    st.caption("Insight: Shows which cuisines are delivery-heavy vs dine-in focused.")

    # 2. UberEats Share by Cuisine — Horizontal bar
    st.markdown('<div class="section-header">2. UberEats Share by Cuisine Type</div>', unsafe_allow_html=True)
    st.caption("Description: Ranks cuisines by UberEats usage.")

    ue_cuisine = fdf.groupby("CuisineType")["UE_share"].mean().reset_index().sort_values("UE_share")

    fig = px.bar(ue_cuisine, x="UE_share", y="CuisineType", orientation="h",
                 color="UE_share", color_continuous_scale="Blues",
                 text="UE_share", title="Mean UberEats Share per Cuisine")
    fig.update_traces(texttemplate="%{text:.1%}", textposition="outside", marker_line_width=0)
    fig.update_layout(coloraxis_showscale=False, xaxis_tickformat=".0%", yaxis_title="")
    st.plotly_chart(plotly_defaults(fig, height=400), use_container_width=True)

    st.caption("Insight: Identifies aggregator-driven cuisines.")

    # 3. Total Orders by Segment — Pie
    st.markdown('<div class="section-header">3. Order Volume by Segment</div>', unsafe_allow_html=True)
    st.caption("Description: Orders split by business type and cuisine.")

    left, right = st.columns(2)
    seg_orders = fdf.groupby("Segment")["TotalOrders"].sum().reset_index()

    with left:
        fig = px.pie(seg_orders, names="Segment", values="TotalOrders", hole=0.4,
                     color_discrete_sequence=PALETTE, title="Orders by Segment")
        fig.update_traces(textposition="outside", textinfo="percent+label")
        st.plotly_chart(plotly_defaults(fig), use_container_width=True)

    with right:
        cuisine_orders = fdf.groupby("CuisineType")["TotalOrders"].sum().reset_index().sort_values("TotalOrders", ascending=False)
        fig = px.bar(cuisine_orders, x="TotalOrders", y="CuisineType", orientation="h",
                     color="CuisineType", color_discrete_sequence=PALETTE,
                     title="Total Orders by Cuisine")
        fig.update_layout(showlegend=False, xaxis_title="Orders", yaxis_title="")
        st.plotly_chart(plotly_defaults(fig), use_container_width=True)
        st.caption("Insight: Highlights top-performing segments and cuisines.")

# ──────────────── TAB 4: Forecasting & Validation ─────────────────────────────
with tab4:

    # 1. Share Sum Validation — Scatter
    st.markdown('<div class="section-header">1. Share Sum Validation</div>', unsafe_allow_html=True)
    st.caption("Description: Checks if channel shares sum to ~100%.")

    invalid = fdf[abs(fdf["ShareSum"] - 1) > 0.05].copy()

    left, right = st.columns([2, 1])
    with left:
        fig = px.scatter(fdf, x=fdf.index, y="ShareSum",
                         color=(abs(fdf["ShareSum"] - 1) > 0.05).map({True: "⚠️ Invalid", False: "✅ Valid"}),
                         color_discrete_map={"⚠️ Invalid": "#ef4444", "✅ Valid": "#10b981"},
                         title="Channel Share Sum per Restaurant (should ≈ 1.0)")
        fig.add_hline(y=1.0, line_dash="dash", line_color="#f59e0b", annotation_text="Expected = 1.0")
        fig.add_hrect(y0=0.95, y1=1.05, fillcolor="rgba(34,197,94,0.08)", line_width=0)
        fig.update_layout(xaxis_title="Restaurant Index", yaxis_title="Sum of Shares",
                          legend_title="Status")
        st.plotly_chart(plotly_defaults(fig), use_container_width=True)
    with right:
        st.metric("✅ Valid Records",   f"{len(fdf) - len(invalid)}")
        st.metric("⚠️ Invalid Records", f"{len(invalid)}")
        if not invalid.empty:
            st.dataframe(invalid[["ShareSum"]].style.background_gradient(cmap="Reds"), height=200)

        st.caption("Insight: Ensures data accuracy and reliability.")

    # 2. Standard Deviation Analysis
    st.markdown('<div class="section-header">2. Standard Deviation of Numeric Columns</div>', unsafe_allow_html=True)
    st.caption("Description: Shows variability in data.")

    std_vals = fdf.describe().loc["std"].dropna().reset_index()
    std_vals.columns = ["Column", "StdDev"]
    std_vals = std_vals.sort_values("StdDev", ascending=False).head(20)

    fig = px.bar(std_vals, x="Column", y="StdDev", color="StdDev",
                 color_continuous_scale="Reds",
                 title="Top 20 Columns by Standard Deviation")
    fig.update_layout(xaxis_title="", yaxis_title="Std Dev", coloraxis_showscale=False,
                      xaxis_tickangle=-30)
    st.plotly_chart(plotly_defaults(fig, height=400), use_container_width=True)
    st.caption("High std dev indicates wide variability — impacts forecast reliability")
    
    st.caption("Insight: High variation = less predictable performance.")

    # 3. Channel Volume Aggregations — 2×2 grid
    st.markdown('<div class="section-header">3. Channel Volume Aggregations</div>', unsafe_allow_html=True)
    st.caption("Description: Channel share + delivery vs in-store comparison. ")

    ch_vol = fdf[["InStoreOrders","UberEatsOrders","DoorDashOrders","SelfDeliveryOrders"]].sum().reset_index()
    ch_vol.columns = ["Channel", "Orders"]
    ch_vol["Channel"] = ch_vol["Channel"].map(CHANNEL_LABELS)

    geo_vol    = fdf.groupby("Subregion")["TotalOrders"].sum().reset_index()
    cuisine_vol = fdf.groupby("CuisineType")["TotalOrders"].sum().reset_index()
    seg_vol    = fdf.groupby("Segment")["TotalOrders"].sum().reset_index()

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(ch_vol, x="Channel", y="Orders", color="Channel",
                     color_discrete_sequence=PALETTE, text="Orders", title="By Channel")
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside", marker_line_width=0)
        fig.update_layout(showlegend=False)
        st.plotly_chart(plotly_defaults(fig, height=320), use_container_width=True)
    with c2:
        fig = px.bar(geo_vol, x="Subregion", y="TotalOrders",
                     color_discrete_sequence=PALETTE, text="TotalOrders", title="By Subregion")
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside", marker_line_width=0)
        st.plotly_chart(plotly_defaults(fig, height=320), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        fig = px.bar(cuisine_vol, x="CuisineType", y="TotalOrders",
                     color="CuisineType", color_discrete_sequence=PALETTE,
                     text="TotalOrders", title="By Cuisine")
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside", marker_line_width=0)
        fig.update_layout(showlegend=False, xaxis_tickangle=-20)
        st.plotly_chart(plotly_defaults(fig, height=320), use_container_width=True)
    with c4:
        fig = px.pie(seg_vol, names="Segment", values="TotalOrders", hole=0.45,
                     color_discrete_sequence=PALETTE, title="By Segment")
        fig.update_traces(textposition="outside", textinfo="percent+label")
        st.plotly_chart(plotly_defaults(fig, height=320), use_container_width=True)

        st.caption("Insight: Gives a complete demand overview. ")

    # 4. Market Share
    st.markdown('<div class="section-header">4. Market Share Analysis</div>', unsafe_allow_html=True)
    st.caption("Description: Channel share + delivery vs in-store comparison.")

    total = ch_vol["Orders"].sum()
    ch_vol["Share"] = ch_vol["Orders"] / total
    delivery_total = fdf[["UberEatsOrders","DoorDashOrders","SelfDeliveryOrders"]].sum().sum()
    instore_total  = fdf["InStoreOrders"].sum()

    c5, c6, c7 = st.columns(3)
    with c5:
        fig = px.pie(ch_vol, names="Channel", values="Share", hole=0.5,
                     color_discrete_sequence=PALETTE, title="Market Share by Channel")
        fig.update_traces(textinfo="percent+label", textposition="outside")
        st.plotly_chart(plotly_defaults(fig, height=320), use_container_width=True)
    with c6:
        di_df = pd.DataFrame({"Type": ["Delivery", "In-Store"],
                              "Orders": [delivery_total, instore_total]})
        fig = px.pie(di_df, names="Type", values="Orders", hole=0.5,
                     color_discrete_sequence=["#6366f1","#22d3ee"],
                     title="Delivery vs In-Store")
        fig.update_traces(textinfo="percent+label", textposition="outside")
        st.plotly_chart(plotly_defaults(fig, height=320), use_container_width=True)
    with c7:
        fig = px.bar(ch_vol.sort_values("Orders", ascending=False),
                     x="Channel", y="Orders", color="Channel",
                     color_discrete_sequence=PALETTE, text="Orders",
                     title="Ranked Orders per Channel")
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside", marker_line_width=0)
        fig.update_layout(showlegend=False)
        st.plotly_chart(plotly_defaults(fig, height=320), use_container_width=True)

        st.caption("Insight: Shows overall dominance and customer trends.")

    # 5. Geographic Dominant Channel — Heatmap
    st.markdown('<div class="section-header">5. Geographic Channel Preference Heatmap</div>', unsafe_allow_html=True)
    st.caption("Description: Visual intensity of channel usage by region. ")

    geo_heat = fdf.groupby("Subregion")[["InStoreOrders","UberEatsOrders","DoorDashOrders","SelfDeliveryOrders"]].sum()
    geo_heat_norm = geo_heat.div(geo_heat.sum(axis=1), axis=0).rename(columns=CHANNEL_LABELS)

    fig = px.imshow(geo_heat_norm.T, color_continuous_scale="Viridis",
                    aspect="auto", title="Channel Share Heatmap by Subregion",
                    labels=dict(x="Subregion", y="Channel", color="Share"))
    fig.update_layout(coloraxis_colorbar=dict(tickformat=".0%"))
    st.plotly_chart(plotly_defaults(fig, height=300), use_container_width=True)

    st.caption("Insight: Quickly identifies regional channel preferences.")

    # 6. Growth Factor Distribution
    st.markdown('<div class="section-header">6. Growth Factor Distribution</div>', unsafe_allow_html=True)
    st.caption("Description: Distribution of growth across restaurants.")

    fig = px.histogram(fdf, x="GrowthFactor", nbins=30, color_discrete_sequence=["#6366f1"],
                       title="Distribution of Growth Factor Across Restaurants",
                       marginal="box")
    fig.update_layout(xaxis_title="Growth Factor", yaxis_title="Count")
    st.plotly_chart(plotly_defaults(fig, height=380), use_container_width=True)

    st.caption("Insight: Shows growth trends and performance spread.")


    