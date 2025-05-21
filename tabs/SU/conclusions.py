import streamlit as st

def show_conclusions(df_filtered):
    st.markdown(
        """
        **Insights:**
        - Total SU per student has steadily increased since 2000.
        - Handicap and forsørger allowances vary more significantly.
        - Correlations indicate that as total SU increases, the loan portion tends to be relatively lower.
        """
    )

def show_summary_stats(df_filtered):
    st.write(df_filtered.describe())

def show_final_conclusion(df_filtered):
    st.subheader("📘 Final Conclusion & Trends")

    def calculate_growth(col):
        start_year, end_year = df_filtered['Aar'].iloc[0], df_filtered['Aar'].iloc[-1]
        start_val, end_val = df_filtered[col].iloc[0], df_filtered[col].iloc[-1]
        n_years = end_year - start_year
        if start_val > 0 and n_years > 0:
            cagr = (end_val / start_val) ** (1 / n_years) - 1
            total_growth = (end_val - start_val) / start_val
            return {
                'Start': start_val,
                'End': end_val,
                'CAGR': cagr,
                'Total Growth': total_growth
            }
        return None

    stats = {
        'SU_pr_student': calculate_growth('SU_pr_student'),
        'SU_pr_handicap': calculate_growth('SU_pr_handicap'),
        'SU_pr_forsorger': calculate_growth('SU_pr_forsorger')
    }

    for label, result in stats.items():
        if result:
            st.markdown(f"**{label.replace('_', ' ').title()}**")
            st.write(f"- From {result['Start']:,.0f} DKK to {result['End']:,.0f} DKK")
            st.write(f"- Total Growth: {result['Total Growth']*100:.2f}%")
            st.write(f"- Average Annual Growth: {result['CAGR']*100:.2f}% per year")

    max_growth_key = max(stats, key=lambda k: stats[k]['CAGR'] if stats[k] else -1)
    st.success(f"📈 The fastest growing SU component is **{max_growth_key.replace('_', ' ').title()}**.")

