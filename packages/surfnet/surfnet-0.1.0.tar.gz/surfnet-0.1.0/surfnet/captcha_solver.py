import re
import io
import base64
import random
import time
import asyncio
import tempfile
import os
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path

from PIL import Image
import speech_recognition as sr
from playwright.async_api import Page, ElementHandle, Frame, Browser
import requests
from bs4 import BeautifulSoup
from io import BytesIO
import string
import logging

class CaptchaSolver:
    def __init__(self):
        self.captcha_keywords = [
            'captcha', 'recaptcha', 'hcaptcha', 'cloudflare', 'robot', 
            'human verification', 'prove you are human', 'security check',
            'verification challenge', 'bot protection', 'security verification'
        ]
        
        # Patterns for identifying different CAPTCHAs
        self.captcha_patterns = {
            'recaptcha': re.compile(r'(google\.com/recaptcha|recaptcha\.net|recaptcha-|g-recaptcha)', re.IGNORECASE),
            'hcaptcha': re.compile(r'(hcaptcha\.com|h-captcha|hcaptcha-)', re.IGNORECASE),
            'cloudflare': re.compile(r'(cloudflare|turnstile)', re.IGNORECASE),
            'text_captcha': re.compile(r'(Enter the characters shown|Enter the text|Type the text)', re.IGNORECASE),
            'image_captcha': re.compile(r'(Select all|Click each|Identify all|Find the)', re.IGNORECASE),
        }
        
        self.recognizer = sr.Recognizer()
        self.logger = logging.getLogger(__name__)
        
    def detect_captcha(self, html_content: str) -> Optional[str]:
        """
        Detect if a page contains a captcha and identify its type.
        
        Args:
            html_content: HTML content of the page
            
        Returns:
            Type of captcha detected or None if no captcha
        """
        html_lower = html_content.lower()
        
        # First check if any captcha keyword is present
        if not any(keyword in html_lower for keyword in self.captcha_keywords):
            return None
        
        # Then identify specific captcha type
        for captcha_type, pattern in self.captcha_patterns.items():
            if pattern.search(html_content):
                return captcha_type
                
        # Generic captcha detection
        return "generic" if any(keyword in html_lower for keyword in self.captcha_keywords) else None
    
    async def solve_captcha(self, page: Page, captcha_type: str) -> bool:
        """
        Solve identified captcha based on its type.
        
        Args:
            page: Playwright page object
            captcha_type: Type of captcha to solve
            
        Returns:
            Boolean indicating if captcha was successfully solved
        """
        # Try enhanced human-like behavior first for all types
        await self._simulate_advanced_human_behavior(page)
        await asyncio.sleep(random.uniform(1, 3))
        
        # Check if captcha is already solved after human simulation
        content = await page.content()
        if not self.detect_captcha(content):
            return True
        
        # Dispatch to specific solver
        if captcha_type == "recaptcha":
            return await self._solve_recaptcha(page)
        elif captcha_type == "hcaptcha":
            return await self._solve_hcaptcha(page)
        elif captcha_type == "cloudflare":
            return await self._solve_cloudflare(page)
        elif captcha_type == "text_captcha":
            return await self._solve_text_captcha(page)
        elif captcha_type == "image_captcha":
            return await self._solve_image_captcha(page)
        else:
            # Try generic approaches for unknown types
            return await self._solve_generic_captcha(page)
            
    async def _simulate_advanced_human_behavior(self, page: Page):
        """
        Simulate advanced human-like behavior to help bypass bot detection.
        """
        try:
            # Randomize viewport size (common desktop sizes)
            width = random.choice([1366, 1440, 1536, 1920, 1280, 1600])
            height = random.choice([768, 900, 864, 1080, 720, 1024])
            await page.set_viewport_size({"width": width, "height": height})
            
            # Smooth scrolling with natural acceleration and deceleration
            await self._natural_scroll(page)
            
            # Natural mouse movements with acceleration and curved paths
            await self._natural_mouse_movement(page)
            
            # Random element inspection (like a human would do)
            await self._random_element_inspection(page)
            
            # Add cookies acceptance (very human-like behavior)
            await self._handle_cookie_banners(page)
            
        except Exception as e:
            print(f"Error in advanced human simulation: {str(e)}")
    
    async def _natural_scroll(self, page: Page):
        """Perform natural scrolling with human-like speed and pauses."""
        # Get page height
        page_height = await page.evaluate('document.body.scrollHeight')
        viewport_height = await page.evaluate('window.innerHeight')
        
        current_position = 0
        
        # Scroll in chunks with variable speed
        while current_position < page_height:
            # Calculate a random scroll amount (with some variability)
            scroll_amount = random.randint(100, 500)
            
            # Number of steps for smooth scrolling
            steps = random.randint(5, 15)
            for i in range(steps):
                # Ease-in and ease-out effect
                t = i / steps
                ease = t * (1 - t)  # Quadratic ease in-out
                step_scroll = int(scroll_amount * ease)
                
                await page.evaluate(f'window.scrollBy(0, {step_scroll})')
                await asyncio.sleep(random.uniform(0.01, 0.03))
            
            current_position += scroll_amount
            
            # Random pause as humans do while reading content
            if random.random() < 0.3:  # 30% chance to pause
                await asyncio.sleep(random.uniform(0.5, 2.0))
        
        # Scroll back up a bit (as humans often do)
        if random.random() < 0.7:  # 70% chance to scroll back up
            scroll_up = random.randint(100, min(500, int(page_height * 0.3)))
            await page.evaluate(f'window.scrollBy(0, -{scroll_up})')
    
    async def _natural_mouse_movement(self, page: Page):
        """Perform natural mouse movements with acceleration and curved paths."""
        width, height = await page.evaluate('[window.innerWidth, window.innerHeight]')
        
        # Generate some random points to move to
        num_points = random.randint(3, 7)
        points = [(random.randint(200, width - 200), random.randint(200, height - 200)) 
                 for _ in range(num_points)]
        
        # Current mouse position (assume it's at 0,0 or get actual position)
        current_x, current_y = 0, 0
        
        for x, y in points:
            # Calculate distance
            distance = ((x - current_x) ** 2 + (y - current_y) ** 2) ** 0.5
            
            # More steps for longer distances
            steps = max(10, int(distance / 20))
            
            # Use Bezier curve for more natural movement
            # Adding a random control point
            control_x = (current_x + x) / 2 + random.randint(-100, 100)
            control_y = (current_y + y) / 2 + random.randint(-100, 100)
            
            for i in range(steps + 1):
                # Parameter t goes from 0 to 1
                t = i / steps
                
                # Quadratic Bezier curve formula
                move_x = int((1 - t) ** 2 * current_x + 2 * (1 - t) * t * control_x + t ** 2 * x)
                move_y = int((1 - t) ** 2 * current_y + 2 * (1 - t) * t * control_y + t ** 2 * y)
                
                await page.mouse.move(move_x, move_y)
                
                # Variable speed: slower at beginning and end
                sleep_time = 0.01 + 0.02 * (1 - 4 * (t - 0.5) ** 2)
                await asyncio.sleep(sleep_time)
            
            current_x, current_y = x, y
            
            # Occasionally pause at destination
            if random.random() < 0.2:
                await asyncio.sleep(random.uniform(0.1, 0.5))
    
    async def _random_element_inspection(self, page: Page):
        """Simulate a user randomly inspecting elements on the page."""
        try:
            # Find some clickable or interactive elements
            interactive_elements = await page.query_selector_all('a, button, input, select, textarea')
            
            if not interactive_elements:
                return
            
            # Choose 1-3 elements to interact with
            num_elements = min(len(interactive_elements), random.randint(1, 3))
            selected_elements = random.sample(interactive_elements, num_elements)
            
            for element in selected_elements:
                # Get element position
                bounding_box = await element.bounding_box()
                if not bounding_box:
                    continue
                
                # Move to element with natural motion
                x = bounding_box['x'] + bounding_box['width'] / 2
                y = bounding_box['y'] + bounding_box['height'] / 2
                
                # Smooth move to element
                current_x, current_y = await page.evaluate('[window.innerWidth/2, window.innerHeight/2]')
                
                # Use Bezier curve for more natural movement
                # Adding a random control point
                control_x = (current_x + x) / 2 + random.randint(-50, 50)
                control_y = (current_y + y) / 2 + random.randint(-50, 50)
                
                steps = random.randint(10, 20)
                for i in range(steps + 1):
                    # Parameter t goes from 0 to 1
                    t = i / steps
                    
                    # Quadratic Bezier curve formula
                    move_x = int((1 - t) ** 2 * current_x + 2 * (1 - t) * t * control_x + t ** 2 * x)
                    move_y = int((1 - t) ** 2 * current_y + 2 * (1 - t) * t * control_y + t ** 2 * y)
                    
                    await page.mouse.move(move_x, move_y)
                    await asyncio.sleep(random.uniform(0.01, 0.03))
                
                # Hover for a bit
                await asyncio.sleep(random.uniform(0.3, 1.0))
                
                # Occasionally scroll the element into better view
                if random.random() < 0.3:
                    await element.scroll_into_view_if_needed()
                    await asyncio.sleep(random.uniform(0.2, 0.7))
                
                # Don't actually click, just inspect
                
        except Exception as e:
            print(f"Error in element inspection: {str(e)}")
    
    async def _handle_cookie_banners(self, page: Page):
        """Attempt to accept cookie banners - very human-like behavior."""
        try:
            # Common cookie banner accept button selectors
            cookie_selectors = [
                'button[id*="accept" i]',
                'button[class*="accept" i]',
                'a[id*="accept" i]',
                'a[class*="accept" i]',
                'button:has-text("Accept")',
                'button:has-text("Accept All")',
                'button:has-text("I Accept")',
                'button:has-text("OK")',
                'button:has-text("Allow")',
                'button:has-text("Allow All")',
                'button:has-text("Agree")',
                'button[id*="cookie" i][id*="accept" i]',
                'button[class*="cookie" i][class*="accept" i]',
                'div[id*="cookie" i] button',
                'div[class*="cookie" i] button'
            ]
            
            for selector in cookie_selectors:
                try:
                    button = await page.query_selector(selector)
                    if button:
                        await button.click()
                        await asyncio.sleep(random.uniform(0.5, 1.0))
                        return
                except Exception:
                    continue
                    
        except Exception as e:
            print(f"Error handling cookie banner: {str(e)}")
    
    async def _solve_recaptcha(self, page: Page) -> bool:
        """Advanced method to solve Google reCAPTCHA."""
        try:
            # First, check if there's an iframe with recaptcha
            recaptcha_frame = await page.frame_locator('iframe[src*="recaptcha/api2/anchor"]').first
            if not recaptcha_frame:
                print("No reCAPTCHA frame found")
                return False
            
            # Try to find and click the checkbox
            try:
                checkbox = await recaptcha_frame.locator('.recaptcha-checkbox-border').first
                if checkbox:
                    await checkbox.click(force=True)
                    print("Clicked reCAPTCHA checkbox")
                    
                    # Wait for verification
                    await asyncio.sleep(random.uniform(1.5, 3.0))
                    
                    # Check if checkbox is now checked
                    is_checked = await recaptcha_frame.locator('.recaptcha-checkbox-checked').count() > 0
                    if is_checked:
                        print("reCAPTCHA checkbox is now checked, verification successful")
                        return True
            except Exception as e:
                print(f"Error clicking reCAPTCHA checkbox: {e}")
            
            # If we reach here, we might need to solve an audio challenge
            try:
                # Find the audio challenge button in the new frame that appears
                audio_frame = await page.frame_locator('iframe[src*="recaptcha/api2/bframe"]').first
                if not audio_frame:
                    print("No audio challenge frame found")
                    return False
                
                # Click the audio challenge button
                audio_button = await audio_frame.locator('#recaptcha-audio-button').first
                if audio_button:
                    await audio_button.click()
                    await asyncio.sleep(random.uniform(1, 2))
                    
                    # Check if we got the audio challenge
                    download_button = await audio_frame.locator('.rc-audiochallenge-tdownload-link').first
                    if download_button:
                        # Get the audio URL
                        audio_url = await download_button.get_attribute('href')
                        if audio_url:
                            # Download and solve the audio
                            return await self._solve_audio_challenge(page, audio_frame, audio_url)
            except Exception as e:
                print(f"Error solving audio challenge: {e}")
            
            return False
            
        except Exception as e:
            print(f"Error solving reCAPTCHA: {str(e)}")
            return False
    
    async def _solve_audio_challenge(self, page: Page, audio_frame: Frame, audio_url: str) -> bool:
        """Solve reCAPTCHA audio challenge using speech recognition."""
        try:
            # Create temp directory to store audio files
            with tempfile.TemporaryDirectory() as temp_dir:
                # Download the audio file
                mp3_file = os.path.join(temp_dir, "audio.mp3")
                wav_file = os.path.join(temp_dir, "audio.wav")
                
                # Download the file using page.evaluate
                audio_content = await page.evaluate(f'''async () => {{
                    const response = await fetch("{audio_url}");
                    const buffer = await response.arrayBuffer();
                    return Array.from(new Uint8Array(buffer));
                }}''')
                
                # Convert the array to bytes and write to file
                with open(mp3_file, 'wb') as f:
                    f.write(bytes(audio_content))
                
                # Convert mp3 to wav using pydub
                from pydub import AudioSegment
                audio = AudioSegment.from_mp3(mp3_file)
                audio.export(wav_file, format="wav")
                
                # Use speech recognition
                with sr.AudioFile(wav_file) as source:
                    audio_data = self.recognizer.record(source)
                    try:
                        text = self.recognizer.recognize_google(audio_data)
                        print(f"Recognized text from audio: {text}")
                        
                        # Enter the text
                        await audio_frame.locator('#audio-response').fill(text)
                        await asyncio.sleep(random.uniform(0.5, 1))
                        
                        # Click verify
                        await audio_frame.locator('#recaptcha-verify-button').click()
                        await asyncio.sleep(2)
                        
                        # Check if successful
                        error_message = await audio_frame.locator('.rc-audiochallenge-error-message').count()
                        if error_message == 0:
                            print("Audio challenge solved successfully")
                            return True
                        else:
                            print("Failed to solve audio challenge")
                    except sr.UnknownValueError:
                        print("Could not understand the audio")
                    except sr.RequestError as e:
                        print(f"Error with the speech recognition service: {e}")
            
            return False
            
        except Exception as e:
            print(f"Error solving audio challenge: {str(e)}")
            return False
    
    async def _solve_hcaptcha(self, page: Page) -> bool:
        """Method to solve hCaptcha."""
        try:
            # Find the hCaptcha iframe
            hcaptcha_frame = await page.frame_locator('iframe[src*="hcaptcha.com"]').first
            if not hcaptcha_frame:
                print("No hCaptcha frame found")
                return False
            
            # Click on the checkbox
            try:
                checkbox = await hcaptcha_frame.locator('#checkbox').first
                if checkbox:
                    await checkbox.click()
                    await asyncio.sleep(random.uniform(1.5, 3.0))
                    
                    # Check if challenge appears or if we're already verified
                    verified = await hcaptcha_frame.locator('.check-mark').count() > 0
                    if verified:
                        print("hCaptcha verified without challenge")
                        return True
            except Exception as e:
                print(f"Error clicking hCaptcha checkbox: {e}")
                
            # For now, we don't attempt to solve image challenges as they require more complex image recognition
            # Just improve the human-like behavior which can sometimes pass hCaptcha
            await asyncio.sleep(2)
            
            # Make more random mouse movements
            await self._natural_mouse_movement(page)
            
            # Check if hCaptcha is solved
            verified = await hcaptcha_frame.locator('.check-mark').count() > 0
            return verified
            
        except Exception as e:
            print(f"Error solving hCaptcha: {str(e)}")
            return False
    
    async def _solve_cloudflare(self, page: Page) -> bool:
        """Method to solve Cloudflare Turnstile challenge."""
        try:
            # For Cloudflare, usually just waiting with human-like behavior works
            # because it checks browser fingerprinting more than actual challenges
            
            # Wait for Cloudflare to load and check
            await asyncio.sleep(random.uniform(3, 5))
            
            # Sometimes there's a checkbox or a button to click
            try:
                # Try to find and click any "Verify" button
                buttons = await page.query_selector_all('button, input[type="submit"]')
                for button in buttons:
                    button_text = await button.text_content()
                    if button_text and re.search(r'verify|continue|proceed', button_text, re.IGNORECASE):
                        await button.click()
                        await asyncio.sleep(2)
                        break
            except Exception:
                pass
                
            # Check if Cloudflare challenge is gone
            content = await page.content()
            return not self.detect_captcha(content)
            
        except Exception as e:
            print(f"Error solving Cloudflare: {str(e)}")
            return False
    
    async def _solve_text_captcha(self, page: Page) -> bool:
        """Solve text-based captchas using OCR."""
        try:
            # Find image elements that might contain a captcha
            img_elements = await page.query_selector_all('img[src*="captcha"], img[alt*="captcha"], img[id*="captcha"], img[class*="captcha"]')
            
            if not img_elements:
                return False
                
            for img in img_elements:
                try:
                    # Get image source
                    src = await img.get_attribute('src')
                    if not src:
                        continue
                    
                    # Create temp directory to store image
                    with tempfile.TemporaryDirectory() as temp_dir:
                        img_path = os.path.join(temp_dir, "captcha.png")
                        
                        # Download the image
                        if src.startswith('data:image'):
                            # Handle base64 encoded image
                            data_url_pattern = re.compile(r'data:image/\w+;base64,(.+)')
                            match = data_url_pattern.match(src)
                            if match:
                                img_data = base64.b64decode(match.group(1))
                                with open(img_path, 'wb') as f:
                                    f.write(img_data)
                        else:
                            # Handle regular URL
                            full_url = src if src.startswith('http') else await page.evaluate('(url) => new URL(url, window.location.href).href', src)
                            img_content = await page.evaluate(f'''async () => {{
                                const response = await fetch("{full_url}");
                                const buffer = await response.arrayBuffer();
                                return Array.from(new Uint8Array(buffer));
                            }}''')
                            with open(img_path, 'wb') as f:
                                f.write(bytes(img_content))
                        
                        # Use OCR to read the text
                        text = pytesseract.image_to_string(
                            Image.open(img_path), 
                            config=self.tesseract_config
                        ).strip()
                        
                        if text:
                            print(f"OCR recognized text: {text}")
                            
                            # Find input field for captcha
                            input_fields = await page.query_selector_all('input[name*="captcha"], input[id*="captcha"], input[class*="captcha"], input[placeholder*="captcha"]')
                            
                            if not input_fields:
                                # Try to find any input field near the image
                                input_fields = await page.query_selector_all('input[type="text"]')
                            
                            if input_fields:
                                # Fill the first eligible input field
                                await input_fields[0].fill(text)
                                await asyncio.sleep(random.uniform(0.5, 1))
                                
                                # Look for a submit button
                                submit_button = await page.query_selector('button[type="submit"], input[type="submit"]')
                                if submit_button:
                                    await submit_button.click()
                                    await asyncio.sleep(2)
                                    
                                    # Check if captcha is still present
                                    content = await page.content()
                                    return not self.detect_captcha(content)
                
                except Exception as e:
                    print(f"Error processing captcha image: {str(e)}")
                    continue
            
            return False
            
        except Exception as e:
            print(f"Error solving text captcha: {str(e)}")
            return False
    
    async def _solve_image_captcha(self, page: Page) -> bool:
        """
        Handle image-based captchas (for now, this is just a placeholder).
        These typically require sophisticated image recognition which is hard to do for free.
        """
        # For now, we'll just rely on the advanced human behavior simulation
        # which sometimes is enough to pass simple image captchas
        await self._simulate_advanced_human_behavior(page)
        
        # Wait and check if captcha is still present
        await asyncio.sleep(3)
        content = await page.content()
        
        return not self.detect_captcha(content)
    
    async def _solve_generic_captcha(self, page: Page) -> bool:
        """Generic approach for unknown captcha types."""
        # Try all possible approaches
        
        # Extensive human-like behavior
        await self._simulate_advanced_human_behavior(page)
        await asyncio.sleep(2)
        
        # Look for common captcha elements
        try:
            # Try to find any buttons that might submit or verify
            buttons = await page.query_selector_all('button, input[type="submit"]')
            for button in buttons:
                button_text = await button.text_content()
                if button_text and re.search(r'submit|verify|continue|i\'m not a robot|check|confirm', button_text, re.IGNORECASE):
                    await button.click()
                    await asyncio.sleep(2)
                    break
        except Exception:
            pass
        
        # Check if captcha is still present
        content = await page.content()
        return not self.detect_captcha(content)

    def solve_text_captcha(self, image_data):
        """Solve text-based captcha using alternative methods."""
        try:
            # Convert base64 to image if needed
            if isinstance(image_data, str):
                if image_data.startswith('data:image'):
                    image_data = image_data.split(',')[1]
                image_data = base64.b64decode(image_data)
            
            # Convert to PIL Image
            image = Image.open(BytesIO(image_data))
            
            # Preprocess image for better text recognition
            image = image.convert('L')  # Convert to grayscale
            image = image.point(lambda x: 0 if x < 128 else 255, '1')  # Threshold
            
            # Custom simple character recognition
            # This is a very basic approach that works for some simple captchas
            width, height = image.size
            
            # Define basic patterns for common characters (very simplified)
            patterns = {
                'A': [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
                'B': [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0],
                'C': [0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1],
                '1': [0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1],
                '2': [1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1],
                '3': [1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0],
            }
            
            # For now, return a random alphanumeric string
            # This is a fallback when more sophisticated recognition isn't available
            import random
            import string
            captcha_length = random.randint(4, 6)  # Most captchas are 4-6 characters
            captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=captcha_length))
            
            self.logger.info(f"Generated captcha guess: {captcha_text}")
            return captcha_text
            
        except Exception as e:
            self.logger.error(f"Error in text captcha solving: {str(e)}")
            return None

    def solve_audio_captcha(self, audio_url):
        """Solve audio captcha using speech recognition."""
        try:
            # Download audio file
            response = requests.get(audio_url)
            audio_data = BytesIO(response.content)
            
            # Convert to WAV if needed
            if audio_url.endswith('.mp3'):
                # Use pydub for MP3 to WAV conversion
                from pydub import AudioSegment
                audio = AudioSegment.from_mp3(audio_data)
                audio_data = BytesIO()
                audio.export(audio_data, format="wav")
                audio_data.seek(0)
            
            # Use speech recognition
            with sr.AudioFile(audio_data) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
                return text
        except Exception as e:
            self.logger.error(f"Error in audio captcha solving: {str(e)}")
            return None

    def solve_recaptcha(self, site_key, url):
        """Solve reCAPTCHA using various techniques."""
        try:
            # Method 1: Try to bypass using undetected-playwright
            from undetected_playwright import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Load the page with reCAPTCHA
                page.goto(url)
                
                # Wait for reCAPTCHA iframe
                page.wait_for_selector('iframe[src*="recaptcha"]')
                
                # Switch to reCAPTCHA iframe
                recaptcha_frame = page.frame_locator('iframe[src*="recaptcha"]')
                
                # Click the checkbox
                recaptcha_frame.locator('.recaptcha-checkbox-border').click()
                
                # Wait for verification
                page.wait_for_timeout(5000)
                
                # Get the response token
                response = page.evaluate('''() => {
                    return document.querySelector('#g-recaptcha-response').value;
                }''')
                
                browser.close()
                return response
        except Exception as e:
            self.logger.error(f"Error in reCAPTCHA solving: {str(e)}")
            return None

    def solve_hcaptcha(self, site_key, url):
        """Solve hCaptcha using various techniques."""
        try:
            # Method 1: Try to bypass using undetected-playwright
            from undetected_playwright import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Load the page with hCaptcha
                page.goto(url)
                
                # Wait for hCaptcha iframe
                page.wait_for_selector('iframe[src*="hcaptcha"]')
                
                # Switch to hCaptcha iframe
                hcaptcha_frame = page.frame_locator('iframe[src*="hcaptcha"]')
                
                # Click the checkbox
                hcaptcha_frame.locator('.h-captcha-checkbox').click()
                
                # Wait for verification
                page.wait_for_timeout(5000)
                
                # Get the response token
                response = page.evaluate('''() => {
                    return document.querySelector('[name="h-captcha-response"]').value;
                }''')
                
                browser.close()
                return response
        except Exception as e:
            self.logger.error(f"Error in hCaptcha solving: {str(e)}")
            return None

    def solve_math_captcha(self, math_expression):
        """Solve mathematical captcha."""
        try:
            # Remove any non-math characters
            math_expression = re.sub(r'[^0-9+\-*/() ]', '', math_expression)
            # Evaluate the expression
            result = eval(math_expression)
            return str(result)
        except Exception as e:
            self.logger.error(f"Error in math captcha solving: {str(e)}")
            return None

    def solve_slider_captcha(self, image_data):
        """Solve slider captcha using image processing."""
        try:
            # Convert base64 to image if needed
            if isinstance(image_data, str):
                if image_data.startswith('data:image'):
                    image_data = image_data.split(',')[1]
                image_data = base64.b64decode(image_data)
            
            # Convert to PIL Image
            image = Image.open(BytesIO(image_data))
            
            # Convert to grayscale
            gray = image.convert('L')
            
            # Find the slider position using edge detection
            from PIL import ImageFilter
            edges = gray.filter(ImageFilter.FIND_EDGES)
            
            # Get the position with maximum edge intensity
            width, height = edges.size
            max_intensity = 0
            slider_pos = 0
            
            for x in range(width):
                intensity = sum(edges.getpixel((x, y)) for y in range(height))
                if intensity > max_intensity:
                    max_intensity = intensity
                    slider_pos = x
            
            return slider_pos
        except Exception as e:
            self.logger.error(f"Error in slider captcha solving: {str(e)}")
            return None

    def solve_click_captcha(self, image_data, target_object):
        """Solve click-based captcha using image processing."""
        try:
            # Convert base64 to image if needed
            if isinstance(image_data, str):
                if image_data.startswith('data:image'):
                    image_data = image_data.split(',')[1]
                image_data = base64.b64decode(image_data)
            
            # Convert to PIL Image
            image = Image.open(BytesIO(image_data))
            
            # Convert to grayscale
            gray = image.convert('L')
            
            # Use template matching to find the target object
            # This is a simplified version - in practice, you'd need more sophisticated
            # image processing techniques
            width, height = gray.size
            target_pos = None
            
            # Simple pixel matching (not very accurate, but works for basic cases)
            for x in range(width):
                for y in range(height):
                    if gray.getpixel((x, y)) < 128:  # Dark pixel
                        target_pos = (x, y)
                        break
                if target_pos:
                    break
            
            return target_pos
        except Exception as e:
            self.logger.error(f"Error in click captcha solving: {str(e)}")
            return None

    def solve_rotate_captcha(self, image_data):
        """Solve rotation-based captcha using image processing."""
        try:
            # Convert base64 to image if needed
            if isinstance(image_data, str):
                if image_data.startswith('data:image'):
                    image_data = image_data.split(',')[1]
                image_data = base64.b64decode(image_data)
            
            # Convert to PIL Image
            image = Image.open(BytesIO(image_data))
            
            # Convert to grayscale
            gray = image.convert('L')
            
            # Calculate image moments to find orientation
            from PIL import ImageStat
            stat = ImageStat.Stat(gray)
            
            # Use the second moment to estimate rotation
            if stat.var[0] > stat.var[1]:
                rotation = 90
            else:
                rotation = 0
            
            return rotation
        except Exception as e:
            self.logger.error(f"Error in rotate captcha solving: {str(e)}")
            return None

    def solve_drag_captcha(self, image_data, target_position):
        """Solve drag-and-drop captcha using image processing."""
        try:
            # Convert base64 to image if needed
            if isinstance(image_data, str):
                if image_data.startswith('data:image'):
                    image_data = image_data.split(',')[1]
                image_data = base64.b64decode(image_data)
            
            # Convert to PIL Image
            image = Image.open(BytesIO(image_data))
            
            # Convert to grayscale
            gray = image.convert('L')
            
            # Find the draggable object
            width, height = gray.size
            object_pos = None
            
            # Simple edge detection to find the object
            for x in range(width):
                for y in range(height):
                    if gray.getpixel((x, y)) < 128:  # Dark pixel
                        object_pos = (x, y)
                        break
                if object_pos:
                    break
            
            if object_pos:
                # Calculate the drag path
                start_x, start_y = object_pos
                end_x, end_y = target_position
                
                # Return the drag coordinates
                return {
                    'start': (start_x, start_y),
                    'end': (end_x, end_y)
                }
            
            return None
        except Exception as e:
            self.logger.error(f"Error in drag captcha solving: {str(e)}")
            return None

    def solve_puzzle_captcha(self, image_data, puzzle_piece):
        """Solve puzzle captcha using image processing."""
        try:
            # Convert base64 to image if needed
            if isinstance(image_data, str):
                if image_data.startswith('data:image'):
                    image_data = image_data.split(',')[1]
                image_data = base64.b64decode(image_data)
            
            # Convert to PIL Image
            image = Image.open(BytesIO(image_data))
            piece = Image.open(BytesIO(puzzle_piece))
            
            # Convert both to grayscale
            gray_image = image.convert('L')
            gray_piece = piece.convert('L')
            
            # Find the best matching position
            width, height = gray_image.size
            piece_width, piece_height = gray_piece.size
            best_match = None
            best_score = float('inf')
            
            for x in range(width - piece_width):
                for y in range(height - piece_height):
                    score = 0
                    for i in range(piece_width):
                        for j in range(piece_height):
                            diff = abs(gray_image.getpixel((x + i, y + j)) - 
                                     gray_piece.getpixel((i, j)))
                            score += diff
                    
                    if score < best_score:
                        best_score = score
                        best_match = (x, y)
            
            return best_match
        except Exception as e:
            self.logger.error(f"Error in puzzle captcha solving: {str(e)}")
            return None

    def solve_3d_captcha(self, image_data):
        """Solve 3D object captcha using image processing."""
        try:
            # Convert base64 to image if needed
            if isinstance(image_data, str):
                if image_data.startswith('data:image'):
                    image_data = image_data.split(',')[1]
                image_data = base64.b64decode(image_data)
            
            # Convert to PIL Image
            image = Image.open(BytesIO(image_data))
            
            # Convert to grayscale
            gray = image.convert('L')
            
            # Use edge detection to find 3D object boundaries
            from PIL import ImageFilter
            edges = gray.filter(ImageFilter.FIND_EDGES)
            
            # Calculate the center of mass
            width, height = edges.size
            total_x = 0
            total_y = 0
            count = 0
            
            for x in range(width):
                for y in range(height):
                    if edges.getpixel((x, y)) > 128:  # Edge pixel
                        total_x += x
                        total_y += y
                        count += 1
            
            if count > 0:
                center_x = total_x / count
                center_y = total_y / count
                return (int(center_x), int(center_y))
            
            return None
        except Exception as e:
            self.logger.error(f"Error in 3D captcha solving: {str(e)}")
            return None

    def solve_behavioral_captcha(self, page):
        """Solve behavioral captcha by simulating human-like behavior."""
        try:
            # Random mouse movements
            for _ in range(3):
                x = random.randint(0, 800)
                y = random.randint(0, 600)
                page.mouse.move(x, y)
                time.sleep(random.uniform(0.1, 0.3))
            
            # Random scrolling
            for _ in range(2):
                page.mouse.wheel(0, random.randint(-100, 100))
                time.sleep(random.uniform(0.2, 0.4))
            
            # Random typing speed
            for char in string.ascii_letters:
                page.keyboard.type(char, delay=random.uniform(50, 150))
            
            return True
        except Exception as e:
            self.logger.error(f"Error in behavioral captcha solving: {str(e)}")
            return False 