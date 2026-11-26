# 🎓 Certificate Generator

A simple, web-based certificate generator built with **Python, Streamlit, Pandas, and Pillow**. Upload a certificate template and a participant CSV, customize the placement and appearance of the participant name and certificate ID, preview the result, and generate certificates in bulk.

## ✨ Features

- **Upload a template:** Supports PNG, JPG, and JPEG certificate templates.
- **Bulk generation:** Creates a separate certificate for every participant in the uploaded CSV.
- **Live preview:** Preview a sample certificate while adjusting the layout.
- **Custom name styling:** Configure the name's X/Y position, font size, maximum width, and text color.
- **Custom certificate ID styling:** Configure the ID's X/Y position and font size.
- **Automatic name sizing:** Reduces the name font size when the text exceeds the configured maximum width.
- **Multiple output formats:** Generates both PNG and PDF versions of each certificate.
- **ZIP download:** Packages all generated certificates into one downloadable ZIP file.
- **Progress indicator:** Shows generation progress while certificates are being created.

## 🛠️ Technologies Used

| Technology | Purpose |
| --- | --- |
| Python | Application logic |
| Streamlit | Web interface |
| Pandas | Reading and displaying participant data |
| Pillow (PIL) | Editing certificate images and creating PNG/PDF files |
| Montserrat | Font used for certificate text |

## 📁 Project Structure

```text
certificates_generator/
├── app.py
├── requirements.txt
├── README.md
└── fonts/
    ├── Montserrat-VariableFont_wght.ttf
    ├── Montserrat-Italic-VariableFont_wght.ttf
    └── OFL.txt
```

The application loads the bold Montserrat font from `fonts/Montserrat-VariableFont_wght.ttf`. Keep this font file and the `fonts/` directory in place when running the application.

## ✅ Prerequisites

- Python installed on your system
- Git (to clone the repository)

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/SHIVAREDDY2005/certificates_generator.git
cd certificates_generator
```

### 2. (Recommended) Create a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

Run this command from the project root directory:

```bash
streamlit run app.py
```

Streamlit will display a local URL in the terminal (usually **http://localhost:8501**). Open that URL in your browser to use the application.

## 📄 Preparing the Participant CSV

Create a CSV file with these **exact column names**:

- `username` — participant name to print on the certificate
- `credential_id` — unique certificate ID to print on the certificate and use in the output filenames

Example:

```csv
username,credential_id
Shiva Reddy,CERT-001
Rahul Kumar,CERT-002
Ananya Sharma,CERT-003
```

Save the file as `participants.csv` or another name ending in `.csv`.

## 🧭 How to Use

1. **Upload files:** Upload your certificate template image (PNG, JPG, or JPEG) and the participant CSV.
2. **Customize the certificate:** Adjust the name position, font size, maximum name width, and color. Adjust the certificate ID position and font size as well.
3. **Preview:** Check the sample certificate in the preview panel and fine-tune the settings.
4. **Review participants:** Once both files are uploaded and the CSV headers are valid, the participant data is displayed.
5. **Generate:** Select **Generate All Certificates**.
6. **Download:** When generation is complete, select **Download All Certificates (ZIP)**.

## ⚙️ Customization Options

Coordinates are measured in **pixels from the top-left corner** of the uploaded template.

| Setting | What it controls |
| --- | --- |
| Name X Coordinate | Horizontal position of the participant name |
| Name Y Coordinate | Vertical position of the participant name |
| Name Font Size | Starting font size for the participant name |
| Maximum Name Width | Maximum text width used when adjusting the name size |
| Name Color | Text color used for the name and certificate ID |
| ID X Coordinate | Horizontal position of the certificate ID |
| ID Y Coordinate | Vertical position of the certificate ID |
| ID Font Size | Font size of the certificate ID |

The name and certificate ID are drawn centered around their configured coordinates.

## 📦 Generated Files

The ZIP download contains two files for each participant:

- `<credential_id>.png`
- `<credential_id>.pdf`

The certificate ID is converted to a filename-safe form when needed. Both formats use the uploaded template with the participant's name and certificate ID added.

## 🧰 Troubleshooting

**The application cannot find the font**

Make sure you start Streamlit from the project root and that this file exists:

```text
fonts/Montserrat-VariableFont_wght.ttf
```

**The CSV is not accepted**

Check that the first row contains the exact headers `username` and `credential_id`. Column names are case-sensitive.

**The application does not start**

Make sure your virtual environment is activated and install the dependencies again:

```bash
pip install -r requirements.txt
```

Then run:

```bash
streamlit run app.py
```

## 👤 Repository

GitHub: https://github.com/SHIVAREDDY2005/certificates_generator
