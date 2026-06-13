import random
import os

from llm.planner import generate_test_plan
from llm.critic import analyze_failure
from rl.dqn_agent import DQNAgent
from env.selenium_env import SeleniumEnv

from utils.logger import Logger
from utils.bug_detector import BugDetector
from utils.vision import compare_screenshots


def execute_action(env, step):
    try:
        action = step["action"]
        target = step["target"]
        value = step["value"]

        if action == "open_url":
            env.open_url()

        elif action == "type":
            env.type(target, value)

        elif action == "click":
            env.click(target)

        elif action == "verify":
            return env.verify(target)

        return 0

    except Exception as e:
        print("⚠️ Invalid action:", e)
        return -1, str(e)


if __name__ == "__main__":

    # =============================
    # Clear screenshots
    # =============================
    screenshot_dir = "outputs/screenshots"
    if os.path.exists(screenshot_dir):
        for file in os.listdir(screenshot_dir):
            os.remove(os.path.join(screenshot_dir, file))

    logger = Logger()
    bug_detector = BugDetector()

    user_input = "Test login with valid and invalid credentials and logout"

    # =============================
    # 🔥 NEW: DOM-AWARE PLANNING
    # =============================
    print("\n🌐 Fetching HTML for intelligent planning...")

    env_temp = SeleniumEnv()
    env_temp.open_url()

    html = env_temp.get_page_html()

    env_temp.close()

    plan = generate_test_plan(user_input, html)

    # =============================
    # Show Plan
    # =============================
    print("\nLLM Generated Plan:\n")
    for i, step in enumerate(plan):
        print(i, step)

    action_dim = len(plan)
    agent = DQNAgent(action_dim)

    episodes = 5

    # =============================
    # RL LOOP
    # =============================
    for episode in range(episodes):
        print(f"\n🚀 Episode {episode+1}")
        logger.log(f"=== Episode {episode+1} ===")

        env = SeleniumEnv(episode)

        try:
            state = [0]
            done = False
            step_count = 0

            while not done and step_count < action_dim:

                # Exploration vs Exploitation
                epsilon = max(0.1, 1.0 - episode * 0.2)

                if random.random() < epsilon:
                    print("🎲 Exploring")
                else:
                    print("🧠 Exploiting")

                action_idx = step_count
                step = plan[action_idx]

                print(f"➡️ Executing step {action_idx}: {step}")
                logger.log(f"Executing: {step}")

                result = execute_action(env, step)

                if isinstance(result, tuple):
                    reward, message = result
                else:
                    reward = result
                    message = ""

                # =============================
                # FUNCTIONAL RESULT (PRIMARY)
                # =============================
                if step["action"] == "verify":
                    if reward == 1:
                        print("✅ FUNCTIONAL SUCCESS")
                    else:
                        print("❌ FUNCTIONAL FAILURE")

                # =============================
                # Bug Detection
                # =============================
                bug = bug_detector.detect(message)

                logger.log(f"Reward: {reward}")

                if message:
                    logger.log(f"Message: {message}")

                if bug:
                    print(f"🚨 BUG TYPE: {bug}")
                    logger.log(f"🚨 Bug Type: {bug}")

                # =============================
                # 👁️ Vision Check (SECONDARY)
                # =============================
                try:
                    screenshots = sorted(os.listdir("outputs/screenshots"))

                    if len(screenshots) >= 2:
                        last = f"outputs/screenshots/{screenshots[-1]}"
                        prev = f"outputs/screenshots/{screenshots[-2]}"

                        diff_score = compare_screenshots(prev, last)

                        print(f"🧠 Visual Difference Score: {diff_score}")

                        if reward == 1:
                            if diff_score < 5:
                                print("ℹ️ UI looks similar (NOT a bug)")
                            else:
                                print("🟢 UI changed as expected")

                        elif reward == -1:
                            if diff_score < 5:
                                print("⚠️ Possible silent failure (no UI change)")
                            else:
                                print("🔴 UI changed but logic failed")

                except Exception as e:
                    print("OpenCV error:", e)

                # =============================
                # Critic Agent
                # =============================
                if reward == -1 and message and step["action"] in ["click", "type"]:
                    print("🧠 Critic Agent Activated...")
                    logger.log("🧠 Critic analyzing failure...")

                    new_step = analyze_failure(step, message)

                    if new_step:
                        print("🔁 Critic Suggestion:", new_step)
                        logger.log(f"Critic Suggestion: {new_step}")

                        execute_action(env, new_step)

                # =============================
                # Status Logging
                # =============================
                if reward == 1:
                    logger.log("STATUS: SUCCESS")
                elif reward == -1:
                    logger.log("STATUS: FAILED")

                next_state = [step_count + 1]

                # Stop after verify
                if step["action"] == "verify":
                    done = True

                agent.memory.push(state, action_idx, reward, next_state, done)
                agent.train()

                state = next_state
                step_count += 1

        except Exception as e:
            print("❌ Episode Error:", e)
            logger.log(f"❌ Episode Error: {e}")

        finally:
            env.close()

    print("\n✅ Fully Autonomous Multi-Agent Testing Completed.")