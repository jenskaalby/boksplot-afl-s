import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Boksplot træning", layout="wide")

# CSS for mindre inputfelter
st.markdown("""
    <style>
    .small-input input {
        height: 2em !important;
        padding: 3px !important;
        font-size: 0.9em !important;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Funktioner
def round_down_5(x):
    return x - (x % 5)

def round_up_5(x):
    return x + (5 - x % 5) if x % 5 != 0 else x

def generate_data():
    min_val = np.random.randint(0, 71)
    range_width = np.random.randint(30, 41)
    max_val = min_val + range_width
    size = np.random.randint(10, 20)
    data = np.random.randint(min_val, max_val + 1, size=size)
    return data

def calculate_integer_quartiles(data):
    return {
        "Minimum": int(data.min()),
        "Q1": int(np.percentile(data, 25, method='nearest')),
        "Median": int(np.percentile(data, 50, method='nearest')),
        "Q3": int(np.percentile(data, 75, method='nearest')),
        "Maksimum": int(data.max()),
    }

def plot_precise_boxplot(ax, stats, x_min, x_max):
    y = 0.5
    h = 0.3

    ax.plot([stats["Minimum"], stats["Q1"]], [y, y], color="black", lw=2)
    ax.plot([stats["Q3"], stats["Maksimum"]], [y, y], color="black", lw=2)

    for bound in ["Minimum", "Maksimum"]:
        ax.plot([stats[bound], stats[bound]], [y - h/2, y + h/2], color="black", lw=2)

    rect = plt.Rectangle((stats["Q1"], y - h/2), stats["Q3"] - stats["Q1"], h,
                         facecolor="skyblue", edgecolor="black", lw=2)
    ax.add_patch(rect)

    ax.plot([stats["Median"], stats["Median"]], [y - h/2, y + h/2], color="black", lw=2)

    ax.set_ylim(0, 1)
    ax.set_xlim(x_min, x_max)
    ax.set_yticks([])
    ax.set_xticks(np.arange(round_down_5(x_min), round_up_5(x_max) + 1, 5))
    ax.set_xticks(np.arange(x_min, x_max + 1, 1), minor=True)
    ax.tick_params(axis='x', which='minor', length=3, color='gray')
    ax.grid(True, axis='x', which='major', linestyle='--', alpha=0.5)
    ax.set_xlabel("Værdi")

# Init session state
if "data" not in st.session_state or st.button("🔁 Ny opgave"):
    st.session_state["data"] = generate_data()
    st.session_state["answers"] = calculate_integer_quartiles(st.session_state["data"])
    st.session_state["checked"] = False

data = st.session_state["data"]
answers = st.session_state["answers"]

x_min = answers["Minimum"] - 1
x_max = answers["Maksimum"] + 1

# --- Overskrift og plot ---
st.markdown("## 📊 Aflæs et boksplot")
fig, ax = plt.subplots(figsize=(8, 1.5))
plot_precise_boxplot(ax, answers, x_min, x_max)
st.pyplot(fig)

st.markdown(f"**🔢 Antal observationer i datasættet:** {len(data)}")

# --- Brugerinput vandret ---
st.markdown("### ✏️ Indtast aflæste værdier")
labels = ["Minimum", "Q1", "Median", "Q3", "Maksimum"]
cols = st.columns(5)
user_input = {}

for col, label in zip(cols, labels):
    with col:
        st.markdown(f"<div style='text-align: center'><b>{label}</b></div>", unsafe_allow_html=True)
        val = st.text_input("", key=f"input_{label}", label_visibility="collapsed", placeholder="",
                            help=f"Aflæs {label.lower()}", value="", max_chars=5)
        user_input[label] = val.strip()

# --- Tjek svar ---
if st.button("Tjek svar"):
    correct = True
    for label in labels:
        correct_val = answers[label]
        try:
            val = int(user_input[label])
            if val == correct_val:
                st.success(f"{label}: ✅ Korrekt")
            else:
                st.error(f"{label}: ❌ Forkert (rigtigt svar: {correct_val})")
                correct = False
        except ValueError:
            st.error(f"{label}: ⚠️ Indtast et heltal")
            correct = False

    if correct:
        st.balloons()
        st.success("🎉 Alle værdier er korrekte!")

# --- Sidebar med licens ---
with st.sidebar:
    st.markdown("### ℹ️ Licens og kredit")
    st.markdown(
        "Denne opgave er udgivet under [MIT-licensen](https://opensource.org/licenses/MIT).  \n"
        "Udviklet af Jens Kaalby Thomsen."
    )
