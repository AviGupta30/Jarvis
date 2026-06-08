import time
import threading
import re
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager

class DSAEnforcer:
    _instance = None

    def __init__(self):
        self.driver = None
        self.is_active = False
        self.num_questions = 0
        self.completed_questions = 0
        self.thread = None

    def start_mode(self, num_questions: int):
        if self.is_active:
            print("DSA Mode is already active.")
            return "DSA Mode is already active."

        self.num_questions = num_questions
        self.completed_questions = 0
        self.is_active = True

        print(f"Initializing Native DSA Environment for {num_questions} questions, Sir...")
        
        try:
            options = EdgeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            import os
            profile_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Jarvis_DSA_Profile")
            options.add_argument(f"user-data-dir={profile_dir}")
            
            # Launch Edge
            self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
            
            # Stealth: remove webdriver property
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            })
            
            # Direct to LeetCode
            self.driver.get("https://leetcode.com/problemset/all/")
            
            # Start background thread
            self.thread = threading.Thread(target=self._run_enforcement_loop, daemon=True)
            self.thread.start()
            
            return f"DSA mode activated for {num_questions} questions. A dedicated Edge browser has been launched. Good luck, Sir."
        except Exception as e:
            self.is_active = False
            error_msg = f"Failed to initialize Edge browser: {e}"
            print(error_msg)
            return error_msg

    def stop_mode(self):
        self.is_active = False
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            self.driver = None
        return "DSA Mode deactivated."

    def _get_problem_slug(self, url: str):
        match = re.search(r'leetcode\.com/problems/([^/]+)', url)
        return match.group(1) if match else None

    def _run_enforcement_loop(self):
        current_problem_slug = None
        start_time = 0
        problem_solved_flag = False

        while self.is_active:
            try:
                handles = self.driver.window_handles
                if not handles:
                    print("Browser closed by user. Terminating DSA Mode early.")
                    self.stop_mode()
                    break
                
                # Safely get current window handle, fallback to first handle if current was closed
                try:
                    curr = self.driver.current_window_handle
                except Exception:
                    self.driver.switch_to.window(handles[0])
                    curr = self.driver.current_window_handle

                if curr != handles[0]:
                    self.driver.switch_to.window(handles[0])

                current_url = self.driver.current_url
                slug = self._get_problem_slug(current_url)

                if slug:
                    # New problem detected
                    if slug != current_problem_slug:
                        print(f"Problem detected: {slug}. Starting master discipline clock.")
                        current_problem_slug = slug
                        start_time = time.time()
                        problem_solved_flag = False

                    if not problem_solved_flag:
                        elapsed_minutes = (time.time() - start_time) / 60

                        # Check if solved
                        is_solved = self._check_if_solved()
                        if is_solved:
                            problem_solved_flag = True
                            self.completed_questions += 1
                            print(f"Question solved! ({self.completed_questions}/{self.num_questions})")
                            
                            if self.completed_questions >= self.num_questions:
                                print("Target reached! Shutting down DSA mode.")
                                self.stop_mode()
                                break
                        else:
                            # PHASE 1: Hide tags for first 5 minutes
                            if elapsed_minutes < 5:
                                self._hide_tags()
                            else:
                                self._show_tags()

                            # PHASE 2: Lock hints for first 10 minutes
                            if elapsed_minutes < 10:
                                self._disable_hint_buttons()
                            else:
                                self._enable_hint_buttons()

                            # PHASE 3: Tab Lock down for first 30 minutes
                            if elapsed_minutes < 30:
                                self._monitor_tab_switching()
                else:
                    pass

                time.sleep(0.5)  # Very fast loop for strict tab and DOM enforcement
            except Exception as e:
                # E.g., window closed
                print(f"Browser closed or error encountered: {e}")
                self.stop_mode()
                break

    def _check_if_solved(self):
        # Natively inject JS to check for LeetCode's 'Accepted' text after submission
        script = """
        let accepted = false;
        // LeetCode's submission result typically uses specific data attributes or spans with 'Accepted'
        let elements = document.querySelectorAll('span[data-e2e-locator="submission-result"], span');
        for (let el of elements) {
            if (el.innerText && el.innerText.trim() === 'Accepted') {
                let color = window.getComputedStyle(el).color;
                if (color.includes('44, 181, 93') || color === 'rgb(44, 181, 93)') {
                    return true;
                }
            }
        }
        return false;
        """
        try:
            return self.driver.execute_script(script)
        except Exception:
            return False

    def _hide_tags(self):
        script = """
        let tags = document.querySelectorAll('a[href*="/tag/"]');
        for(let t of tags) { t.style.display = 'none'; }
        
        let allDivs = document.querySelectorAll('div, span');
        for(let el of allDivs) {
            let text = el.innerText ? el.innerText.trim() : '';
            if (text === 'Topics' || text === 'Related Topics' || text === 'Companies') {
                if (el.parentElement && el.parentElement.innerText.length < 300) {
                    el.parentElement.style.display = 'none';
                }
            }
        }
        """
        try:
            self.driver.execute_script(script)
        except Exception:
            pass

    def _show_tags(self):
        script = """
        let tags = document.querySelectorAll('a[href*="/tag/"]');
        for(let t of tags) { t.style.display = ''; }
        
        let allDivs = document.querySelectorAll('div, span');
        for(let el of allDivs) {
            let text = el.innerText ? el.innerText.trim() : '';
            if (text === 'Topics' || text === 'Related Topics' || text === 'Companies') {
                if (el.parentElement && el.parentElement.innerText.length < 300) {
                    el.parentElement.style.display = '';
                }
            }
        }
        """
        try:
            self.driver.execute_script(script)
        except Exception:
            pass

    def _disable_hint_buttons(self):
        script = """
        let els = document.querySelectorAll('div, a, span, button');
        for(let el of els) {
            let text = el.innerText ? el.innerText.trim() : '';
            if (text === 'Editorial' || text === 'Solutions' || text.startsWith('Hint')) {
                // To avoid breaking the whole page if a huge container matches
                if (text.length < 40) {
                    el.style.pointerEvents = 'none';
                    el.style.opacity = '0.2';
                    el.title = 'Locked by JARVIS';
                }
            }
        }
        """
        try:
            self.driver.execute_script(script)
        except Exception:
            pass

    def _enable_hint_buttons(self):
        script = """
        let els = document.querySelectorAll('div, a, span, button');
        for(let el of els) {
            if (el.title === 'Locked by JARVIS') {
                el.style.pointerEvents = '';
                el.style.opacity = '';
                el.title = '';
            }
        }
        """
        try:
            self.driver.execute_script(script)
        except Exception:
            pass

    def _monitor_tab_switching(self):
        try:
            handles = self.driver.window_handles
            if len(handles) > 1:
                print("Sir, unauthorized tab manipulation detected. Closing.")
                # Close all tabs except the first one
                for handle in handles[1:]:
                    try:
                        self.driver.switch_to.window(handle)
                        self.driver.close()
                    except Exception:
                        pass
                # Always safely switch back
                try:
                    self.driver.switch_to.window(self.driver.window_handles[0])
                except Exception:
                    pass
        except Exception:
            pass

# Global instance for easy access from tools.py
_global_dsa_enforcer = DSAEnforcer()

def get_dsa_enforcer():
    return _global_dsa_enforcer
