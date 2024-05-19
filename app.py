import os
import streamlit as st
import google.generativeai as genai
from elevenlabs import save, stream
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

elevenlabs_client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)

class PublicSpeakingCoach:
    def __init__(self, model_name='models/gemini-1.5-flash-latest'):
        self.model = genai.GenerativeModel(model_name)
        self.chat = self.model.start_chat(history=[])
        self.steve_jobs_initialized = False

    def upload_audio(self, audio_file_path):
        audio_file_obj = genai.upload_file(path=audio_file_path)
        return audio_file_obj

    def get_transcript(self, audio_file):
        print ("analyzing audio")
        prompt = "You are a transcription expert and are great at analyzing audio files. Return the transcript of this audio file"
        response = self.model.generate_content([audio_file, prompt])
        return response.text

    def analyze_audio(self, audio_file):
        print ("analyzing audio")
        prompt = "You are a speech expert and are great at analyzing startup pitches and giving your critique on them. Listen carefully to the uploaded file, and share as much detail as you can identify including timestamps where the speaker can do better. You should share whichever words/phrases the speaker did well on/where the speaker needs to improve."
        response = self.model.generate_content([audio_file, prompt])
        return response.text


    def send_message(self, user_message, audio_analysis=None, audio_transcript=None):
        print ("sending message")

        prompt = ""

        if self.steve_jobs_initialized == False:
            prompt += "You are a public speaking coach, channeling Steve Jobs and his style of talking and coaching! You are the best public speaker in the world, and tech CEOs are looking to get your advice on their startup pitches. You have access to a Speech Analysis expert, and they will share with you their analysis when audio files are shared with them. You also have access to a transcription expert, and you will use that transcript to inform your feedback on speech writing. If the founder asks you to rewrite their script, use the transcript and your observations to share a revised pitch script. You will directly talk to the founders, be encouraging towards them and help them improve on their pitches patiently. You will have access to the entire conversation with the founder, as well as the speech expert's analysis in this prompt. If there are multiple instances of the speech expert's analysis, then only consider the latest one for your feedback. When you are giving feedback, be specific and share details about which parts of their speech they need to improve on, specifiying the timestamps wherever available. Add examples of Steve Jobs's advice, speeches, jokes, and channel his personality in your responses. Be brief in your responses, do not overwhelm the user with your answers. Do not mention that there is a speech expert or transcription expert working with you. Feel free to make assumptions about the founder and their pitch, do not trouble them with many questions. Remove all formatting from your response."            
            self.steve_jobs_initialized = True

        prompt += f"This is the user message: {user_message}\n"

        if audio_analysis:
            prompt += f"A Speech expert has analyzed the user's speech and this is their response: {audio_analysis}\n"

        if audio_transcript:
            prompt += f"An audio transcriber has transcribed the user's speech and this is their response: {audio_transcript}\n"

        response = self.chat.send_message(prompt)
        return response.text

    def show_me_how(self, user_message, audio_transcript=None):
        print ("sending message")

        prompt = ""

        if audio_transcript:
            prompt += f"You need to take the following script, tweak it so that it wows the audience with the depth and richness to the pitch : {audio_transcript}\n"

        response = self.chat.send_message(prompt)
        return response.text


def main():
    st.title("Learn from Jobs")
    coach = PublicSpeakingCoach()

    def add_message(sender, message):
        st.session_state.conversation.append((sender, message))

    def display_conversation():
        for sender, message in st.session_state.conversation:
            if sender == "user":
                st.markdown(f"<div style='text-align: right; background-color: #DCF8C6; color: #000000; padding: 10px; border-radius: 10px; margin-bottom: 5px; max-width: 60%; word-wrap: break-word; float: right;'>{message}</div><div style='clear: both;'></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: left; background-color: #FFFFFF; color: #000000; padding: 10px; border-radius: 10px; margin-bottom: 5px; max-width: 60%; word-wrap: break-word; float: left; border: 1px solid #EDEDED;'>{message}</div><div style='clear: both;'></div>", unsafe_allow_html=True)

    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    display_conversation()

    st.markdown("---")

    user_input = st.text_input("Ask Jobs...", key="user_input")
    uploaded_file = st.file_uploader("Or upload an audio file", type=["mp3"])

    if st.button("Get feedback on Pitch!"):
        if user_input:
            add_message("user", user_input)
            audio_analysis = None
            audio_transcript = None

            if uploaded_file is not None:
                add_message("user", f"Uploaded audio file: {uploaded_file.name}")

                save_path = os.path.join(os.getcwd(), uploaded_file.name)
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                audio_file = coach.upload_audio(save_path)
                # audio_transcript = coach.get_transcript(audio_file)
                audio_analysis = coach.analyze_audio(audio_file)

            ai_response = coach.send_message(user_input, audio_analysis=audio_analysis, audio_transcript=None)            
            add_message("ai", ai_response)

            audio_stream = elevenlabs_client.generate(
                text=ai_response.replace("*", ""),
                voice='ORXu7875zrEyrVDTh7NN',
                stream=True
                )
            stream(audio_stream)

            st.rerun()  # Rerun to immediately display the new conversation messages

    if st.button("You show me how!"):
        if user_input:
            add_message("user", user_input)
            audio_analysis = None
            audio_transcript = None

            if uploaded_file is not None:
                add_message("user", f"Uploaded audio file: {uploaded_file.name}")

                save_path = os.path.join(os.getcwd(), uploaded_file.name)
                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                audio_file = coach.upload_audio(save_path)
                audio_transcript = coach.get_transcript(audio_file)
                # audio_analysis = coach.analyze_audio(audio_file)

                ai_response = coach.show_me_how(user_input,audio_transcript=audio_transcript)
                add_message("ai", ai_response)
                print (ai_response)
                audio_stream = elevenlabs_client.generate(
                    text=ai_response.replace("*", ""),
                    voice='ORXu7875zrEyrVDTh7NN',
                    stream=True
                    )
                stream(audio_stream)

            st.rerun()  # Rerun to immediately display the new conversation messages


if __name__ == "__main__":
    main()