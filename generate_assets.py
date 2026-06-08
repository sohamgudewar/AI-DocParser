"""Generate placeholder NDVI overlays and sample documents for KrishiNetra demo."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import json

BASE = os.path.dirname(os.path.abspath(__file__))
NDVI_DIR = os.path.join(BASE, "krishinetra_mvp", "data", "ndvi_overlays")

os.makedirs(NDVI_DIR, exist_ok=True)

def make_ndvi_overlay(filename, pattern="mixed", size=(400, 400)):
    arr = np.zeros((size[1], size[0]), dtype=np.float32)
    cy, cx = size[1] // 2, size[0] // 2
    for y in range(size[1]):
        for x in range(size[0]):
            dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2) / (size[0] * 0.4)
            noise = np.random.normal(0, 0.08)
            if pattern == "healthy":
                val = 0.7 - dist * 0.3 + noise
            elif pattern == "stressed":
                val = 0.5 - dist * 0.4 + noise
                val += 0.2 * np.sin(x * 0.05) * np.cos(y * 0.05)
            elif pattern == "mixed":
                val = 0.6 - dist * 0.3 + noise
                val += 0.15 * np.sin(x * 0.03 + y * 0.02)
            elif pattern == "dry":
                val = 0.25 + noise * 0.5
            else:
                val = 0.5 + noise
            arr[y, x] = np.clip(val, 0.0, 1.0)
    cmap = np.zeros((size[1], size[0], 4), dtype=np.uint8)
    r_mask = arr < 0.3
    y_mask = (arr >= 0.3) & (arr <= 0.5)
    g_mask = arr > 0.5
    cmap[r_mask] = [255, 50, 50, 180]
    cmap[y_mask] = [255, 230, 50, 160]
    cmap[g_mask] = [50, 200, 80, 140]
    img = Image.fromarray(cmap, "RGBA")
    img.save(os.path.join(NDVI_DIR, filename))
    print(f"  Created {filename}")

print("Generating NDVI overlays...")
make_ndvi_overlay("vidarbha_cotton_ndvi.png", "stressed")
make_ndvi_overlay("nashik_onion_ndvi.png", "mixed")
make_ndvi_overlay("pune_sugarcane_ndvi.png", "healthy")
make_ndvi_overlay("marathwada_soybean_ndvi.png", "dry")
make_ndvi_overlay("western_maharashtra_sugarcane_ndvi.png", "mixed")
make_ndvi_overlay("konkan_rice_ndvi.png", "healthy")

print("Creating sample PDF document...")
try:
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Arial", "", r"C:\Windows\Fonts\arial.ttf", uni=True)
    pdf.add_font("Arial", "B", r"C:\Windows\Fonts\arialbd.ttf", uni=True)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Maharashtra Land Record (Satbara Utara)", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "", 11)
    details = [
        ("District", "Pune"),
        ("Taluka", "Sangamner"),
        ("Village", "Pimpalgaon"),
        ("Survey No.", "123/45"),
        ("Owner Name", "Rajesh Vitthal Patil"),
        ("Father's Name", "Vitthal Govind Patil"),
        ("Area (Hectares)", "3.25"),
        ("Crop Type", "Sugarcane"),
        ("Irrigation Type", "Drip Irrigation"),
        ("GPS Coordinates", "18.5204 N, 73.8567 E"),
        ("7/12 Extract Date", "15-Jan-2026"),
        ("Mutation Entry No.", "M-2026/458"),
    ]
    for label, value in details:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(60, 8, f"{label}:", border=1)
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 8, f" {value}", border=1, ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Land Use History", ln=True)
    pdf.set_font("Arial", "", 10)
    history = [
        ("2023-24", "Sugarcane", "32.5", "Good"),
        ("2022-23", "Sugarcane", "31.2", "Average"),
        ("2021-22", "Soybean", "28.0", "Good"),
        ("2020-21", "Cotton", "27.5", "Poor"),
    ]
    cols = ["Year", "Crop", "Yield (tonnes)", "Status"]
    pdf.set_font("Arial", "B", 10)
    for c in cols:
        pdf.cell(40, 8, c, border=1)
    pdf.ln()
    pdf.set_font("Arial", "", 10)
    for row in history:
        for val in row:
            pdf.cell(40, 8, val, border=1)
        pdf.ln()
    pdf.output(os.path.join(BASE, "krishinetra_mvp", "data", "sample_documents", "sample_land_record.pdf"))
    print("  Created sample_land_record.pdf")
except Exception as e:
    print(f"  PDF creation skipped (fallback to text): {e}")
    txt = "Sample Land Record - Maharashtra\nSurvey No: 123/45\nOwner: Rajesh Vitthal Patil\nArea: 3.25 Hectares\nCrop: Sugarcane\nGPS: 18.5204 N, 73.8567 E"
    with open(os.path.join(BASE, "krishinetra_mvp", "data", "sample_documents", "sample_land_record.txt"), "w") as f:
        f.write(txt)
    print("  Created sample_land_record.txt instead")

print("\nDone! All assets generated.")
