import os
import uuid

import streamlit as st

from database.repository import ReceiptRepository
from extractor.parser import ReceiptParser
from ocr.ocr_engine import extract_text
from export.csv_exporter import export_receipt_csv
from export.excel_exporter import export_receipt_excel
from export.pdf_exporter import export_receipt_pdf

import time
import pandas as pd


def extractor_page():

    page_start = time.perf_counter()
    # -------------------------------
    # Session State
    # -------------------------------

    if "receipt_info" not in st.session_state:
        st.session_state.receipt_info = None

    if "ocr_text" not in st.session_state:
        st.session_state.ocr_text = ""

    if "best_image" not in st.session_state:
        st.session_state.best_image = None

    if "angle" not in st.session_state:
        st.session_state.angle = 0

    if "confidence" not in st.session_state:
        st.session_state.confidence = 0.0

    if "image_path" not in st.session_state:
        st.session_state.image_path = ""

    if "receipt_type" not in st.session_state:
        st.session_state.receipt_type = ""

    if "timings" not in st.session_state:
        st.session_state.timings = None

    if "is_saved" not in st.session_state:
        st.session_state.is_saved = False

    if "csv_path" not in st.session_state:
        st.session_state.csv_path = ""

    if "excel_path" not in st.session_state:
        st.session_state.excel_path = ""

    if "pdf_path" not in st.session_state:
        st.session_state.pdf_path = ""


    # -------------------------------
    # Upload
    # -------------------------------
    t = time.perf_counter()

    receipt_type = st.selectbox(
        "Receipt Type",
        [
            "Pharmacy",
            "Grocery",
            "Restaurant",
            "Other"
        ]
    )

    if st.session_state.receipt_info is None:

        uploaded_file = st.file_uploader(
            "Upload Receipt",
            type=["jpg", "jpeg", "png"]
        )

    else:

        uploaded_file = None

    if uploaded_file:

        st.image(
            uploaded_file,
            caption="Uploaded Receipt",
            width=300
        )

    st.info(
        """
        📌 **Important**

        The accuracy of extracted information depends on the quality of the uploaded receipt.
        For best results, upload a clear, high-resolution image where all text is visible and readable.
        """
    )

    # -------------------------------
    # Extract Button
    # -------------------------------
    if uploaded_file is not None:

        
        if st.button("Extract Receipt", type="primary", use_container_width=True):

            if uploaded_file is None:

                st.warning("Please upload a receipt.")

            else:

                os.makedirs("uploads", exist_ok=True)

                extension = os.path.splitext(uploaded_file.name)[1]

                filename = f"{uuid.uuid4()}{extension}"

                image_path = os.path.join(
                    "uploads",
                    filename
                )

                with open(image_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                with st.spinner("Extracting receipt..."):

                    print("Calling OCR from:", extract_text.__module__)

                    ocr_text, best_image, angle, confidence, timings = extract_text(image_path)

                parser = ReceiptParser(
                    ocr_text,
                    receipt_type
                )

                info = parser.parse()

                print("\n===== AFTER PARSER =====")
                print(info["Items"])
                print("Length:", len(info["Items"]))

                st.session_state.receipt_info = info
                st.session_state.edited_items_df = pd.DataFrame(info["Items"])
                st.session_state.ocr_text = ocr_text
                st.session_state.best_image = best_image
                st.session_state.angle = angle
                st.session_state.confidence = confidence
                st.session_state.image_path = image_path
                st.session_state.receipt_type = receipt_type
                st.session_state.total = info["Total"]
                st.session_state.timings = timings

                st.success("Receipt extracted successfully.")

    # ==================================================
    # DISPLAY RESULTS
    # ==================================================

    if st.session_state.receipt_info is not None:

        info = st.session_state.receipt_info

        st.divider()

        st.markdown("## 📋 Edit Extracted Information")

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                "**Receipt Type:**",
                st.session_state.receipt_type
            )

            info["Store"] = st.text_input(
                "Store",
                value=info["Store"]
            )

            info["Customer"] = st.text_input(
                "Customer",
                value=info["Customer"]
            )

            info["Bill No"] = st.text_input(
                "Bill No",
                value=info["Bill No"]
            )

        with col2:

            info["Date"] = st.text_input(
                "Date",
                value=info["Date"]
            )

            info["GSTIN"] = st.text_input(
                "GSTIN",
                value=info["GSTIN"]
            )

            info["Total"] = st.text_input(
                "Total",
                value=str(st.session_state.total)
            )
            # Keep session state synchronized
            st.session_state.total = info["Total"]

        # -------------------------------
        # Editable Items
        # -------------------------------

        st.markdown("---")
        st.markdown("## 🛒 Purchased Items")

        # If OCR found no items, create an empty table
        if len(info["Items"]) == 0:

            st.warning(
                "⚠️ Unable to detect purchased items.\n\n"
                "The uploaded receipt may be blurry, low quality, or difficult for OCR to read.\n"
                "Please upload a clearer receipt image."
            )

            df = pd.DataFrame(
                columns=[
                    "Qty",
                    "Item",
                    "Price",
                    "Amount"
                ]
            )

        else:

            print("\n===== ITEMS SENT TO UI =====")
            print(info["Items"])
            print("Length:", len(info["Items"]))

            df = pd.DataFrame(info["Items"])


        if "edited_items_df" not in st.session_state:

            if len(info["Items"]) == 0:
                st.session_state.edited_items_df = pd.DataFrame(
                    columns=["Qty", "Item", "Price", "Amount"]
                )
            else:
                st.session_state.edited_items_df = pd.DataFrame(info["Items"])

        edited_df = st.data_editor(
            st.session_state.edited_items_df,
            hide_index=True,
            #use_container_width=True,
            num_rows="dynamic",
            column_config={

                "Qty": st.column_config.NumberColumn(
                    "Qty",
                    format="%.3f"
                ),

                "Item": st.column_config.TextColumn(
                    "Item Name"
                ),

                "Price": st.column_config.NumberColumn(
                    "Price",
                    format="₹ %.2f"
                ),

                "Amount": st.column_config.NumberColumn(
                    "Amount",
                    format="₹ %.2f",
                    disabled=True

                ),
            }
        )

        # Save edited items back to session
        st.session_state.edited_items_df = edited_df
        info["Items"] = edited_df.to_dict("records")

        # ---------------------------------------
        # Auto Calculate Amount
        # ---------------------------------------

        if (
            "Qty" in edited_df.columns
            and "Price" in edited_df.columns
        ):

            edited_df["Qty"] = pd.to_numeric(
                edited_df["Qty"],
                errors="coerce"
            ).fillna(0)

            edited_df["Price"] = pd.to_numeric(
                edited_df["Price"],
                errors="coerce"
            ).fillna(0)

            edited_df["Amount"] = (
                edited_df["Qty"]
                * edited_df["Price"]
            )

            info["Items"] = edited_df.to_dict("records")

        # Show calculated total
        if "Amount" in edited_df.columns:

            print(edited_df["Amount"])
            print(edited_df["Amount"].dtype)

            edited_df["Amount"] = (
                pd.to_numeric(
                    edited_df["Amount"],
                    errors="coerce"
                )
                .fillna(0)
            )

            edited_df["Amount"] = (
                edited_df["Amount"]
                .astype(str)
                .str.replace(",", "", regex=False)
            )

            edited_df["Amount"] = pd.to_numeric(
                edited_df["Amount"],
                errors="coerce"
            ).fillna(0)

            calculated_total = edited_df["Amount"].sum()

            print(edited_df["Amount"].dtype)
            print(calculated_total)

            st.metric(
                "Calculated Total",
                f"₹ {calculated_total:.2f}"
            )



        if st.button("Use Calculated Total", type="primary"):

            st.session_state.total = f"{calculated_total:.2f}"

            st.rerun()

        # -------------------------------
        # OCR Details
        # -------------------------------

        with st.expander("🔍 OCR Text"):

            st.text_area(
                "OCR Text",
                st.session_state.ocr_text,
                height=300,
                label_visibility="collapsed"
            )

        with st.expander("📊 OCR Information"):

            c1, c2 = st.columns(2)

            with c1:

                st.metric(
                    "Rotation",
                    st.session_state.angle
                )

            with c2:

                st.metric(
                    "Confidence",
                    f"{st.session_state.confidence:.2f}"
                )

        st.subheader("⏱ OCR Performance")

        timings = st.session_state.get("timings", None)

        if timings:

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Image Load", f"{timings['image_load']:.3f} s")
                st.metric("Preprocessing", f"{timings['preprocessing']:.3f} s")

            with col2:
                st.metric("OCR", f"{timings['ocr']:.3f} s")
                st.metric("Total", f"{timings['total']:.3f} s")

        with st.expander("🖼 Processed Receipt"):

            st.image(
                st.session_state.best_image,
                width=450
            )

        st.divider()

        # -------------------------------
        # Save Button
        # -------------------------------

        if st.button("💾 Save Receipt", type="primary"):

            repo = ReceiptRepository()

            info["Receipt Type"] = st.session_state.receipt_type

            receipt_id = repo.save_receipt(
                info,
                st.session_state.image_path
            )

            repo.save_items(
                receipt_id,
                info["Items"]
            )

            repo.close()

            st.success(
                f"Receipt saved successfully! (ID: {receipt_id})"
            )

            os.makedirs("exports", exist_ok=True)

            csv_path = os.path.join(
                "exports",
                f"receipt_{receipt_id}.csv"
            )

            excel_path = os.path.join(
                "exports",
                f"receipt_{receipt_id}.xlsx"
            )

            pdf_path = os.path.join(
                "exports",
                f"receipt_{receipt_id}.pdf"
            )

            export_receipt_csv(
                st.session_state.receipt_info,
                csv_path
            )

            export_receipt_excel(
                st.session_state.receipt_info,
                excel_path
            )

            export_receipt_pdf(
                st.session_state.receipt_info,
                pdf_path
            )

            # Store export information
            st.session_state.csv_path = csv_path
            st.session_state.excel_path = excel_path
            st.session_state.pdf_path = pdf_path
            st.session_state.receipt_id = receipt_id
            st.session_state.is_saved = True


        # -------------------------------
        # Download Buttons
        # -------------------------------

        if st.session_state.is_saved:

            st.markdown("### 📥 Download Export Files")

            col1, col2, col3 = st.columns(3)

            with col1:

                with open(st.session_state.csv_path, "rb") as f:

                    st.download_button(

                        "⬇ Download CSV",

                        data=f,

                        file_name=f"receipt_{st.session_state.receipt_id}.csv",

                        mime="text/csv",

                        use_container_width=True

                    )

            with col2:

                with open(st.session_state.excel_path, "rb") as f:

                    st.download_button(

                        "⬇ Download Excel",

                        data=f,

                        file_name=f"receipt_{st.session_state.receipt_id}.xlsx",

                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

                        use_container_width=True

                    )

            with col3:

                with open(st.session_state.pdf_path, "rb") as f:

                    st.download_button(

                        "📄 Download PDF",

                        data=f,

                        file_name=f"receipt_{st.session_state.receipt_id}.pdf",

                        mime="application/pdf",

                        use_container_width=True

                    )

            st.divider()

            if st.button(
                "🆕 Process New Receipt",
                type="secondary",
                use_container_width=True
            ):

                for key in [

                    "receipt_info",
                    "ocr_text",
                    "best_image",
                    "angle",
                    "confidence",
                    "image_path",
                    "receipt_type",
                    "timings",
                    "total",
                    "csv_path",
                    "excel_path",
                    "pdf_path",
                    "receipt_id",
                    "is_saved"

                ]:

                    if key in st.session_state:
                        del st.session_state[key]

                st.rerun()