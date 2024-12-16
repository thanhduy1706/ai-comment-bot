import os
import random
import time
import logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException
)
from webdriver_manager.chrome import ChromeDriverManager
import openai
import os
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    'POST_URL': os.getenv('POST_URL'),
    # Change 'Write a comment...' to your language in Facebook settings like 'Comment as Nguyen Duy' or 'Viết bình luận...'
    'COMMENT_BOX_XPATH': "//div[contains(@aria-label, 'Write a comment') and @contenteditable='true']",
    'MAX_COMMENTS': 100,
    'MAX_ITERATIONS': 10000,
    'DELAYS': {
        'SHORT_MIN': 0.5,
        'SHORT_MAX': 2.0,
        'MEDIUM_MIN': 1,
        'MEDIUM_MAX': 3,
        'LONG_MIN': 5,
        'LONG_MAX': 20,
        'RELOAD_PAUSE': 180,
    },
    'CHROME_PROFILE': 'Default'
}

OPENAI_CONFIG = {
    'API_KEY': os.getenv('OPENAI_API_KEY'),
    'MODEL': os.getenv('OPENAI_MODEL'),
    'PROMPT': os.getenv('OPENAI_PROMPT') + 'Do not include emojis or any introductory phrases or additional text.'
}

def setup_logger():
    """
    Set up comprehensive logging configuration.
    """
    os.makedirs('logs', exist_ok=True)
    log_filename = f'logs/facebook_comment_bot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logger()

