#!/usr/bin/env python
"""Pure-Python SVG -> PDF converter (no external deps).

Handles the subset of SVG used by 05_paper/figures/generated/*.svg:
rect, line, polyline, circle, text (with rotate transform), basic colors.
"""
import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path


def _color(v, default=None):
    if not v:
        return default
    v = v.strip()
    if v.startswith("#"):
        h = v.lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if len(h) == 6:
            return (int(h[0:2], 16) / 255.0,
                    int(h[2:4], 16) / 255.0,
                    int(h[4:6], 16) / 255.0)
    named = {"black": (0, 0, 0), "white": (1, 1, 1), "red": (1, 0, 0),
             "green": (0, 0.5, 0), "blue": (0, 0, 1), "gray": (0.5, 0.5, 0.5),
             "grey": (0.5, 0.5, 0.5)}
    return named.get(v.lower(), default)


def _f(v, default=0.0):
    if v is None:
        return default
    v = v.strip()
    if v.endswith("px"):
        v = v[:-2]
    try:
        return float(v)
    except ValueError:
        return default


NS = "{http://www.w3.org/2000/svg}"


def convert(svg_path, pdf_path):
    tree = ET.parse(svg_path)
    root = tree.getroot()
    w = _f(root.get("width", "560"))
    h = _f(root.get("height", "340"))
    vb = root.get("viewBox")
    if vb:
        parts = vb.split()
        if len(parts) == 4:
            _, _, vw, vh = parts
            sx = w / float(vw)
            sy = h / float(vh)
        else:
            sx = sy = 1.0
    else:
        sx = sy = 1.0

    # Collect content stream ops.
    ops = []
    ops.append("q")
    # scale from viewBox to width/height if needed
    if sx != 1.0 or sy != 1.0:
        ops.append(f"{sx} 0 0 {sy} 0 0 cm")

    def transform_point(x, y):
        return x, h - y  # flip y

    # We'll process children recursively (no nesting groups beyond root).
    font_size = _f(root.get("font-size", "11"))
    font_family = root.get("font-family", "Helvetica")

    def set_stroke(color, width):
        if color is not None:
            ops.append(f"{color[0]:.4f} {color[1]:.4f} {color[2]:.4f} RG")
        ops.append(f"{width:.3f} w")

    def set_fill(color):
        if color is not None:
            ops.append(f"{color[0]:.4f} {color[1]:.4f} {color[2]:.4f} rg")

    for el in root:
        tag = el.tag.replace(NS, "")
        if tag == "rect":
            x = _f(el.get("x", "0"))
            y = _f(el.get("y", "0"))
            rw = _f(el.get("width", "0"))
            rh = _f(el.get("height", "0"))
            fill = _color(el.get("fill"))
            stroke = _color(el.get("stroke"))
            sw = _f(el.get("stroke-width", "1")) if el.get("stroke") else 0
            x0, y0 = transform_point(x, y + rh)  # bottom-left in PDF
            if fill is not None:
                set_fill(fill)
                ops.append(f"{x0:.3f} {y0:.3f} {rw * sx:.3f} {rh * sy:.3f} re f")
            if stroke is not None and sw > 0:
                set_stroke(stroke, sw)
                ops.append(f"{x0:.3f} {y0:.3f} {rw * sx:.3f} {rh * sy:.3f} re S")
        elif tag == "line":
            x1 = _f(el.get("x1")); y1 = _f(el.get("y1"))
            x2 = _f(el.get("x2")); y2 = _f(el.get("y2"))
            stroke = _color(el.get("stroke"), (0, 0, 0))
            sw = _f(el.get("stroke-width", "1"))
            set_stroke(stroke, sw)
            ax, ay = transform_point(x1, y1)
            bx, by = transform_point(x2, y2)
            ops.append(f"{ax:.3f} {ay:.3f} m {bx:.3f} {by:.3f} l S")
        elif tag == "polyline" or tag == "polygon":
            pts = el.get("points", "").strip().split()
            coords = []
            for p in pts:
                if "," in p:
                    a, b = p.split(",")
                    coords.append((_f(a), _f(b)))
                else:
                    # space separated pairs
                    pass
            # handle case where points are "x,y x,y"
            if not coords:
                nums = re.findall(r"[-+]?\d*\.?\d+", el.get("points", ""))
                for i in range(0, len(nums) - 1, 2):
                    coords.append((_f(nums[i]), _f(nums[i + 1])))
            stroke = _color(el.get("stroke"))
            fill = _color(el.get("fill"))
            sw = _f(el.get("stroke-width", "1"))
            if coords:
                first = coords[0]
                fx, fy = transform_point(*first)
                ops.append(f"{fx:.3f} {fy:.3f} m")
                for (px, py) in coords[1:]:
                    qx, qy = transform_point(px, py)
                    ops.append(f"{qx:.3f} {qy:.3f} l")
                if stroke is not None:
                    set_stroke(stroke, sw)
                    ops.append("S")
                if fill is not None and fill != "none" and tag == "polygon":
                    set_fill(fill)
                    ops.append("f")
        elif tag == "circle":
            cx = _f(el.get("cx")); cy = _f(el.get("cy")); r = _f(el.get("r"))
            fill = _color(el.get("fill"))
            stroke = _color(el.get("stroke"))
            sw = _f(el.get("stroke-width", "1")) if el.get("stroke") else 0
            # approximate circle with 4 bezier curves
            k = 0.5522847498
            x0, y0 = transform_point(cx, cy)
            r_px = r * sx
            r_py = r * sy
            ops.append(f"{x0 + r_px:.3f} {y0:.3f} m")
            ops.append(f"{x0 + r_px:.3f} {y0 + k * r_py:.3f} "
                      f"{x0 + k * r_px:.3f} {y0 + r_py:.3f} "
                      f"{x0:.3f} {y0 + r_py:.3f} c")
            ops.append(f"{x0 - k * r_px:.3f} {y0 + r_py:.3f} "
                      f"{x0 - r_px:.3f} {y0 + k * r_py:.3f} "
                      f"{x0 - r_px:.3f} {y0:.3f} c")
            ops.append(f"{x0 - r_px:.3f} {y0 - k * r_py:.3f} "
                      f"{x0 - k * r_px:.3f} {y0 - r_py:.3f} "
                      f"{x0:.3f} {y0 - r_py:.3f} c")
            ops.append(f"{x0 + k * r_px:.3f} {y0 - r_py:.3f} "
                      f"{x0 + r_px:.3f} {y0 - k * r_py:.3f} "
                      f"{x0 + r_px:.3f} {y0:.3f} c")
            if fill is not None:
                set_fill(fill)
                ops.append("f")
            if stroke is not None and sw > 0:
                set_stroke(stroke, sw)
                ops.append("S")
        elif tag == "text":
            txt = (el.text or "").strip()
            if not txt:
                continue
            x = _f(el.get("x", "0"))
            y = _f(el.get("y", "0"))
            fs = _f(el.get("font-size", str(font_size)))
            anchor = el.get("text-anchor", "start")
            transform = el.get("transform", "")
            # parse rotate(-90 cx cy)
            rotate = 0
            rcx = ry = 0
            m = re.search(r"rotate\(([-\d.]+)(?:\s+([-\d.]+)\s+([-\d.]+))?\)", transform)
            if m:
                rotate = float(m.group(1))
                if m.group(2) is not None:
                    rcx = float(m.group(2))
                    ry = float(m.group(3))
            px, py = transform_point(x, y)
            # Adjust for text anchor
            # approximate width
            approx_w = len(txt) * fs * 0.5
            if anchor == "middle":
                tx = -approx_w / 2
            elif anchor == "end":
                tx = -approx_w
            else:
                tx = 0
            ops.append("BT")
            ops.append(f"/F1 {fs:.2f} Tf")
            if rotate:
                # rotate around (rcx, h-ry)
                cxp, cyp = transform_point(rcx, ry)
                rad = rotate * 3.14159265 / 180.0
                cos = __import__("math").cos(rad)
                sin = __import__("math").sin(rad)
                # translate to center, rotate, translate back
                ops.append(f"1 0 0 1 {cxp:.3f} {cyp:.3f} Tm")
                ops.append(f"{cos:.4f} {sin:.4f} {-sin:.4f} {cos:.4f} 0 0 Tm")
                ops.append(f"1 0 0 1 {-cxp:.3f} {-cyp:.3f} Tm")
            ops.append(f"1 0 0 1 {px + tx:.3f} {py:.3f} Tm")
            # escape text
            safe = txt.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            ops.append(f"({safe}) Tj")
            ops.append("ET")

    ops.append("Q")

    content = "\n".join(ops).encode("latin-1", "replace")

    # Build PDF
    objects = []
    def add(obj):
        objects.append(obj)
        return len(objects)

    # Font object
    font_obj = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    # Content stream
    content_obj = add(b"<< /Length %d >>\nstream\n" % len(content) + content + b"\nendstream")
    # Page
    page_obj = add((f"<< /Type /Page /Parent 4 0 R /MediaBox [0 0 {w} {h}] "
                    f"/Resources << /Font << /F1 {font_obj} 0 R >> >> "
                    f"/Contents {content_obj} 0 R >>").encode())
    # Pages
    pages_obj = add(f"<< /Type /Pages /Kids [{page_obj} 0 R] /Count 1 >>".encode())
    # Fix page parent reference (pages is object 4)
    # We added pages after page; page referenced Parent 4 0 R. Need ensure pages is object 4.
    # Reorder: we need pages before page. Rebuild carefully.
    # Simpler: regenerate with pages first.

    # Rebuild properly
    objects = []
    font_obj = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    pages_placeholder = add(None)  # placeholder for pages
    content_obj = add(b"<< /Length %d >>\nstream\n" % len(content) + content + b"\nendstream")
    page_obj = add((f"<< /Type /Page /Parent {pages_placeholder} 0 R /MediaBox [0 0 {w} {h}] "
                    f"/Resources << /Font << /F1 {font_obj} 0 R >> >> "
                    f"/Contents {content_obj} 0 R >>").encode())
    # fill pages
    objects[pages_placeholder - 1] = f"<< /Type /Pages /Kids [{page_obj} 0 R] /Count 1 >>".encode()
    catalog_obj = add(f"<< /Type /Catalog /Pages {pages_placeholder} 0 R >>".encode())

    # Write file
    out = Path(pdf_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as fh:
        fh.write(b"%PDF-1.4\n")
        offsets = [0]
        for i, obj in enumerate(objects, start=1):
            offsets.append(fh.tell())
            fh.write(f"{i} 0 obj\n".encode())
            fh.write(obj)
            fh.write(b"\nendobj\n")
        xref_pos = fh.tell()
        fh.write(f"xref\n0 {len(objects) + 1}\n".encode())
        fh.write(b"0000000000 65535 f \n")
        for i in range(1, len(objects) + 1):
            fh.write(f"{offsets[i]:010d} 00000 n \n".encode())
        fh.write(f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_obj} 0 R >>\n".encode())
        fh.write(f"startxref\n{xref_pos}\n%%EOF\n".encode())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    convert(args.inp, args.out)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
