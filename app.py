from flask import Flask, jsonify, request
from flask_cors import CORS
from googleapiclient.discovery import build
from google.oauth2 import service_account



# Google API Credentials
SERVICE_ACCOUNT_FILE = "ics-timeline-8bf43b8105c7.json"  # Path to your JSON key file

# Google Doc ID
DOCUMENT_ID = "1t8Kwum1qJLqZLu-fG2tiE7cszsKg44c2LEHjWL9AXYQ"

app = Flask(__name__)
CORS(app)

SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

def get_google_doc_html():
    service = build('docs', 'v1', credentials=credentials)
    document = service.documents().get(documentId=DOCUMENT_ID).execute()

    content = ""
    for element in document.get("body", {}).get("content", []):
        if "paragraph" in element:
            paragraph = element["paragraph"]
            para_text = ""

            for elem in paragraph["elements"]:
                text_run = elem.get("textRun")
                if text_run:
                    text = text_run["content"].strip()
                    
                    # Extract styling
                    styles = text_run.get("textStyle", {})
                    bold = styles.get("bold", False)
                    italic = styles.get("italic", False)
                    underline = styles.get("underline", False)
                    font_size = styles.get("fontSize", {}).get("magnitude", 12)
                    link = styles.get("link", {}).get("url")
                    
                    # Apply styles
                    if bold:
                        text = f" <b>{text}</b> "
                    if italic:
                        text = f" <i>{text}</i> "
                    if underline:
                        text = f" <u>{text}</u> "
                    if link:
                        text = f' <a href="{link}" target="_blank">{text}</a> '

                    # Apply font size
                    scaled_font_size = int(font_size * 1.4)  # Increase font size by 50%
                    text = f'<span style="font-size: {scaled_font_size}px;">{text}</span>'
                    para_text += text

            # Detect heading levels
            heading_styles = {
                "HEADING_1": "h1",
                "HEADING_2": "h2",
                "HEADING_3": "h3",
                "HEADING_4": "h4",
                "HEADING_5": "h5",
                "HEADING_6": "h6"
            }
            heading_tag = heading_styles.get(paragraph.get("paragraphStyle", {}).get("namedStyleType"))

            # Detect alignment
            alignment_styles = {
                "START": "left",
                "CENTER": "center",
                "END": "right",
                "JUSTIFIED": "justify"
            }
            alignment = alignment_styles.get(paragraph.get("paragraphStyle", {}).get("alignment"), "left")

            # Convert content based on detected styles
            if heading_tag:
                content += f'<{heading_tag} style="text-align: {alignment};">{para_text}</{heading_tag}>'
            elif paragraph.get("bullet"):
                content += f'<li>{para_text}</li>'
            else:
                content += f'<p style="text-align: {alignment};">{para_text}</p>'

    return f"<div>{content}</div>"

@app.route('/get-doc', methods=['GET'])
def get_doc():
    return jsonify({"content": get_google_doc_html()})

if __name__ == "__main__":
    from os import environ
    app.run(host="0.0.0.0", port=int(environ.get("PORT", 5000)), debug=True)


