import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# --- Function to generate dataset ---
def generate_data():
    min_val = random.randint(50, 70)
    max_val = min_val + random.randint(30, 40)
    data = np.random.randint(min_val, max_val + 1, size=21)
    return np.sort(data)

# --- Function to calculate quartiles and descriptors ---
def calculate_descriptors(data):
    q1 = int(np.percentile(data, 25, method="midpoint"))
    median = int(np.percentile(data, 50, method="midpoint"))
    q3 = int(np.percentile(data, 75, method="midpoint"))
    return {
        "Minimum": int(np.min(data)),
        "Q1": q1,
        "Median": median,
        "Q3": q3,
        "Maksimum": int(np.max(data)),
    }

# --- Initialize session state ---
if "data" not in st.session_state or st.button("Ny opgave"):
    st.session_state["data"] = generate_data()
    st.session_state["answers"] = calculate_descriptors(st.session_state["data"])
    st.session_state["checked"] = False

# --- Page config ---
st.set_page_config(page_title="Aflæs Boksplot", layout="wide")

# --- Title ---
st.markdown("## 📊 Aflæs et boksplot")

# --- Plotting boxplot ---
fig, ax = plt.subplots(figsize=(6, 2))
ax.boxplot(st.session_state["data"], vert=False, patch_artist=True,
           boxprops=dict(facecolor='lightblue', color='black'),
           medianprops=dict(color='black', linewidth=2),
           whiskerprops=dict(color='black'),
           capprops=dict(color='black'))

# Axis settings
data_min = int(np.min(st.session_state["data"]))
data_max = int(np.max(st.session_state["data"]))
ax.set_xlim(data_min - 1, data_max + 1)
ax.set_xticks(np.arange(data_min - 1, data_max + 2, 1), minor=True)
ax.set_xticks(range(((data_min - 1) // 5) * 5, data_max + 2, 5), minor=False)
ax.grid(True, axis='x', which='both', linestyle=':', linewidth=0.5)
ax.get_yaxis().set_visible(False)

st.pyplot(fig)

# --- Sidebar Input ---
with st.sidebar:
    st.markdown("### ✏️ Aflæs værdier")

    # Header row
    col_labels = st.columns(5)
    labels = ["Min", "Q1", "Median", "Q3", "Maks"]
    for col, label in zip(col_labels, labels):
        col.markdown(f"<div style='text-align: center'><b>{label}</b></div>", unsafe_allow_html=True)

    # Input fields
    cols = st.columns(5)
    user_input = {}
    for col, label in zip(cols, labels):
        with col:
            user_input[label] = st.text_input(
                label=label,
                key=f"input_{label}",
                label_visibility="collapsed",
                placeholder="",
            )

    # Check answers
    if st.button("Tjek svar"):
        all_correct = True
        label_map = {
            "Min": "Minimum",
            "Q1": "Q1",
            "Median": "Median",
            "Q3": "Q3",
            "Maks": "Maksimum"
        }
        for short_label in labels:
            label = label_map[short_label]
            correct_val = st.session_state["answers"][label]
            try:
                user_val = int(user_input[short_label])
                if user_val == correct_val:
                    st.success(f"{label}: ✅ Korrekt")
                else:
                    st.error(f"{label}: ❌ Forkert (rigtigt svar: {correct_val})")
                    all_correct = False
            except ValueError:
                st.error(f"{label}: ⚠️ Indtast et heltal")
                all_correct = False

        if all_correct:
            st.balloons()
            st.success("Super godt! Alle værdier er korrekte 🎉")

    # License and credit
    st.markdown("---")
    st.markdown("### ℹ️ Licens og kredit")
    st.markdown(
        "Denne opgave er udgivet under [MIT-licensen](https://opensource.org/licenses/MIT).  \n"
        "Udviklet af Jens Kaalby Thomsen."
    )
