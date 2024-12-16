# 📢 Facebook Comment Bot

![Facebook Comment Bot](https://img.shields.io/badge/Facebook%20Comment-Bot-blue)
![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT4-green)

A **Selenium-based bot** designed to automatically post **human-like comments** on a specified Facebook post using **OpenAI's language models**. This bot simulates genuine user interactions to enhance engagement on your Facebook posts.

---

## 📋 Table of Contents

- [🌟 Features](#🌟-features)
- [🔧 Prerequisites](#🔧-prerequisites)
- [💻 Installation](#💻-installation)
- [⚙️ Configuration](#⚙️-configuration)
- [🚀 Usage](#🚀-usage)
- [🔑 Handling Login](#🔑-handling-login)
- [📝 Logging and Debugging](#📝-logging-and-debugging)
- [⚠️ Ethical Considerations](#⚠️-ethical-considerations)
- [🛠️ Troubleshooting](#🛠️-troubleshooting)
- [📄 License](#📄-license)
- [📞 Contact](#📞-contact)
- [🔗 Acknowledgements](#🔗-acknowledgements)

---

## 🌟 Features

- **Automated Commenting:** Automatically generate and post comments on a specified Facebook post.
- **Human-like Interactions:** Simulates human behavior with random pauses, mouse movements, and typing patterns to mimic genuine user interactions.
- **OpenAI Integration:** Utilizes OpenAI's language models to generate contextually relevant and engaging comments.
- **Robust Logging:** Comprehensive logging for monitoring bot activities and debugging.
- **Error Handling:** Captures and logs errors, raising exceptions for critical issues.

---

## 🔧 Prerequisites

Before setting up the bot, ensure you have the following:

- **Python 3.7 or Higher:** [Download Python](https://www.python.org/downloads/)
- **Google Chrome Browser:** Ensure it's installed on your system.
- **ChromeDriver:** Managed automatically by `webdriver-manager`, so no manual setup is required.
- **OpenAI API Key:** Sign up at [OpenAI](https://platform.openai.com/signup/) to obtain your API key.
- **Facebook Account:** A Facebook account to post comments.

---

## 💻 Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/thanhduy1706/ai-comment-bot.git
   cd ai-comment-bot
   ```

2. **Create a Virtual Environment (Optional but Recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Required Packages:**

   Ensure you have pip installed. Then run:

   ```bash
   pip install -r requirements.txt
   ```

   `requirements.txt` Content:

   ```
   selenium
   webdriver-manager
   openai==0.28
   python-dotenv
   pre-commit
   ```

---

## ⚙️ Configuration

1. **Create a `.env` File:**

   In the root directory of the project, create a `.env` file to store your sensitive information.

2. **Populate the `.env` File:**

   Open the `.env` file in a text editor and add the following configurations:

   ```makefile
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4o-mini
   OPENAI_PROMPT=Generate a friendly, specific, and engaging Facebook comment.
   POST_URL=https://www.facebook.com/your_post_url_here
   ```

   Replace:

   - `your_openai_api_key_here` with your actual OpenAI API key.
   - `gpt-4o-mini` with the desired OpenAI model (e.g., `gpt-4`, `gpt-4-turbo`, `gpt-4o-mini`).
   - `Generate a friendly, specific, and engaging Facebook comment.` with your desired OpenAI prompt.
   - `https://www.facebook.com/your_post_url_here` with the URL of the Facebook post you want to comment on.

---

## 🚀 Usage

Follow these steps to run the Facebook Comment Bot:

1. **Ensure Environment Variables are Set:**

   Double-check your `.env` file to ensure all required variables are correctly set.

2. **Run the Script:**

   Execute the bot using the following command:

   ```bash
   python cmt.py
   ```

3. **Bot Execution Flow:**

   - **Initialization:** The bot sets up the Chrome WebDriver with specified options to minimize detection.
   - **Navigating to Post:** It navigates to the specified Facebook post URL.
   - **Commenting Process:**
     - The bot generates comments using OpenAI's API.
     - Simulates human-like typing and interactions to post comments.
     - Repeats the process based on `MAX_COMMENTS` and `MAX_ITERATIONS` settings.
     - Periodically refreshes the page to maintain session stability.

   **Example Command:**

   ```bash
   python cmt.py
   ```

---

## 🔑 Handling Login

**Manual Login Process:**

- **Step 1:** If not logged in, you need opens a new tab directing to Facebook's login page.
- **Step 2:** Manually log in to Facebook in the newly opened tab.
- **Step 3:** After successfully logging in, closes the login tab.
- **Step 4:** Refreshes the main tab, and resumes the commenting process.

_Note: This manual login step ensures that your credentials remain secure and adheres to Facebook's policies by avoiding automated login attempts._

---

## 📝 Logging and Debugging

The bot maintains detailed logs to monitor its activities and assist in debugging:

1. **Log Files:**

   - Stored in the `logs/` directory.
   - Named using the timestamp format: `facebook_comment_bot_YYYYMMDD_HHMMSS.log`.

2. **Log Levels:**

   - `INFO`: General operational messages (e.g., driver setup, comment posting).
   - `DEBUG`: Detailed information useful for debugging (e.g., pauses, mouse movements).
   - `WARNING`: Non-critical issues (e.g., failed comment posts).
   - `ERROR`: Critical problems that may halt execution.
   - `CRITICAL`: Severe issues requiring immediate attention.

---

## ⚠️ Ethical Considerations

**Important:** Automating interactions on platforms like Facebook can violate their Terms of Service and Community Standards. Use such bots responsibly and ethically, ensuring compliance with all relevant policies.

**Potential Risks:**

- **Account Restrictions or Bans:** Automated actions can lead to your Facebook account being restricted or banned.
- **Legal Implications:** Depending on jurisdiction and usage, there could be legal consequences.

**Recommendation:** Use this bot for educational purposes only and ensure you have the necessary permissions to interact with the targeted Facebook posts.

---

## 🛠️ Troubleshooting

**Issue:** Bot fails to post comments.

**Solution:**

- Ensure you're logged into Facebook. If prompted, follow the manual login steps.
- Check the `logs/` directory for detailed error messages.
- Update the `COMMENT_BOX_XPATH` in the `CONFIG` if Facebook has updated its UI.

**Issue:** "element click intercepted" error persists.

**Solution:**

- Enhance the `close_overlays` method to handle new pop-ups or overlays.
- Implement additional delays to ensure elements are fully loaded.
- Use more robust selectors to accurately locate the comment box.

**Issue:** Unable to locate comment box.

**Solution:**

- Verify the `COMMENT_BOX_XPATH` in the `CONFIG`.
- Update the XPath based on the current Facebook UI.
- Ensure that Facebook hasn't changed the structure or labels of the comment box.

---

## 📄 License

This project is licensed under the MIT License.

---

## 📞 Contact

For any inquiries or support, please contact thanhduy1706@gmail.com.

---

## 🔗 Acknowledgements

- Selenium
- WebDriver Manager
- OpenAI
- Python-dotenv
