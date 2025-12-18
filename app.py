import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

# Check if the API key is set
if not openai_api_key:
    st.error("OpenAI API Key not found. Please set the OPENAI_API_KEY environment variable in your .env file.")
else:
    # Initialize the OpenAI client
    # The 'openai.OpenAI()' client is the recommended way for newer API versions.
    client = openai.OpenAI(api_key=openai_api_key)

    st.set_page_config(page_title="Simple AI Idea Generator", page_icon="💡")
    st.title("💡 Simple AI Idea Generator")

    st.markdown("""
    Welcome to the Simple AI Idea Generator! 
    Just tell me a topic, and I'll brainstorm some creative ideas for you.
    """)

    # User input for the topic
    user_topic = st.text_input("Enter a topic (e.g., 'new app ideas', 'sci-fi story plots', 'healthy snack recipes'):", "")

    # Button to generate ideas
    if st.button("Generate Ideas"):
        if user_topic:
            with st.spinner("Brainstorming ideas..."):
                try:
                    # Construct the prompt for the OpenAI model
                    # We ask for a numbered list to make the output clear.
                    prompt_text = f"Generate 5 unique and creative ideas for: {user_topic}. Present them as a numbered list."

                    # Call the OpenAI API to get completions
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",  # A good balance of cost and performance. You can try "gpt-4" if you have access and need higher quality.
                        messages=[
                            {"role": "system", "content": "You are a highly creative brainstorming assistant."}, # Sets the AI's persona
                            {"role": "user", "content": prompt_text} # The user's specific request
                        ],
                        max_tokens=300,  # Limits the length of the AI's response to prevent overly long outputs
                        n=1,             # Request only one completion
                        stop=None,       # No specific stop sequence needed for this task
                        temperature=0.7  # Controls creativity: 0.0 (very focused) to 1.0 (very creative). 0.7 is a good balance.
                    )

                    # Extract the generated ideas from the response
                    generated_ideas = response.choices[0].message.content.strip()
                    st.subheader("Here are some ideas for you:")
                    st.write(generated_ideas) # Display the ideas in the Streamlit app

                except openai.APIError as e:
                    # Catch specific OpenAI API errors (e.g., invalid key, rate limits)
                    st.error(f"OpenAI API Error: {e}. Please check your API key and try again.")
                except Exception as e:
                    # Catch any other unexpected errors
                    st.error(f"An unexpected error occurred: {e}")
        else:
            st.warning("Please enter a topic to generate ideas.")

    st.markdown("---")
    st.markdown("Developed with ❤️ using Python, Streamlit, and OpenAI API.")