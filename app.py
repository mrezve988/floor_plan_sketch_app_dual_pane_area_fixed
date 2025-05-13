
import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.set_page_config(layout="wide")
st.title("📐 Dual Pane Floor Plan Sketch App with Area")

# Two-column layout
col1, col2 = st.columns([2, 1])

# Sidebar settings
with st.sidebar:
    st.header("🛠️ Drawing Settings")
    stroke_width = st.slider("Stroke width: ", 1, 10, 2)
    stroke_color = st.color_picker("Stroke color: ", "#000000")
    bg_color = st.color_picker("Canvas background color:", "#ffffff")
    drawing_mode = st.selectbox("Drawing tool:", ["freedraw", "rect", "circle"])
    realtime_update = st.checkbox("Update in realtime", True)
    show_labels = st.checkbox("Enable Room Labels", True)

pixels_per_meter = 50
room_labels = {}

# Column 1: Drawing Canvas
with col1:
    st.subheader("✏️ Draw your floor plan here")
    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 0.3)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        update_streamlit=realtime_update,
        height=600,
        width=800,
        drawing_mode=drawing_mode,
        key="canvas",
    )

# Column 2: Room Size Display
with col2:
    st.subheader("📏 Room Measurements")
    if canvas_result and canvas_result.json_data is not None:
        for idx, obj in enumerate(canvas_result.json_data["objects"]):
            if obj["type"] == "rect":
                left = obj["left"]
                top = obj["top"]
                width_px = obj["width"]
                length_px = obj["height"]

                width_m = width_px / pixels_per_meter
                length_m = length_px / pixels_per_meter
                area_sqm = width_m * length_m

                st.markdown(f"""
**Room {idx+1}**
- Length: `{length_m:.2f} m`
- Width: `{width_m:.2f} m`
- Area: `{area_sqm:.2f} m²`
""")

                if show_labels:
                    label = st.text_input(f"Label for Room {idx+1}", key=f"label_{idx}")
                    room_labels[f"Room_{idx+1}"] = {
                        "label": label,
                        "position": [int(left), int(top)],
                        "size_m": [round(length_m, 2), round(width_m, 2)],
                        "area_m2": round(area_sqm, 2)
                    }

    if room_labels:
        st.subheader("🏷 Room Labels Summary")
        st.json(room_labels)


# Display grid image as visual reference
st.markdown("### 📎 Reference Grid (1m x 1m)")
st.image("reference_grid.png", caption="Use this grid as a visual reference for drawing.")
