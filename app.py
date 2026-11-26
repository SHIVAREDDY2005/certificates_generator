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
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --ink: #1d1a3a;
        --accent: #393078;
        --accent-soft: #ece9f7;
        --muted: #6b6882;
        --line: #dedbec;
        --page: #f7f6fb;
    }

    html, body, [class*="css"], .stApp {
        font-family: 'Manrope', sans-serif;
        color: var(--ink);
    }
    .stApp { background: var(--page); }

    .block-container {
        max-width: 1280px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }
    header[data-testid="stHeader"] { background: transparent; }

    /* Page header */
    .app-title {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0;
        color: var(--ink);
    }
    .app-sub {
        color: var(--muted);
        font-size: 1rem;
        margin: 0.25rem 0 1.6rem 0;
    }

    /* Section headings */
    .section-title {
        font-size: 1.05rem;
        font-weight: 700;
        margin: 0 0 0.15rem 0;
        color: var(--ink);
    }
    .section-hint {
        font-size: 0.85rem;
        color: var(--muted);
        margin: 0 0 0.9rem 0;
    }

    /* Bordered containers */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff;
        border: 1px solid var(--line) !important;
        border-radius: 10px;
    }

    /* Inputs */
    /* File uploader - Improved visibility */
    div[data-testid="stFileUploaderDropzone"] {
        background: #F5EEDC !important;
        border: 1.5px dashed #94702D !important;
        border-radius: 10px !important;
    }

    /* Upload text */
    div[data-testid="stFileUploaderDropzone"] p,
    div[data-testid="stFileUploaderDropzone"] span,
    div[data-testid="stFileUploaderDropzone"] small {
        color: #172033 !important;
    }

    /* Upload button */
    div[data-testid="stFileUploaderDropzone"] button {
        background: #FFFFFF !important;
        color: #172033 !important;
        border: 1px solid #94702D !important;
        border-radius: 7px !important;
        font-weight: 700 !important;
    }

    div[data-testid="stFileUploaderDropzone"] button:hover {
        background: #94702D !important;
        color: #FFFFFF !important;
    }

    /* Buttons */
    .stButton > button, .stDownloadButton > button {
        font-family: 'Manrope', sans-serif;
        font-weight: 700;
        border-radius: 8px;
        padding: 0.7rem 1.2rem;
        border: 1px solid var(--accent);
    }
    .stButton > button[kind="primary"] {
        background: var(--accent);
        color: #ffffff;
    }
    .stButton > button[kind="primary"]:hover {
        background: #2b2460;
        border-color: #2b2460;
    }
    .stDownloadButton > button {
        background: #ffffff;
        color: var(--accent);
    }
    .stDownloadButton > button:hover {
        background: var(--accent-soft);
        color: var(--accent);
        border-color: var(--accent);
    }

    /* Progress bar */
    .stProgress > div > div > div > div { background-color: var(--accent); }

    /* Preview image + table */
    div[data-testid="stImage"] img {
        border-radius: 6px;
        border: 1px solid var(--line);
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        border-radius: 8px;
        overflow: hidden;
    }

    /* Hide default Streamlit chrome */
    #MainMenu, footer { visibility: hidden; }
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
        section("1. Upload files", "A PNG or JPG template, and a CSV with username and credential_id columns.")

        template_file = st.file_uploader(
            "Upload Certificate Template",
            type=["png", "jpg", "jpeg"]
        )

        csv_file = st.file_uploader(
            "Upload Participants CSV",
            type=["csv"]
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