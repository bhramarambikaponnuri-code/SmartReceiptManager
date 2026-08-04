import streamlit as st
import os
from database.database import get_connection
from database.repository import ReceiptRepository


if "maintenance_action" not in st.session_state:
    st.session_state.maintenance_action = None

def delete_all_files(folder):
    """
    Delete all files inside the given folder.
    Returns the number of deleted files.
    """

    if not os.path.exists(folder):
        return 0

    deleted = 0

    for file in os.listdir(folder):

        path = os.path.join(folder, file)

        if os.path.isfile(path):

            os.remove(path)

            deleted += 1

    return deleted


def clear_receipt_history():
    """
    Delete all receipts and receipt items from the database.
    """

    repo = ReceiptRepository()

    try:

        repo.cursor.execute("DELETE FROM receipt_items")

        repo.cursor.execute("DELETE FROM receipts")

        repo.connection.commit()

    finally:

        repo.close()


def get_folder_size(folder):

    if not os.path.exists(folder):
        return 0

    total = 0

    for root, _, files in os.walk(folder):

        for file in files:

            path = os.path.join(root, file)

            total += os.path.getsize(path)

    return total


def format_size(size):

    for unit in ["B", "KB", "MB", "GB"]:

        if size < 1024:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} TB"


def settings_page():

    st.title("⚙ Settings")

    # ---------------------------------------
    # Application Information
    # ---------------------------------------

    st.subheader("📌 Application Information")

    col1, col2 = st.columns(2)

    with col1:

        st.write("**Application**")
        st.write("Smart Receipt Manager")

        st.write("**Version**")
        st.write("1.0")

        st.write("**OCR Engine**")
        st.write("EasyOCR")

    with col2:

        st.write("**Database**")
        st.write("receipts.db")

        st.write("**Uploads Folder**")
        st.write("uploads/")

        st.write("**Exports Folder**")
        st.write("exports/")

    st.divider()

    # ---------------------------------------
    # Storage Statistics
    # ---------------------------------------

    st.subheader("📊 Storage Statistics")

    receipt_count = 0

    if os.path.exists("receipts.db"):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM receipts")

        receipt_count = cursor.fetchone()[0]

        conn.close()

    upload_files = 0

    if os.path.exists("uploads"):

        upload_files = len(
            [
                f
                for f in os.listdir("uploads")
                if os.path.isfile(os.path.join("uploads", f))
            ]
        )

    export_files = 0

    if os.path.exists("exports"):

        export_files = len(
            [
                f
                for f in os.listdir("exports")
                if os.path.isfile(os.path.join("exports", f))
            ]
        )

    db_size = 0

    if os.path.exists("receipts.db"):

        db_size = os.path.getsize("receipts.db")

    upload_size = get_folder_size("uploads")

    export_size = get_folder_size("exports")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Receipts",
            receipt_count
        )

        st.metric(
            "Database Size",
            format_size(db_size)
        )

    with c2:

        st.metric(
            "Uploaded Images",
            upload_files
        )

        st.metric(
            "Uploads Size",
            format_size(upload_size)
        )

    with c3:

        st.metric(
            "Export Files",
            export_files
        )

        st.metric(
            "Exports Size",
            format_size(export_size)
        )

    st.divider()

    # ---------------------------------------
    # Maintenance
    # ---------------------------------------

    st.subheader("🧹 Maintenance")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🗑 Clear Receipt History",
            width="stretch"
        ):
            st.session_state.maintenance_action = "history"

        if st.button(
            "🗑 Delete Uploaded Images",
            width="stretch"
        ):
            st.session_state.maintenance_action = "uploads"

    with col2:

        if st.button(
            "🗑 Delete Export Files",
            width="stretch"
        ):
            st.session_state.maintenance_action = "exports"

        if st.button(
            "🔄 Reset Application",
            width="stretch"
        ):
            st.session_state.maintenance_action = "reset"

        action = st.session_state.maintenance_action

        if action is not None:

            st.warning(
                "⚠ This action cannot be undone.\n\nAre you sure?"
            )

            yes, no = st.columns(2)

            with yes:

                if st.button(
                    "✅ Yes",
                    width="stretch"
                ):

                    if action == "history":

                        clear_receipt_history()

                        st.success("Receipt history cleared.")

                    elif action == "uploads":

                        deleted = delete_all_files("uploads")

                        st.success(
                            f"{deleted} uploaded images deleted."
                        )

                    elif action == "exports":

                        deleted = delete_all_files("exports")

                        st.success(
                            f"{deleted} exported files deleted."
                        )

                    elif action == "reset":

                        clear_receipt_history()

                        delete_all_files("uploads")

                        delete_all_files("exports")

                        st.success("Application reset successfully.")

                    st.session_state.maintenance_action = None

                    st.rerun()

            with no:

                if st.button(
                    "❌ Cancel",
                    width="stretch"
                ):

                    st.session_state.maintenance_action = None

                    st.rerun()