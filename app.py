import streamlit as st
import speech_recognition as sr
import os
import datetime

def transcribe_audio(provider, language):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Please speak into the microphone...")
        try:
            audio = r.listen(source, timeout=15)
            if provider == "Google":
                st.info("Transcribing using Google Speech Recognition...")
                text = r.recognize_google(audio, language=language)
                return text
            elif provider == "Sphinx":
                st.info("Transcribing using CMU Sphinx...")
                text = r.recognize_sphinx(audio, language=language)
                return text
            else:
                st.error("Unsupported provider. Please choose either Google or Sphinx.")
                return "Error: Unsupported provider."
        except sr.WaitTimeoutError:
            return "Error: No speech detected within the timeout period."
        except sr.UnknownValueError:
            return "Error: Could not understand the audio."
        except sr.RequestError as e:
            return f"Error: Could not request results from the service; {e}"
        except Exception as e:
            return f"Error: An unexpected error occurred; {str(e)}"
        
#Save transcription to a file
def save_transcription(transcription, custom_name):
    if not custom_name.endswith('.txt'):
        custom_name += '.txt'
    with open(custom_name, 'w') as f:
        f.write(transcription)
    return custom_name
        
        
def main():
    st.title("Audio Transcription App")
    
    st.write("This app transcribes audio from your microphone.")

    api_provider = st.selectbox("Select API Provider", ["Google", "Sphinx"])
    language = st.selectbox("Select Language", ["en-US", "fr-FR", "es-ES", "de-DE", "it-IT"])

    if 'paused' not in st.session_state:
        st.session_state.paused = False

    column1, column2 = st.columns(2)

    with column1:
        if st.button("Start Transcription"):
            if not st.session_state.paused:
                st.write("Transcription started. Please speak into the microphone.")
                transcription = transcribe_audio(provider=api_provider, language=language)
                st.session_state.transcription = transcription
                st.write("Transcription Result:" + transcription)
                st.success("Transcription completed.")

            else:
                st.warning("Transcription is paused. Please resume to start.")


    with column2:
        if st.button("Pause/Resume Transcription"):
            st.session_state.paused = not st.session_state.paused
            if st.session_state.paused:
                st.warning("Transcription paused. Click 'Resume' to continue.")
            else:
                st.success("Transcription resumed.")

    if 'transcription' in st.session_state and "Error" not in st.session_state.transcription:
                    custom_name = st.text_input("Enter filename to save:", value="transcription.txt")
                    if st.button("Save Transcription to TXT File"):
                        filename = save_transcription(st.session_state.transcription, custom_name)
                        st.download_button(
                            label="Download Transcription",
                            data=st.session_state.transcription,
                            file_name=custom_name,
                        )
                        st.success(f"Transcription saved as `{filename}`")
        

if __name__ == "__main__":
    main()