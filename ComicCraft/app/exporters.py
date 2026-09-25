from pathlib import Path
from datetime import datetime
import re

from fpdf import FPDF
from PIL import Image

from .config import BASE_DIR

EXPORT_DIR = BASE_DIR / "static" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def clean_text(text):
    if text is None:
        return ""

    text = str(text)

    replacements = {
        "—": "-",
        "–": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "…": "...",
        "•": "-",
        "→": "->",
        "←": "<-",
        "✨": "",
        "🚀": "",
        "🎉": "",
        "🔥": "",
        "😊": "",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = text.encode("latin-1", "replace").decode("latin-1")

    return text.strip()


def write_text(pdf, text, height=7):
    text = clean_text(text)

    if text:
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(0, height, text)


def get_image_path(image_url):
    return BASE_DIR / image_url.lstrip("/")


def save_pdf(layout):

    filename = (
        "comiccraft-"
        + datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        + ".pdf"
    )

    pdf_path = EXPORT_DIR / filename

    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4"
    )

    pdf.set_margins(
        left=15,
        top=15,
        right=15
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    for panel in layout:

        pdf.add_page()

        # -------------------------
        # TITLE
        # -------------------------

        pdf.set_font(
            "Helvetica",
            "B",
            18
        )

        write_text(
            pdf,
            f"Panel {panel['panel_number']}: {panel['title']}",
            8
        )

        pdf.ln(5)

        # -------------------------
        # IMAGE
        # -------------------------

        image_path = get_image_path(
            panel["image_path"]
        )

        if image_path.exists():

            try:

                with Image.open(image_path) as img:

                    width, height = img.size

                # A4 printable area
                max_width = 180
                max_height = 115

                scale = min(
                    max_width / width,
                    max_height / height
                )

                display_width = width * scale
                display_height = height * scale

                # Center image
                x = (
                    210 - display_width
                ) / 2

                # Make sure image starts inside page
                x = max(15, x)

                y = pdf.get_y()

                pdf.image(
                    str(image_path),
                    x=x,
                    y=y,
                    w=display_width,
                    h=display_height
                )

                # Move cursor BELOW image
                pdf.set_y(
                    y + display_height + 8
                )

            except Exception as error:

                print(
                    "[ComicCraft] PDF image error:",
                    error
                )

        # -------------------------
        # SCENE
        # -------------------------

        pdf.set_font(
            "Helvetica",
            "I",
            10
        )

        write_text(
            pdf,
            panel["scene_description"],
            6
        )

        pdf.ln(3)

        # -------------------------
        # CAPTION
        # -------------------------

        pdf.set_font(
            "Helvetica",
            "B",
            11
        )

        write_text(
            pdf,
            "Caption:",
            6
        )

        pdf.set_font(
            "Helvetica",
            "",
            10
        )

        write_text(
            pdf,
            panel["caption"],
            6
        )

        pdf.ln(3)

        # -------------------------
        # NARRATION
        # -------------------------

        pdf.set_font(
            "Helvetica",
            "B",
            11
        )

        write_text(
            pdf,
            "Narration:",
            6
        )

        pdf.set_font(
            "Helvetica",
            "",
            10
        )

        write_text(
            pdf,
            panel["narration"],
            6
        )

        pdf.ln(3)

        # -------------------------
        # DIALOGUE
        # -------------------------

        pdf.set_font(
            "Helvetica",
            "B",
            11
        )

        write_text(
            pdf,
            "Dialogue:",
            6
        )

        pdf.set_font(
            "Helvetica",
            "",
            10
        )

        write_text(
            pdf,
            panel["dialogue"],
            6
        )

    # -------------------------
    # SAVE PDF
    # -------------------------

    pdf.output(
        str(pdf_path)
    )

    print(
        f"[ComicCraft] PDF saved: {pdf_path}"
    )

    return f"/static/exports/{filename}"