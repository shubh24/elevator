# Elevator

## Inspiration
As founders, we constantly pitch our company, our vision, our product, our team, and heck, so many times we're pitching ourselves! They say, practice makes perfect, and I wondered what if we could practice our elevator pitches with an expert - someone who can help us think about the script, the emotion, the storytelling, the voice modulation, the tone, enunciation, etc.

As I was listening to a bunch of "team formation pitches" yesterday at the hackathon kickoff, I wondered how much better these elevator pitches could be! Only if they had a personalized speaking coach, and who better to do this than the GOAT of pitches, Steve Jobs?

## What it does
Elevator is an AI-powered speaking coach, designed to elevate your elevator pitches to the next level.

It provides personalized coaching on various aspects of pitch delivery and even helps with rewriting the script to iterate on the script.

Channeling the legendary Steve Jobs, he'd be offering insights and tips in his own voice, inspired by his iconic presentation style!

## How we built it
We're using Gemini 1.5(multimodal) for analyzing audio files, Gemini's chat module to maintain conversation history, ElevenLabs to create a voice clone for Steve Jobs, and Streamlit for the user interface

## Challenges we ran into
- Wanted to integrate video, so that speaker could get feedback on their body language - Gemini offers it, but video processing is too slow to be helpful
- LipSync: Too complicated + High latency in getting Steve Jobs avatar to lipsync what he's saying

## Accomplishments that we're proud of
- Sub-1 second feedback with streaming audio from Steve Jobs
- Crazy good feedback, crazy good analogies!

## What we learned
- Gemini's multimodal capabilities
- ElevenLabs's voice cloning

## What's next for Elevator
- Video integration, so that Steve Jobs could give feedback on the speaker's body language, executive presence, smile, etc.
(Reverse) Interrupts: As the speaker speaks, Steve Jobs should be able to interrupt and share feedback in-real-time about what the speaker messed up.
- A neat user interface where Steve Jobs could speak out the exact phrases/sentences that the speaker should improve on. This would help with targeted feedback!
