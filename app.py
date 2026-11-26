import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import zipfile
import io
import re

st.set_page_config(
    page_title="Certificate Generator",
    page_icon="🎓",
    layout="wide"
)

# ---------------------------------------------------------------- UI styling
# ---------------------------------------------------------------- UI styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --ink: #172033;
        --accent: #5145A5;
        --accent-hover: #393078;
        --muted: #596579;
        --line: #E2E5EC;
        --page: #FFFFFF;
        --input: #FFFFFF;
        --soft: #F6F7FB;
    }

    /* Main application */
    html, body, .stApp,
    [data-testid="stAppViewContainer"] {
        background: #FFFFFF !important;
        color: var(--ink) !important;
        font-family: 'Manrope', sans-serif !important;
        color-scheme: light !important;
    }

    /* All text */
    .stApp p,
    .stApp span,
    .stApp label,
    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp li,
    .stApp [data-testid="stWidgetLabel"] {
        color: var(--ink) !important;
    }

    .block-container {
        max-width: 1280px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }

    header[data-testid="stHeader"] {
        background: #FFFFFF !important;
    }

    /* Page header */
    .app-title {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0;
        color: var(--ink) !important;
    }

    .app-sub {
        color: var(--muted) !important;
        font-size: 1rem;
        margin: 0.25rem 0 1.6rem 0;
    }

    /* Section headings */
    .section-title {
        font-size: 1.05rem;
        font-weight: 800;
        margin: 0 0 0.15rem 0;
        color: var(--ink) !important;
    }

    .section-hint {
        font-size: 0.85rem;
        color: var(--muted) !important;
        margin: 0 0 0.9rem 0;
    }

    /* Cards and containers */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border: 1px solid var(--line) !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(23, 32, 51, 0.04);
    }

    /* File uploader */
/* File uploader - Force white background */
[data-testid="stFileUploaderDropzone"] {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    border: 2px dashed #5145A5 !important;
    border-radius: 10px !important;
    color: #172033 !important;
}

/* Inner uploader containers */
[data-testid="stFileUploaderDropzone"] > div,
[data-testid="stFileUploaderDropzone"] section {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
}

/* Drag and drop text */
[data-testid="stFileUploaderDropzone"] p,
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] small {
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
}

/* Browse files button */
[data-testid="stFileUploaderDropzone"] button,
[data-testid="stFileUploaderDropzone"] button span {
    background: #5145A5 !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    border: 1px solid #5145A5 !important;
    border-radius: 7px !important;
    font-weight: 700 !important;
}

[data-testid="stFileUploaderDropzone"] button:hover {
    background: #393078 !important;
}

    /* Number inputs */
    div[data-testid="stNumberInput"] input,
    div[data-baseweb="input"] input {
        background: #FFFFFF !important;
        color: var(--ink) !important;
        -webkit-text-fill-color: var(--ink) !important;
        border-radius: 7px !important;
        font-family: 'Manrope', sans-serif !important;
        font-weight: 600 !important;
    }

    div[data-testid="stNumberInput"] [data-baseweb="input"],
    div[data-baseweb="input"] {
        background: #FFFFFF !important;
        border-color: #D5D9E2 !important;
    }

    /* Input labels */
    div[data-testid="stWidgetLabel"] p,
    .stSlider label,
    .stNumberInput label {
        color: var(--ink) !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }

    /* Slider */
    div[data-testid="stSlider"] {
        color: var(--ink) !important;
    }

    div[data-testid="stSlider"] [role="slider"] {
        background: var(--accent) !important;
        border-color: var(--accent) !important;
    }

    /* Color picker */
    div[data-testid="stColorPicker"] input {
        color: var(--ink) !important;
    }

    /* Buttons */
    .stButton > button,
    .stDownloadButton > button {
        font-family: 'Manrope', sans-serif !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        padding: 0.7rem 1.2rem !important;
        border: 1px solid var(--accent) !important;
    }

    .stButton > button[kind="primary"] {
        background: var(--accent) !important;
        color: #FFFFFF !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: var(--accent-hover) !important;
        color: #FFFFFF !important;
    }

    .stDownloadButton > button {
        background: #FFFFFF !important;
        color: var(--accent) !important;
    }

    .stDownloadButton > button:hover {
        background: var(--accent) !important;
        color: #FFFFFF !important;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background: var(--accent) !important;
    }

    /* Preview image */
    div[data-testid="stImage"] img {
        border-radius: 8px;
        border: 1px solid var(--line);
    }

    /* Participant table */
    div[data-testid="stDataFrame"] {
        background: #FFFFFF !important;
        border: 1px solid var(--line);
        border-radius: 8px;
        overflow: hidden;
    }

    /* Alerts */
    div[data-testid="stAlert"] {
        background: #F6F7FB !important;
        border-radius: 9px;
    }

    /* Dividers */
    hr {
        border-color: var(--line) !important;
    }

    /* Hide default Streamlit chrome */
    #MainMenu, footer {
        visibility: hidden;
    }
