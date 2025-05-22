# --- STREAMLIT APP ---
st.title("📈 Food Price Development in Denmark")

# Dropdown for selecting product
product_list = df_melted['Product'].dropna().unique()
selected_product = st.selectbox("Choose a product to view:", product_list)

# Filter data
filtered = df_melted[df_melted['Product'] == selected_product]

# Plot
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(filtered['Year'], filtered['Change (%)'], marker='o', linestyle='-', color='royalblue')

# Add value labels
for i, row in filtered.iterrows():
    ax.text(row['Year'], row['Change (%)'] + 0.5, f"{row['Change (%)']:.1f}%", ha='center', fontsize=8)

# Decorations
ax.axhline(0, color='gray', linestyle='--', linewidth=1)
ax.set_title(f"Annual Price Change: {selected_product}")
ax.set_ylabel("Change (%)")
ax.set_xlabel("Year (June)")
ax.grid(True)

# Show plot
st.pyplot(fig)
