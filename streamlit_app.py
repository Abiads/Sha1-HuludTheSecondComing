import base64
import binascii
import json
import streamlit as st


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


def main():
    st.set_page_config(
        page_title="Sha1-Hulud: The Second Coming",
        layout="wide",
    )

    st.title("Sha1-Hulud: The Second Coming")
    st.caption("Base64 is encoding, not encryption. Decode and inspect safely.")

    col_left, col_right = st.columns([1.1, 1.2])

    with col_left:
        st.markdown(
            """
            Paste any **Base64-encoded string** in the panel on the right.

            This app will decode it and show you the real content, optionally trying
            to decode **a second Base64 layer** if your data is wrapped twice.

            > Never paste live production secrets or credentials here.
            """
        )

        st.info(
            "Educational demo only. Treat Base64 as plain text, not security.",
            icon="⚠️",
        )

    with col_right:
        b64_input = st.text_area(
            "Base64 input",
            placeholder="Paste Base64 here...",
            height=220,
        )
        double_decode = st.checkbox(
            "Try double decode (Base64 wrapped in Base64)",
            value=True,
        )

        decode_clicked = st.button("🧩 Decode Base64", type="primary")

    if decode_clicked:
        if not b64_input.strip():
            st.error("No Base64 input provided.")
            return

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

                # Try to pretty-print JSON for nicer formatting in the UI
                try:
                    parsed_json = json.loads(stripped)
                    decoded_text = json.dumps(
                        parsed_json, indent=2, ensure_ascii=False
                    )
                except Exception:
                    # If it fails, just show the raw decoded text
                    pass

        except Exception as e:
            st.error(f"Decode error: {e}")
            return

        # Show result
        cols = st.columns([1, 3])
        with cols[0]:
            label = f"{layers} layer{'s' if layers > 1 else ''} decoded"
            st.success(label)
            if probably_json:
                st.caption("Looks like JSON 🧾")

        with cols[1]:
            st.code(decoded_text or "(empty output)", language="text")


if __name__ == "__main__":
    main()


