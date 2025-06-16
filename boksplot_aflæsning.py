import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Præcist Boksplot Træning", layout="centered")


# Mindre overskrift med markdown
st.markdown("## 📦 Træn aflæsning af boksplot")
st.write("Aflæs værdierne for minimum, Q1, median, Q3 og maksimum fra boksplottet og skriv dem ind.")

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
    minimum = int(data.min())
    maksimum = int(data.max())
    Q1 = int(np.percentile(data, 25, method='nearest'))
    median = int(np.percentile(data, 50, method='nearest'))
    Q3 = int(np.percentile(data, 75, method='nearest'))
    return {
        "Minimum": minimum,
        "Q1": Q1,
        "Median": median,
        "Q3": Q3,
        "Maksimum": maksimum,
    }

def plot_precise_boxplot(ax, stats, x_min, x_max):
    y_center = 0.5
    box_height = 0.3

    ax.plot([stats["Minimum"], stats["Q1"]], [y_center, y_center], color="black", lw=2)
    ax.plot([stats["Q3"], stats["Maksimum"]], [y_center, y_center], color="black", lw=2)

    cap_height = box_height / 2
    ax.plot([stats["Minimum"], stats["Minimum"]], [y_center - cap_height, y_center + cap_height], color="black", lw=2)
    ax.plot([stats["Maksimum"], stats["Maksimum"]], [y_center - cap_height, y_center + cap_height], color="black", lw=2)

    box_left = stats["Q1"]
    box_right = stats["Q3"]
    rect = plt.Rectangle((box_left, y_center - box_height / 2),
                         box_right - box_left,
                         box_height,
                         facecolor="skyblue",
                         edgecolor="black",
                         lw=2)
    ax.add_patch(rect)

    ax.plot([stats["Median"], stats["Median"]],
            [y_center - box_height / 2, y_center + box_height / 2],
            color="black", lw=2)

    ax.set_ylim(0, 1)
    ax.set_xlim(x_min, x_max)
    ax.set_yticks([])
    ax.set_xlabel("Værdi")

    major_ticks = np.arange(round_down_5(x_min), round_up_5(x_max) + 1, 5)
    ax.set_xticks(major_ticks)

    minor_ticks = np.arange(round_down_5(x_min), round_up_5(x_max) + 1, 1)
    ax.set_xticks(minor_ticks, minor=True)

    ax.tick_params(axis='x', which='minor', length=4, color='gray')
    ax.grid(axis='x', which='major', linestyle='--', alpha=0.5)

if "data" not in st.session_state or st.button("🔁 Ny opgave"):
    data = generate_data()
    st.session_state["data"] = data
    st.session_state["checked"] = False

data = st.session_state["data"]
answers = calculate_integer_quartiles(data)
st.session_state["answers"] = answers

x_min = answers["Minimum"] - 1
x_max = answers["Maksimum"] + 1

st.markdown(f"🔢 Antal tal i datasættet: **{len(data)}**")

fig, ax = plt.subplots(figsize=(8, 2))
plot_precise_boxplot(ax, answers, x_min, x_max)
st.pyplot(fig)


# Brugerinput i sidebar

with st.sidebar:
    st.markdown("### ✏️ Aflæs værdier")

    # Overskrift over felterne
    st.markdown("**Indtast værdier for:**")
    col_labels = st.columns(5)
    labels = ["Min", "Q1", "Median", "Q3", "Maks"]
    for col, label in zip(col_labels, labels):
        col.markdown(f"<div style='text-align: center'><b>{label}</b></div>", unsafe_allow_html=True)

    # Inputfelter under overskrifterne
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

    # Tjek svar
    if st.button("Tjek svar"):
        all_correct = True
        mapping = {
            "min": "Minimum",
            "Q1": "Q1",
            "median": "Median",
            "Q3": "Q3",
            "maks": "Maksimum"
        }

        for short_label in labels:
            label = mapping[short_label]
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

# Licens og kredit i sidebar
with st.sidebar:
    st.markdown("### ℹ️ Licens og kredit")
    st.markdown(
        "Denne opgave er udgivet under [MIT-licensen](https://opensource.org/licenses/MIT).  \n"
        "Udviklet af Jens Kaalby Thomsen."
    )
