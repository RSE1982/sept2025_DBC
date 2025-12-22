import textwrap
from typing import Dict, List

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# ---------------- Page config ----------------
st.set_page_config(page_title="Titanic Explorer (No-ML)", page_icon="🚢", layout="wide")
st.title("🚢 Titanic Explorer (No-ML)")
st.caption("Filter → Summarise → Visualise. Built with Streamlit + pandas + matplotlib (no ML).")


# ---------------- Data loading ----------------
@st.cache_data(show_spinner=False)
def load_titanic() -> pd.DataFrame:
    df = sns.load_dataset("titanic").copy()
    # Canonical tidy-ups
    # Ensure consistent dtypes
    cat_cols = ["sex", "class", "embark_town", "who", "adult_male", "alone", "deck", "embarked", "alive"]
    for c in df.columns:
        if c in cat_cols:
            df[c] = df[c].astype("category")
    # Rename a couple for clarity in UI
    df = df.rename(columns={"embark_town": "embark_town",
                            "pclass": "pclass"})  # pclass isn't in seaborn titanic (they use 'class')
    return df

@st.cache_data(show_spinner=False)
def describe_missing(df: pd.DataFrame) -> pd.DataFrame:
    miss = df.isna().mean().mul(100).round(2).rename("missing_%")
    miss = miss.reset_index()
    miss.columns = ["column", "missing_%"]
    return miss.sort_values("missing_%", ascending=False)


df = load_titanic()

# ---------------- Sidebar (filters) ----------------
with st.sidebar:
    st.header("🧭 Filters")

    # Basic categorical filters
    sex = st.multiselect("Sex", options=sorted(df["sex"].dropna().unique().tolist()), default=None)
    cls = st.multiselect("Class", options=sorted(df["class"].dropna().unique().tolist()), default=None)
    embarked = st.multiselect("Embarked (town)", options=sorted(df["embark_town"].dropna().unique().tolist()), default=None)

    # Numeric ranges
    age_min, age_max = float(df["age"].min(skipna=True)), float(df["age"].max(skipna=True))
    fare_min, fare_max = float(df["fare"].min(skipna=True)), float(df["fare"].max(skipna=True))
    age_range = st.slider("Age range", min_value=0.0, max_value=float(np.ceil(age_max)), value=(float(np.floor(age_min)) if not np.isnan(age_min) else 0.0, float(np.ceil(age_max)) if not np.isnan(age_max) else 80.0))
    fare_range = st.slider("Fare range", min_value=0.0, max_value=float(np.ceil(fare_max)), value=(0.0, float(np.ceil(fare_max))))

    # Extras
    include_missing_deck = st.checkbox("Include missing deck", value=True)
    show_row_index = st.checkbox("Show row index", value=False)
    page_size = st.slider("Preview page size", 5, 100, 20, step=5)

# Apply filters
fdf = df.copy()
if sex:
    fdf = fdf[fdf["sex"].isin(sex)]
if cls:
    fdf = fdf[fdf["class"].isin(cls)]
if embarked:
    fdf = fdf[fdf["embark_town"].isin(embarked)]

# Age/Fare numeric filters (ignore NaNs)
if "age" in fdf.columns:
    fdf = fdf[(fdf["age"].isna()) | ((fdf["age"] >= age_range[0]) & (fdf["age"] <= age_range[1]))]
if "fare" in fdf.columns:
    fdf = fdf[(fdf["fare"].isna()) | ((fdf["fare"] >= fare_range[0]) & (fdf["fare"] <= fare_range[1]))]

if not include_missing_deck and "deck" in fdf.columns:
    fdf = fdf[~fdf["deck"].isna()]

st.sidebar.markdown(f"### {len(fdf)} passengers selected")

# ---------------- Tabs ----------------
tab_overview, tab_insights, tab_charts, tab_answers = st.tabs(["Overview", "Survival Insights", "Charts", "Answers"])