class FacebookAICommentBot:
    def __init__(self, config=None):
        """
        Initialize the Facebook comment bot with configuration.
        """
        self.config = {**CONFIG, **(config or {})}
        self.driver = None

        openai.api_key = OPENAI_CONFIG['API_KEY']

    def setup_driver(self):
        """
        Sets up and configures the Selenium WebDriver.
        """
        try:
            chrome_options = Options()
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            # Set Chrome binary location (adjust as needed)
            chrome_options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"

            # Create a custom user-data dir (so we don't need your real profile path)
            user_data_dir = os.path.join(os.getcwd(), "chrome_data")
            chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
            chrome_options.add_argument(f"--profile-directory={self.config['CHROME_PROFILE']}")

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("Chrome driver set up successfully.")
        except Exception as e:
            logger.error(f"Failed to setup Chrome Driver: {e}")
            raise

    def random_pause(self, min_time=1, max_time=5):
        """
        Pause execution for a random duration between min_time and max_time seconds.
        """
        delay = random.uniform(min_time, max_time)
        time.sleep(delay)
        logger.debug(f"Paused for {delay:.2f} seconds.")

    def human_mouse_jiggle(self, element, moves=2):
        """
        Simulate human-like mouse movements over a given element.

        Args:
            element: The web element to move the mouse over.
            moves: Number of jiggle movements.
        """
        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()

            for _ in range(moves):
                x_offset = random.randint(-15, 15)
                y_offset = random.randint(-15, 15)
                actions.move_by_offset(x_offset, y_offset).perform()
                self.random_pause(0.3, 1)

            # Return to the element
            actions.move_to_element(element).perform()
            self.random_pause(0.3, 1)
            logger.debug(f"Performed mouse jiggle with {moves} moves.")
        except Exception as e:
            logger.error(f"Mouse jiggle failed: {e}")

    def human_type(self, element, text):
        """
        Simulate human-like typing into a web element.

        Args:
            element: The web element to type into.
            text: The text to type.
        """
        words = text.split()
        for w_i, word in enumerate(words):
            # Introduce random fake words
            if random.random() < 0.05:
                fake_word = random.choice(["aaa", "zzz", "hmm"])
                for c in fake_word:
                    element.send_keys(c)
                    time.sleep(random.uniform(0.08, 0.35))
                for _ in fake_word:
                    element.send_keys(Keys.BACKSPACE)
                    time.sleep(random.uniform(0.06, 0.25))

            for char in word:
                if random.random() < 0.05:
                    wrong_char = random.choice("abcdefghijklmnopqrstuvwxyz")
                    element.send_keys(wrong_char)
                    time.sleep(random.uniform(0.08, 0.35))
                    element.send_keys(Keys.BACKSPACE)
                    time.sleep(random.uniform(0.06, 0.25))
                element.send_keys(char)
                time.sleep(random.uniform(0.08, 0.35))

            if w_i < len(words) - 1:
                element.send_keys(" ")
                time.sleep(random.uniform(0.08, 0.3))

            # random cursor movements
            if random.random() < 0.03:
                element.send_keys(Keys.ARROW_LEFT)
                time.sleep(random.uniform(0.1, 0.3))
                element.send_keys(Keys.ARROW_RIGHT)
                time.sleep(random.uniform(0.1, 0.3))

        self.random_pause(0.5, 1.5)
        logger.debug("Completed human-like typing.")

    def random_scroll(self):
        """
        Scroll up/down randomly to mimic a user's reading or browsing.
        """
        scroll_direction = random.choice(["up", "down"])
        scroll_distance = random.randint(200, 800)

        if scroll_direction == "down":
            self.driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
            logger.debug(f"Scrolling down {scroll_distance} pixels.")
        else:
            self.driver.execute_script(f"window.scrollBy(0, -{scroll_distance});")
            logger.debug(f"Scrolling up {scroll_distance} pixels.")

        self.random_pause(1, 3)

    def random_hover_or_click(self):
        """
        Randomly hover or click on some links or elements on the page to mimic user exploration.
        """
        all_links = self.driver.find_elements(By.TAG_NAME, "a")
        if not all_links:
            return

        if random.random() < 0.5:
            random_link = random.choice(all_links)
            try:
                actions = ActionChains(self.driver)
                actions.move_to_element(random_link).perform()
                logger.debug("Hovering over a random link.")
                self.random_pause(1, 3)

                if random.random() < 0.2:
                    random_link.click()
                    logger.debug("Clicked a random link. Going back in 3 seconds.")
                    time.sleep(3)
                    self.driver.back()
                    self.random_pause(1, 3)
            except Exception as e:
                logger.debug(f"Random hover/click failed: {e}")

    def generate_comment(self) -> str:
        """
        Use OpenAI API to generate a random, personalized comment.
        """
        try:
            prompt = OPENAI_CONFIG['PROMPT']
            response = openai.ChatCompletion.create(
                model=OPENAI_CONFIG['MODEL'],
                messages=[{"role": "user", "content": prompt}],
            )
            comment = response.choices[0].message['content'].strip()
            logger.info(f"Generated comment: {comment}")
            return comment
        except Exception as e:
            logger.error(f"Failed to generate comment: {e}")
            # Default fallback comment if OpenAI fails
            return "Such a thoughtful post! Thanks for sharing! 😊"

    def post_comment(self, comment: str, comment_count: int):
        """
        Locate the comment box, click it, and post a comment with "human-like" actions.
        """
        try:
            comment_area = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.config['COMMENT_BOX_XPATH']))
            )

            # Random scroll or random hover before posting the comment
            if random.random() < 0.4:
                self.random_scroll()
            else:
                self.random_hover_or_click()

            # Human-like mouse movements before clicking
            self.human_mouse_jiggle(comment_area, moves=3)

            # Click inside the comment box
            comment_area.click()
            self.random_pause(0.5, 2.0)

            # Human-like typing into the comment box
            self.human_type(comment_area, comment)
            self.random_pause(0.5, 2.0)

            # Submit the comment (press Enter)
            comment_area.send_keys(Keys.RETURN)
            self.random_pause(0.5, 2.0)

            logger.info(f"Comment {comment_count} posted: '{comment}'")
        except TimeoutException:
            logger.warning(f"Comment {comment_count} posting timeout - element not found")
            raise
        except NoSuchElementException:
            logger.warning(f"Comment {comment_count} posting element not found")
            raise
        except Exception as e:
            logger.error(f"Error during comment posting for comment count {comment_count}: {e}")
            raise

    def run(self):
        """
        Main method to execute the Facebook comment bot with human-like actions.
        """
        try:
            self.setup_driver()
            self.driver.get(self.config['POST_URL'])
            logger.info(f"Loaded Facebook post URL: {self.config['POST_URL']}")

            comment_count = 0

            for i in range(self.config['MAX_ITERATIONS']):
                # Stop if we've hit the maximum comment limit
                if comment_count >= self.config['MAX_COMMENTS']:
                    logger.info("Max comments reached.")
                    break

                self.random_pause(0.5, 2.0)

                # Occasional "idle time" as if the user is reading or distracted
                if random.random() < 0.2:
                    idle_time = random.randint(5, 10)
                    logger.debug(f"Idling for {idle_time} seconds.")
                    time.sleep(idle_time)

                # Generate comment using OpenAI
                comment = self.generate_comment()

                try:
                    self.post_comment(comment, comment_count + 1)
                    comment_count += 1
                except Exception as e:
                    logger.warning(f"Iteration {i+1} failed to post comment: {e}")

                # Every 30 comments, refresh and take a longer pause
                if comment_count % 30 == 0 and comment_count != 0:
                    logger.info(f"Comment count: {comment_count}. Refreshing page.")
                    self.driver.refresh()
                    self.random_pause(self.config['DELAYS']['RELOAD_PAUSE'] - 10, self.config['DELAYS']['RELOAD_PAUSE'] + 10)  # Adding some randomness to the pause
        except Exception as e:
            logger.critical(f"Bot execution failed: {e}")
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("Browser closed.")

def main():
    """
    Main function for the Facebook comment bot.
    """
    try:
        bot = FacebookAICommentBot()
        bot.run()
    except Exception as e:
        logger.critical(f"Bot initialization failed: {e}")

if __name__ == "__main__":
    main()
