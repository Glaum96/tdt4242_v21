import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime

# <---------- IMPORTANT --------->
# MUST HAVE FIREFOX, SELENIUM AND WEBDRIVER INSTALLED TO RUN THESE TESTS:
# pip install selenium
# pip install webdriver-manager

# Before running this test, remember to host the application on http://localhost:9090 using docker-compose up --build
# in the main project folder

# Test is run by: python seleniumFR5Test.py (when in the workouts-folder)
class AccessWorkoutTestCase(unittest.TestCase):

    # Creates two unique usernames to be used in the tests;
    # by appending the current exact time to the username, we will always have unique usernames
    uniqueUsername1 = "AccessWorkoutTestUser1-" + datetime.utcnow().strftime("%m-%d-%Y-%H-%M-%S.%f")
    uniqueUsername2 = "AccessWorkoutTestUser2-" + datetime.utcnow().strftime("%m-%d-%Y-%H-%M-%S.%f")
    uniqueUsername3 = "AccessWorkoutTestUser3-" + datetime.utcnow().strftime("%m-%d-%Y-%H-%M-%S.%f")
    coach_uniqueUsername = "AccessWorkoutTestUserCoach-" + datetime.utcnow().strftime("%m-%d-%Y-%H-%M-%S.%f")
    athlete_uniqueUsername = "AccessWorkoutTestUserAthlete-" + datetime.utcnow().strftime("%m-%d-%Y-%H-%M-%S.%f")


    # Runs before each test
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

        # Sets an implicit wait of 10 seconds (Test will wait for up to 10 seconds for an expected DOM element)
        self.driver.implicitly_wait(10)

    # Tests that a user can log in, create a private workout, then access it again and check if it is the users' own. Tests lastly if thw workout details, files and comments are available.
    def test_access_own_private_exercise(self):
        driver = self.driver

        # Opens the web browser, and logs out just in case someone was already logged in
        driver.get("http://localhost:9090/logout.html")

        # Finds and clicks the button in the main page that brings us to the register page
        registerButton = driver.find_element_by_id("btn-register")
        registerButton.click()

        # Finds all the input fields in the register form
        usernameField = driver.find_element_by_name('username')
        emailField = driver.find_element_by_name('email')
        passwordField = driver.find_element_by_name('password')
        repeatPasswordField = driver.find_element_by_name('password1')
        phoneNumberField = driver.find_element_by_name('phone_number')
        countryField = driver.find_element_by_name('country')
        cityField = driver.find_element_by_name('city')
        streetAddressField = driver.find_element_by_name('street_address')

        # Fetches the first unique username
        uniqueUsername1 = self.__class__.uniqueUsername1

        # Inputs values in all the registration fields
        usernameField.send_keys(uniqueUsername1)
        emailField.send_keys(uniqueUsername1+"@test.test")
        passwordField.send_keys("123")
        repeatPasswordField.send_keys("123")
        phoneNumberField.send_keys("12312312")
        countryField.send_keys("Norway")
        cityField.send_keys("Molde")
        streetAddressField.send_keys("Hovedgata")

        # Finds and clicks the button that creates the account
        createAccountButton = driver.find_element_by_id("btn-create-account")
        createAccountButton.click()

        # The "new workout" button sometimes doesn't registers clicks even though it has been loaded into the DOM.
        # Therefore, we wait 1 second before clicking it
        time.sleep(0.5)

        # Finds and clicks the button that opens the page for creating a new workout
        newWorkoutButton = driver.find_element_by_id("btn-create-workout")
        newWorkoutButton.click()

        # Input fields for a new workout
        workoutNameField = driver.find_element_by_id("inputName")
        workoutDateField = driver.find_element_by_id("inputDateTime")
        workoutNotesField = driver.find_element_by_id("inputNotes")
        workoutVisibilityField = driver.find_element_by_id("inputVisibility")

        # Waits until fields become editable
        time.sleep(0.5)

        # Inputs values into fields
        workoutNameField.send_keys("TestWorkout")
        workoutDateField.clear()
        workoutDateField.send_keys("1111-01-01 00:01")
        workoutNotesField.send_keys("This is an auto-generated workout meant for testing")
        workoutVisibilityField.send_keys("PR")

        time.sleep(0.5)

        # Finds and clicks the button that publishes the new workout
        publishWorkoutButton = driver.find_element_by_id("btn-ok-workout")
        publishWorkoutButton.click()

        time.sleep(0.5)

        # Scrolls to the bottom of the page; a 'problem' (due to dynamic loading) with not every workout being
        # loaded into the DOM appears when we have too many workouts. Scrolling to the bottom fixes this.
        self.scroll_down()
        time.sleep(0.5)

        # Finds and clicks the button that views the user's own workouts
        myWorkoutsButton = driver.find_element_by_id("list-my-workouts-list")
        myWorkoutsButton.click()
        time.sleep(0.5)

        # Finds and clicks the new workout
        workoutElement = driver.find_elements_by_css_selector("a.list-group-item")[-1]
        workoutElement.click()

        time.sleep(0.5)

        workoutOwnerField = driver.find_element_by_id("inputOwner")
        workoutOwner = workoutOwnerField.get_attribute("value")

        #Tests that the owner name of the newly created and accessed workout matches the one of the logged in user
        self.assertEqual(workoutOwner,uniqueUsername1)

        #Tests if all the page elements (workout details, files, and comments) are available on the page 
        self.assertTrue(self.check_workout_page_elements_exists())

    #Tests that a user can access someone else's public workout
    def test_access_not_own_public_exercise(self):
        driver = self.driver

        # Opens the web browser, and logs out just in case someone was already logged in
        driver.get("http://localhost:9090/logout.html")

        # Finds and clicks the button in the main page that brings us to the register page
        registerButton = driver.find_element_by_id("btn-register")
        registerButton.click()

        # Finds all the input fields in the register form
        usernameField = driver.find_element_by_name('username')
        emailField = driver.find_element_by_name('email')
        passwordField = driver.find_element_by_name('password')
        repeatPasswordField = driver.find_element_by_name('password1')
        phoneNumberField = driver.find_element_by_name('phone_number')
        countryField = driver.find_element_by_name('country')
        cityField = driver.find_element_by_name('city')
        streetAddressField = driver.find_element_by_name('street_address')

        # Fetches the first unique username
        uniqueUsername2 = self.__class__.uniqueUsername2

        # Inputs values in all the registration fields
        usernameField.send_keys(uniqueUsername2)
        emailField.send_keys(uniqueUsername2+"@test.test")
        passwordField.send_keys("123")
        repeatPasswordField.send_keys("123")
        phoneNumberField.send_keys("12312312")
        countryField.send_keys("Norway")
        cityField.send_keys("Molde")
        streetAddressField.send_keys("Hovedgata")

        # Finds and clicks the button that creates the account
        createAccountButton = driver.find_element_by_id("btn-create-account")
        createAccountButton.click()

        # The "new workout" button sometimes doesn't registers clicks even though it has been loaded into the DOM.
        # Therefore, we wait 1 second before clicking it
        time.sleep(0.5)

        # Finds and clicks the button that opens the page for creating a new workout
        newWorkoutButton = driver.find_element_by_id("btn-create-workout")
        newWorkoutButton.click()

        # Input fields for a new workout
        workoutNameField = driver.find_element_by_id("inputName")
        workoutDateField = driver.find_element_by_id("inputDateTime")
        workoutNotesField = driver.find_element_by_id("inputNotes")
        workoutVisibilityField = driver.find_element_by_id("inputVisibility")

        # Waits until fields become editable
        time.sleep(0.5)

        # Inputs values into fields
        workoutNameField.send_keys("TestWorkout")
        workoutDateField.clear()
        workoutDateField.send_keys("1111-01-01 00:01")
        workoutNotesField.send_keys("This is an auto-generated public workout meant for testing")
        workoutVisibilityField.send_keys("PU")

        time.sleep(0.5)

        # Finds and clicks the button that publishes the new workout
        publishWorkoutButton = driver.find_element_by_id("btn-ok-workout")
        publishWorkoutButton.click()

        time.sleep(0.5)


        #Logs the user out
        log_out_btn = driver.find_element_by_id("btn-logout")
        log_out_btn.click()

        time.sleep(0.5)

        #Registers a new user
        # Finds and clicks the button in the main page that brings us to the register page
        registerButton = driver.find_element_by_id("btn-register")
        registerButton.click()

        # Finds all the input fields in the register form
        usernameField = driver.find_element_by_name('username')
        emailField = driver.find_element_by_name('email')
        passwordField = driver.find_element_by_name('password')
        repeatPasswordField = driver.find_element_by_name('password1')
        phoneNumberField = driver.find_element_by_name('phone_number')
        countryField = driver.find_element_by_name('country')
        cityField = driver.find_element_by_name('city')
        streetAddressField = driver.find_element_by_name('street_address')

        # Fetches the first unique username
        uniqueUsername3 = self.__class__.uniqueUsername3

        # Inputs values in all the registration fields
        usernameField.send_keys(uniqueUsername3)
        emailField.send_keys(uniqueUsername3+"@test.test")
        passwordField.send_keys("123")
        repeatPasswordField.send_keys("123")
        phoneNumberField.send_keys("12312312")
        countryField.send_keys("Norway")
        cityField.send_keys("Oslo")
        streetAddressField.send_keys("Sideveien")

        # Finds and clicks the button that creates the account
        createAccountButton = driver.find_element_by_id("btn-create-account")
        createAccountButton.click()

        # The "new workout" button sometimes doesn't registers clicks even though it has been loaded into the DOM.
        # Therefore, we wait 1 second before clicking it
        time.sleep(0.5)

        # Scrolls to the bottom of the page; a 'problem' (due to dynamic loading) with not every workout being
        # loaded into the DOM appears when we have too many workouts. Scrolling to the bottom fixes this.
        self.scroll_down()
        time.sleep(0.5)

        # Finds and clicks the new workout
        workoutElement = driver.find_elements_by_css_selector("a.list-group-item")[-1]
        workoutElement.click()

        time.sleep(0.5)

        #Tests if all the page elements (workout details, files, and comments) are available on the page 
        self.assertTrue(self.check_workout_page_elements_exists())

    #Tests that a coac can access an athletes non-private workout
    def test_coach_can_access_athlete_workout(self):
        #This one's a little heavy, so here is a brief description of the flow:
        # 1. Athlete registers himself
        # 2. Athlete logs out
        # 3. Coach registers himself
        # 4. Coach sends coaching request to athlete
        # 5. Coach logs out
        # 6. Athlete logs in
        # 7. Athlete accepts the coaching request from the coach
        # 8. Athlete creates a workout with CO/Coach visibility
        # 9. Athlete logs out
        # 10. Coach logs in
        # 11. Coach accesses the created workout
        
        # --- 1 ---
        driver = self.driver

        # Opens the web browser, and logs out just in case someone was already logged in
        driver.get("http://localhost:9090/logout.html")

        # Finds and clicks the button in the main page that brings us to the register page
        registerButton = driver.find_element_by_id("btn-register")
        registerButton.click()

        # Finds all the input fields in the register form
        usernameField = driver.find_element_by_name('username')
        emailField = driver.find_element_by_name('email')
        passwordField = driver.find_element_by_name('password')
        repeatPasswordField = driver.find_element_by_name('password1')
        phoneNumberField = driver.find_element_by_name('phone_number')
        countryField = driver.find_element_by_name('country')
        cityField = driver.find_element_by_name('city')
        streetAddressField = driver.find_element_by_name('street_address')

        # Fetches the first unique username
        athlete_uniqueUsername = self.__class__.athlete_uniqueUsername

        # Inputs values in all the registration fields
        usernameField.send_keys(athlete_uniqueUsername)
        emailField.send_keys(athlete_uniqueUsername+"@test.test")
        passwordField.send_keys("123")
        repeatPasswordField.send_keys("123")
        phoneNumberField.send_keys("12312312")
        countryField.send_keys("Norway")
        cityField.send_keys("Molde")
        streetAddressField.send_keys("Hovedgata")

        # Finds and clicks the button that creates the account
        createAccountButton = driver.find_element_by_id("btn-create-account")
        createAccountButton.click()
        time.sleep(0.5)

        # --- 2 ---
        #Logs the user out
        log_out_btn = driver.find_element_by_id("btn-logout")
        log_out_btn.click()
        time.sleep(0.5)

        # --- 3 ---
        # Finds and clicks the button in the main page that brings us to the register page
        registerButton = driver.find_element_by_id("btn-register")
        registerButton.click()
        time.sleep(0.5)

        # Finds all the input fields in the register form
        usernameField = driver.find_element_by_name('username')
        emailField = driver.find_element_by_name('email')
        passwordField = driver.find_element_by_name('password')
        repeatPasswordField = driver.find_element_by_name('password1')
        phoneNumberField = driver.find_element_by_name('phone_number')
        countryField = driver.find_element_by_name('country')
        cityField = driver.find_element_by_name('city')
        streetAddressField = driver.find_element_by_name('street_address')

        # Fetches the first unique username
        coach_uniqueUsername = self.__class__.coach_uniqueUsername

        # Inputs values in all the registration fields
        usernameField.send_keys(coach_uniqueUsername)
        emailField.send_keys(coach_uniqueUsername+"@test.test")
        passwordField.send_keys("123")
        repeatPasswordField.send_keys("123")
        phoneNumberField.send_keys("12312312")
        countryField.send_keys("Norway")
        cityField.send_keys("Molde")
        streetAddressField.send_keys("Hovedgata")

        # Finds and clicks the button that creates the account
        createAccountButton = driver.find_element_by_id("btn-create-account")
        createAccountButton.click()
        time.sleep(0.5)

        # --- 4 ---
        #Presses the athlete button
        athleteButton = driver.find_element_by_id("nav-myathletes")
        athleteButton.click()
        time.sleep(0.5)

        #Inputs the athlete's name
        athleteNameInputField = driver.find_elements_by_css_selector("input.form-control")[-1]
        athleteNameInputField.click()
        athleteNameInputField.send_keys(athlete_uniqueUsername)

        #Presses submit
        submitRequestBtn = driver.find_element_by_id("button-submit-roster")
        submitRequestBtn.click()
        time.sleep(0.5)

        # --- 5 ---
        #Logs the user out
        log_out_btn = driver.find_element_by_id("btn-logout")
        log_out_btn.click()
        time.sleep(0.5)

        # --- 6 ---
        #Press the log in button
        log_in_btn = driver.find_element_by_id("btn-login-nav")
        log_in_btn.click()
        time.sleep(0.5)

        # Finds all the input fields in the register form
        usernameField = driver.find_element_by_name('username')
        passwordField = driver.find_element_by_name('password')

        # Inputs values in all the registration fields
        usernameField.send_keys(athlete_uniqueUsername)
        passwordField.send_keys("123")

        send_log_in_btn = driver.find_element_by_id("btn-login")
        send_log_in_btn.click()
        time.sleep(0.5)

        # --- 7 ---
        #Athletes navigates to the coach request arrival page
        coach_btn = driver.find_element_by_id("nav-mycoach")
        coach_btn.click()
        time.sleep(0.5)

        #Tries to click the accept button
        try:
            accept_btn = driver.find_elements_by_css_selector("button.btn.btn-success")[-1]
            accept_btn.click()
        except:
            self.assertTrue(False)
        time.sleep(0.5)

        # --- 8 ---
        #Athlete has now accpted the coach request and creates a workout
        #Clicks the workouts button in the nav bar
        workout_btn = driver.find_element_by_id("nav-workouts")
        workout_btn.click()
        time.sleep(0.5)

        # Finds and clicks the button that opens the page for creating a new workout
        newWorkoutButton = driver.find_element_by_id("btn-create-workout")
        newWorkoutButton.click()
        time.sleep(0.5)

        # Input fields for a new workout
        workoutNameField = driver.find_element_by_id("inputName")
        workoutDateField = driver.find_element_by_id("inputDateTime")
        workoutNotesField = driver.find_element_by_id("inputNotes")
        workoutVisibilityField = driver.find_element_by_id("inputVisibility")

        # Waits until fields become editable
        time.sleep(0.5)

        # Inputs values into fields
        workoutNameField.send_keys("TestWorkout")
        workoutDateField.clear()
        workoutDateField.send_keys("1111-01-01 00:01")
        workoutNotesField.send_keys("This is an auto-generated coach workout meant for testing")
        workoutVisibilityField.send_keys("CO")

        time.sleep(0.5)

        # Finds and clicks the button that publishes the new workout
        publishWorkoutButton = driver.find_element_by_id("btn-ok-workout")
        publishWorkoutButton.click()

        time.sleep(0.5)

        # --- 9 ---
        #Logs the user out
        log_out_btn = driver.find_element_by_id("btn-logout")
        log_out_btn.click()
        time.sleep(0.5)

        # --- 10 ---
        #Press the log in button
        log_in_btn = driver.find_element_by_id("btn-login-nav")
        log_in_btn.click()
        time.sleep(0.5)

        # Finds all the input fields in the register form
        usernameField = driver.find_element_by_name('username')
        passwordField = driver.find_element_by_name('password')

        # Inputs values in all the registration fields
        usernameField.send_keys(coach_uniqueUsername)
        passwordField.send_keys("123")

        send_log_in_btn = driver.find_element_by_id("btn-login")
        send_log_in_btn.click()
        time.sleep(0.5)

        # --- 11 ---
        self.scroll_down()

        # Finds and clicks the new workout
        workoutElement = driver.find_elements_by_css_selector("a.list-group-item")[-1]
        workoutElement.click()

        time.sleep(0.5)

        workoutOwnerField = driver.find_element_by_id("inputOwner")
        workoutOwner = workoutOwnerField.get_attribute("value")

        #Tests that the owner name of the newly created workout matches the athletes name
        self.assertEqual(workoutOwner, athlete_uniqueUsername)

        #Tests if all the page elements (workout details, files, and comments) are available on the page 
        self.assertTrue(self.check_workout_page_elements_exists())

    # *Not a test*, just a cleanup that deletes the workout that was created during the other tests. Tried using
    # tearDownClass, but that did not let me access the website
    def test_remove_created_workouts(self):
        usernames = [self.uniqueUsername1,self.uniqueUsername2,self.athlete_uniqueUsername]
        time.sleep(0.5)
        for name in usernames:
            driver = self.driver

            # Opens the web browser, and logs out just in case someone was already logged in
            driver.get("http://localhost:9090/logout.html")
            time.sleep(0.5)

            driver.get("http://localhost:9090/login.html")
            time.sleep(0.5)

            # Finds all the input fields in the register form
            usernameField = driver.find_element_by_name('username')
            passwordField = driver.find_element_by_name('password')

            # Inputs values in all the registration fields
            usernameField.send_keys(name)
            passwordField.send_keys("123")

            logInButton = driver.find_element_by_id("btn-login")
            logInButton.click()
            time.sleep(0.5)

            # Scrolls to the bottom of the page; a 'problem' (due to dynamic loading) with not every workout being
            # loaded into the DOM appears when we have too many workouts. Scrolling to the bottom fixes this.
            self.scroll_down()
            time.sleep(0.5)

            # Finds and clicks the button that views the user's own workouts
            myWorkoutsButton = driver.find_element_by_id("list-my-workouts-list")
            myWorkoutsButton.click()
            time.sleep(0.5)

            workout = driver.find_elements_by_css_selector("a.list-group-item")[-1]
            workout.click()
            time.sleep(0.5)

            editButton = driver.find_element_by_id("btn-edit-workout")
            editButton.click()
            time.sleep(0.5)

            deleteWorkoutButton = driver.find_element_by_id("btn-delete-workout")
            deleteWorkoutButton.click()
            time.sleep(0.5)


    # Runs after running the tests
    def tearDown(self):
        self.driver.close()

    # Code for scrolling to the end of a dynamically loading page;
    # from https://stackoverflow.com/questions/48850974/selenium-scroll-to-end-of-page-in-dynamically-loading-webpage
    def scroll_down(self):
        """A method for scrolling the page."""

        # Get scroll height.
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:

            # Scroll down to the bottom.
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load the page.
            time.sleep(0.5)

            # Calculate new scroll height and compare with last scroll height.
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height
    
    #Helper method
    def check_workout_page_elements_exists(self):
        #Tests if all the page elements (workout details, files, and comments) are available on the page        
        try:
            workoutNameField = self.driver.find_element_by_id("inputName")
            workoutDateField = self.driver.find_element_by_id("inputDateTime")
            workoutNotesField = self.driver.find_element_by_id("inputNotes")
            workoutVisibilityField = self.driver.find_element_by_id("inputVisibility")
            workoutFileField = self.driver.find_element_by_id("customFile")
            workoutCommentField = self.driver.find_elements_by_css_selector("div.card-header")[-1]
        except:
            return False  
        return True


if __name__ == "__main__":
    unittest.main()


