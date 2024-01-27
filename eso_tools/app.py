import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to ESO Tools! 👋")

    with open("eso_tools/docs/app_py.md", "r") as f:
        st.markdown(f.read())

    st.sidebar.success("⬆️ Select a tool above.")
    


if __name__ == "__main__":
    run()