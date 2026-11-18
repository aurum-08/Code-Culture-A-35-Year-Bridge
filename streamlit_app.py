import streamlit as st
import turtle
import io
from PIL import Image

st.set_page_config(page_title="Oyu.py – 35 Years of U.S.-Kazakhstan Partnership", layout="centered")

st.title("🇰🇿🇺🇸 Oyu.py: Code & Culture")
st.markdown("### 35 Years of U.S.-Kazakhstan Partnership — Cultural Exchange & Innovation")
st.write("Нажми кнопку ниже, чтобы сгенерировать узор с помощью Python-алгоритма прямо в реальном времени!")

# Палитра и логика рисования узора
TURQUOISE = "#2A9D8F"
TERRACOTTA = "#E76F51"
DEEP_BLUE = "#264653"
SANDY = "#E9C46A"
CREAM = "#FAF0E6"
BG_COLOR = "#F5E8C7"
TILE_SIZE = 40
COLORS = [TURQUOISE, TERRACOTTA, DEEP_BLUE, SANDY]

def draw_rhombus(t, cx, cy, size, fill_col, outline_col):
    half = size / 2
    points = [
        (cx, cy + half),
        (cx + half, cy),
        (cx, cy - half),
        (cx - half, cy)
    ]
    t.penup()
    t.goto(points[0])
    t.pendown()
    t.color(outline_col, fill_col)
    t.begin_fill()
    for p in points[1:]:
        t.goto(p)
    t.goto(points[0])
    t.end_fill()

def draw_oyu(t, cx, cy, size, main_col, outline_col):
    s = size * 0.22
    arm = size * 0.38
    horn = s * 1.15

    t.pensize(2)
    t.color(outline_col, main_col)

    # horizontal bar
    t.penup()
    t.goto(cx - arm, cy - s * 0.45)
    t.pendown()
    t.begin_fill()
    t.goto(cx + arm, cy - s * 0.45)
    t.goto(cx + arm, cy + s * 0.45)
    t.goto(cx - arm, cy + s * 0.45)
    t.goto(cx - arm, cy - s * 0.45)
    t.end_fill()

    # vertical bar
    t.penup()
    t.goto(cx - s * 0.45, cy - arm)
    t.pendown()
    t.begin_fill()
    t.goto(cx + s * 0.45, cy - arm)
    t.goto(cx + s * 0.45, cy + arm)
    t.goto(cx - s * 0.45, cy + arm)
    t.goto(cx - s * 0.45, cy - arm)
    t.end_fill()

    # top horns
    for dx in (-1, 1):
        t.penup()
        t.goto(cx + dx * s * 0.45, cy + arm)
        t.pendown()
        t.begin_fill()
        t.goto(cx + dx * s * 0.45, cy + arm + horn)
        t.goto(cx + dx * (s * 0.45 + horn), cy + arm + horn)
        t.goto(cx + dx * (s * 0.45 + horn), cy + arm + horn - s * 0.7)
        t.goto(cx + dx * s * 0.45, cy + arm + horn - s * 0.7)
        t.goto(cx + dx * s * 0.45, cy + arm)
        t.end_fill()

    # bottom horns
    for dx in (-1, 1):
        t.penup()
        t.goto(cx + dx * s * 0.45, cy - arm)
        t.pendown()
        t.begin_fill()
        t.goto(cx + dx * s * 0.45, cy - arm - horn)
        t.goto(cx + dx * (s * 0.45 + horn), cy - arm - horn)
        t.goto(cx + dx * (s * 0.45 + horn), cy - arm - horn + s * 0.7)
        t.goto(cx + dx * s * 0.45, cy - arm - horn + s * 0.7)
        t.goto(cx + dx * s * 0.45, cy - arm)
        t.end_fill()

    # left horns
    for dy in (-1, 1):
        t.penup()
        t.goto(cx - arm, cy + dy * s * 0.45)
        t.pendown()
        t.begin_fill()
        t.goto(cx - arm - horn, cy + dy * s * 0.45)
        t.goto(cx - arm - horn, cy + dy * (s * 0.45 + horn))
        t.goto(cx - arm - horn + s * 0.7, cy + dy * (s * 0.45 + horn))
        t.goto(cx - arm - horn + s * 0.7, cy + dy * s * 0.45)
        t.goto(cx - arm, cy + dy * s * 0.45)
        t.end_fill()

    # right horns
    for dy in (-1, 1):
        t.penup()
        t.goto(cx + arm, cy + dy * s * 0.45)
        t.pendown()
        t.begin_fill()
        t.goto(cx + arm + horn, cy + dy * s * 0.45)
        t.goto(cx + arm + horn, cy + dy * (s * 0.45 + horn))
        t.goto(cx + arm + horn - s * 0.7, cy + dy * (s * 0.45 + horn))
        t.goto(cx + arm + horn - s * 0.7, cy + dy * s * 0.45)
        t.goto(cx + arm, cy + dy * s * 0.45)
        t.end_fill()

def draw_tile(t, x, y, color_idx):
    fill_col = COLORS[color_idx % 4]
    rhomb_col = COLORS[(color_idx + 1) % 4]

    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(CREAM, fill_col)
    t.begin_fill()
    for _ in range(4):
        t.forward(TILE_SIZE)
        t.left(90)
    t.end_fill()

    cx = x + TILE_SIZE / 2
    cy = y + TILE_SIZE / 2

    draw_rhombus(t, cx, cy, TILE_SIZE * 0.78, rhomb_col, CREAM)
    draw_oyu(t, cx, cy, TILE_SIZE * 0.72, fill_col, CREAM)

if st.button("Сгенерировать узор через Python (Turtle)"):
    with st.spinner("Генерация узора..."):
        canvas = turtle.ScrolledCanvas(width=900, height=180)
        screen = turtle.TurtleScreen(canvas)
        screen.bgcolor(BG_COLOR)
        screen.tracer(0)

        t = turtle.RawTurtle(screen)
        t.hideturtle()
        t.speed(0)

        total_width = 20 * TILE_SIZE
        start_x = -total_width / 2
        start_y = -TILE_SIZE / 2

        for i in range(20):
            draw_tile(t, start_x + i * TILE_SIZE, start_y, i)

        screen.update()
        
        # Сохранение скриншота холста turtle
        ps_data = canvas.postscript(colormode='color')
        img = Image.open(io.BytesIO(ps_data.encode('utf-8')))
        st.image(img, caption="Сгенерированный Python узор (Oyu.py)")
        st.success("Узор успешно сгенерирован кодом!")

st.markdown("---")
st.markdown("**О проекте:** Этот проект объединяет историю Тараза, США и современные технологии с помощью Python.")