# ---------------- Overview ----------------
with tab_overview:
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Rows (filtered)", f"{len(fdf):,}")
    with c2:
        st.metric("Columns", f"{fdf.shape[1]}")
    with c3:
        # Survival rate
        if "survived" in fdf.columns:
            surv_rate = fdf["survived"].mean() * 100
            st.metric("Survival rate", f"{surv_rate:.1f}%")
        else:
            st.metric("Survival rate", "N/A")
    with c4:
        st.metric("Missing age (%)", f"{fdf['age'].isna().mean()*100:.1f}%")

    st.subheader("Preview")
    st.dataframe(fdf.head(page_size), use_container_width=True, hide_index=not show_row_index)

    colA, colB = st.columns([2,1])
    with colA:
        st.subheader("Summary (numeric)")
        numeric_cols = fdf.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            st.dataframe(fdf[numeric_cols].describe().T, use_container_width=True)
        else:
            st.caption("No numeric columns.")
    with colB:
        st.subheader("Missing values (%)")
        st.dataframe(describe_missing(fdf), use_container_width=True)

# ---------------- Survival Insights ----------------
with tab_insights:
    st.subheader("Group survival rates")
    left, right = st.columns([2,1])

    with left:
        # Pick a grouping column
        cat_cols = [c for c in fdf.select_dtypes(include=["category", "object"]).columns if c not in ["alive"]]
        group_col = st.selectbox("Group by (categorical)", options=cat_cols if cat_cols else ["sex"], index=(cat_cols.index("sex") if "sex" in cat_cols else 0))
        # Aggregated survival rate by group
        if "survived" in fdf.columns:
            grp = fdf.groupby(group_col, dropna=False)["survived"].mean().mul(100).reset_index().rename(columns={"survived": "survival_rate_%"}).sort_values("survival_rate_%", ascending=False)
            st.dataframe(grp, use_container_width=True)

            # Bar plot (matplotlib)
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(grp[group_col].astype(str), grp["survival_rate_%"])
            ax.set_ylabel("Survival rate (%)")
            ax.set_xlabel(group_col)
            ax.set_title(f"Survival rate by {group_col}")
            plt.xticks(rotation=45, ha="right")
            st.pyplot(fig, use_container_width=True)
        else:
            st.info("No `survived` column found.")

    with right:
        # Compare means for Age and Fare by Survived
        st.markdown("**Mean comparison (by Survived)**")
        if "survived" in fdf.columns:
            comp = fdf.groupby("survived")[["age", "fare"]].mean(numeric_only=True).round(2)
            st.dataframe(comp, use_container_width=True)
        st.markdown("**Download filtered data**")
        st.download_button("⬇️ CSV", data=fdf.to_csv(index=False).encode("utf-8"), file_name="titanic_filtered.csv", mime="text/csv")

    st.divider()
    st.subheader("Crosstab: Survived vs chosen group")
    if "survived" in fdf.columns:
        # Use the same group_col
        ct = pd.crosstab(fdf[group_col], fdf["survived"], dropna=False, normalize="index").mul(100).round(1)
        st.dataframe(ct, use_container_width=True)
        # Stacked bar (counts)
        counts = pd.crosstab(fdf[group_col], fdf["survived"], dropna=False)
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        bottom = None
        for surv_value in counts.columns:
            vals = counts[surv_value].values
            ax2.bar(counts.index.astype(str), vals, bottom=bottom, label=f"survived={surv_value}")
            bottom = vals if bottom is None else bottom + vals
        ax2.set_title(f"Counts by {group_col} and survival")
        ax2.set_xlabel(group_col)
        ax2.set_ylabel("Count")
        ax2.legend()
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig2, use_container_width=True)

