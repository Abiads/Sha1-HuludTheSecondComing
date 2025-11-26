

import base64
import binascii
import json
import streamlit as st

# -------------------------------------------------
# Modern UI Theme + Page Setup
# -------------------------------------------------
st.set_page_config(
    page_title="Sha1-Hulud: The Second Coming",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inject premium CSS styling
st.markdown(
    """
    <style>

    /* Global UI */
    body {
        font-family: 'Inter', sans-serif;
        background: #0d0f17;
    }
    .main {
        background: #0d0f17;
        padding-top: 2rem;
    }

    /* Title */
    h1 {
        font-weight: 700 !important;
        color: #e2e8f0 !important;
        letter-spacing: -1px;
    }

    /* Subtle caption */
    .caption-text {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-top: -10px;
        margin-bottom: 20px;
    }

    /* Textarea */
    textarea {
        background: #11121a !important;
        color: #e2e8f0 !important;
        border-radius: 12px !important;
        border: 1px solid #2c3242 !important;
        font-family: "JetBrains Mono", monospace !important;
        padding: 15px !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: white;
        padding: 0.6rem 1.4rem;
        border-radius: 10px;
        border: none;
        font-weight: 600;
        transition: 0.2s ease-in-out;
    }
    .stButton>button:hover {
        transform: scale(1.03);
        filter: brightness(1.15);
    }

    /* Success box */
    .status-box {
        padding: 12px 18px;
        border-radius: 10px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #34d399;
        font-weight: 500;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown("<h1>🧩 Sha1-Hulud: The Second Coming</h1>", unsafe_allow_html=True)
st.markdown(
    "<div class='caption-text'>A powerful demonstration: Base64 is <strong>encoding</strong>, not encryption.</div>",
    unsafe_allow_html=True,
)

# -------------------------------------------------
# Layout: Two Columns
# -------------------------------------------------
left, right = st.columns([1.1, 1.3])

with left:
    st.markdown(
        """
        ### 🔍 What this tool does

        - Decodes **Base64** safely  
        - Optional **second-layer Base64 decode**  
        - Pretty-prints JSON automatically  
        - Helps educate people that **Base64 ≠ security**

        **⚠️ Warning:** Never paste real credentials or production secrets here.
        """
    )

    st.info(
        "This tool is for awareness and educational purposes only.",
        icon="⚠️",
    )

with right:
    b64_input = st.text_area(
        "Base64 Input",
        placeholder="Paste Base64 text here…",
        height=230,
    )

    double_decode = st.checkbox(
        "Try double decode (Base64 wrapped inside Base64)",
        value=True,
    )

    decode_clicked = st.button("🔓 Decode Base64", type="primary")

# -------------------------------------------------
# Decoding helper
# -------------------------------------------------
def safe_b64_decode(data: str) -> str:
    """
    Decode a Base64 string safely and return text.
    - Strips whitespace
    - Attempts to fix missing padding
    - Returns UTF-8 text if possible, otherwise repr of bytes
    """
    data = data.strip()

    # Add padding if missing
    missing = len(data) % 4
    if missing:
        data += "=" * (4 - missing)

    try:
        raw = base64.b64decode(data, validate=False)
    except binascii.Error as e:
        raise ValueError(f"Invalid Base64 data: {e}")

    # Try UTF-8 decode; if fails, show a safe bytes repr
    try:
        return raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        # Fallback: show bytes representation (still useful for secrets)
        return repr(raw)

# -------------------------------------------------
# Handle Decode Button Click
# -------------------------------------------------
if decode_clicked:
    if not b64_input or not b64_input.strip():
        st.error("❌ No Base64 input provided.")
    else:
        decoded_text = ""
        layers = 0
        probably_json = False

        try:
            # First decode
            decoded_text = safe_b64_decode(b64_input)
            layers = 1

            # Optional second decode
            if double_decode:
                try:
                    decoded_text = safe_b64_decode(decoded_text)
                    layers = 2
                except Exception as inner_e:
                    decoded_text += (
                        "\n\n[!] Double-decode failed: " + str(inner_e)
                    )

            # Heuristic: looks like JSON?
            stripped = decoded_text.strip()
            if stripped.startswith("{") or stripped.startswith("["):
                probably_json = True
                # Try to pretty-print JSON
                try:
                    parsed_json = json.loads(stripped)
                    decoded_text = json.dumps(
                        parsed_json, indent=2, ensure_ascii=False
                    )
                except Exception:
                    # If parsing fails, just keep raw decoded_text
                    pass

        except Exception as e:
            st.error(f"❌ Decode error: {e}")
        else:
            # Output layout
            res_left, res_right = st.columns([0.9, 2.1])

            with res_left:
                st.markdown(
                    f"<div class='status-box'>✅ {layers} layer"
                    f"{'s' if layers > 1 else ''} decoded</div>",
                    unsafe_allow_html=True,
                )
                if probably_json:
                    st.caption("Looks like JSON 🧾")
                st.caption(f"Output length: {len(decoded_text)} characters")

            with res_right:
                st.subheader("Decoded Output")
                st.code(decoded_text or "(empty output)", language="text")