/* -----------------------------------------
   FIX 1: INFO AND WARNING MESSAGES
----------------------------------------- */

div[data-testid="stAlert"] {
    background: #F6F7FB !important;
    background-color: #F6F7FB !important;
    border: 1px solid #E2E5EC !important;
    border-radius: 9px !important;
}

div[data-testid="stAlert"] * {
    color: #172033 !important;
    background-color: transparent !important;
}

div[data-testid="stAlert"] svg {
    color: #5145A5 !important;
}

/* -----------------------------------------
   FIX 2: NUMBER INPUT + AND - BUTTONS
----------------------------------------- */

div[data-testid="stNumberInput"] button {
    background: #F6F7FB !important;
    background-color: #F6F7FB !important;
    color: #172033 !important;
    border: 1px solid #D5D9E2 !important;
}

div[data-testid="stNumberInput"] button:hover {
    background: #E9E7F7 !important;
    color: #393078 !important;
}

div[data-testid="stNumberInput"] button svg {
    color: #393078 !important;
    fill: #393078 !important;
}

/* -----------------------------------------
   FIX 3: MOBILE RESPONSIVE LAYOUT
----------------------------------------- */

@media (max-width: 768px) {

    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 1.2rem !important;
    }

    /* Stack the main sections vertically */
    div[data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
        gap: 1rem !important;
    }

    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        width: 100% !important;
        min-width: 100% !important;
        flex: 1 1 100% !important;
    }

    /* Responsive title */
    .app-title {
        font-size: 1.7rem !important;
    }

    .app-sub {
        font-size: 0.9rem !important;
    }
}

/* -----------------------------------------
   FIX 4: INPUT FIELD COLORS
----------------------------------------- */

div[data-testid="stNumberInput"] input {
    background: #FFFFFF !important;
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
}

div[data-testid="stNumberInput"] > div {
    background: #FFFFFF !important;
    border-color: #D5D9E2 !important;
}
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown('<p class="app-title">🎓 Certificate Generator</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="app-sub">Upload a template and a participant list, position the text, then download every certificate as PNG and PDF.</p>',
    unsafe_allow_html=True,
)


def section(title, hint=None):
    st.markdown(f'<p class="section-title">{title}</p>', unsafe_allow_html=True)
    if hint:
        st.markdown(f'<p class="section-hint">{hint}</p>', unsafe_allow_html=True)


# ---------------------------------------------------------------- Layout
left, right = st.columns([5, 7], gap="large")

with left:
# File uploads
    with st.container(border=True):
        section(
            "1. Upload files",
            "A PNG or JPG template, and a CSV with participant details."
        )

        template_file = st.file_uploader(
            "Upload Certificate Template",
            type=["png", "jpg", "jpeg"]
        )

        csv_file = st.file_uploader(
            "Upload Participants CSV",
            type=["csv"]
        )

        # CSV format instructions
        st.info("⚠️ Your CSV file must contain these exact two columns:")

        st.markdown("""
        | username | credential_id |
        |----------|---------------|
        | name 1 | CERT-001 |
        | name 2 | CERT-002 |
        """)

        st.caption(
            "Make sure the column names are exactly username and credential_id."
        )

    # Settings
    with st.container(border=True):
        section("2. Customize certificate", "Coordinates are in pixels from the top-left of the template.")

        st.markdown("**Name position**")

        if True:
            c1, c2 = st.columns(2)

            with c1:
                name_x = st.number_input(
                    "Name X Coordinate",
                    min_value=0,
                    value=100
                )

            with c2:
                name_y = st.number_input(
                    "Name Y Coordinate",
                    min_value=0,
                    value=100
                )

            font_size = st.slider(
                "Name Font Size",
                min_value=20,
                max_value=200,
                value=100
            )

            max_width = st.number_input(
                "Maximum Name Width",
                min_value=100,
                value=11000
            )

            name_color = st.color_picker(
                "Name Color",
                "#393078"
            )

        st.divider()
        st.markdown("**Certificate ID position**")

        if True:
            c3, c4 = st.columns(2)

            with c3:
                id_x = st.number_input(
                    "ID X Coordinate",
                    min_value=0,
                    value=100
                )

            with c4:
                id_y = st.number_input(
                    "ID Y Coordinate",
                    min_value=0,
                    value=100
                )

            id_font_size = st.slider(
                "ID Font Size",
                min_value=10,
                max_value=80,
                value=28
            )

