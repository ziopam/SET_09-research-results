import streamlit as st
import matplotlib.pyplot as plt

def parse_file(file_content):
    lines = file_content.strip().split('\n')
    if len(lines) < 6:
        st.warning("Файл должен содержать минимум 6 строк.")
        return None

    results = []
    for line in lines[:6]:
        nums = [float(x.strip()) for x in line.strip().split(';') if x.strip()]
        results.append(nums)
    return results

# Отрисовка 6 графиков
def plot_graphs(file_data, sizes, titles, ylabel, convert_to_ms=False):
    fig, axes = plt.subplots(3, 2, figsize=(16, 18))
    axes = axes.flatten()

    for idx, ax in enumerate(axes):
        for filename, result in file_data.items():
            data = result[idx]
            if convert_to_ms:
                data = [val / 1_000_000.0 for val in data]
            ax.plot(sizes, data, label=filename, marker='o')
        ax.set_title(titles[idx])
        ax.set_xlabel("Размер массива")
        ax.set_ylabel(ylabel)
        ax.grid(True)
        ax.legend()

    st.pyplot(fig)

# Названия графиков
graph_titles = [
    "Случайные строки",
    "Обратные строки",
    "Почти отсортированные строки",
    "Случайные строки (с префиксами)",
    "Обратные строки (с префиксами)",
    "Почти отсортированные строки (с префиксами)"
]

sizes = list(range(100, 3100, 100))

# ==== UI ====

st.title("Сравнение сортировок")

# === Блок 1: время выполнения ===
st.header("Время выполнения")

uploaded_time_files = st.file_uploader("Загрузите файлы со временем выполнения", type="txt", accept_multiple_files=True)

time_data = {}
if uploaded_time_files:
    for file in uploaded_time_files:
        content = file.read().decode("utf-8")
        parsed = parse_file(content)
        if parsed:
            time_data[file.name] = parsed

    if time_data:
        plot_graphs(time_data, sizes, graph_titles, ylabel="Время (мс)", convert_to_ms=True)

# === Блок 2: количество сравнений ===
st.header("Количество сравнений")

uploaded_comp_files = st.file_uploader("Загрузите файлы с количеством сравнений", type="txt", accept_multiple_files=True, key="comparisons")

comp_data = {}
if uploaded_comp_files:
    for file in uploaded_comp_files:
        content = file.read().decode("utf-8")
        parsed = parse_file(content)
        if parsed:
            comp_data[file.name] = parsed

    if comp_data:
        plot_graphs(comp_data, sizes, graph_titles, ylabel="Сравнения", convert_to_ms=False)
