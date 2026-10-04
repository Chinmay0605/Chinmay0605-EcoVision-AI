from pathlib import Path
from datetime import datetime

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader


class ReportAgent:
    """
    EcoVision AI Report Agent

    Generates a professional single-page A4
    waste analysis report with city-specific
    disposal guidance.
    """

    def __init__(self):
        print("EcoVision Report Agent initialized.")

    # =========================================================
    # TEXT WRAPPING
    # =========================================================

    def wrap_text(
        self,
        pdf,
        text,
        font_name,
        font_size,
        max_width
    ):
        text = str(text or "")

        words = text.split()

        lines = []
        current = ""

        for word in words:

            test = (
                f"{current} {word}"
                if current
                else word
            )

            width = pdf.stringWidth(
                test,
                font_name,
                font_size
            )

            if width <= max_width:
                current = test

            else:

                if current:
                    lines.append(current)

                current = word

        if current:
            lines.append(current)

        return lines

    # =========================================================
    # DRAW WRAPPED TEXT
    # =========================================================

    def draw_wrapped_text(
        self,
        pdf,
        text,
        x,
        y,
        max_width,
        font_name="Helvetica",
        font_size=9,
        color=colors.HexColor("#334155"),
        line_height=12,
        max_lines=2
    ):

        pdf.setFont(
            font_name,
            font_size
        )

        pdf.setFillColor(
            color
        )

        lines = self.wrap_text(
            pdf,
            text,
            font_name,
            font_size,
            max_width
        )

        lines = lines[:max_lines]

        for line in lines:

            pdf.drawString(
                x,
                y,
                line
            )

            y -= line_height

        return y

    # =========================================================
    # ROUNDED BOX
    # =========================================================

    def rounded_box(
        self,
        pdf,
        x,
        y,
        width,
        height,
        fill,
        stroke=colors.HexColor("#BBE7C8"),
        radius=8
    ):

        pdf.setFillColor(
            fill
        )

        pdf.setStrokeColor(
            stroke
        )

        pdf.setLineWidth(
            0.8
        )

        pdf.roundRect(
            x,
            y,
            width,
            height,
            radius,
            fill=1,
            stroke=1
        )

    # =========================================================
    # GENERATE REPORT
    # =========================================================

    def generate_report(
        self,
        scan,
        image_path,
        output_path,
        local_guidance=None
    ):

        output_path = Path(
            output_path
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # =====================================================
        # PAGE
        # =====================================================

        page_width, page_height = A4

        pdf = canvas.Canvas(
            str(output_path),
            pagesize=A4
        )

        pdf.setTitle(
            "EcoVision AI Waste Analysis Report"
        )

        pdf.setAuthor(
            "EcoVision AI"
        )

        # =====================================================
        # COLORS
        # =====================================================

        dark_green = colors.HexColor(
            "#166534"
        )

        main_green = colors.HexColor(
            "#22C55E"
        )

        light_green = colors.HexColor(
            "#F0FDF4"
        )

        very_light = colors.HexColor(
            "#F8FAFC"
        )

        border_green = colors.HexColor(
            "#B7E4C7"
        )

        dark_text = colors.HexColor(
            "#0F172A"
        )

        normal_text = colors.HexColor(
            "#334155"
        )

        muted_text = colors.HexColor(
            "#64748B"
        )

        divider_color = colors.HexColor(
            "#D8ECDD"
        )

        # =====================================================
        # PAGE MARGIN
        # =====================================================

        margin = 32

        content_width = (
            page_width -
            (margin * 2)
        )

        # =====================================================
        # HEADER
        # =====================================================

        header_y = page_height - 48

        pdf.setFillColor(
            dark_green
        )

        pdf.setFont(
            "Helvetica-Bold",
            23
        )

        pdf.drawString(
            margin,
            header_y,
            "EcoVision AI"
        )

        pdf.setFont(
            "Helvetica",
            10
        )

        pdf.setFillColor(
            muted_text
        )

        pdf.drawString(
            margin,
            header_y - 17,
            "Intelligent Waste Analysis Report"
        )

        # Header line

        pdf.setStrokeColor(
            main_green
        )

        pdf.setLineWidth(
            2.5
        )

        pdf.line(
            margin,
            header_y - 31,
            page_width - margin,
            header_y - 31
        )

        # =====================================================
        # SCAN DATA
        # =====================================================

        scan_id = scan.get(
            "id",
            "N/A"
        )

        confidence = scan.get(
            "confidence",
            0
        )

        created_at = scan.get(
            "created_at",
            datetime.now().isoformat(
                timespec="seconds"
            )
        )

        filename = scan.get(
            "filename",
            "Unknown"
        )

        waste_type = str(
            scan.get(
                "waste_type",
                "Unknown"
            )
        ).replace(
            "_",
            " "
        ).title()

        category = scan.get(
            "category",
            "Unknown"
        )

        material = scan.get(
            "material",
            "Unknown"
        )

        recyclable = bool(
            scan.get(
                "recyclable",
                False
            )
        )

        recyclable_text = (
            "Recyclable"
            if recyclable
            else "Not Recyclable"
        )

        recommended_bin = scan.get(
            "recommended_bin",
            "General Waste"
        )

        disposal = scan.get(
            "disposal_instruction",
            "No disposal instruction available."
        )

        handling = scan.get(
            "handling_instruction",
            "No handling instruction available."
        )

        eco_tip = scan.get(
            "eco_tip",
            "Reduce, reuse and recycle whenever possible."
        )

        # =====================================================
        # LOCAL GUIDANCE
        # =====================================================

        if local_guidance is None:
            local_guidance = {}

        local_city = local_guidance.get(
            "city",
            "Indore"
        )

        local_instruction = local_guidance.get(
            "local_instruction",
            (
                "Follow local municipal "
                "waste-segregation rules "
                "and use the appropriate "
                "waste stream."
            )
        )

        important_note = local_guidance.get(
            "important_note",
            (
                "Local collection rules and "
                "authorized facilities can change. "
                "Verify current municipal guidance "
                "before disposal."
            )
        )

        # =====================================================
        # META INFORMATION BOX
        # =====================================================

        meta_y = page_height - 125

        meta_height = 48

        self.rounded_box(
            pdf,
            margin,
            meta_y,
            content_width,
            meta_height,
            light_green,
            border_green,
            8
        )

        # -----------------------------------------------------
        # SCAN ID
        # -----------------------------------------------------

        pdf.setFont(
            "Helvetica-Bold",
            8
        )

        pdf.setFillColor(
            dark_green
        )

        pdf.drawString(
            margin + 14,
            meta_y + 30,
            "SCAN ID"
        )

        pdf.setFont(
            "Helvetica-Bold",
            9
        )

        pdf.setFillColor(
            dark_text
        )

        pdf.drawString(
            margin + 55,
            meta_y + 30,
            str(scan_id)
        )

        # -----------------------------------------------------
        # CONFIDENCE
        # -----------------------------------------------------

        pdf.setFont(
            "Helvetica-Bold",
            8
        )

        pdf.setFillColor(
            dark_green
        )

        pdf.drawString(
            margin + 120,
            meta_y + 30,
            "CONFIDENCE"
        )

        pdf.setFont(
            "Helvetica-Bold",
            9
        )

        pdf.setFillColor(
            dark_text
        )

        pdf.drawString(
            margin + 190,
            meta_y + 30,
            f"{confidence}%"
        )

        # -----------------------------------------------------
        # DATE
        # -----------------------------------------------------

        pdf.setFont(
            "Helvetica-Bold",
            8
        )

        pdf.setFillColor(
            dark_green
        )

        pdf.drawString(
            margin + 250,
            meta_y + 30,
            "DATE"
        )

        pdf.setFont(
            "Helvetica-Bold",
            8.5
        )

        pdf.setFillColor(
            dark_text
        )

        pdf.drawString(
            margin + 285,
            meta_y + 30,
            str(created_at)
        )

        # -----------------------------------------------------
        # FILE
        # -----------------------------------------------------

        pdf.setFont(
            "Helvetica-Bold",
            8
        )

        pdf.setFillColor(
            dark_green
        )

        pdf.drawString(
            margin + 14,
            meta_y + 12,
            "FILE"
        )

        pdf.setFont(
            "Helvetica",
            8.5
        )

        pdf.setFillColor(
            dark_text
        )

        pdf.drawString(
            margin + 55,
            meta_y + 12,
            str(filename)[:75]
        )

        # =====================================================
        # DETECTION SUMMARY TITLE
        # =====================================================

        title_y = meta_y - 28

        pdf.setFont(
            "Helvetica-Bold",
            13
        )

        pdf.setFillColor(
            dark_green
        )

        pdf.drawString(
            margin,
            title_y,
            "Detection Summary"
        )

        # =====================================================
        # IMAGE + DETAILS
        # =====================================================

        section_top = title_y - 17

        image_width = 245

        image_height = 175

        image_x = margin

        image_y = (
            section_top -
            image_height
        )

        # -----------------------------------------------------
        # IMAGE BOX
        # -----------------------------------------------------

        self.rounded_box(
            pdf,
            image_x,
            image_y,
            image_width,
            image_height,
            very_light,
            border_green,
            8
        )

        # -----------------------------------------------------
        # IMAGE
        # -----------------------------------------------------

        image_file = Path(
            image_path
        )

        if image_file.exists():

            try:

                image_reader = ImageReader(
                    str(image_file)
                )

                img_w, img_h = (
                    image_reader.getSize()
                )

                inner_width = (
                    image_width - 16
                )

                inner_height = (
                    image_height - 16
                )

                scale = min(
                    inner_width / img_w,
                    inner_height / img_h
                )

                draw_width = (
                    img_w * scale
                )

                draw_height = (
                    img_h * scale
                )

                draw_x = (
                    image_x +
                    (
                        image_width -
                        draw_width
                    ) / 2
                )

                draw_y = (
                    image_y +
                    (
                        image_height -
                        draw_height
                    ) / 2
                )

                pdf.drawImage(
                    image_reader,
                    draw_x,
                    draw_y,
                    width=draw_width,
                    height=draw_height,
                    preserveAspectRatio=True,
                    mask="auto"
                )

            except Exception:

                pdf.setFont(
                    "Helvetica",
                    10
                )

                pdf.setFillColor(
                    muted_text
                )

                pdf.drawCentredString(
                    image_x +
                    image_width / 2,
                    image_y +
                    image_height / 2,
                    "Image unavailable"
                )

        else:

            pdf.setFont(
                "Helvetica",
                10
            )

            pdf.setFillColor(
                muted_text
            )

            pdf.drawCentredString(
                image_x +
                image_width / 2,
                image_y +
                image_height / 2,
                "Image unavailable"
            )

        # =====================================================
        # DETECTION DETAILS BOX
        # =====================================================

        details_x = (
            image_x +
            image_width +
            18
        )

        details_width = (
            content_width -
            image_width -
            18
        )

        details_height = image_height

        details_y = image_y

        self.rounded_box(
            pdf,
            details_x,
            details_y,
            details_width,
            details_height,
            light_green,
            border_green,
            8
        )

        rows = [
            (
                "Detected Waste",
                waste_type
            ),
            (
                "Category",
                category
            ),
            (
                "Material",
                material
            ),
            (
                "Recyclability",
                recyclable_text
            ),
            (
                "Recommended Bin",
                recommended_bin
            ),
        ]

        row_y = (
            details_y +
            details_height -
            29
        )

        row_gap = 29

        for label, value in rows:

            pdf.setFont(
                "Helvetica-Bold",
                8
            )

            pdf.setFillColor(
                muted_text
            )

            pdf.drawString(
                details_x + 14,
                row_y,
                label
            )

            pdf.setFont(
                "Helvetica-Bold",
                10
            )

            pdf.setFillColor(
                dark_text
            )

            value_text = str(
                value
            )

            pdf.drawString(
                details_x + 112,
                row_y,
                value_text[:28]
            )

            pdf.setStrokeColor(
                divider_color
            )

            pdf.setLineWidth(
                0.6
            )

            pdf.line(
                details_x + 12,
                row_y - 9,
                details_x +
                details_width - 12,
                row_y - 9
            )

            row_y -= row_gap

        # =====================================================
        # RESPONSIBLE DISPOSAL GUIDANCE
        # =====================================================

        guidance_title_y = (
            image_y - 32
        )

        pdf.setFont(
            "Helvetica-Bold",
            13
        )

        pdf.setFillColor(
            dark_green
        )

        pdf.drawString(
            margin,
            guidance_title_y,
            "Responsible Disposal Guidance"
        )

        # -----------------------------------------------------
        # GUIDANCE BOX
        # -----------------------------------------------------

        guidance_height = 180

        guidance_y = (
            guidance_title_y -
            20 -
            guidance_height
        )

        self.rounded_box(
            pdf,
            margin,
            guidance_y,
            content_width,
            guidance_height,
            very_light,
            border_green,
            8
        )

        # -----------------------------------------------------
        # DISPOSAL INSTRUCTION
        # -----------------------------------------------------

        disposal_title_y = (
            guidance_y +
            guidance_height -
            25
        )

        pdf.setFont(
            "Helvetica-Bold",
            8.5
        )

        pdf.setFillColor(
            dark_green
        )

        pdf.drawString(
            margin + 16,
            disposal_title_y,
            "DISPOSAL INSTRUCTION"
        )

        self.draw_wrapped_text(
            pdf,
            disposal,
            margin + 16,
            disposal_title_y - 17,
            content_width - 32,
            font_name="Helvetica",
            font_size=8.5,
            color=normal_text,
            line_height=11,
            max_lines=2
        )

        # -----------------------------------------------------
        # FIRST DIVIDER
        # -----------------------------------------------------

        divider_1 = (
            guidance_y +
            guidance_height -
            64
        )

        pdf.setStrokeColor(
            divider_color
        )

        pdf.setLineWidth(
            0.6
        )

        pdf.line(
            margin + 16,
            divider_1,
            page_width - margin - 16,
            divider_1
        )

        # -----------------------------------------------------
        # HANDLING INSTRUCTION
        # -----------------------------------------------------

        handling_title_y = (
            divider_1 - 17
        )

        pdf.setFont(
            "Helvetica-Bold",
            8.5
        )

        pdf.setFillColor(
            dark_green
        )

        pdf.drawString(
            margin + 16,
            handling_title_y,
            "HANDLING INSTRUCTION"
        )

        self.draw_wrapped_text(
            pdf,
            handling,
            margin + 16,
            handling_title_y - 17,
            content_width - 32,
            font_name="Helvetica",
            font_size=8.5,
            color=normal_text,
            line_height=11,
            max_lines=2
        )

        # -----------------------------------------------------
        # SECOND DIVIDER
        # -----------------------------------------------------

        divider_2 = (
            handling_title_y - 42
        )

        pdf.line(
            margin + 16,
            divider_2,
            page_width - margin - 16,
            divider_2
        )

        # -----------------------------------------------------
        # ECO TIP
        # -----------------------------------------------------

        eco_title_y = (
            divider_2 - 17
        )

        pdf.setFont(
            "Helvetica-Bold",
            8.5
        )

        pdf.setFillColor(
            dark_green
        )

        pdf.drawString(
            margin + 16,
            eco_title_y,
            "ECO TIP"
        )

        self.draw_wrapped_text(
            pdf,
            eco_tip,
            margin + 16,
            eco_title_y - 17,
            content_width - 32,
            font_name="Helvetica",
            font_size=8.5,
            color=normal_text,
            line_height=11,
            max_lines=2
        )

        # =====================================================
        # LOCAL DISPOSAL GUIDANCE
        # =====================================================

        local_title_y = (
            guidance_y - 30
        )

        pdf.setFont(
            "Helvetica-Bold",
            12
        )

        pdf.setFillColor(
            dark_green
        )

        pdf.drawString(
            margin,
            local_title_y,
            f"Local Disposal Guidance — {local_city}"
        )

        # -----------------------------------------------------
        # LOCAL GUIDANCE BOX
        # -----------------------------------------------------

        local_box_height = 86

        local_box_y = (
            local_title_y -
            14 -
            local_box_height
        )

        self.rounded_box(
            pdf,
            margin,
            local_box_y,
            content_width,
            local_box_height,
            light_green,
            border_green,
            8
        )

        # -----------------------------------------------------
        # RECOMMENDED ACTION
        # -----------------------------------------------------

        pdf.setFont(
            "Helvetica-Bold",
            8
        )

        pdf.setFillColor(
            dark_green
        )

        pdf.drawString(
            margin + 14,
            local_box_y + 66,
            "RECOMMENDED ACTION"
        )

        self.draw_wrapped_text(
            pdf,
            local_instruction,
            margin + 14,
            local_box_y + 50,
            content_width - 28,
            font_name="Helvetica",
            font_size=8.5,
            color=normal_text,
            line_height=10,
            max_lines=2
        )

        # -----------------------------------------------------
        # IMPORTANT NOTE
        # -----------------------------------------------------

        pdf.setFont(
            "Helvetica-Bold",
            8
        )

        pdf.setFillColor(
            dark_green
        )

        pdf.drawString(
            margin + 14,
            local_box_y + 25,
            "IMPORTANT NOTE"
        )

        self.draw_wrapped_text(
            pdf,
            important_note,
            margin + 14,
            local_box_y + 11,
            content_width - 28,
            font_name="Helvetica",
            font_size=7.5,
            color=muted_text,
            line_height=9,
            max_lines=1
        )

        # =====================================================
        # FOOTER
        # =====================================================

        footer_line_y = 62

        pdf.setStrokeColor(
            border_green
        )

        pdf.setLineWidth(
            1
        )

        pdf.line(
            margin,
            footer_line_y,
            page_width - margin,
            footer_line_y
        )

        # Left footer

        pdf.setFont(
            "Helvetica-Bold",
            10
        )

        pdf.setFillColor(
            dark_green
        )

        pdf.drawString(
            margin,
            43,
            "EcoVision AI"
        )

        pdf.setFont(
            "Helvetica",
            8
        )

        pdf.setFillColor(
            muted_text
        )

        pdf.drawString(
            margin,
            29,
            "AI-powered responsible waste management"
        )

        # Right footer

        pdf.drawRightString(
            page_width - margin,
            43,
            "Waste Analysis Report"
        )

        pdf.drawRightString(
            page_width - margin,
            29,
            "Generated automatically"
        )

        # =====================================================
        # SAVE ONE PAGE ONLY
        # =====================================================

        pdf.showPage()

        pdf.save()

        return str(output_path)


# =========================================================
# REPORT AGENT INSTANCE
# =========================================================

report_agent = ReportAgent()