# ---------------- Charts ----------------
with tab_charts:
    st.subheader("Custom charts")

    chart_type = st.selectbox("Chart type", ["Bar (survival rate by group)", "Scatter (Age vs Fare)", "Line (sorted Fare or Age)"])

    if chart_type == "Bar (survival rate by group)":
        # Choose any categorical field
        cat_cols = [c for c in fdf.select_dtypes(include=["category", "object"]).columns if c not in ["alive"]]
        if cat_cols and "survived" in fdf.columns:
            group_col2 = st.selectbox("Group by", options=cat_cols, index=(cat_cols.index("class") if "class" in cat_cols else 0), key="bar_group")
            grp2 = fdf.groupby(group_col2, dropna=False)["survived"].mean().mul(100).reset_index().rename(columns={"survived": "survival_rate_%"}).dropna()
            fig3, ax3 = plt.subplots(figsize=(8, 4))
            ax3.bar(grp2[group_col2].astype(str), grp2["survival_rate_%"])
            ax3.set_xlabel(group_col2)
            ax3.set_ylabel("Survival rate (%)")
            ax3.set_title(f"Survival rate by {group_col2}")
            plt.xticks(rotation=45, ha="right")
            st.pyplot(fig3, use_container_width=True)
        else:
            st.info("Need a categorical column and `survived`.")

    elif chart_type == "Scatter (Age vs Fare)":
        # Color by survived or sex
        color_by = st.selectbox("Color by", ["survived", "sex", "(none)"])
        sdf = fdf[["age", "fare", "survived", "sex"]].dropna(subset=["age", "fare"]).copy()
        fig4, ax4 = plt.subplots(figsize=(7, 4))
        if color_by == "(none)":
            ax4.scatter(sdf["age"], sdf["fare"], alpha=0.8)
        else:
            for level, sub in sdf.groupby(color_by, dropna=False):
                ax4.scatter(sub["age"], sub["fare"], alpha=0.8, label=str(level))
            ax4.legend(loc="best", title=color_by, fontsize="small")
        ax4.set_xlabel("Age")
        ax4.set_ylabel("Fare")
        ax4.set_title("Fare vs Age")
        st.pyplot(fig4, use_container_width=True)

    else:  # Line
        series = st.selectbox("Series", ["fare", "age"])
        order_by = st.selectbox("Order by", ["increasing", "decreasing"])
        s = fdf[series].dropna().sort_values(ascending=(order_by == "increasing")).reset_index(drop=True)
        fig5, ax5 = plt.subplots(figsize=(8, 4))
        ax5.plot(s.index, s.values)
        ax5.set_xlabel("Index (sorted)")
        ax5.set_ylabel(series.capitalize())
        ax5.set_title(f"{series.capitalize()} (sorted {order_by})")
        st.pyplot(fig5, use_container_width=True)

