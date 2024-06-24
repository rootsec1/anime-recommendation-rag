import streamlit as st
import requests


def get_bot_response(user_message: str) -> str:
    # Function to call the FastAPI backend
    api_url = st.secrets["BACKEND_API_HOST"]
    response = requests.post(
        api_url,
        json={"prompt": user_message}
    )
    if response.ok:
        return (response.json()).get("recommendation", "Sorry, I couldn't find a recommendation.")
    else:
        return "Error: Unable to get a recommendation from the backend."


# Set up the Streamlit page
st.set_page_config(
    page_title="Anime Recommendation Bot",
    page_icon="🤖"
)

# Display the header image
st.markdown(
    f"""
    <style>
    .header-image {{
        background-image: url('https://wallpapers.com/images/hd/anime-all-characters-hd-4r9pb6ju4v1b0m48.jpg');
        background-size: cover;
        background-position: center;
        height: 200px;
    }}
    </style>
    <div class="header-image" />
    """,
    unsafe_allow_html=True
)

# CSS to inject specified fonts and background image
background_css = """
<style>
@import url("https://fonts.googleapis.com/css?family=EB+Garamond:400,400i,700|Open+Sans:400,400i,700");

body {
    font-family: 'Open Sans', 'Helvetica Neue', 'Segoe UI', Helvetica, Arial, sans-serif;
    font-size: 14px;
    color: black;
}

h1, h2, h3, h4, h5, h6, [class*="css-"] {
    font-family: 'EB Garamond', Georgia, 'Times New Roman', Times, serif;
    color: black;
}

.stMarkdown, .stTextInput, .stButton, .stTextarea {
    border-radius: 10px;
    padding: 10px;
}

.stTextInput>div>div>input, .stTextInput>div>div>textarea {
    color: black;
}

.stButton>button {
    color: black;
    border: 1px solid black;
}
</style>
"""
st.markdown(background_css, unsafe_allow_html=True)

st.title("Anime Recommendation Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat messages from history on app rerun
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def send_user_message(user_message: str):
    # Add user message to chat history
    st.session_state["messages"].append(
        {"role": "user", "content": user_message}
    )


def send_bot_message(bot_message: str):
    # Add bot message to chat history
    st.session_state["messages"].append(
        {"role": "assistant", "content": bot_message}
    )


# Accept user input
if prompt := st.chat_input("Ask for anime recommendations: What should I watch next?"):
    # Add user message to chat history
    send_user_message(prompt)
    # Echo user message as bot response and add to chat history
    # bot_response = get_bot_response(prompt)
    bot_response = get_bot_response(prompt)
    send_bot_message(bot_response)

    # Rerun the Streamlit app to update the conversation display
    st.experimental_rerun()
