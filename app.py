import os
import streamlit as st
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class PublicSpeakingCoach:
    def __init__(self, model_name='models/gemini-1.5-flash-latest'):
        self.model = genai.GenerativeModel(model_name)
        self.history = []

    def upload_audio(self, audio_file):
        st.write("Jobs is thinking...")
        audio_file_obj = genai.upload_file(path=audio_file)
        st.write(f"Completed upload: {audio_file_obj.uri}")
        return audio_file_obj

    def analyze_audio(self, audio_file, prompt):
        response = self.model.generate_content([audio_file, prompt])
        self.history.append((audio_file.uri, prompt, response.text))
        return response.text

    def ask_followup(self, followup_prompt):
        context = "\n".join([f"Audio: {h[0]}, Prompt: {h[1]}, Response: {h[2]}" for h in self.history])
        print (context)
        full_prompt = f"Context: {context}\n\nFollowup: {followup_prompt}"
        response = self.model.generate_content([full_prompt])
        self.history.append((None, followup_prompt, response.text))
        return response.text

def main():
    st.title("Public Speaking Coach")
    coach = PublicSpeakingCoach()

    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    input_method = st.radio("Input Method", ["Text Input", "Upload Audio"])

    if input_method == "Text Input":
        user_input = st.text_input("Enter your question or prompt:")
    else:
        uploaded_file = st.file_uploader("Upload an audio file", type=["mp3"])
        user_input = uploaded_file

    if st.button("Send"):
        if input_method == "Text Input" and user_input:
            followup_prompt = user_input
            followup_response = coach.ask_followup(followup_prompt)
            st.session_state.conversation.append(("user", followup_prompt))
            st.session_state.conversation.append(("ai", followup_response))
            st.session_state.user_input = ""

        elif input_method == "Upload Audio" and uploaded_file is not None:
            file_details = {
                "filename": uploaded_file.name,
                "filetype": uploaded_file.type,
                "filesize": uploaded_file.size
            }
            st.write(file_details)

            # Save the uploaded file to a local directory
            save_path = os.path.join(os.getcwd(), uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            audio_file = coach.upload_audio(save_path)
            initial_prompt = "Listen carefully to the uploaded file. You are a public speaking coach, and you should tell exactly how the speaker could improve his tonality, enunciation, pronunciation, punctuation, pauses, etc. Tell exactly at which timestamps did the speaker make a mistake."
            initial_response = coach.analyze_audio(audio_file, initial_prompt)
            st.session_state.conversation.append(("user", "Please analyze the audio file."))
            st.session_state.conversation.append(("ai", initial_response))

    if st.session_state.conversation:
        st.write("Conversation History:")
        for sender, message in st.session_state.conversation:
            if sender == "user":
                st.markdown(f"<div style='text-align: right; background-color: #D3D3D3; padding: 10px; border-radius: 5px; margin-bottom: 5px;'>{message}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: left; background-color: #ADD8E6; padding: 10px; border-radius: 5px; margin-bottom: 5px;'>{message}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()