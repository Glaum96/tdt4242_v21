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

# Test is run by: python seleniumLeaderboardIntegrationTest.py (when in the workouts-folder)
class TestExerciseLeaderboard(unittest.TestCase):

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
    def test_is_on_leaderboard(self):
        driver = self.driver

        # Opens the web browser, and logs out just in case someone was already logged in
        driver.get("http://localhost:9090/logout.html")
        time.sleep(2)

        # Registers a new user
        self.registerUser(self.__class__.uniqueUsername1)

        # Find and clicks the button to go to the exercise page
        exerciseNavButton = driver.find_element_by_id("nav-exercises")
        exerciseNavButton.click()
        time.sleep(2)

        # Find and clicks the button to go the the "create new exercise" page
        createExerciseButton = driver.find_element_by_id("btn-create-exercise")
        createExerciseButton.click()
        time.sleep(2)

        # Finds the input fields
        exerciseNameField = driver.find_element_by_id("inputName")
        exerciseDescriptionField = driver.find_element_by_id("inputDescription")
        exerciseUnitField = driver.find_element_by_id("inputUnit")

        # Inputs values into the input fields
        exerciseNameField.send_keys("TestLeaderboardExercise")
        exerciseDescriptionField.send_keys("This exercise is only meant for testing purposes")
        exerciseUnitField.send_keys("Test")
        time.sleep(1)

        # Submits the new exerice
        submitExerciseButton = driver.find_element_by_id("btn-ok-exercise")
        submitExerciseButton.click()
        time.sleep(2)

        self.scroll_down()

        # Inspects the newest exercise
        exercise = driver.find_elements_by_css_selector("a.list-group-item")[-1]
        exercise.click()
        time.sleep(2)

        # All the rows in the leaderboard
        leaderboardRows = driver.find_elements_by_tag_name("tr")

        # Tests that the leaderboard has 2 rows; one is the header, and the other should be the user's entry
        self.assertEqual(2, len(leaderboardRows))

        print([ele.text for ele in leaderboardRows])

        leaderboard = []

        # Converts the text into a list of dictionaries for easy testing purposes
        for i in range(1, len(leaderboardRows)):
            row = leaderboardRows[i].text.split(" ")
            leaderboard.append({"rank": row[0], "username": row[1], "score": row[2]})

        # Tests that the rank is correct in the leaderboard
        self.assertEqual("1", leaderboard[0]["rank"])

        # Tests that the username is correct in the leaderboard
        self.assertEqual(self.__class__.uniqueUsername1, leaderboard[0]["username"])

        #Tests that the score is correct in the leaderboard
        self.assertEqual("0", leaderboard[0]["score"])

        time.sleep(100)


        # <---------Deletes the newest exercise-------->
        # Find and clicks the button to go to the exercise page
        exerciseNavButton = driver.find_element_by_id("nav-exercises")
        exerciseNavButton.click()
        time.sleep(2)

        self.scroll_down()

        # Inspects the newest exercise
        exerciseToDelete = driver.find_elements_by_css_selector("a.list-group-item")[-1]
        exerciseToDelete.click()
        time.sleep(2)

        # Starts editing the exercise
        editButton = driver.find_element_by_id("btn-edit-exercise")
        editButton.click()
        time.sleep(1)

        # Deletes the exercise
        deleteWorkoutButton = driver.find_element_by_id("btn-delete-exercise")
        deleteWorkoutButton.click()
        time.sleep(1)
        # >---------------------------<






    # Function used to register a new user
    def registerUser(self, uniqueUsername):

        print(uniqueUsername)
        driver = self.driver

        # Logs out, just in case a user is already logged in
        driver.get("http://localhost:9090/logout.html")
        time.sleep(2)

        # Goes to the register page
        driver.get("http://localhost:9090/register.html")
        time.sleep(2)

        # Finds all the input fields in the register form
        usernameField = driver.find_element_by_name('username')
        emailField = driver.find_element_by_name('email')
        passwordField = driver.find_element_by_name('password')
        repeatPasswordField = driver.find_element_by_name('password1')
        phoneNumberField = driver.find_element_by_name('phone_number')
        countryField = driver.find_element_by_name('country')
        cityField = driver.find_element_by_name('city')
        streetAddressField = driver.find_element_by_name('street_address')

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
        time.sleep(2)



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


