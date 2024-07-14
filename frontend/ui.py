import streamlit as st
import requests


def get_bot_response(user_message: str) -> str:
    """
    Calls the FastAPI backend with a user message and returns the bot's response.

    Args:
        user_message (str): The message input by the user.

    Returns:
        str: The bot's recommendation or an error message.
    """
    # Retrieve the API URL from Streamlit's secrets
    api_url = st.secrets["BACKEND_API_HOST"]
    # Make a POST request to the backend API with the user message
    response = requests.post(
        api_url,
        json={"prompt": user_message}
    )
    # If the request is successful, return the recommendation; otherwise, return an error message
    if response.ok:
        return (response.json()).get("recommendation", "Sorry, I couldn't find a recommendation.")
    else:
        return "Error: Unable to get a recommendation from the backend."


# Configure the Streamlit page with a title and icon
st.set_page_config(
    page_title="Anime Recommendation Bot",
    page_icon="🤖"
)

# Display a header image using HTML and CSS
st.markdown(
    """
    <style>
    .header-image {
        background-image: url('https://wallpapers.com/images/hd/anime-all-characters-hd-4r9pb6ju4v1b0m48.jpg');
        background-size: cover;
        background-position: center;
        height: 200px;
    }
    </style>
    <div class="header-image" />
    """,
    unsafe_allow_html=True
)

# Inject custom CSS for styling the page
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

# Set the title of the Streamlit app
st.title("Anime Recommendation Bot")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat messages from history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def send_user_message(user_message: str):
    """
    Adds a user message to the chat history.

    Args:
        user_message (str): The message input by the user.
    """
    st.session_state["messages"].append(
        {"role": "user", "content": user_message}
    )


def send_bot_message(bot_message: str):
    """
    Adds a bot message to the chat history.

    Args:
        bot_message (str): The message generated by the bot.
    """
    st.session_state["messages"].append(
        {"role": "assistant", "content": bot_message}
    )


# Accept user input through a chat input box
if prompt := st.chat_input("Ask for anime recommendations: What should I watch next?"):
    # Add user message to chat history
    send_user_message(prompt)
    # Get bot response and add to chat history
    bot_response = get_bot_response(prompt)
    send_bot_message(bot_response)

    # Rerun the Streamlit app to update the conversation display
    st.experimental_rerun()
