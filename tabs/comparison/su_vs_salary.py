import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from utils.salary_loader import load_salary_data
from tabs.SU.su_tab import load_and_clean_data as load_su_data

def run_su_vs_salary_comparison():
    st.title("🎓 SU vs 💼 Salary Comparison")

    # --- Load SU data ---
    su_df, _, _ = load_su_data(
        file_stipend="Data/SU/SU stipendier og lån (mio. kr.).xlsx",
        file_antal="Data/SU/Antal støttemodtagere og låntagere.xlsx",
        file_aarsvaerk="Data/SU/Støtteårsværk.xlsx",
        file_home="Data/SU/students_living_at_home.xlsx",
        file_not_home="Data/SU/students_not_living_at_home.xlsx"
    )

    # --- Prepare SU data ---
    su_df = su_df[["Aar", "SU_pr_student"]].copy()
    su_df = su_df.sort_values("Aar")
    su_df["SU_growth_pct"] = su_df["SU_pr_student"].pct_change() * 100
    su_df["Year"] = su_df["Aar"].astype(int)

    # --- Load Salary data for same years ---
    wage_category = "standardberegnet timefortjeneste"
    salary_data = []
    for year in su_df["Year"]:
        df, error = load_salary_data("All", str(year), wage_category)
        if df is not None:
            avg_salary = df["Timefortjeneste (kr)"].mean()
            salary_data.append({"Year": year, "Avg Salary": round(avg_salary, 1)})

    salary_df = pd.DataFrame(salary_data)
    salary_df = salary_df.sort_values("Year")
    salary_df["Salary_Growth_pct"] = salary_df["Avg Salary"].pct_change() * 100

    # --- Merge both ---
    combined = pd.merge(su_df, salary_df, on="Year", how="inner")
    combined["Real_Salary_Growth_vs_SU"] = combined["Salary_Growth_pct"] - combined["SU_growth_pct"]

    # --- Year filter ---
    available_years = combined["Year"].tolist()
    selected_years = st.multiselect(
        "Select years to include:",
        options=available_years,
        default=available_years
    )
    combined = combined[combined["Year"].isin(selected_years)]
    if combined.empty:
        st.warning("No data for selected years.")
        return

    # --- Main chart: SU value and growth comparison ---
    st.subheader("📈 SU Amount and Growth vs. Salary Growth")
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(combined["Year"], combined["SU_pr_student"], marker="o", color="teal", label="SU per Student (DKK)")
    ax1.set_ylabel("SU per Student (DKK)", color="teal")
    ax1.tick_params(axis='y', labelcolor="teal")

    ax2 = ax1.twinx()
    ax2.plot(combined["Year"], combined["Salary_Growth_pct"], marker="^", color="purple", label="Salary Growth (%)")
    ax2.plot(combined["Year"], combined["SU_growth_pct"], marker="s", color="orange", label="SU Growth (%)")
    ax2.plot(combined["Year"], combined["Real_Salary_Growth_vs_SU"], marker="d", color="green", label="Real Salary Growth (vs SU)")
    ax2.set_ylabel("Percent Change (%)")
    ax2.tick_params(axis='y')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=8)

    plt.title("SU vs. Salary Growth Rates")
    ax1.set_xlabel("Year")
    ax1.grid(True)
    fig.tight_layout()
    st.pyplot(fig)

    st.markdown("""
    📊 **Explanation:**  
    - **Teal**: SU amount per student (left axis)  
    - **Orange**: SU year-over-year growth  
    - **Purple**: Salary growth percentage  
    - **Green**: Difference between salary growth and SU growth — a measure of relative improvement in wages vs. SU  
    """)

    # --- Bar chart: SU growth ---
    st.markdown("### 🟧 SU Growth (%)")
    fig_su, ax_su = plt.subplots()
    ax_su.bar(combined["Year"], combined["SU_growth_pct"], color="orange")
    ax_su.axhline(0, color="gray", linestyle="--")
    ax_su.set_ylabel("Growth (%)")
    ax_su.set_title("Annual SU Growth")
    st.pyplot(fig_su)

    st.markdown("""
    🧾 **Insight:**  
    Shows how much SU increased from year to year.  
    If values are flat or negative, students’ income didn't grow or declined.
    """)

    # --- Bar chart: Salary growth ---
    st.markdown("### 📈 Salary Growth (%)")
    fig_sal, ax_sal = plt.subplots()
    ax_sal.bar(combined["Year"], combined["Salary_Growth_pct"], color="skyblue")
    ax_sal.axhline(0, color="gray", linestyle="--")
    ax_sal.set_ylabel("Growth (%)")
    ax_sal.set_title("Annual Salary Growth")
    st.pyplot(fig_sal)

    st.markdown("""
    📘 **Insight:**  
    Indicates whether salaries kept pace or lagged behind inflation and SU adjustments.  
    """)

    # --- Real Salary vs SU growth line ---
    st.markdown("### 💶 Real Salary Growth vs SU")
    fig_real, ax_real = plt.subplots()
    ax_real.plot(combined["Year"], combined["Real_Salary_Growth_vs_SU"], color="green", marker="d")
    ax_real.axhline(0, color="red", linestyle="--")
    ax_real.set_ylabel("Difference (%)")
    ax_real.set_title("Salary Growth – SU Growth")
    st.pyplot(fig_real)

    st.markdown("""
    🧠 **Interpretation:**  
    This shows whether salary growth was higher (positive) or lower (negative) than SU growth.  
    Useful to understand economic pressure on working citizens compared to students.
    """)

    # --- Data table ---
    with st.expander("📄 View Data Table"):
        st.markdown("""
        This table summarizes key indicators:
        - SU per student (DKK)
        - SU growth (%)
        - Average hourly salary (DKK)
        - Salary growth (%)
        - Real salary growth relative to SU
        """)
        st.dataframe(combined, use_container_width=True)

    # --- Latest year insights ---
    latest = combined.iloc[-1]
    st.markdown(f"### Summary – {int(latest['Year'])}")
    st.markdown(f"- SU: **{latest['SU_pr_student']:.0f} kr/student**")
    st.markdown(f"- SU Growth: **{latest['SU_growth_pct']:.2f}%**")
    st.markdown(f"- Salary Growth: **{latest['Salary_Growth_pct']:.2f}%**")
    st.markdown(f"- Real Salary Growth vs SU: **{latest['Real_Salary_Growth_vs_SU']:.2f}%**")

    if latest["Real_Salary_Growth_vs_SU"] > 0:
        st.success("In this year, salary growth outpaced SU increase.")
    else:
        st.error("In this year, SU increased more than salary — reducing relative purchasing power of workers.")
