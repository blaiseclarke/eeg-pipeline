#!/usr/bin/env python3
import argparse
import base64


def create_html_report(image_files, output_path):
    print(f"Generating HTML report for {len(image_files)} images...")
    html = "<html><head><title>EEG Pipeline Report</title>"
    html += "<style>body {font-family: sans-serif; margin: 2em;} "
    html += "h1, h2 {color: #333;} img {max-width: 800px; border: 1px solid #ccc; margin-top: 1em;}</style>"
    html += "</head><body>"
    html += "<h1>EEG Power Spectral Density Report</h1>"

    for img_path in sorted(image_files):
        try:
            with open(img_path, "rb") as f:
                encoded_string = base64.b64encode(f.read()).decode("utf-8")
            html += f"<div><h2>{img_path}</h2>"
            html += f'<img src="data:image/png;base64,{encoded_string}">'
            html += "</div><hr>"
        except FileNotFoundError:
            print(f"Warning: Could not find image file {img_path}")

    html += "</body></html>"

    with open(output_path, "w") as f:
        f.write(html)
    print(f"Report saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create an HTML report from PNG images."
    )
    parser.add_argument(
        "--images", nargs="+", required=True, help="List of PNG image files"
    )
    parser.add_argument(
        "--output", type=str, required=True, help="Path to the output HTML file"
    )
    args = parser.parse_args()
    create_html_report(args.images, args.output)
