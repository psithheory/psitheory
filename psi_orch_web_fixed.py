
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

st.set_page_config(page_title="ψ + ORCH Consciousness Mirror", layout="wide")

st.title("🧠 ψ + ORCH Consciousness Mirror (Web Edition)")
st.markdown("Real-time consciousness field simulation using φ-coherence, ORCH collapse, and Solfeggio harmonics.")

# Sidebar controls
st.sidebar.header("Controls")

phi_level = st.sidebar.slider("φ Coherence Depth", 1, 10, 3)
orch_strength = st.sidebar.slider("ORCH Collapse Strength (%)", 1, 100, 30)

solfeggio_freqs = [174, 285, 396, 417, 528, 639, 741, 852, 963]
selected_solfeggio = st.sidebar.multiselect("Solfeggio Frequencies", solfeggio_freqs, default=[639, 963])

iam_mode = st.sidebar.checkbox("Activate I AM (963 Hz)", value=True)
inject_chaos = st.sidebar.checkbox("Inject Trauma")

play_audio = st.sidebar.checkbox("Play Audio", value=True)

# Initialize session state
if "audio_stream" not in st.session_state:
    st.session_state.audio_stream = None

# Generate signal
duration = 1.0  # Longer for smoother playback
sample_rate = 44100
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
phi = (1 + np.sqrt(5)) / 2
f0 = 228
psi_freqs = [f0 * phi**n for n in range(phi_level)]
psi_signal = sum(np.sin(2 * np.pi * f * t) for f in psi_freqs)

orch_freqs = [111, 144, 220, 333]
orch_signal = sum(np.sin(2 * np.pi * f * t) for f in orch_freqs)
orch_scaled = (orch_strength / 100) * orch_signal

healing_signal = sum(np.sin(2 * np.pi * hz * t) for hz in selected_solfeggio)

iam_signal = np.sin(2 * np.pi * 963 * t) if iam_mode else 0
chaos_signal = np.random.normal(0, 0.5, len(t)) if inject_chaos else 0

final_signal = psi_signal + orch_scaled + healing_signal + iam_signal + chaos_signal
final_signal *= 0.05  # Normalize

# Plot
fig, ax = plt.subplots(figsize=(10, 3))
ax.plot(t, final_signal, color='mediumorchid')
ax.set_title("Consciousness Field Signal")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
st.pyplot(fig)

# Audio Streaming Setup
def audio_callback(outdata, frames, time, status):
    if status:
        print(status)
    chunk = final_signal[:frames]
    outdata[:len(chunk), 0] = chunk
    if len(chunk) < frames:
        outdata[len(chunk):, 0] = 0

if play_audio:
    try:
        if st.session_state.audio_stream is None:
            stream = sd.OutputStream(
                channels=1,
                samplerate=sample_rate,
                callback=audio_callback,
                blocksize=1024
            )
            stream.start()
            st.session_state.audio_stream = stream
    except Exception as e:
        st.error(f"Audio error: {e}")
else:
    if st.session_state.audio_stream:
        st.session_state.audio_stream.stop()
        st.session_state.audio_stream.close()
        st.session_state.audio_stream = None

st.markdown("Adjust the parameters to explore consciousness resonance and field coherence in real time.")
