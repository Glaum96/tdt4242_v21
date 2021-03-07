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

# Test is run by: python seleniumLikeIntegrationTest.py (when in the workouts-folder and while website is live with docker)
class TestWorkoutLikes(unittest.TestCase):

    # Creates two unique usernames to be used in the tests;
    # by appending the current exact time to the username, we will always have unique usernames
    uniqueUsername1 = "LikeTestUser1-" + datetime.utcnow().strftime("%m-%d-%Y-%H-%M-%S.%f")
    uniqueUsername2 = "LikeTestUser2-" + datetime.utcnow().strftime("%m-%d-%Y-%H-%M-%S.%f")


    # Runs before each test
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

        # Sets an implicit wait of 10 seconds (Test will wait for up to 10 seconds for an expected DOM element)
        self.driver.implicitly_wait(10)

    # Tests that a user auto-likes his own workout
    def test_auto_liked_own_workout_and_only_one_like(self):
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
        uniqueUsername = self.__class__.uniqueUsername1

        # Inputs values in all the registration fields
        usernameField.send_keys(uniqueUsername)
        emailField.send_keys(uniqueUsername+"@test.test")
        passwordField.send_keys("123")
        repeatPasswordField.send_keys("123")
        phoneNumberField.send_keys("12312312")
        countryField.send_keys("Norway")
        cityField.send_keys("Narvik")
        streetAddressField.send_keys("Kvartslia")

        # Finds and clicks the button that creates the account
        createAccountButton = driver.find_element_by_id("btn-create-account")
        createAccountButton.click()

        # The "new workout" button sometimes doesn't registers clicks even though it has been loaded into the DOM.
        # Therefore, we wait 1 second before clicking it
        time.sleep(1)

        # Finds and clicks the button that opens the page for creating a new workout
        newWorkoutButton = driver.find_element_by_id("btn-create-workout")
        newWorkoutButton.click()

        # Input fields for a new workout
        workoutNameField = driver.find_element_by_id("inputName")
        workoutDateField = driver.find_element_by_id("inputDateTime")
        workoutNotesField = driver.find_element_by_id("inputNotes")

        # Waits until fields become editable
        time.sleep(2)

        # Inputs values into fields
        workoutNameField.send_keys("TestWorkout")
        workoutDateField.clear();
        workoutDateField.send_keys("1111-01-01 00:01");
        workoutNotesField.send_keys("This is an auto-generated workout meant for testing")

        time.sleep(1)

        # Finds and clicks the button that publishes the new workout
        publishWorkoutButton = driver.find_element_by_id("btn-ok-workout")
        publishWorkoutButton.click()

        time.sleep(2)

        # Scrolls to the bottom of the page; a 'problem' (due to dynamic loading) with not every workout being
        # loaded into the DOM appears when we have too many workouts. Scrolling to the bottom fixes this.
        self.scroll_down()
        time.sleep(1)

        # Finds and clicks the button that views the user's own workouts
        myWorkoutsButton = driver.find_element_by_id("list-my-workouts-list")
        myWorkoutsButton.click()
        time.sleep(2)

        # Finds the like button and the like amount of the newly-created workout
        likeButton = driver.find_elements_by_css_selector("a.like-button")[-1]
        likeNumber = driver.find_elements_by_css_selector("td.like-amount")[-1]

        # Tests that the newly-created workout has a like amount of 1 (auto-liked by the workout owner)
        self.assertEqual("1", likeNumber.text)

        # Tests that the like button is active (already liked by the owner)
        self.assertEqual("like-button active", likeButton.get_attribute("class"))

        # Tries to re-click the like button to unlike; this should not be possible
        try:
            likeButton.click()
            self.fail("Users should not be able to unlike after liking")

        except:
            pass

        # Changes the class of the like button so that it is no longer disabled,
        # so we can test that re-clicking an already-liked workout doesn't increment the like amount
        driver.execute_script("arguments[0].setAttribute('class','like-button')", likeButton)
        time.sleep(1)

        likeButton.click()
        time.sleep(2)

        # Gets the newest like number that is in the DOM
        likeNumber = driver.find_elements_by_css_selector("td.like-amount")[-1]

        # Tests that the newly-created workout still has a like amount of 1 (auto-liked by the workout owner)
        self.assertEqual("1", likeNumber.text)

        # Refresh the site so that we can be sure that we fetch the newest like amounts, and that the workout wasn't
        # actually re-liked by the owner (that no change happened in the database)
        driver.refresh()
        time.sleep(2)

        # Scrolls to the bottom of the page; a 'problem' (due to dynamic loading) with not every workout being
        # loaded into the DOM appears when we have too many workouts. Scrolling to the bottom fixes this.
        self.scroll_down()
        time.sleep(1)

        # Finds and clicks the button that views the user's own workouts
        myWorkoutsButton = driver.find_element_by_id("list-my-workouts-list")
        myWorkoutsButton.click()
        time.sleep(2)

        # Finds the like button and the like amount of the newly-created workout
        likeButton = driver.find_elements_by_css_selector("a.like-button")[-1]
        likeNumber = driver.find_elements_by_css_selector("td.like-amount")[-1]

        # We re-test that the newly-created workout still has a like amount of 1;
        # the like amount should not have incremented
        self.assertEqual("1", likeNumber.text)

        # Tests that the like button is still active (already liked by the owner)
        self.assertEqual("like-button active", likeButton.get_attribute("class"))

        time.sleep(1)


    # Tests that a user can like another user's public workout *once*
    def test_liked_by_other_user_and_only_one_like(self):
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
        uniqueUsername = self.__class__.uniqueUsername2

        # Inputs values in all the registration fields
        usernameField.send_keys(uniqueUsername)
        emailField.send_keys(uniqueUsername + "@test.test")
        passwordField.send_keys("123")
        repeatPasswordField.send_keys("123")
        phoneNumberField.send_keys("12312312")
        countryField.send_keys("Norway")
        cityField.send_keys("Narvik")
        streetAddressField.send_keys("Kvartslia")

        # Finds and clicks the button that creates the account
        createAccountButton = driver.find_element_by_id("btn-create-account")
        createAccountButton.click()

        time.sleep(1)

        # Scrolls to the bottom of the page; a 'problem' (due to dynamic loading) with not every workout being
        # loaded into the DOM appears when we have too many workouts. Scrolling to the bottom fixes this.
        self.scroll_down()
        time.sleep(1)

        # Finds the like button and the like amount of the newly-created workout
        likeButton = driver.find_elements_by_css_selector("a.like-button")[-1]
        likeNumber = driver.find_elements_by_css_selector("td.like-amount")[-1]

        # Tests that the newly-created workout has a like amount of 1 (auto-liked by the workout owner)
        self.assertEqual("1", likeNumber.text)

        # Tests that the like button is not active (not already liked)
        self.assertEqual("like-button", likeButton.get_attribute("class"))

        # Clicks the like button
        likeButton.click()
        time.sleep(2)

        # Gets the newest like number that is in the DOM
        likeNumber = driver.find_elements_by_css_selector("td.like-amount")[-1]

        # Tests that the newly-created workout now has a like amount of 2
        self.assertEqual("2", likeNumber.text)

        # Refresh the site so that we can be sure that we fetch the newest like amounts, and that the workout was
        # actually liked by the new user (that the change happened in the database as well)
        driver.refresh()
        time.sleep(2)

        # Scrolls to the bottom of the page; a 'problem' (due to dynamic loading) with not every workout being
        # loaded into the DOM appears when we have too many workouts. Scrolling to the bottom fixes this.
        self.scroll_down()
        time.sleep(1)

        # Finds the like button and the like amount of the newly-created workout
        likeButton = driver.find_elements_by_css_selector("a.like-button")[-1]
        likeNumber = driver.find_elements_by_css_selector("td.like-amount")[-1]

        # We re-test that the newly-created workout still has a like amount of 2;
        # the like amount should have incremented
        self.assertEqual("2", likeNumber.text)

        # Tests that the like button is still active (already liked)
        self.assertEqual("like-button active", likeButton.get_attribute("class"))
        time.sleep(1)

        # Tries to re-click the like button to unlike; this should not be possible
        try:
            likeButton.click()
            self.fail("Users should not be able to unlike after liking")

        except:
            pass

        # Changes the class of the like button so that it is no longer disabled,
        # so we can test that re-clicking an already-liked workout doesn't increment the like amount
        driver.execute_script("arguments[0].setAttribute('class','like-button')", likeButton)
        time.sleep(1)

        likeButton.click()
        time.sleep(2)

        # Gets the newest like number that is in the DOM
        likeNumber = driver.find_elements_by_css_selector("td.like-amount")[-1]

        # Tests that the newly-created workout still has a like amount of 2
        self.assertEqual("2", likeNumber.text)

        # Refresh the site so that we can be sure that we fetch the newest like amounts, and that the workout wasn't
        # actually re-liked by the owner (that the change happened in the database as well)
        driver.refresh()
        time.sleep(2)

        # Scrolls to the bottom of the page; a 'problem' (due to dynamic loading) with not every workout being
        # loaded into the DOM appears when we have too many workouts. Scrolling to the bottom fixes this.
        self.scroll_down()
        time.sleep(1)

        # Finds the like button and the like amount of the newly-created workout
        likeButton = driver.find_elements_by_css_selector("a.like-button")[-1]
        likeNumber = driver.find_elements_by_css_selector("td.like-amount")[-1]

        # We re-test that the newly-created workout still has a like amount of 2;
        # the like amount should not have incremented further
        self.assertEqual("2", likeNumber.text)

        # Tests that the like button is still active (already liked)
        self.assertEqual("like-button active", likeButton.get_attribute("class"))

        time.sleep(1)


    # *Not a test*, just a cleanup that deletes the workout that was created during the other tests. Tried using
    # tearDownClass, but that did not let me access the website
    def test_remove_created_workout(self):
        driver = self.driver

        # Opens the web browser, and logs out just in case someone was already logged in
        driver.get("http://localhost:9090/logout.html")
        time.sleep(2)

        driver.get("http://localhost:9090/login.html")
        time.sleep(2)

        # Finds all the input fields in the register form
        usernameField = driver.find_element_by_name('username')
        passwordField = driver.find_element_by_name('password')

        # Fetches the username for the user that created the workout
        uniqueUsername = self.__class__.uniqueUsername1

        # Inputs values in all the registration fields
        usernameField.send_keys(uniqueUsername)
        passwordField.send_keys("123")

        logInButton = driver.find_element_by_id("btn-login")
        logInButton.click()
        time.sleep(2)

        # Scrolls to the bottom of the page; a 'problem' (due to dynamic loading) with not every workout being
        # loaded into the DOM appears when we have too many workouts. Scrolling to the bottom fixes this.
        self.scroll_down()
        time.sleep(1)

        # Finds and clicks the button that views the user's own workouts
        myWorkoutsButton = driver.find_element_by_id("list-my-workouts-list")
        myWorkoutsButton.click()
        time.sleep(2)

        workout = driver.find_elements_by_css_selector("a.list-group-item")[-1]
        workout.click()
        time.sleep(2)

        editButton = driver.find_element_by_id("btn-edit-workout")
        editButton.click()
        time.sleep(1)

        deleteWorkoutButton = driver.find_element_by_id("btn-delete-workout")
        deleteWorkoutButton.click()
        time.sleep(1)


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
            time.sleep(2)

            # Calculate new scroll height and compare with last scroll height.
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height


if __name__ == "__main__":
    unittest.main()


