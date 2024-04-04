import os
import streamlit as st
import shutil
from PIL import Image
from lyzr import ChatBot

os.environ["OPENAI_API_KEY"] = st.secrets["apikey"]

st.set_page_config(
    page_title="Lyzr",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png",
)

# Load and display the logo
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Budget Planner💵 ")
st.markdown("### Built using Lyzr SDK🚀")
st.markdown("Elevate your budget management with Lyzr's SDK, simplifying expense allocation for a balanced financial month.")
def remove_existing_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            st.error(f"Error while removing existing files: {e}")


# Set the local directory
data_directory = "data"

# Create the data directory if it doesn't exist
os.makedirs(data_directory, exist_ok=True)

# Remove existing files in the data directory
remove_existing_files(data_directory)

# Streamlit app header
# st.title("Word File Uploader")

# File upload widget
uploaded_file = st.file_uploader("Choose Word file", type=["docx"])

if uploaded_file is not None:
    # Save the uploaded Word file to the data directory
    file_path = os.path.join(data_directory, uploaded_file.name)
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getvalue())
    
    # Display the path of the stored file
    st.success(f"File successfully saved")


def get_files_in_directory(directory="data"):
    # This function helps us get the file path along with the filename.
    files_list = []

    # Ensure the directory exists
    if os.path.exists(directory) and os.path.isdir(directory):
        # Iterate through all files in the directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            # Check if the path points to a file (not a directory)
            if os.path.isfile(file_path):
                files_list.append(file_path)

    return files_list


def rag_implementation():
    # This function will implement RAG Lyzr QA bot
    path = get_files_in_directory()
    path = path[0]

    rag = ChatBot.docx_chat(
        input_files=[str(path)],
        llm_params={"model": "gpt-3.5-turbo"},
        # vector_store_params=vector_store_params
    )

    return rag


def resume_response():
    rag = rag_implementation()
    prompt = """  Please follow the instructions below to determine the ideal allocation of expenses based on the provided total budget for the month,
                    - From the total budget given for a month , take that amount and use it to allocate for these expenses.
                    - Calculate the expense for these below using the formula given and after calculation not display it.
                    - Housing : To calculate housing expenses it is 31.91% the total budget, later describe how to spend the amount for better living.
                    - Utilities: To calculate Utilities expense it is 4.21% the total budget, later describe how to spend the amount for better living.
                    - Transportation: To calculate Transportation expense it is 6.38% the total budget, later describe how to spend the amount for better living.
                    - Groceries: To calculate Groceries expense it is 8.51% the total budget, later describe how to spend the amount for better living.
                    - Insurance: To calculate Insurance expense it is 3.19% the total budget, later describe how to spend the amount for better living.
                    - Entertainment: To calculate Entertainment expense it is 3.19% the total budget, later describe how to spend the amount for better living.
                    - Personal Care: To calculate Personal Care expense it is 2.13% the total budget, later describe how to spend the amount for better living.
                    - Savings: To calculate Savings expense it is 10.36% the total budget, later describe how to spend the amount for better living.
                    - Miscellaneous: To calculate Miscellaneous expense it is 4.26% the total budget, later describe how to spend the amount for better living.
                    - Just show the amount not the calculation part. """
    
    response = rag.chat(prompt)
    return response.response

if uploaded_file is not None:
    automatice_response = resume_response()
    st.markdown(f"""{automatice_response}""")


# Footer or any additional information
with st.expander("ℹ️ - About this App"):
    st.markdown(
        """Experience the seamless integration of Lyzr's ChatBot . For any inquiries or issues, please contact Lyzr.

    """
    )
    st.link_button("Lyzr", url="https://www.lyzr.ai/", use_container_width=True)
    st.link_button(
        "Book a Demo", url="https://www.lyzr.ai/book-demo/", use_container_width=True
    )
    st.link_button(
        "Discord", url="https://discord.gg/nm7zSyEFA2", use_container_width=True
    )
    st.link_button(
        "Slack",
        url="https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw",
        use_container_width=True,
    )
