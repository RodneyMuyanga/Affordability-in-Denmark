import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Plot line chart for SU metrics
def plot_line_chart(df_filtered):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_filtered['Aar'], df_filtered['SU_pr_student'], marker='o', color='teal', label='Total SU per student')
    ax.plot(df_filtered['Aar'], df_filtered['SU_pr_handicap'], marker='o', color='orange', label='Handicap tillæg per student')
    ax.plot(df_filtered['Aar'], df_filtered['SU_pr_forsorger'], marker='o', color='purple', label='Forsørger tillæg per student')
    ax.set_xlabel('Year')
    ax.set_ylabel('Amount (DKK)')
    ax.set_title('Average SU per Student Over Time')
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    st.pyplot(fig)

# Summary statistics under the line chart
def show_conclusions_for_plot_line_chart(df_filtered):
    st.markdown("**Conclusions:**")
    st.write(f"Average SU per student over selected years: {df_filtered['SU_pr_student'].mean():,.0f} DKK")
    st.write(f"Average Handicap tillæg per eligible student: {df_filtered['SU_pr_handicap'].mean():,.0f} DKK")
    st.write(f"Average Forsørger tillæg per eligible student: {df_filtered['SU_pr_forsorger'].mean():,.0f} DKK")

# Boxplot for distribution across years
def plot_boxplot(df_filtered):
    data = pd.melt(df_filtered,
                   id_vars='Aar',
                   value_vars=['SU_pr_student', 'SU_pr_handicap', 'SU_pr_forsorger'],
                   var_name='Type',
                   value_name='Amount')
    type_order = ['SU_pr_student', 'SU_pr_handicap', 'SU_pr_forsorger']
    labels = ['Total SU', 'Handicap Tillæg', 'Forsørger Tillæg']
    data['Type'] = pd.Categorical(data['Type'], categories=type_order, ordered=True)
    data['Type'] = data['Type'].cat.rename_categories(labels)

    fig, ax = plt.subplots(figsize=(14, 7))
    sns.boxplot(x='Aar', y='Amount', hue='Type', data=data, ax=ax, palette='Set2')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_title('Distribution of SU Types per Year')
    fig.tight_layout()
    st.pyplot(fig)

    if st.checkbox("Show boxplot data summary"):
        st.dataframe(data.groupby('Type')['Amount'].describe())

# Correlation matrix of selected features
def plot_correlation_heatmap(df):
    st.subheader("Correlation Heatmap (Selected Features)")
    cols = ['Aar', 'Antal_stoettemodtagere', 'Antal_handicap_tillaeg', 'Antal_forsorger_tillaeg', 'SU_pr_student']
    corr = df[cols].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax, annot_kws={"size": 10})
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    ax.set_title("Correlation Matrix (Selected Features)")
    st.pyplot(fig)

# Calculate year-over-year growth rates
def calculate_growth_rates(df, columns):
    growth_df = df[['Aar'] + columns].copy()
    for col in columns:
        growth_df[f'{col}_growth_rate'] = growth_df[col].pct_change() * 100  # percent growth
    return growth_df

# Display growth rate plots and table
def show_growth_rates(df):
    st.subheader("Year-over-Year Growth Rates (%)")
    columns = ['SU_pr_student', 'SU_pr_handicap', 'SU_pr_forsorger']
    growth_df = calculate_growth_rates(df, columns)

    if st.checkbox("Show growth rate table"):
        st.dataframe(growth_df[['Aar'] + [f'{col}_growth_rate' for col in columns]].round(2))

    if st.checkbox("Plot growth rates"):
        fig, ax = plt.subplots(figsize=(10, 5))
        for col, label, color in zip(columns,
                                     ['Total SU', 'Handicap Tillæg', 'Forsørger Tillæg'],
                                     ['teal', 'orange', 'purple']):
            ax.plot(growth_df['Aar'], growth_df[f'{col}_growth_rate'], marker='o', label=label, color=color)
        ax.set_ylabel('Growth Rate (%)')
        ax.set_title('Year-over-Year Growth in SU per Student Type')
        ax.axhline(0, color='gray', linestyle='--')
        ax.legend()
        ax.grid(True)
        fig.tight_layout()
        st.pyplot(fig)

# Show total growth and CAGR for SU metrics (with checkbox)
def show_su_growth_summary(df):
    def calc_growth_stats(series, label):
        start_val = series.iloc[0]
        end_val = series.iloc[-1]
        years = series.index[-1] - series.index[0]

        if 'Aar' in df.columns:
            years = df['Aar'].iloc[-1] - df['Aar'].iloc[0]

        total_growth = ((end_val - start_val) / start_val) * 100 if start_val != 0 else float('nan')
        cagr = ((end_val / start_val) ** (1 / years) - 1) * 100 if start_val > 0 and years > 0 else float('nan')

        st.markdown(f"📊 **{label}:**")
        st.write(f"Total growth: {total_growth:.2f}%")
        st.write(f"CAGR: {cagr:.2f}% per year\n")

    if st.checkbox("Show SU Growth Summary"):
        st.subheader("SU Growth Summary")
        calc_growth_stats(df['SU_pr_student'], "Total SU per Student")
        calc_growth_stats(df['SU_pr_handicap'], "Handicap Tillæg per Student")
        calc_growth_stats(df['SU_pr_forsorger'], "Forsørger Tillæg per Student")