# ---------------- Answers (guided findings) ----------------
with tab_answers:
    st.subheader("Guided answers (based on current filters)")
    st.caption(
        "These summaries update with your sidebar filters, so answers reflect the current subset."
    )

    if fdf.empty or "survived" not in fdf.columns:
        st.info("No data to analyse (check filters) or no `survived` column.")
    else:
        # Helper for safe survival% format
        def _pct(x): 
            return float(x) * 100.0

        # Q1. Highest survival rate by Sex × Class × Embark town
        with st.expander("Q1) Who had the highest survival rate (Sex × Class × Embark town)?", expanded=True):
            cats = ["sex", "class", "embark_town"]
            have = [c for c in cats if c in fdf.columns]
            if len(have) >= 2:  # need at least sex & class, embark may be missing in some rows
                g = (
                    fdf.groupby(have, dropna=False)["survived"]
                    .mean()
                    .mul(100)
                    .reset_index()
                    .rename(columns={"survived": "survival_rate_%"})
                    .sort_values("survival_rate_%", ascending=False)
                )
                st.dataframe(g, use_container_width=True)
                if not g.empty:
                    top = g.iloc[0].to_dict()
                    st.markdown(
                        f"**Top group:** {', '.join(f'{k}={top[k]}' for k in have)} - "
                        f"**{top['survival_rate_%']:.1f}%**"
                    )
            else:
                st.write("Need at least `sex` and `class` present.")

        # Q2. Relationship between Fare and Survival
        with st.expander("Q2) Fare vs Survival... do higher fares always mean better odds?"):
            means = (
                fdf.groupby("survived")[["fare"]]
                .mean(numeric_only=True)
                .rename(columns={"fare": "mean_fare"})
                .round(2)
            )
            st.dataframe(means, use_container_width=True)
            # Correlation (Spearman handles ranks; survived is 0/1)
            try:
                corr = fdf[["fare", "survived"]].dropna().corr(method="spearman").loc["fare", "survived"]
                st.markdown(f"**Spearman correlation (fare vs survived): {corr:.3f}**")
                st.caption("Positive means higher fare tends to align with higher survival, within the current filters.")
            except Exception:
                st.caption("Correlation not available (insufficient data).")

            # Quick quantile look
            q = (
                fdf[["fare", "survived"]]
                .dropna()
                .assign(fare_bin=pd.qcut(fdf["fare"].dropna(), q=4, duplicates="drop"))
                .groupby("fare_bin")["survived"].mean().mul(100).reset_index()
                .rename(columns={"survived": "survival_rate_%"})
            )
            if not q.empty:
                st.markdown("**Survival by fare quartile**")
                st.dataframe(q, use_container_width=True)

        # Q3. Age and Survival (children vs adults vs seniors)
        with st.expander("Q3) How does age affect survival (children, adults, seniors)?"):
            if "age" in fdf.columns:
                bins   = [0, 12, 18, 40, 60, 200]
                labels = ["Child (0–12)", "Teen (13–18)", "Adult (19–40)", "Midlife (41–60)", "Senior (60+)"]
                ageb = pd.cut(fdf["age"], bins=bins, labels=labels, right=True)
                tbl = (
                    fdf.assign(age_group=ageb)
                    .groupby("age_group", dropna=False)["survived"]
                    .mean()
                    .mul(100)
                    .reset_index()
                    .rename(columns={"survived": "survival_rate_%"})
                )
                st.dataframe(tbl, use_container_width=True)
                if not tbl.empty:
                    best = tbl.sort_values("survival_rate_%", ascending=False).iloc[0]
                    st.markdown(f"**Highest survival:** {best['age_group']} | **{best['survival_rate_%']:.1f}%**")
            else:
                st.write("No `age` column in the current dataset.")

        # Q4. Combine Sex & Class
        with st.expander("Q4) What changes when you filter by both Sex and Class?"):
            if all(c in fdf.columns for c in ["sex", "class"]):
                pivot = (
                    pd.crosstab(fdf["sex"], fdf["class"], values=fdf["survived"], aggfunc="mean")
                    .mul(100)
                    .round(1)
                )
                st.markdown("**Survival rate (%) by Sex × Class**")
                st.dataframe(pivot, use_container_width=True)
            else:
                st.write("Need `sex` and `class`.")

        # Q5. Bonus - surface interesting groups automatically
        with st.expander("Q5) Bonus: non-obvious highs & lows across categories"):
            cand_cols = [
                c for c in fdf.select_dtypes(include=["category", "object"]).columns
                if c not in {"alive"}  # skip duplicate status
            ]
            results = []
            overall = _pct(fdf["survived"].mean())
            for c in cand_cols:
                tmp = (
                    fdf.groupby(c, dropna=False)["survived"]
                    .agg(rate=lambda s: _pct(s.mean()), n="count")
                    .reset_index()
                    .rename(columns={"rate": "survival_rate_%", "n": "count"})
                )
                tmp["column"] = c
                results.append(tmp)
            if results:
                allg = pd.concat(results, ignore_index=True)
                # keep groups with at least 8 rows to avoid noise
                allg = allg[allg["count"] >= 8]
                high = allg.sort_values("survival_rate_%", ascending=False).head(5)
                low  = allg.sort_values("survival_rate_%", ascending=True).head(5)

                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**Top 5 highest survival groups**")
                    st.dataframe(high, use_container_width=True)
                    st.markdown("See those top four groups? They look impressive at first glance - 75% survival! But look at what the column says: deck=None, who=None. That’s not a pattern in the real world, it’s just where data was missing. It’s a good reminder that data gaps can create fake correlations.")
                with c2:
                    st.markdown("**Top 5 lowest survival groups**")
                    st.dataframe(low, use_container_width=True)
                    st.markdown("At first glance, it looks like people with missing deck or class info had low survival — but that’s not the cause. It’s a proxy for something else: they were probably 3rd class passengers, and those passengers were hit hardest. The only genuinely meaningful variable here is sex=male, with a survival rate of just 19%. That tells a clear story that matches history — men were much less likely to survive than women. The rest mostly remind us that missing data often clusters in the least fortunate groups.")

                st.caption(f"Overall survival (current filters): **{overall:.1f}%**  •  Minimum group size = 8")
            else:
                st.write("No categorical columns available to scan.")

# ---------------- Notes ----------------
st.divider()
st.subheader("📝 Analysis notes (session only)")
if "notes" not in st.session_state:
    st.session_state.notes = ""
st.session_state.notes = st.text_area("Write observations you’d like to remember", value=st.session_state.notes, height=120)

with st.expander("Help"):
    st.markdown(textwrap.dedent("""
    **Tips**
    - Use the sidebar filters to subset by Sex, Class, Embarked, Age, and Fare.
    - **Survival Insights** shows group survival rates, a crosstab, and stacked bars.
    - **Charts** gives quick bar/scatter/line options using matplotlib.
    - Click **CSV** to download the filtered dataset.
    """))
