"""
MathTutor Pro — Платформа для репетитора
Запуск: streamlit run math_tutor.py
Залежності: pip install streamlit plotly pandas
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, date, timedelta
import random
import json

# ─────────────────────────────────────────
# Конфігурація сторінки
# ─────────────────────────────────────────
st.set_page_config(
    page_title="MathTutor Pro",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# CSS стилізація
# ─────────────────────────────────────────
st.markdown("""
<style>
/* Загальні скидання */
[data-testid="stAppViewContainer"] { background: #f8f7f4; }
[data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #e8e6e0; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { font-size: 13px; }

/* Метрики */
[data-testid="metric-container"] {
    background: #f0eeea;
    border-radius: 10px;
    padding: 12px 16px;
    border: none;
}
[data-testid="metric-container"] label { font-size: 12px !important; color: #888; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { font-size: 24px !important; }

/* Картки */
.card { background: white; border-radius: 12px; padding: 16px; border: 0.5px solid #e8e6e0; margin-bottom: 12px; }
.card-title { font-size: 11px; font-weight: 600; color: #888; text-transform: uppercase; letter-spacing: .06em; margin-bottom: 10px; }

/* Розклад */
.lesson-row { display: flex; align-items: center; gap: 10px; padding: 8px 0; border-bottom: 0.5px solid #f0eeea; font-size: 13px; }
.lesson-row:last-child { border-bottom: none; }
.lesson-time { color: #aaa; min-width: 46px; font-size: 12px; }
.lesson-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.dot-done    { background: #d0d0d0; }
.dot-active  { background: #1D9E75; }
.dot-upcoming{ background: #534AB7; }
.lesson-name { font-weight: 500; }
.lesson-topic{ color: #888; font-size: 11px; }

/* Бейджі */
.badge { display: inline-flex; align-items: center; padding: 2px 8px; border-radius: 6px; font-size: 11px; font-weight: 500; }
.badge-green  { background:#E1F5EE; color:#085041; }
.badge-purple { background:#EEEDFE; color:#26215C; }
.badge-amber  { background:#FAEEDA; color:#633806; }
.badge-red    { background:#FCEBEB; color:#791F1F; }

/* Учні */
.student-card { background: white; border: 0.5px solid #e8e6e0; border-radius: 10px; padding: 14px; cursor: pointer; transition: border-color .2s, box-shadow .2s; }
.student-card:hover { border-color: #534AB7; box-shadow: 0 2px 12px rgba(83,74,183,.08); }
.avatar { width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 500; margin-bottom: 8px; }

/* Сповіщення */
.notif { display:flex; gap:10px; padding:8px 0; border-bottom:0.5px solid #f0eeea; }
.notif:last-child { border-bottom:none; }
.notif-icon { width:28px; height:28px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:14px; flex-shrink:0; }
.notif-text { font-size:12px; color:#555; line-height:1.5; }
.notif-time { font-size:11px; color:#aaa; margin-top:2px; }

/* Теплова карта */
.hm-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(80px, 1fr)); gap: 6px; margin-top: 6px; }
.hm-cell { border-radius: 6px; padding: 8px 6px; text-align: center; font-size: 11px; font-weight: 500; cursor: pointer; }

/* Бібліотека */
.lib-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 8px; }
.lib-item { background:white; border:0.5px solid #e8e6e0; border-radius:8px; padding:12px; cursor:pointer; transition:border-color .15s; }
.lib-item:hover { border-color:#534AB7; }
.lib-icon { font-size:22px; margin-bottom:5px; }
.lib-name { font-size:12px; font-weight:500; color:#1a1a1a; }
.lib-meta { font-size:11px; color:#aaa; margin-top:2px; }

/* Фінанси */
.finance-row { display:flex; justify-content:space-between; align-items:center; padding:9px 0; border-bottom:0.5px solid #f0eeea; font-size:13px; }
.finance-row:last-child { border-bottom:none; }

/* Кнопки навігації в sidebar */
div[data-testid="stRadio"] > div { gap: 4px; }
div[data-testid="stRadio"] label { background: transparent; border-radius: 6px; padding: 7px 12px !important; font-size: 13px; cursor: pointer; transition: background .15s; width: 100%; }
div[data-testid="stRadio"] label:hover { background: #f0eeea; }

/* Кнопки streamlit */
.stButton > button { border-radius: 8px; font-size: 12px; border: 0.5px solid #d0cec8; }
.stButton > button:hover { border-color: #534AB7; color: #534AB7; }
div[data-testid="stExpander"] { border: 0.5px solid #e8e6e0 !important; border-radius: 10px !important; background: white; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# Дані (state)
# ─────────────────────────────────────────
def load_students():
    return [
        {
            "id": 1, "name": "Дарія Костур", "initials": "ДК",
            "color_bg": "#EEEDFE", "color_txt": "#3C3489",
            "goal": "Школа · 6 клас (Математика)", "level": "Середній",
            "progress": 65, "lessons_total": 8, "rate": 350,
            "paid_lessons": 2, "phone": "+380 99 123-45-67",
            "email": "daria.k@ukr.net",
            "notes": "Повторення звичайних дробів, підготовка до контрольної роботи.",
            "topics": {"Звичайні дроби": 80, "Десяткові дроби": 90, "Відсотки": 45, "Рівняння": 60, "Геометрія (база)": 50},
            "test_scores": [50, 55, 60, 65],
        },
        {
            "id": 2, "name": "Анастасія", "initials": "АН",
            "color_bg": "#E1F5EE", "color_txt": "#085041",
            "goal": "Технікум (Польща) · Математика", "level": "Високий",
            "progress": 82, "lessons_total": 14, "rate": 500,
            "paid_lessons": 4, "phone": "+380 67 987-65-43",
            "email": "anastasia.pl@gmail.com",
            "notes": "Вища математика, польська термінологія. Акцент на функції та тригонометрію.",
            "topics": {"Функції": 90, "Тригонометрія": 80, "Похідна": 75, "Інтеграли": 65, "Алгебра": 95},
            "test_scores": [70, 75, 78, 82],
        },
        {
            "id": 3, "name": "Макар", "initials": "МА",
            "color_bg": "#FAEEDA", "color_txt": "#633806",
            "goal": "Програмування · Python", "level": "Початковий",
            "progress": 45, "lessons_total": 6, "rate": 450,
            "paid_lessons": 1, "phone": "+380 63 111-22-33",
            "email": "makar.dev@gmail.com",
            "notes": "Основи Python. Працюємо над проєктами (Аналізатор та Шляхошукач).",
            "topics": {"Змінні": 90, "If/Else": 75, "Цикли for/while": 40, "Списки": 20, "Функції": 0},
            "test_scores": [25, 35, 45],
        }
    ]

def load_schedule():
    return [
        {"time": "11:00", "student": "Дарія Костур", "topic": "Звичайні дроби: Додавання", "status": "done"},
        {"time": "14:00", "student": "Анастасія", "topic": "Похідна складеної функції", "status": "active"},
        {"time": "16:30", "student": "Макар", "topic": "Цикли for та while", "status": "upcoming"},
    ]

def load_notifications():
    return [
        {"icon": "📋", "style": "background:#EEEDFE;color:#534AB7", "text": "<strong>Макар</strong> надіслав код проєкту на перевірку", "time": "10 хвилин тому"},
        {"icon": "💬", "style": "background:#E1F5EE;color:#0F6E56", "text": "<strong>Анастасія</strong> запитує переклад терміну «Calka»", "time": "1 годину тому"},
        {"icon": "💰", "style": "background:#FAEEDA;color:#854F0B", "text": "<strong>Дарія Костур</strong> — залишився 1 оплачений урок", "time": "Вчора"},
    ]

def load_library():
    return [
        {"icon": "📄", "name": "НМТ 2024 — збірник завдань", "meta": "PDF · 48 стор.", "type": "pdf"},
        {"icon": "📊", "name": "Тригонометрія — презентація", "meta": "PPT · 32 слайди", "type": "ppt"},
        {"icon": "✅", "name": "Тест: Інтеграли", "meta": "Квіз · 15 питань", "type": "quiz"},
        {"icon": "📄", "name": "Стереометрія", "meta": "PDF · 24 стор.", "type": "pdf"},
        {"icon": "✅", "name": "Тест: Рівняння", "meta": "Квіз · 20 питань", "type": "quiz"},
        {"icon": "🖼️", "name": "Геометричні моделі", "meta": "Зображення · 18 шт.", "type": "img"},
        {"icon": "💻", "name": "Python: Основи синтаксису", "meta": "PPT · 20 слайдів", "type": "ppt"},
    ]


# ─────────────────────────────────────────
# Ініціалізація session state
# ─────────────────────────────────────────
if "students" not in st.session_state:
    st.session_state.students = load_students()
if "selected_student" not in st.session_state:
    st.session_state.selected_student = None
if "show_add_student" not in st.session_state:
    st.session_state.show_add_student = False
if "test_questions" not in st.session_state:
    st.session_state.test_questions = []
if "hw_items" not in st.session_state:
    st.session_state.hw_items = [
        {"student": "Анастасія", "task": "Дослідити функцію y=x^3-3x+2", "due": "сьогодні", "status": "В процесі"},
        {"student": "Макар", "task": "Написати скрипт «Аналізатор»", "due": "завтра", "status": "Здано"},
        {"student": "Дарія Костур", "task": "Задачі на відсотки № 15-20", "due": "пт", "status": "Не розпочато"},
    ]


# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:4px 0 16px;border-bottom:0.5px solid #e8e6e0;margin-bottom:12px'>
        <div style='font-size:18px;font-weight:600;color:#1a1a1a'>📐 MathTutor Pro</div>
        <div style='font-size:12px;color:#aaa;margin-top:2px'>Панель репетитора</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Навігація",
        ["🏠  Дашборд", "👥  Учні", "✏️  Дошка", "📊  Аналітика", "📚  Бібліотека", "💰  Фінанси"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    today_str = datetime.now().strftime("%A, %d %B")
    st.markdown(f"<div style='font-size:12px;color:#aaa;padding:0 4px'>{today_str}</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:13px;font-weight:500;color:#1a1a1a;padding:2px 4px 6px'>Сьогодні 3 уроки</div>", unsafe_allow_html=True)

    with st.expander("⚡ Швидкі дії"):
        if st.button("➕ Додати учня", use_container_width=True):
            st.session_state.show_add_student = True


# ─────────────────────────────────────────
# ── ДАШБОРД ────────────────────────────
# ─────────────────────────────────────────
if "Дашборд" in page:
    st.markdown("## Дашборд")

    # Метрики
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📅 Уроки сьогодні", "3", "1 завершено")
    c2.metric("👥 Активні учні", str(len(st.session_state.students)), "в базі")
    c3.metric("📋 ДЗ на перевірку", "3", "1 нове")
    total_income_projected = sum(s["lessons_total"] * s["rate"] for s in st.session_state.students)
    c4.metric("💰 Дохід (травень)", f"{total_income_projected} ₴", "прогноз")

    st.markdown("")

    col_left, col_right = st.columns(2)

    # Розклад
    with col_left:
        st.markdown("<div class='card'><div class='card-title'>Розклад на сьогодні</div>", unsafe_allow_html=True)
        for lesson in load_schedule():
            dot_class = f"dot-{lesson['status']}"
            if lesson["status"] == "done":
                badge = "<span class='badge badge-green'>✓ Завершено</span>"
            elif lesson["status"] == "active":
                badge = "<span class='badge badge-purple'>▶ Зараз</span>"
            else:
                badge = f"<span class='badge badge-amber'>⏰ {lesson['time']}</span>"

            st.markdown(f"""
            <div class='lesson-row'>
                <div class='lesson-time'>{lesson['time']}</div>
                <div class='lesson-dot {dot_class}'></div>
                <div style='flex:1'>
                    <div class='lesson-name'>{lesson['student']}</div>
                    <div class='lesson-topic'>{lesson['topic']}</div>
                </div>
                {badge}
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Сповіщення
    with col_right:
        st.markdown("<div class='card'><div class='card-title'>Сповіщення</div>", unsafe_allow_html=True)
        for n in load_notifications():
            st.markdown(f"""
            <div class='notif'>
                <div class='notif-icon' style='{n["style"]}'>{n["icon"]}</div>
                <div>
                    <div class='notif-text'>{n["text"]}</div>
                    <div class='notif-time'>{n["time"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Домашні завдання
    st.markdown("### 📋 Домашні завдання")
    hw_df = pd.DataFrame(st.session_state.hw_items)
    status_colors = {"Здано": "🟢", "В процесі": "🟡", "Не розпочато": "🔴"}
    hw_df["Статус"] = hw_df["status"].map(lambda s: f"{status_colors.get(s,'⚪')} {s}")
    hw_df = hw_df.rename(columns={"student": "Учень", "task": "Завдання", "due": "Здати до"})
    st.dataframe(hw_df[["Учень", "Завдання", "Здати до", "Статус"]], use_container_width=True, hide_index=True)

    # Мінідіаграма прогресу учнів
    st.markdown("### 📈 Прогрес учнів")
    students = st.session_state.students
    if students:
        prog_df = pd.DataFrame({
            "Учень": [s["name"].split()[0] + (" " + s["name"].split()[1][0] + "." if len(s["name"].split()) > 1 else "") for s in students],
            "Прогрес": [s["progress"] for s in students],
        })
        fig = px.bar(
            prog_df, x="Учень", y="Прогрес", color="Прогрес",
            color_continuous_scale=["#EEEDFE", "#7F77DD", "#26215C"], range_color=[0, 100], text="Прогрес",
        )
        fig.update_traces(texttemplate="%{text}%", textposition="outside", marker_line_width=0)
        fig.update_layout(
            height=260, margin=dict(l=0, r=0, t=10, b=0), plot_bgcolor="white", paper_bgcolor="white",
            coloraxis_showscale=False, yaxis=dict(range=[0, 110], showgrid=True, gridcolor="#f0eeea", title=""),
            xaxis=dict(title=""), font=dict(size=12),
        )
        st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────
# ── УЧНІ ───────────────────────────────
# ─────────────────────────────────────────
elif "Учні" in page:
    st.markdown("## 👥 Учні та Керування Базою")

    # Імпорт/Експорт
    with st.expander("💾 Резервне копіювання (Імпорт / Експорт)"):
        col_exp, col_imp = st.columns(2)
        with col_exp:
            st.download_button(
                label="📥 Завантажити файл бази (JSON)",
                data=json.dumps(st.session_state.students, ensure_ascii=False, indent=2),
                file_name="mathtutor_students.json",
                mime="application/json",
                use_container_width=True
            )
        with col_imp:
            uploaded_file = st.file_uploader("📤 Завантажити базу (JSON)", type="json", label_visibility="collapsed")
            if uploaded_file is not None:
                try:
                    imported_data = json.loads(uploaded_file.read())
                    if isinstance(imported_data, list):
                        st.session_state.students = imported_data
                        st.success("✅ Базу успішно оновлено!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Помилка імпорту: {e}")

    students = st.session_state.students

    # Додавання учня
    if st.session_state.show_add_student:
        with st.expander("➕ Новий учень", expanded=True):
            with st.form("add_student_form"):
                c1, c2 = st.columns(2)
                name = c1.text_input("Ім'я та прізвище *")
                phone = c2.text_input("Телефон")
                c3, c4 = st.columns(2)
                email = c3.text_input("Email")
                goal = c4.text_input("Мета / Напрямок навчання")
                c5, c6 = st.columns(2)
                level = c5.selectbox("Рівень", ["Початковий", "Середній", "Високий"])
                rate = c6.number_input("Вартість уроку (грн)", value=400, step=50)
                notes = st.text_area("Нотатки")
                
                submitted = st.form_submit_button("Зберегти учня", type="primary")
                if submitted and name:
                    initials = "".join(w[0].upper() for w in name.split()[:2])
                    colors = [("#EEEDFE","#3C3489"),("#E1F5EE","#085041"),("#FAEEDA","#633806"),("#FAECE7","#712B13")]
                    bg, txt = colors[len(students) % len(colors)]
                    
                    new_id = max([s["id"] for s in students] + [0]) + 1
                    st.session_state.students.append({
                        "id": new_id, "name": name, "initials": initials,
                        "color_bg": bg, "color_txt": txt, "goal": goal, "level": level,
                        "progress": 0, "lessons_total": 0, "rate": rate,
                        "paid_lessons": 0, "phone": phone, "email": email, "notes": notes,
                        "topics": {"Основи": 0},
                        "test_scores": [],
                    })
                    st.session_state.show_add_student = False
                    st.rerun()

    # Фільтри
    col_search, col_btn = st.columns([4, 1])
    search = col_search.text_input("🔍 Пошук учня...", label_visibility="collapsed", placeholder="Пошук учня...")
    if col_btn.button("➕ Додати учня", use_container_width=True):
        st.session_state.show_add_student = True

    filtered = [s for s in students if search.lower() in s["name"].lower()]

    # Картки учнів (3 в рядок)
    for i in range(0, len(filtered), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(filtered):
                s = filtered[i + j]
                level_badge = {
                    "Початковий": "<span class='badge badge-red'>Початковий</span>",
                    "Середній":   "<span class='badge badge-amber'>Середній</span>",
                    "Високий":    "<span class='badge badge-green'>Високий</span>",
                }.get(s["level"], "")
                
                paid_badge = (
                    "<span class='badge badge-red'>Не оплачено</span>" if s["paid_lessons"] == 0
                    else f"<span class='badge badge-green'>Оплачено {s['paid_lessons']} ур.</span>" if s["paid_lessons"] >= 3
                    else f"<span class='badge badge-amber'>Залишилось {s['paid_lessons']} ур.</span>"
                )
                bar_w = s["progress"]
                col.markdown(f"""
                <div class='student-card'>
                    <div style='display:flex;align-items:center;gap:10px;margin-bottom:8px'>
                        <div class='avatar' style='background:{s["color_bg"]};color:{s["color_txt"]}'>{s["initials"]}</div>
                        <div>
                            <div style='font-size:14px;font-weight:500;color:#1a1a1a'>{s["name"]}</div>
                            <div style='font-size:11px;color:#aaa'>{s["goal"]}</div>
                        </div>
                    </div>
                    <div style='display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px'>
                        {level_badge} {paid_badge}
                    </div>
                    <div style='font-size:12px;color:#888;margin-bottom:4px'>Загальний прогрес: {s["progress"]}%</div>
                    <div style='background:#f0eeea;height:5px;border-radius:3px;overflow:hidden'>
                        <div style='width:{bar_w}%;height:100%;background:#534AB7;border-radius:3px'></div>
                    </div>
                    <div style='font-size:11px;color:#aaa;margin-top:6px'>{s["lessons_total"]} уроків · {s["rate"]} грн/урок</div>
                </div>
                """, unsafe_allow_html=True)
                if col.button("Детальніше", key=f"btn_{s['id']}", use_container_width=True):
                    st.session_state.selected_student = s["id"]

    # Відкрита картка учня
    if st.session_state.selected_student:
        s = next((x for x in students if x["id"] == st.session_state.selected_student), None)
        if s:
            st.markdown("---")
            st.markdown(f"### Профіль — {s['name']}")
            tab1, tab2, tab3 = st.tabs(["📌 Загальне", "📊 Прогрес", "💰 Оплата"])

            with tab1:
                c1, c2 = st.columns(2)
                c1.markdown(f"**Телефон:** {s['phone']}")
                c1.markdown(f"**Email:** {s['email']}")
                c1.markdown(f"**Мета:** {s['goal']}")
                c1.markdown(f"**Рівень:** {s['level']}")
                c2.markdown(f"**Уроків проведено:** {s['lessons_total']}")
                c2.markdown(f"**Вартість уроку:** {s['rate']} грн")
                c2.markdown(f"**Оплачено наперед:** {s['paid_lessons']} уроків")
                st.markdown(f"**Нотатки викладача:**")
                new_note = st.text_area("", value=s["notes"], key=f"note_{s['id']}", height=80)
                if st.button("Зберегти нотатки", key=f"save_note_{s['id']}"):
                    s["notes"] = new_note
                    st.success("Збережено!")

            with tab2:
                # Теплова карта тем
                topics = s.get("topics", {})
                colors_map = {
                    range(0, 30): ("#FCEBEB", "#791F1F"),
                    range(30, 60): ("#FAEEDA", "#633806"),
                    range(60, 80): ("#EEEDFE", "#3C3489"),
                    range(80, 101): ("#E1F5EE", "#085041"),
                }
                def get_color(v):
                    for rng, clr in colors_map.items():
                        if v in rng:
                            return clr
                    return ("#f0f0f0", "#888")

                if topics:
                    html_cells = ""
                    for topic, val in topics.items():
                        bg, txt = get_color(val)
                        html_cells += f"<div class='hm-cell' style='background:{bg};color:{txt}'><div style='font-size:10px;margin-bottom:2px'>{topic}</div><div style='font-size:14px;font-weight:600'>{val}%</div></div>"
                    st.markdown(f"<div class='hm-grid'>{html_cells}</div>", unsafe_allow_html=True)
                st.markdown("")

                # Графік динаміки
                months = ["Берез.", "Квіт.", "Трав.", "Черв.", "Лип.", "Серп."]
                scores = s.get("test_scores", [])
                n = min(len(months), len(scores))
                if n > 0:
                    fig2 = go.Figure()
                    fig2.add_trace(go.Scatter(
                        x=months[:n], y=scores[:n], mode="lines+markers+text", text=[f"{v}%" for v in scores[:n]],
                        textposition="top center", line=dict(color="#534AB7", width=2.5), marker=dict(size=7, color="#534AB7"),
                        fill="tozeroy", fillcolor="rgba(83,74,183,0.07)",
                    ))
                    fig2.update_layout(
                        title="Динаміка результатів тестів", height=220, margin=dict(l=0,r=0,t=30,b=0),
                        plot_bgcolor="white", paper_bgcolor="white", yaxis=dict(range=[0,110], gridcolor="#f0eeea", title="Бали (%)"),
                        xaxis=dict(gridcolor="#f0eeea"), font=dict(size=12), showlegend=False,
                    )
                    st.plotly_chart(fig2, use_container_width=True)

            with tab3:
                st.metric("Оплачено уроків", s["paid_lessons"])
                st.metric("Заборгованість", "0 грн" if s["paid_lessons"] > 0 else f"{s['rate']} грн", delta=None)
                n_add = st.number_input("Додати оплачених уроків", min_value=1, max_value=20, value=5, key=f"n_add_{s['id']}")
                if st.button("➕ Зарахувати оплату", key=f"pay_{s['id']}"):
                    s["paid_lessons"] += n_add
                    st.success(f"Зараховано {n_add} уроків. Разом: {s['paid_lessons']}")

            st.markdown("---")
            # Кнопки CRUD для відкритого учня
            c_edit, c_del, c_close = st.columns(3)
            
            if c_edit.button("✏️ Редагувати профіль", use_container_width=True):
                st.session_state[f"edit_mode_{s['id']}"] = not st.session_state.get(f"edit_mode_{s['id']}", False)
                
            if c_del.button("🗑 Видалити учня", type="primary", use_container_width=True):
                st.session_state.students = [x for x in st.session_state.students if x["id"] != s["id"]]
                st.session_state.selected_student = None
                st.rerun()
                
            if c_close.button("✕ Закрити картку", use_container_width=True):
                st.session_state.selected_student = None
                st.rerun()

            # Форма редагування
            if st.session_state.get(f"edit_mode_{s['id']}", False):
                with st.form(f"edit_form_{s['id']}"):
                    st.markdown("#### Редагування даних")
                    e_name = st.text_input("Ім'я", value=s["name"])
                    e_goal = st.text_input("Мета/Напрямок", value=s["goal"])
                    e_phone = st.text_input("Телефон", value=s["phone"])
                    e_rate = st.number_input("Вартість", value=s["rate"])
                    
                    if st.form_submit_button("💾 Зберегти зміни"):
                        for idx, student in enumerate(st.session_state.students):
                            if student["id"] == s["id"]:
                                st.session_state.students[idx]["name"] = e_name
                                st.session_state.students[idx]["goal"] = e_goal
                                st.session_state.students[idx]["phone"] = e_phone
                                st.session_state.students[idx]["rate"] = e_rate
                                break
                        st.session_state[f"edit_mode_{s['id']}"] = False
                        st.rerun()


# ─────────────────────────────────────────
# ── ДОШКА ──────────────────────────────
# ─────────────────────────────────────────
elif "Дошка" in page:
    st.markdown("## ✏️ Інтерактивна дошка")

    tab_wb, tab_graph, tab_geo = st.tabs(["🖊 Полотно + Формули", "📈 Графіки функцій", "📐 Геометрія"])

    with tab_wb:
        st.info("💡 Введіть формулу в полі нижче або скористайтеся готовими шаблонами для пояснення учням.")

        # Шаблони
        st.markdown("**Готові шаблони:**")
        tmpl_cols = st.columns(4)
        templates = [
            ("Теорема Піфагора", "a^2 + b^2 = c^2"),
            ("Квадратне рівняння", "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}"),
            ("Звичайний дріб", "\\frac{a}{b} + \\frac{c}{d} = \\frac{ad+bc}{bd}"),
            ("Інтеграл (Анастасія)", "\\int x^n dx = \\frac{x^{n+1}}{n+1} + C"),
        ]
        for i, (label, formula) in enumerate(templates):
            if tmpl_cols[i].button(label, key=f"tmpl_{i}", use_container_width=True):
                st.session_state.formula_input = formula

        st.markdown("---")
        st.markdown("**Введіть LaTeX-формулу:**")
        formula_val = st.session_state.get("formula_input", "")
        col_f1, col_f2 = st.columns([4, 1])
        formula = col_f1.text_input("LaTeX формула", value=formula_val, label_visibility="collapsed",
                                     placeholder=r"Приклад: \frac{a}{b} = \sqrt{x^2 + y^2}")
        render_btn = col_f2.button("▶ Показати", use_container_width=True)

        if formula:
            st.markdown("**Відображення:**")
            st.latex(formula)

        st.markdown("---")
        st.markdown("**Швидке введення елементів:**")
        c1, c2, c3, c4, c5 = st.columns(5)
        if c1.button("½ Дріб"):     st.session_state.formula_input = r"\frac{a}{b}"
        if c2.button("√ Корінь"):   st.session_state.formula_input = r"\sqrt{x}"
        if c3.button("∫ Інтеграл"): st.session_state.formula_input = r"\int_a^b f(x)\,dx"
        if c4.button("∑ Сума"):     st.session_state.formula_input = r"\sum_{i=1}^{n} a_i"
        if c5.button("Δ Ліміт"):   st.session_state.formula_input = r"\lim_{x \to \infty} f(x)"

        st.markdown("---")
        st.markdown("**Нотатки до уроку:**")
        st.text_area("", height=150, placeholder="Записуйте ключові моменти уроку, пояснення, приклади...",
                     label_visibility="collapsed")
        if st.button("💾 Зберегти нотатки уроку"):
            st.success("Нотатки збережено!")

    with tab_graph:
        st.markdown("**Графік функції**")
        import math

        c1, c2, c3 = st.columns([3, 1, 1])
        func_input = c1.text_input("Функція f(x) =", value="x**3 - 3*x + 2", label_visibility="collapsed",
                                    placeholder="sin(x), x**2, cos(x)*exp(-x/5), ...")
        x_min = c2.number_input("x від", value=-10.0, step=1.0)
        x_max = c3.number_input("x до", value=10.0, step=1.0)

        # Додаткові функції
        func2 = st.text_input("Друга функція (необов'язково)", value="", placeholder="cos(x)")

        try:
            xs = [x_min + i * (x_max - x_min) / 500 for i in range(501)]
            safe_ns = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
            safe_ns["abs"] = abs

            ys = []
            for x in xs:
                try:
                    safe_ns["x"] = x
                    ys.append(eval(func_input, {"__builtins__": {}}, safe_ns))
                except:
                    ys.append(None)

            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(x=xs, y=ys, mode="lines", name=f"f(x) = {func_input}",
                                      line=dict(color="#534AB7", width=2.5)))
            if func2.strip():
                ys2 = []
                for x in xs:
                    try:
                        safe_ns["x"] = x
                        ys2.append(eval(func2, {"__builtins__": {}}, safe_ns))
                    except:
                        ys2.append(None)
                fig3.add_trace(go.Scatter(x=xs, y=ys2, mode="lines", name=f"g(x) = {func2}",
                                          line=dict(color="#D85A30", width=2.5, dash="dash")))

            fig3.update_layout(
                height=380, margin=dict(l=0, r=0, t=10, b=0),
                plot_bgcolor="white", paper_bgcolor="white",
                xaxis=dict(zeroline=True, zerolinewidth=1.5, zerolinecolor="#aaa", gridcolor="#f0eeea", title="x"),
                yaxis=dict(zeroline=True, zerolinewidth=1.5, zerolinecolor="#aaa", gridcolor="#f0eeea", title="f(x)"),
                legend=dict(font=dict(size=12)),
                font=dict(size=12),
            )
            st.plotly_chart(fig3, use_container_width=True)
        except Exception as e:
            st.error(f"Помилка у формулі: {e}")

    with tab_geo:
        st.markdown("**Геометричні фігури та координатна площина**")
        shape = st.selectbox("Оберіть фігуру", ["Трикутник (Піфагор)", "Одиничне коло", "Парабола y=ax²+bx+c", "Вектори"])

        fig4 = go.Figure()

        if shape == "Трикутник (Піфагор)":
            a = st.slider("Катет a", 1, 10, 3)
            b = st.slider("Катет b", 1, 10, 4)
            c_hyp = round((a**2 + b**2)**0.5, 2)
            fig4.add_trace(go.Scatter(
                x=[0, a, 0, 0], y=[0, 0, b, 0],
                mode="lines+markers+text",
                text=["A", "B", "C", ""],
                textposition="top center",
                fill="toself",
                fillcolor="rgba(83,74,183,0.1)",
                line=dict(color="#534AB7", width=2),
                marker=dict(size=8, color="#534AB7"),
            ))
            fig4.add_annotation(x=a/2, y=-0.3, text=f"a = {a}", showarrow=False, font=dict(size=13))
            fig4.add_annotation(x=-0.4, y=b/2, text=f"b = {b}", showarrow=False, font=dict(size=13))
            fig4.add_annotation(x=a/2+0.3, y=b/2, text=f"c = {c_hyp}", showarrow=False, font=dict(size=13, color="#D85A30"))
            st.markdown(f"**a² + b² = c²: {a}² + {b}² = {a**2 + b**2} = {c_hyp}²**")

        elif shape == "Одиничне коло":
            import math
            theta = [i * 2 * math.pi / 100 for i in range(101)]
            fig4.add_trace(go.Scatter(x=[math.cos(t) for t in theta], y=[math.sin(t) for t in theta],
                                      mode="lines", line=dict(color="#534AB7", width=2), name="Одиничне коло"))
            angle_deg = st.slider("Кут α (градуси)", 0, 360, 45)
            angle_rad = math.radians(angle_deg)
            cx, cy = math.cos(angle_rad), math.sin(angle_rad)
            fig4.add_trace(go.Scatter(x=[0, cx], y=[0, cy], mode="lines+markers",
                                      line=dict(color="#D85A30", width=2.5),
                                      marker=dict(size=8, color="#D85A30"), name=f"α={angle_deg}°"))
            fig4.add_trace(go.Scatter(x=[cx, cx], y=[0, cy], mode="lines",
                                      line=dict(color="#1D9E75", width=1.5, dash="dash"), name=f"sin={cy:.3f}"))
            fig4.add_trace(go.Scatter(x=[0, cx], y=[cy, cy], mode="lines",
                                      line=dict(color="#BA7517", width=1.5, dash="dash"), name=f"cos={cx:.3f}"))
            st.markdown(f"**sin({angle_deg}°) = {cy:.4f}, cos({angle_deg}°) = {cx:.4f}**")

        elif shape == "Парабола y=ax²+bx+c":
            c1i, c2i, c3i = st.columns(3)
            a_p = c1i.slider("a", -3.0, 3.0, 1.0, 0.1)
            b_p = c2i.slider("b", -10.0, 10.0, 0.0, 0.5)
            c_p = c3i.slider("c", -10.0, 10.0, 0.0, 0.5)
            xs_p = [i * 0.1 - 10 for i in range(201)]
            ys_p = [a_p*x**2 + b_p*x + c_p for x in xs_p]
            fig4.add_trace(go.Scatter(x=xs_p, y=ys_p, mode="lines",
                                      line=dict(color="#534AB7", width=2.5),
                                      name=f"y = {a_p}x² + {b_p}x + {c_p}"))
            if a_p != 0:
                vx = -b_p / (2*a_p)
                vy = a_p*vx**2 + b_p*vx + c_p
                fig4.add_trace(go.Scatter(x=[vx], y=[vy], mode="markers+text",
                                          text=[f"V({vx:.1f}, {vy:.1f})"], textposition="top center",
                                          marker=dict(size=10, color="#D85A30"), name="Вершина"))

        elif shape == "Вектори":
            st.markdown("Введіть координати двох векторів:")
            c1i, c2i = st.columns(2)
            ax_v = c1i.number_input("a⃗: x", value=3.0); ay_v = c1i.number_input("a⃗: y", value=2.0)
            bx_v = c2i.number_input("b⃗: x", value=1.0); by_v = c2i.number_input("b⃗: y", value=4.0)
            for (vx, vy, name, color) in [(ax_v, ay_v, "a⃗", "#534AB7"), (bx_v, by_v, "b⃗", "#D85A30")]:
                fig4.add_trace(go.Scatter(x=[0, vx], y=[0, vy], mode="lines+markers+text",
                                          text=["", name], textposition="top center",
                                          line=dict(color=color, width=2.5),
                                          marker=dict(size=[0, 10], color=color), name=name))
            # Сума
            fig4.add_trace(go.Scatter(x=[0, ax_v+bx_v], y=[0, ay_v+by_v],
                                      mode="lines+markers+text",
                                      text=["", "a+b"], textposition="top center",
                                      line=dict(color="#1D9E75", width=2, dash="dash"),
                                      marker=dict(size=[0, 10], color="#1D9E75"), name="a⃗+b⃗"))
            dot = ax_v*bx_v + ay_v*by_v
            st.markdown(f"**Скалярний добуток a⃗·b⃗ = {dot:.2f}**")

        fig4.update_layout(
            height=360, margin=dict(l=0, r=0, t=10, b=0),
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(zeroline=True, zerolinewidth=1.5, zerolinecolor="#bbb", gridcolor="#f0eeea", title="x",
                       scaleanchor="y" if shape != "Парабола y=ax²+bx+c" else None),
            yaxis=dict(zeroline=True, zerolinewidth=1.5, zerolinecolor="#bbb", gridcolor="#f0eeea", title="y"),
            legend=dict(font=dict(size=11)),
            font=dict(size=12),
        )
        st.plotly_chart(fig4, use_container_width=True)


# ─────────────────────────────────────────
# ── АНАЛІТИКА ───────────────────────────
# ─────────────────────────────────────────
elif "Аналітика" in page:
    st.markdown("## 📊 Аналітика успішності")

    students = st.session_state.students

    if not students:
        st.warning("База учнів порожня.")
    else:
        # Метрики
        c1, c2, c3, c4 = st.columns(4)
        avg_progress = round(sum(s["progress"] for s in students) / len(students)) if students else 0
        c1.metric("Середній прогрес", f"{avg_progress}%", "+5% за місяць")
        c2.metric("Відвідуваність", "94%", "+2%")
        c3.metric("Тестів здано", "23", "цього місяця")
        c4.metric("Сер. бал (прогноз)", "158", "+12 за місяць")

        st.markdown("---")

        # Оберіть учня для аналізу
        student_names = [s["name"] for s in students]
        selected_name = st.selectbox("Оберіть учня для детального аналізу", student_names)
        s = next(x for x in students if x["name"] == selected_name)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Теплова карта знань**")
            topics_data = s.get("topics", {})
            if topics_data:
                topic_names = list(topics_data.keys())
                topic_vals = list(topics_data.values())

                fig_hm = go.Figure(go.Bar(
                    x=topic_vals, y=topic_names, orientation="h",
                    marker=dict(
                        color=topic_vals,
                        colorscale=[[0, "#FCEBEB"], [0.3, "#FAEEDA"], [0.6, "#EEEDFE"], [1, "#1D9E75"]],
                        cmin=0, cmax=100,
                        showscale=True,
                        colorbar=dict(title="Рівень %", len=0.8),
                    ),
                    text=[f"{v}%" for v in topic_vals],
                    textposition="inside",
                    insidetextanchor="middle",
                ))
                fig_hm.update_layout(
                    height=280, margin=dict(l=0, r=60, t=10, b=0),
                    plot_bgcolor="white", paper_bgcolor="white",
                    xaxis=dict(range=[0, 110], title="Рівень знань (%)"),
                    font=dict(size=12),
                )
                st.plotly_chart(fig_hm, use_container_width=True)
            else:
                st.info("Немає даних по темам")

        with col2:
            st.markdown("**Динаміка результатів тестів**")
            months = ["Берез.", "Квіт.", "Трав.", "Черв.", "Лип.", "Серп."]
            scores = s.get("test_scores", [])
            n = min(len(months), len(scores))
            
            if n > 0:
                fig_line = go.Figure()
                fig_line.add_trace(go.Scatter(
                    x=months[:n], y=scores[:n],
                    mode="lines+markers+text",
                    text=[f"{v}%" for v in scores[:n]],
                    textposition="top center",
                    line=dict(color="#534AB7", width=2.5),
                    marker=dict(size=8, color="#534AB7"),
                    fill="tozeroy",
                    fillcolor="rgba(83,74,183,0.07)",
                ))
                fig_line.add_hline(y=100, line_dash="dot", line_color="#1D9E75", annotation_text="Ціль 100%")
                fig_line.update_layout(
                    height=280, margin=dict(l=0, r=0, t=10, b=0),
                    plot_bgcolor="white", paper_bgcolor="white",
                    yaxis=dict(range=[0, 115], gridcolor="#f0eeea", title="Результат (%)"),
                    xaxis=dict(gridcolor="#f0eeea"),
                    showlegend=False,
                    font=dict(size=12),
                )
                st.plotly_chart(fig_line, use_container_width=True)
            else:
                st.info("Немає результатів тестів")

        # Порівняння всіх учнів
        st.markdown("---")
        st.markdown("**Порівняння прогресу всіх учнів (Динамічний вибір)**")
        
        # Динамічний збір усіх унікальних тем для порівняння
        all_topics = set()
        for student in students:
            all_topics.update(student.get("topics", {}).keys())
        
        if all_topics:
            compare_topic = st.selectbox("Тема для порівняння", sorted(list(all_topics)))
            compare_vals = [st_iter.get("topics", {}).get(compare_topic, 0) for st_iter in students]
            compare_names = [st_iter["name"].split()[0] + (" " + st_iter["name"].split()[1][0] + "." if len(st_iter["name"].split()) > 1 else "") for st_iter in students]

            fig_compare = go.Figure(go.Bar(
                x=compare_names, y=compare_vals,
                marker=dict(
                    color=compare_vals,
                    colorscale=[[0, "#FCEBEB"], [0.4, "#FAEEDA"], [0.7, "#EEEDFE"], [1, "#1D9E75"]],
                    cmin=0, cmax=100,
                ),
                text=[f"{v}%" for v in compare_vals],
                textposition="outside",
            ))
            fig_compare.update_layout(
                height=240, margin=dict(l=0, r=0, t=10, b=0),
                plot_bgcolor="white", paper_bgcolor="white",
                yaxis=dict(range=[0, 115], gridcolor="#f0eeea", title=f"{compare_topic} (%)"),
                xaxis=dict(gridcolor="#f0eeea"),
                showlegend=False, font=dict(size=12),
            )
            st.plotly_chart(fig_compare, use_container_width=True)

        # Статистика залученості
        st.markdown("---")
        st.markdown("**Статистика залученості учнів (травень)**")
        engage_data = {
            "Учень": [st_iter["name"] for st_iter in students],
            "Уроків": [st_iter["lessons_total"] for st_iter in students],
            "Здано ДЗ (%)": [random.randint(60, 100) for _ in students],
            "Сер. час ДЗ (хв)": [random.randint(20, 75) for _ in students],
            "Бал тесту (%)": [st_iter["progress"] for st_iter in students],
        }
        st.dataframe(pd.DataFrame(engage_data), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────
# ── БІБЛІОТЕКА ──────────────────────────
# ─────────────────────────────────────────
elif "Бібліотека" in page:
    st.markdown("## 📚 Бібліотека матеріалів")

    tab_files, tab_test = st.tabs(["📁 Файли", "✅ Конструктор тестів"])

    with tab_files:
        search_lib = st.text_input("🔍 Пошук матеріалів...", label_visibility="collapsed",
                                    placeholder="Пошук матеріалів...")
        filter_type = st.radio("Тип:", ["Всі", "PDF", "Презентація", "Квіз"], horizontal=True)

        library = load_library()
        type_map = {"PDF": "pdf", "Презентація": "ppt", "Квіз": "quiz"}

        if search_lib:
            library = [x for x in library if search_lib.lower() in x["name"].lower()]
        if filter_type != "Всі":
            library = [x for x in library if x["type"] == type_map.get(filter_type, "")]

        items_html = ""
        for item in library:
            items_html += f"""
            <div class='lib-item'>
                <div class='lib-icon'>{item["icon"]}</div>
                <div class='lib-name'>{item["name"]}</div>
                <div class='lib-meta'>{item["meta"]}</div>
            </div>"""
        st.markdown(f"<div class='lib-grid'>{items_html}</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**Завантажити новий матеріал:**")
        uploaded = st.file_uploader("Оберіть файл", type=["pdf", "pptx", "jpg", "png", "docx"])
        if uploaded:
            st.success(f"✅ Файл '{uploaded.name}' завантажено до бібліотеки!")

    with tab_test:
        st.markdown("### Генератор тестів")

        c1, c2, c3 = st.columns(3)
        test_topic = c1.selectbox("Тема", ["Алгебра", "Квадратні рівняння", "Тригонометрія", "Логарифми", "Похідна", "Інтеграли", "Геометрія", "Стереометрія"])
        test_level = c2.selectbox("Рівень", ["Початковий", "Середній", "Складний", "НМТ-рівень"])
        test_count = c3.slider("Кількість питань", 5, 20, 10)

        if st.button("🎲 Згенерувати тест", type="primary"):
            q_bank = {
                "Алгебра": [
                    {"q": "Спростіть вираз: (a+b)² - 2ab", "a": ["a²-b²", "a²+b²", "a²+2ab+b²", "2a²"], "correct": 1},
                    {"q": "Знайдіть значення: |−5| + |3|", "a": ["2", "8", "−2", "15"], "correct": 1},
                    {"q": "Розкладіть на множники: x²−9", "a": ["(x−3)²", "(x+3)(x−3)", "(x+9)(x−1)", "x(x−9)"], "correct": 1},
                ],
                "Квадратні рівняння": [
                    {"q": "Дискримінант рівняння x²−5x+6=0", "a": ["1", "25", "−24", "49"], "correct": 0},
                    {"q": "Корені рівняння x²−5x+6=0", "a": ["2 і 3", "−2 і −3", "1 і 6", "−1 і −6"], "correct": 0},
                ],
                "Тригонометрія": [
                    {"q": "Чому дорівнює sin(90°)?", "a": ["0", "1", "−1", "√2/2"], "correct": 1},
                    {"q": "Основне тригонометричне тотожність:", "a": ["sin²x+cos²x=1", "sinx+cosx=1", "sinx·cosx=1", "tgx=cosx/sinx"], "correct": 0},
                ],
                "Логарифми": [
                    {"q": "log₂(8) =", "a": ["2", "3", "4", "6"], "correct": 1},
                    {"q": "Чому дорівнює log₁₀(100)?", "a": ["10", "1", "2", "20"], "correct": 2},
                ],
                "Похідна": [
                    {"q": "(x³)' =", "a": ["x²", "3x²", "3x", "x³"], "correct": 1},
                    {"q": "(sin x)' =", "a": ["−sin x", "cos x", "−cos x", "sin x"], "correct": 1},
                ],
                "Інтеграли": [
                    {"q": "∫x dx =", "a": ["x²", "x²/2 + C", "2x", "x+C"], "correct": 1},
                    {"q": "∫cos x dx =", "a": ["−sin x + C", "sin x + C", "cos x + C", "−cos x + C"], "correct": 1},
                ],
                "Геометрія": [
                    {"q": "Площа кола радіуса r:", "a": ["2πr", "πr²", "πr²/2", "4πr²"], "correct": 1},
                    {"q": "Сума кутів трикутника:", "a": ["90°", "270°", "360°", "180°"], "correct": 3},
                ],
                "Стереометрія": [
                    {"q": "Об'єм кулі радіуса r:", "a": ["4πr³/3", "πr³", "4πr²", "2πr³"], "correct": 0},
                    {"q": "Об'єм прямокутного паралелепіпеда:", "a": ["2(ab+bc+ca)", "abc", "a²b", "3abc"], "correct": 1},
                ],
            }
            pool = q_bank.get(test_topic, q_bank["Алгебра"])
            questions = []
            for i in range(test_count):
                q = pool[i % len(pool)].copy()
                questions.append(q)
            st.session_state.test_questions = questions
            st.success(f"✅ Згенеровано {test_count} питань — тема: {test_topic}, рівень: {test_level}")

        if st.session_state.test_questions:
            st.markdown("---")
            st.markdown(f"**Тест: {test_topic}** ({len(st.session_state.test_questions)} питань)")
            answers = {}
            for i, q in enumerate(st.session_state.test_questions):
                st.markdown(f"**{i+1}. {q['q']}**")
                answers[i] = st.radio("", q["a"], key=f"q_{i}", label_visibility="collapsed", index=None)

            if st.button("✅ Перевірити відповіді"):
                score = 0
                for i, q in enumerate(st.session_state.test_questions):
                    if answers.get(i) == q["a"][q["correct"]]:
                        score += 1
                pct = round(score / len(st.session_state.test_questions) * 100)
                if pct >= 80:
                    st.success(f"🎉 Результат: {score}/{len(st.session_state.test_questions)} ({pct}%) — Відмінно!")
                elif pct >= 60:
                    st.warning(f"👍 Результат: {score}/{len(st.session_state.test_questions)} ({pct}%) — Добре!")
                else:
                    st.error(f"📚 Результат: {score}/{len(st.session_state.test_questions)} ({pct}%) — Потрібно повторити!")


# ─────────────────────────────────────────
# ── ФІНАНСИ ─────────────────────────────
# ─────────────────────────────────────────
elif "Фінанси" in page:
    st.markdown("## 💰 Фінансовий облік")

    students = st.session_state.students

    # Метрики
    total_income = sum(s["lessons_total"] * s["rate"] for s in students)
    debt = sum(s["rate"] for s in students if s["paid_lessons"] == 0)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💵 Дохід (травень)", f"{total_income:,} ₴".replace(",", " "), "розрахунковий")
    c2.metric("📅 Оплачено уроків", str(sum(s["paid_lessons"] for s in students)), "в базі")
    c3.metric("⚠️ Заборгованість", f"{debt:,} ₴".replace(",", " "), f"{sum(1 for s in students if s['paid_lessons']==0)} учні")
    c4.metric("📈 Прогноз (наст. місяць)", f"{int(total_income*1.15):,} ₴".replace(",", " "), "+15%")

    st.markdown("---")

    # Таблиця оплат
    st.markdown("### Стан оплат по учнях")

    for s in students:
        paid = s["paid_lessons"]
        if paid == 0:
            status_html = "<span class='badge badge-red'>❌ Не оплачено</span>"
        elif paid <= 1:
            status_html = f"<span class='badge badge-amber'>⚠️ Залишився {paid} урок</span>"
        else:
            status_html = f"<span class='badge badge-green'>✅ Оплачено {paid} уроків</span>"

        cols = st.columns([3, 2, 2, 1, 1])
        cols[0].markdown(f"**{s['name']}**")
        cols[1].markdown(status_html, unsafe_allow_html=True)
        cols[2].markdown(f"*{s['rate']} грн/урок*")
        if cols[3].button("💬 Нагадати", key=f"remind_fin_{s['id']}"):
            st.toast(f"Нагадування надіслано {s['name']}")
        if cols[4].button("🧾 Рахунок", key=f"invoice_{s['id']}"):
            st.info(f"Рахунок для {s['name']}: {s['rate']} грн · {s['lessons_total']} уроків · Разом: {s['lessons_total']*s['rate']} грн")

    st.markdown("---")

    # Графік доходів по місяцях
    st.markdown("### Динаміка доходів")
    income_months = ["Лист.", "Груд.", "Січ.", "Лют.", "Берез.", "Квіт.", "Трав."]
    income_vals = [4200, 5800, 3500, 6700, 7200, 8000, total_income if total_income > 0 else 8400]

    fig_income = go.Figure()
    fig_income.add_trace(go.Scatter(
        x=income_months, y=income_vals,
        mode="lines+markers+text",
        text=[f"{v//1000}к" for v in income_vals],
        textposition="top center",
        line=dict(color="#1D9E75", width=2.5),
        marker=dict(size=8, color="#1D9E75"),
        fill="tozeroy",
        fillcolor="rgba(29,158,117,0.08)",
        name="Дохід",
    ))
    target_val = int(max(income_vals) * 1.2) if max(income_vals) > 0 else 10000
    fig_income.add_hline(y=target_val, line_dash="dot", line_color="#534AB7", annotation_text=f"Ціль {target_val:,} ₴".replace(",", " "))
    fig_income.update_layout(
        height=260, margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor="white", paper_bgcolor="white",
        yaxis=dict(range=[0, target_val*1.2], gridcolor="#f0eeea", title="Грн"),
        xaxis=dict(gridcolor="#f0eeea"),
        showlegend=False,
        font=dict(size=12),
    )
    st.plotly_chart(fig_income, use_container_width=True)

    # Додавання нової оплати
    if students:
        st.markdown("### Зарахувати оплату")
        with st.form("payment_form"):
            c1f, c2f, c3f = st.columns(3)
            pay_student = c1f.selectbox("Учень", [s["name"] for s in students])
            pay_lessons = c2f.number_input("Кількість уроків", min_value=1, max_value=30, value=5)
            pay_date = c3f.date_input("Дата оплати", value=date.today())
            submitted = st.form_submit_button("✅ Зарахувати", type="primary")
            if submitted:
                for s in st.session_state.students:
                    if s["name"] == pay_student:
                        s["paid_lessons"] += pay_lessons
                        break
                st.success(f"✅ Зараховано {pay_lessons} уроків для {pay_student}! Дата: {pay_date.strftime('%d.%m.%Y')}")
                st.rerun()