# Font
font_path = Path("fonts/Montserrat-VariableFont_wght.ttf")

def load_font(size):
    font = ImageFont.truetype(str(font_path), size)
    font.set_variation_by_name("Bold")
    return font

# Generate certificate
def generate_certificate(template, name, credential_id):

    image = template.copy().convert("RGBA")
    draw = ImageDraw.Draw(image)

    size = font_size

    while size >= 20:
        font = load_font(size)

        bbox = draw.textbbox((0, 0), name, font=font)

        if bbox[2] - bbox[0] <= max_width:
            break

        size -= 1

    draw.text(
        (name_x, name_y),
        name,
        fill=name_color,
        font=font,
        anchor="mm"
    )

    id_font = load_font(id_font_size)

    draw.text(
        (id_x, id_y),
        f"Certificate ID : {credential_id}",
        fill=name_color,
        font=id_font,
        anchor="mm"
    )

    return image


# Preview
with right:
    with st.container(border=True):
        section("3. Certificate preview", "Updates as you change the settings.")

        if template_file:

            template = Image.open(template_file).convert("RGBA")

            preview_name = "Sample Participant"
            preview_id = "CERT-001"

            preview = generate_certificate(
                template,
                preview_name,
                preview_id
            )

            st.image(
                preview,
                caption="Live Certificate Preview",
                use_container_width=True
            )
        else:
            st.info("Upload a certificate template to see the preview here.")


# Generation
if csv_file and template_file:

    df = pd.read_csv(csv_file)

    required = {"username", "credential_id"}

    if not required.issubset(df.columns):

        st.error(
            "CSV must contain username and credential_id columns."
        )
# File uploads
    else:

        with st.container(border=True):
            section("4. Participants", f"{len(df)} participants loaded.")

            st.dataframe(df, use_container_width=True)

            if st.button(
                "🚀 Generate All Certificates",
                type="primary",
                use_container_width=True
            ):

                zip_buffer = io.BytesIO()

                with zipfile.ZipFile(
                    zip_buffer,
                    "w",
                    zipfile.ZIP_DEFLATED
                ) as zip_file:

                    progress = st.progress(0)

                    for index, row in df.iterrows():

                        name = str(row["username"]).strip()
                        credential_id = str(
                            row["credential_id"]
                        ).strip()

                        if not name or not credential_id:
                            continue

                        certificate = generate_certificate(
                            template,
                            name,
                            credential_id
                        )

                        safe_id = re.sub(
                            r"[^A-Za-z0-9_-]",
                            "_",
                            credential_id
                        )

                        # PNG
                        png_buffer = io.BytesIO()
                        certificate.save(png_buffer, format="PNG")

                        zip_file.writestr(
                            f"{safe_id}.png",
                            png_buffer.getvalue()
                        )

                        # PDF
                        pdf_buffer = io.BytesIO()

                        white_bg = Image.new(
                            "RGB",
                            certificate.size,
                            "white"
                        )

                        white_bg.paste(
                            certificate,
                            mask=certificate.getchannel("A")
                        )

                        white_bg.save(
                            pdf_buffer,
                            format="PDF",
                            resolution=96
                        )

                        zip_file.writestr(
                            f"{safe_id}.pdf",
                            pdf_buffer.getvalue()
                        )

                        progress.progress(
                            (index + 1) / len(df)
                        )

                st.success("Certificates generated successfully!")

                st.download_button(
                    "📥 Download All Certificates (ZIP)",
                    data=zip_buffer.getvalue(),
                    file_name="certificates.zip",
                    mime="application/zip",
                    use_container_width=True
                )