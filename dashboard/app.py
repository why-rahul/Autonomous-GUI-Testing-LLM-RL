import streamlit as st
import os

LOG_DIR = "outputs/logs"
SCREENSHOT_DIR = "outputs/screenshots"

st.set_page_config(
    page_title="LLM-RL GUI Testing Dashboard",
    layout="wide"
)

# ================= HEADER =================
st.title("🤖 Autonomous GUI Testing Dashboard")
st.markdown("### LLM + Reinforcement Learning + Selenium")

# ================= LOGS =================
st.subheader("📄 Execution Logs")

log_files = sorted(os.listdir(LOG_DIR)) if os.path.exists(LOG_DIR) else []

logs = ""

if log_files:
    latest_log = os.path.join(LOG_DIR, log_files[-1])

    with open(latest_log, "r") as f:
        logs = f.read()

    st.text_area("Latest Log", logs, height=300)
else:
    st.warning("No logs found")

# ================= STATUS =================
st.subheader("📊 Status")

if "SUCCESS" in logs:
    st.success("✅ Test Passed")
elif "FAILED" in logs:
    st.error("❌ Test Failed")
else:
    st.info("Execution completed")

# ================= SCREENSHOTS =================
st.subheader("🖼️ Episode Screenshots")

if os.path.exists(SCREENSHOT_DIR):
    images = sorted(os.listdir(SCREENSHOT_DIR))

    if images:
        # sort properly (episode_0 → episode_1 → ...)
        images = sorted(images, key=lambda x: int(x.split("_")[1].split(".")[0]))

        cols = st.columns(4)  # 4 per row

        for i, img in enumerate(images):
            img_path = os.path.join(SCREENSHOT_DIR, img)

            with cols[i % 4]:
                st.image(
                    img_path,
                    caption=f"Episode {i}",
                    use_container_width=True
                )
    else:
        st.warning("No screenshots found")
else:
    st.warning("Screenshot folder not found")

# ================= FOOTER =================
st.markdown("---")
st.markdown("### 📌 Project Info")
st.markdown("""
- **Model**: LLM (Ollama Llama3)  
- **Agent**: Deep Q Network (DQN)  
- **Automation**: Selenium  
- **Type**: Autonomous GUI Testing  
""")