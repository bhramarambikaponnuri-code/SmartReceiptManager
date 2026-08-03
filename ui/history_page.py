import streamlit as st
import os
import pandas as pd

from database.repository import ReceiptRepository


def history_page():

    st.title("📜 Receipt History")

    col1, col2, col3 = st.columns(3)

    with col1:

        search_store = st.text_input(
            "🔍 Search Store"
        )

    with col2:

        receipt_type_filter = st.selectbox(
            "Receipt Type",
            [
                "All",
                "Grocery",
                "Pharmacy",
                "Restaurant",
                "Other"
            ]
        )

    with col3:

        sort_by = st.selectbox(
            "Sort By",
            [
                "Newest First",
                "Oldest First",
                "Highest Total",
                "Lowest Total"
            ]
        )

    repo = ReceiptRepository()

    if "delete_receipt_id" not in st.session_state:
        st.session_state.delete_receipt_id = None

    if "update_success" not in st.session_state:
        st.session_state.update_success = False

    if "delete_success" not in st.session_state:
        st.session_state.delete_success = False


    if st.session_state.update_success:

        st.success("✅ Receipt updated successfully.")

        st.session_state.update_success = False

    if st.session_state.delete_success:

        st.success("✅ Receipt deleted successfully!")

        st.session_state.delete_success = False
        

    receipts = repo.get_receipts()

    filtered_receipts = []

    for receipt in receipts:

        store = receipt[2] or ""
        receipt_type = receipt[1] or ""

        # Search by store
        if search_store:

            if search_store.lower() not in store.lower():
                continue

        # Filter by receipt type
        if receipt_type_filter != "All":

            if receipt_type != receipt_type_filter:
                continue

        filtered_receipts.append(receipt)

    if not receipts:
        st.info("No receipts available.")
        repo.close()
        return
    
    # ----------------------------
    # Sort Receipts
    # ----------------------------

    def safe_total(receipt):

        try:
            return float(receipt[6])
        except:
            return 0.0


    if sort_by == "Newest First":

        filtered_receipts.sort(
            key=lambda x: x[0],
            reverse=True
        )

    elif sort_by == "Oldest First":

        filtered_receipts.sort(
            key=lambda x: x[0]
        )

    elif sort_by == "Highest Total":

        filtered_receipts.sort(
            key=safe_total,
            reverse=True
        )

    elif sort_by == "Lowest Total":

        filtered_receipts.sort(
            key=safe_total
        )
    
    st.success(f"{len(filtered_receipts)} receipt(s) found.")

    for receipt in filtered_receipts:

        receipt_id = receipt[0]

        image_path = repo.get_image_path(receipt_id)

        full_receipt = repo.get_receipt(receipt_id)

        items = repo.get_items(receipt_id)

        session_key = f"items_{receipt_id}"

        if session_key not in st.session_state:

            st.session_state[session_key] = []

            for item in items:

                st.session_state[session_key].append(
                    {
                        "Item": item[0],
                        "Qty": item[1],
                        "Price": item[2],
                        "Amount": item[3]
                    }
                )
        with st.expander(f"🧾 Receipt #{receipt_id} - {receipt[2]}"):

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Receipt Type:**", full_receipt[1])
                store = st.text_input(
                    "Store",
                    value=full_receipt[2],
                    key=f"store_{receipt_id}"
                )

                customer = st.text_input(
                    "Customer",
                    value=full_receipt[3],
                    key=f"customer_{receipt_id}"
                )

                bill_no = st.text_input(
                    "Bill No",
                    value=full_receipt[4],
                    key=f"bill_{receipt_id}"
                )

            with col2:
                date = st.text_input(
                    "Date",
                    value=full_receipt[5],
                    key=f"date_{receipt_id}"
                )

                gstin = st.text_input(
                    "GSTIN",
                    value=full_receipt[6],
                    key=f"gstin_{receipt_id}"
                )

                total = st.text_input(
                    "Total",
                    value=str(full_receipt[7]),
                    key=f"total_{receipt_id}"
                )

            st.markdown("<br>", unsafe_allow_html=True)

            st.subheader("Purchased Items")

            edited_items = st.session_state[session_key]

            for i, item in enumerate(edited_items):

                c1, c2, c3, c4, c5 = st.columns([4,1,2,2,1])

                with c1:
                    item["Item"] = st.text_input(
                        "Item",
                        value=item["Item"],
                        key=f"item_{receipt_id}_{i}"
                    )

                with c2:
                    item["Qty"] = st.text_input(
                        "Qty",
                        value=item["Qty"],
                        key=f"qty_{receipt_id}_{i}"
                    )

                with c3:
                    item["Price"] = st.text_input(
                        "Price",
                        value=item["Price"],
                        key=f"price_{receipt_id}_{i}"
                    )

                with c4:
                    item["Amount"] = st.text_input(
                        "Amount",
                        value=item["Amount"],
                        key=f"amount_{receipt_id}_{i}"
                    )

                with c5:

                    if st.button(
                        "❌",
                        key=f"delete_item_{receipt_id}_{i}"
                    ):

                        edited_items.pop(i)

                        st.rerun()

            if st.button(
                "➕ Add Item",
                key=f"add_item_{receipt_id}"
            ):

                edited_items.append(
                    {
                        "Item": "",
                        "Qty": "",
                        "Price": "",
                        "Amount": ""
                    }
                )

                st.rerun()

            st.divider()

            #image_path = full_receipt[8]

            if image_path and os.path.exists(image_path):

                st.subheader("🖼 Original Receipt")

                st.image(
                    image_path,
                    caption="Original Receipt",
                    width=350
                )

            else:

                st.warning("Receipt image not found.")

            col_update, col_delete = st.columns(2)

            with col_update:

                if st.button(
                    "💾 Update Receipt",
                    type="primary",
                    key=f"update_{receipt_id}"
                ):

                    info = {

                        "Receipt Type": full_receipt[1],
                        "Store": store,
                        "Customer": customer,
                        "Bill No": bill_no,
                        "Date": date,
                        "GSTIN": gstin,
                        "Total": total,
                        "Items": edited_items

                    }

                    repo.update_receipt(
                        receipt_id,
                        info
                    )

                    repo.delete_items(receipt_id)

                    repo.save_items(
                        receipt_id,
                        edited_items
                    )

                    repo.close()

                    st.success("Receipt updated successfully!")

                    st.session_state.update_success = True

                    st.rerun()

            with col_delete:

                if st.button(
                    "🗑 Delete Receipt",
                    key=f"delete_{receipt_id}"
                ):

                    st.session_state.delete_receipt_id = receipt_id

                    st.rerun()

            if st.session_state.delete_receipt_id == receipt_id:

                st.warning("⚠ Are you sure you want to delete this receipt?")

                col_yes, col_no = st.columns(2)

                with col_yes:

                    if st.button(
                        "✅ Yes, Delete",
                        key=f"confirm_delete_{receipt_id}"
                    ):

                        repo.delete_receipt(receipt_id)

                        repo.close()

                        st.session_state.delete_receipt_id = None

                        st.session_state.delete_success = True

                        st.rerun()

                with col_no:

                    if st.button(
                        "❌ Cancel",
                        key=f"cancel_delete_{receipt_id}"
                    ):

                        st.session_state.delete_receipt_id = None

                        st.rerun()

    repo.close()