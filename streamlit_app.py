import streamlit as st
from PIL import Image, ImageDraw
import io

st.set_page_config(page_title="Oyu.py – 35 Years of U.S.-Kazakhstan Partnership", layout="centered")

st.title("🇰🇿🇺🇸 Oyu.py: Code & Culture")
st.markdown("### 35 Years of U.S.-Kazakhstan Partnership — Cultural Exchange & Innovation")
st.write("Нажми кнопку ниже, чтобы запустить анимацию алгоритма Python в реальном времени!")


TURQUOISE = "#2A9D8F"
TERRACOTTA = "#E76F51"
DEEP_BLUE = "#264653"
SANDY = "#E9C46A"
CREAM = "#FAF0E6"
BG_COLOR = "#F5E8C7"

TILE_SIZE = 40
COLORS = [TURQUOISE, TERRACOTTA, DEEP_BLUE, SANDY]

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def draw_rhombus(draw, cx, cy, size, fill_col, outline_col):
    half = size / 2
    points = [
        (cx, cy + half),
        (cx + half, cy),
        (cx, cy - half),
        (cx - half, cy)
    ]
    draw.polygon(points, fill=hex_to_rgb(fill_col), outline=hex_to_rgb(outline_col), width=2)

def draw_oyu(draw, cx, cy, size, main_col, outline_col):
    s = size * 0.22
    arm = size * 0.38
    horn = s * 1.15

    f_col = hex_to_rgb(main_col)
    o_col = hex_to_rgb(outline_col)

    draw.rectangle([cx - arm, cy - s * 0.45, cx + arm, cy + s * 0.45], fill=f_col, outline=o_col, width=2)
    draw.rectangle([cx - s * 0.45, cy - arm, cx + s * 0.45, cy + arm], fill=f_col, outline=o_col, width=2)

    for dx in (-1, 1):
        pts = [
            (cx + dx * s * 0.45, cy + arm),
            (cx + dx * s * 0.45, cy + arm + horn),
            (cx + dx * (s * 0.45 + horn), cy + arm + horn),
            (cx + dx * (s * 0.45 + horn), cy + arm + horn - s * 0.7),
            (cx + dx * s * 0.45, cy + arm + horn - s * 0.7)
        ]
        draw.polygon(pts, fill=f_col, outline=o_col, width=2)

    for dx in (-1, 1):
        pts = [
            (cx + dx * s * 0.45, cy - arm),
            (cx + dx * s * 0.45, cy - arm - horn),
            (cx + dx * (s * 0.45 + horn), cy - arm - horn),
            (cx + dx * (s * 0.45 + horn), cy - arm - horn + s * 0.7),
            (cx + dx * s * 0.45, cy - arm - horn + s * 0.7)
        ]
        draw.polygon(pts, fill=f_col, outline=o_col, width=2)

    for dy in (-1, 1):
        pts = [
            (cx - arm, cy + dy * s * 0.45),
            (cx - arm - horn, cy + dy * s * 0.45),
            (cx - arm - horn, cy + dy * (s * 0.45 + horn)),
            (cx - arm - horn + s * 0.7, cy + dy * (s * 0.45 + horn)),
            (cx - arm - horn + s * 0.7, cy + dy * s * 0.45)
        ]
        draw.polygon(pts, fill=f_col, outline=o_col, width=2)

    for dy in (-1, 1):
        pts = [
            (cx + arm, cy + dy * s * 0.45),
            (cx + arm + horn, cy + dy * s * 0.45),
            (cx + arm + horn, cy + dy * (s * 0.45 + horn)),
            (cx + arm + horn - s * 0.7, cy + dy * (s * 0.45 + horn)),
            (cx + arm + horn - s * 0.7, cy + dy * s * 0.45)
        ]
        draw.polygon(pts, fill=f_col, outline=o_col, width=2)

def draw_tile(draw, x, y, color_idx):
    fill_col = COLORS[color_idx % 4]
    rhomb_col = COLORS[(color_idx + 1) % 4]

    draw.rectangle([x, y, x + TILE_SIZE, y + TILE_SIZE], fill=hex_to_rgb(fill_col), outline=hex_to_rgb(CREAM), width=2)

    cx = x + TILE_SIZE / 2
    cy = y + TILE_SIZE / 2

    draw_rhombus(draw, cx, cy, TILE_SIZE * 0.78, rhomb_col, CREAM)
    draw_oyu(draw, cx, cy, TILE_SIZE * 0.72, fill_col, CREAM)

if st.button("▶ Запустить анимацию отрисовки узора"):
    with st.spinner("Создание покадровой анимации..."):
        num_tiles = 16
        img_width = num_tiles * TILE_SIZE
        img_height = TILE_SIZE * 2
        
        frames = []
        base_image = Image.new("RGB", (img_width, img_height), color=hex_to_rgb(BG_COLOR))
        
        # Генерируем кадры пошагово
        for i in range(num_tiles + 1):
            frame = base_image.copy()
            draw = ImageDraw.Draw(frame)
            start_x = 0
            start_y = TILE_SIZE / 2
            
            for j in range(i):
                draw_tile(draw, start_x + j * TILE_SIZE, start_y, j)
            
            frames.append(frame)

      
        gif_buffer = io.BytesIO()
        frames[0].save(
            gif_buffer,
            format="GIF",
            save_all=True,
            append_images=frames[1:],
            duration=150, 
            loop=0
        )
        gif_buffer.seek(0)

        st.image(gif_buffer, caption="Анимация генерации орнамента Oyu.py", use_container_width=True)
        st.success("Анимация успешно сгенерирована кодом!")

st.markdown("---")
st.markdown("**О проекте:** Этот проект объединяет историю Тараза, США и современные технологии с помощью Python.")
