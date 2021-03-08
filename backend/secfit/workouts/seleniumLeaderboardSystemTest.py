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

# Test is run by: python seleniumLeaderboardSystemTest.py (when in the workouts-folder)
class TestExerciseLeaderboard(unittest.TestCase):

    # Creates 6 unique usernames to be used in the tests;
    # by appending the current exact time to the username, we will always have unique usernames
    uniqueUsername1 = "LikeTestUser1-" + datetime.utcnow().strftime("%m-%d-%Y-%H-%M-%S.%f")
    uniqueUsername2 = "LikeTestUser2-" + datetime.utcnow().strftime("%m-%d-%Y-%H-%M-%S.%f")
    uniqueUsername3 = "LikeTestUser3-" + datetime.utcnow().strftime("%m-%d-%Y-%H-%M-%S.%f")
    uniqueUsername4 = "LikeTestUser4-" + datetime.utcnow().strftime("%m-%d-%Y-%H-%M-%S.%f")
    uniqueUsername5 = "LikeTestUser5-" + datetime.utcnow().strftime("%m-%d-%Y-%H-%M-%S.%f")
    uniqueUsername6 = "LikeTestUser6-" + datetime.utcnow().strftime("%m-%d-%Y-%H-%M-%S.%f")

    # Unique exercise name to be used in the tests
    uniqueExercise = "Exercise-" + datetime.utcnow().strftime("%m-%d-%Y-%H-%M-%S.%f")

    # Simple password for test users
    userPassword = "ABCD1234"


    # Runs before each test
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

        # Sets an implicit wait of 10 seconds (Test will wait for up to 10 seconds for an expected DOM element)
        self.driver.implicitly_wait(10)

        self.driver.get("http://localhost:9090")
        time.sleep(1)


    # Tests that a user is alone on the leaderboard when the user does not have any workouts,
    # and that the leaderboard is correct in regard to size, rank, entrants and score.
    def test01_is_on_leaderboard_without_workout(self):
        driver = self.driver

        # Registers a new user
        self.register_user(self.__class__.uniqueUsername1)

        # Find and clicks the button to go to the exercise page
        exerciseNavButton = driver.find_element_by_id("nav-exercises")
        exerciseNavButton.click()
        time.sleep(1)

        # Find and clicks the button to go the the "create new exercise" page
        createExerciseButton = driver.find_element_by_id("btn-create-exercise")
        createExerciseButton.click()
        time.sleep(1)

        # Finds the input fields
        exerciseNameField = driver.find_element_by_id("inputName")
        exerciseDescriptionField = driver.find_element_by_id("inputDescription")
        exerciseUnitField = driver.find_element_by_id("inputUnit")

        # Inputs values into the input fields
        exerciseNameField.send_keys(self.__class__.uniqueExercise)
        exerciseDescriptionField.send_keys("This exercise is only meant for testing purposes")
        exerciseUnitField.send_keys("Test")
        time.sleep(1)

        # Submits the new exerice
        submitExerciseButton = driver.find_element_by_id("btn-ok-exercise")
        submitExerciseButton.click()
        time.sleep(1)

        # What we expect the leaderboard to be like now
        expected_leaderboard = [{"rank": "1", "username": self.__class__.uniqueUsername1, "score": "0"}]

        # Asserts that the observed leaderboard matches the expected leaderboard
        self.assert_leaderboard(expected_leaderboard)


    # Tests that when the user posts a workout with the exercise, the score is incremented accordingly,
    # in addition to the leaderboard being correct in regard to size, rank and entrants.
    def test02_workout_increase_leaderboard_score(self):
        driver = self.driver

        # Logs in user 1
        self.login_user(self.__class__.uniqueUsername1)

        # Registers a new workout with the newly created exercise, and sets-parameter as input for the workout
        self.register_workout_with_exercise("5")

        # What we expect the leaderboard to be like now
        expected_leaderboard = [{"rank": "1", "username": self.__class__.uniqueUsername1, "score": "50"}]

        # Asserts that the observed leaderboard matches the expected leaderboard
        self.assert_leaderboard(expected_leaderboard)


    # Tests that another user is on the leaderboard together with the first user, even without having any workouts
    # (Tests that the leaderboard is correct in regard to size, rank, score and entrants.)
    def test03_another_user_on_leaderboard_without_workout(self):
        driver = self.driver

        # Registers another new user
        self.register_user(self.__class__.uniqueUsername2)

        # What we expect the leaderboard to be like now
        expected_leaderboard = [
            {"rank": "1", "username": self.__class__.uniqueUsername1, "score": "50"},
            {"rank": "2", "username": self.__class__.uniqueUsername2, "score": "0"},
        ]

        # Asserts that the observed leaderboard matches the expected leaderboard
        self.assert_leaderboard(expected_leaderboard)


    # Tests that the leaderboard is correct in regard to size, rank, score and entrants when:
    #   1 - User 2 post a workout that should increase their score to 20
    #   2 - User 2 posts *another* workout that should accumulate their exercise score to 50; the same as user 1
    #   3 - User 2 posts *yet another* workout that should accumulate their exercise score to 70, and surpass user 1
    def test04_multiple_workouts_accumulates_for_user(self):
        driver = self.driver

        # Logs in user 2
        self.login_user(self.__class__.uniqueUsername2)

        # Registers a new workout with the newly created exercise, and sets-parameter as input for the workout
        self.register_workout_with_exercise("2")

        # What we expect the leaderboard to be like
        expected_leaderboard = [
            {"rank": "1", "username": self.__class__.uniqueUsername1, "score": "50"},
            {"rank": "2", "username": self.__class__.uniqueUsername2, "score": "20"},
        ]

        # Asserts that the observed leaderboard matches the expected leaderboard
        self.assert_leaderboard(expected_leaderboard)

        # Registers a new workout with the newly created exercise, and sets-parameter as input for the workout
        self.register_workout_with_exercise("3")

        # What we expect the leaderboard to be like
        expected_leaderboard = [
            {"rank": "1", "username": self.__class__.uniqueUsername1, "score": "50"},
            {"rank": "1", "username": self.__class__.uniqueUsername2, "score": "50"},
        ]

        # Asserts that the observed leaderboard matches the expected leaderboard
        self.assert_leaderboard(expected_leaderboard)

        # Registers a new workout with the newly created exercise, and sets-parameter as input for the workout
        self.register_workout_with_exercise("2")

        # What we expect the leaderboard to be like
        expected_leaderboard = [
            {"rank": "1", "username": self.__class__.uniqueUsername2, "score": "70"},
            {"rank": "2", "username": self.__class__.uniqueUsername1, "score": "50"},
        ]

        # Asserts that the observed leaderboard matches the expected leaderboard
        self.assert_leaderboard(expected_leaderboard)


    # Tests that the leaderboard only show the top 5 entrants when the logged in user is in the top 5, even though
    # there are more than 5 entrants total.
    # (Tests that the leaderboard is correct in regard to size, rank, score and entrants when number of entrants
    # surpass 5)
    def test05_max_5_leaderboard_entrants_when_user_in_top_5_and_max_6_when_not_in_top_5(self):
        driver = self.driver

        # Registers another new user
        self.register_user(self.__class__.uniqueUsername3)

        # What we expect the leaderboard to be like
        expected_leaderboard = [
            {"rank": "1", "username": self.__class__.uniqueUsername2, "score": "70"},
            {"rank": "2", "username": self.__class__.uniqueUsername1, "score": "50"},
            {"rank": "3", "username": self.__class__.uniqueUsername3, "score": "0"},
        ]

        # Asserts that the observed leaderboard matches the expected leaderboard
        self.assert_leaderboard(expected_leaderboard)

        # Registers a new workout with the newly created exercise, and sets-parameter as input for the workout
        self.register_workout_with_exercise("6")

        # What we expect the leaderboard to be like
        expected_leaderboard = [
            {"rank": "1", "username": self.__class__.uniqueUsername2, "score": "70"},
            {"rank": "2", "username": self.__class__.uniqueUsername3, "score": "60"},
            {"rank": "3", "username": self.__class__.uniqueUsername1, "score": "50"},
        ]

        # Asserts that the observed leaderboard matches the expected leaderboard
        self.assert_leaderboard(expected_leaderboard)

        # Registers another new user
        self.register_user(self.__class__.uniqueUsername4)

        # What we expect the leaderboard to be like
        expected_leaderboard = [
            {"rank": "1", "username": self.__class__.uniqueUsername2, "score": "70"},
            {"rank": "2", "username": self.__class__.uniqueUsername3, "score": "60"},
            {"rank": "3", "username": self.__class__.uniqueUsername1, "score": "50"},
            {"rank": "4", "username": self.__class__.uniqueUsername4, "score": "0"},
        ]

        # Asserts that the observed leaderboard matches the expected leaderboard
        self.assert_leaderboard(expected_leaderboard)

        # Registers a new workout with the newly created exercise, and sets-parameter as input for the workout
        self.register_workout_with_exercise("10")

        # What we expect the leaderboard to be like
        expected_leaderboard = [
            {"rank": "1", "username": self.__class__.uniqueUsername4, "score": "100"},
            {"rank": "2", "username": self.__class__.uniqueUsername2, "score": "70"},
            {"rank": "3", "username": self.__class__.uniqueUsername3, "score": "60"},
            {"rank": "4", "username": self.__class__.uniqueUsername1, "score": "50"},
        ]

        # Asserts that the observed leaderboard matches the expected leaderboard
        self.assert_leaderboard(expected_leaderboard)

        # Registers another new user
        self.register_user(self.__class__.uniqueUsername5)

        # What we expect the leaderboard to be like
        expected_leaderboard = [
            {"rank": "1", "username": self.__class__.uniqueUsername4, "score": "100"},
            {"rank": "2", "username": self.__class__.uniqueUsername2, "score": "70"},
            {"rank": "3", "username": self.__class__.uniqueUsername3, "score": "60"},
            {"rank": "4", "username": self.__class__.uniqueUsername1, "score": "50"},
            {"rank": "5", "username": self.__class__.uniqueUsername5, "score": "0"},
        ]

        # Asserts that the observed leaderboard matches the expected leaderboard
        self.assert_leaderboard(expected_leaderboard)

        # Registers a new workout with the newly created exercise, and sets-parameter as input for the workout
        self.register_workout_with_exercise("1")

        # What we expect the leaderboard to be like
        expected_leaderboard = [
            {"rank": "1", "username": self.__class__.uniqueUsername4, "score": "100"},
            {"rank": "2", "username": self.__class__.uniqueUsername2, "score": "70"},
            {"rank": "3", "username": self.__class__.uniqueUsername3, "score": "60"},
            {"rank": "4", "username": self.__class__.uniqueUsername1, "score": "50"},
            {"rank": "5", "username": self.__class__.uniqueUsername5, "score": "10"},
        ]

        # Asserts that the observed leaderboard matches the expected leaderboard
        self.assert_leaderboard(expected_leaderboard)

        # Registers another new user
        self.register_user(self.__class__.uniqueUsername6)

        # What we expect the leaderboard to be like
        expected_leaderboard = [
            {"rank": "1", "username": self.__class__.uniqueUsername4, "score": "100"},
            {"rank": "2", "username": self.__class__.uniqueUsername2, "score": "70"},
            {"rank": "3", "username": self.__class__.uniqueUsername3, "score": "60"},
            {"rank": "4", "username": self.__class__.uniqueUsername1, "score": "50"},
            {"rank": "5", "username": self.__class__.uniqueUsername5, "score": "10"},
            {"rank": "6", "username": self.__class__.uniqueUsername6, "score": "0"},
        ]

        # Asserts that the observed leaderboard matches the expected leaderboard
        # HERE WE TEST THAT WHEN USER IS NOT IN TOP 5, THE MAX LEADERBOARD SIZE IS 6 ENTRANTS
        self.assert_leaderboard(expected_leaderboard)

        # Registers a new workout with the newly created exercise, and sets-parameter as input for the workout
        self.register_workout_with_exercise("8")

        # What we expect the leaderboard to be like
        expected_leaderboard = [
            {"rank": "1", "username": self.__class__.uniqueUsername4, "score": "100"},
            {"rank": "2", "username": self.__class__.uniqueUsername6, "score": "80"},
            {"rank": "3", "username": self.__class__.uniqueUsername2, "score": "70"},
            {"rank": "4", "username": self.__class__.uniqueUsername3, "score": "60"},
            {"rank": "5", "username": self.__class__.uniqueUsername1, "score": "50"},
        ]

        # Asserts that the observed leaderboard matches the expected leaderboard
        # HERE WE TEST THAT WHEN USER IS IN TOP 5, THE MAX LEADERBOARD SIZE IS 5 ENTRANTS
        self.assert_leaderboard(expected_leaderboard)


    # Tests that when the user deletes a workout that has the exercise, the score is decremented accordingly,
    # (the leaderboard should be correct in regard to size, rank and entrants.)
    def test06_deleted_workouts_decrement_leaderboard_score(self):
        driver = self.driver

        # Logs in user 6
        self.login_user(self.__class__.uniqueUsername6)

        # Deletes user 6's workout
        self.delete_all_user_workouts(self.__class__.uniqueUsername6)

        # What we expect the leaderboard to be like
        expected_leaderboard = [
            {"rank": "1", "username": self.__class__.uniqueUsername4, "score": "100"},
            {"rank": "2", "username": self.__class__.uniqueUsername2, "score": "70"},
            {"rank": "3", "username": self.__class__.uniqueUsername3, "score": "60"},
            {"rank": "4", "username": self.__class__.uniqueUsername1, "score": "50"},
            {"rank": "5", "username": self.__class__.uniqueUsername5, "score": "10"},
            {"rank": "6", "username": self.__class__.uniqueUsername6, "score": "0"},
        ]

        # Asserts that the observed leaderboard matches the expected leaderboard
        self.assert_leaderboard(expected_leaderboard)

    # Tests that when the user makes a public workout into a private workout, the score is decremented accordingly,
    # (the leaderboard should be correct in regard to size, rank and entrants.)
    def test07_public_workouts_made_private_decrement_leaderboard_score(self):
        driver = self.driver

        # Logs in user 5
        self.login_user(self.__class__.uniqueUsername5)

        self.scroll_down()

        # Finds and clicks the button that views the user's own workouts
        myWorkoutsButton = driver.find_element_by_id("list-my-workouts-list")
        myWorkoutsButton.click()
        time.sleep(1)

        # Views the workout
        workout = driver.find_elements_by_css_selector("a.list-group-item")[-1]
        workout.click()
        time.sleep(1)

        # Edits the workout
        editButton = driver.find_element_by_id("btn-edit-workout")
        editButton.click()
        time.sleep(1)

        # Changes the visiblity to private
        workoutVisibilityField = driver.find_element_by_id("inputVisibility")
        workoutVisibilityField.send_keys("PR")

        saveEditChangesButton = driver.find_element_by_id("btn-ok-workout")
        saveEditChangesButton.click()
        time.sleep(1)

        # What we expect the leaderboard to be like
        expected_leaderboard = [
            {"rank": "1", "username": self.__class__.uniqueUsername4, "score": "100"},
            {"rank": "2", "username": self.__class__.uniqueUsername2, "score": "70"},
            {"rank": "3", "username": self.__class__.uniqueUsername3, "score": "60"},
            {"rank": "4", "username": self.__class__.uniqueUsername1, "score": "50"},
            {"rank": "5", "username": self.__class__.uniqueUsername5, "score": "0"},
        ]

        # Asserts that the observed leaderboard matches the expected leaderboard
        self.assert_leaderboard(expected_leaderboard)


    # Tests that when the user changes the visibility of a public workout to "coach", the score is decremented accordingly,
    # (the leaderboard should be correct in regard to size, rank and entrants.)
    def test08_public_workouts_made_coach_decrement_leaderboard_score(self):
        driver = self.driver

        # Logs in user 4
        self.login_user(self.__class__.uniqueUsername4)

        self.scroll_down()

        # Finds and clicks the button that views the user's own workouts
        myWorkoutsButton = driver.find_element_by_id("list-my-workouts-list")
        myWorkoutsButton.click()
        time.sleep(1)

        # Views the workout
        workout = driver.find_elements_by_css_selector("a.list-group-item")[-1]
        workout.click()
        time.sleep(1)

        # Edits the workout
        editButton = driver.find_element_by_id("btn-edit-workout")
        editButton.click()
        time.sleep(1)

        # Changes the visiblity to coach
        workoutVisibilityField = driver.find_element_by_id("inputVisibility")
        workoutVisibilityField.send_keys("CO")

        saveEditChangesButton = driver.find_element_by_id("btn-ok-workout")
        saveEditChangesButton.click()
        time.sleep(1)

        # What we expect the leaderboard to be like
        expected_leaderboard = [
            {"rank": "1", "username": self.__class__.uniqueUsername2, "score": "70"},
            {"rank": "2", "username": self.__class__.uniqueUsername3, "score": "60"},
            {"rank": "3", "username": self.__class__.uniqueUsername1, "score": "50"},
            {"rank": "4", "username": self.__class__.uniqueUsername4, "score": "0"},
        ]

        # Asserts that the observed leaderboard matches the expected leaderboard
        self.assert_leaderboard(expected_leaderboard)


    # Tests that when the several users have the same score they also have the same rank,
    # (the leaderboard should be correct in regard to size, rank and entrants.)
    def test09_same_score_is_same_rank(self):
        driver = self.driver

        # Deletes user 5's workout
        self.delete_all_user_workouts(self.__class__.uniqueUsername5)

        # Creates a new workout
        self.register_workout_with_exercise("6")

        # What we expect the leaderboard to be like now
        expected_leaderboard = [
            {"rank": "1", "username": self.__class__.uniqueUsername2, "score": "70"},
            {"rank": "2", "username": self.__class__.uniqueUsername3, "score": "60"},
            {"rank": "2", "username": self.__class__.uniqueUsername5, "score": "60"},
            {"rank": "4", "username": self.__class__.uniqueUsername1, "score": "50"},
        ]

        # Asserts that the observed leaderboard matches the expected leaderboard
        self.assert_leaderboard(expected_leaderboard)

        # Logs in user 6
        self.login_user(self.__class__.uniqueUsername6)

        # Creates a new workout with the same score as user 3 and 5
        self.register_workout_with_exercise("6")

        # What we expect the leaderboard to be like now
        expected_leaderboard = [
            {"rank": "1", "username": self.__class__.uniqueUsername2, "score": "70"},
            {"rank": "2", "username": self.__class__.uniqueUsername3, "score": "60"},
            {"rank": "2", "username": self.__class__.uniqueUsername5, "score": "60"},
            {"rank": "2", "username": self.__class__.uniqueUsername6, "score": "60"},
            {"rank": "5", "username": self.__class__.uniqueUsername1, "score": "50"},
        ]

        # Asserts that the observed leaderboard matches the expected leaderboard
        self.assert_leaderboard(expected_leaderboard)


    # Tests that when the user changes the visibility of a private workout to "public", the score is incremented accordingly,
    # (the leaderboard should be correct in regard to size, rank and entrants.)
    def test10_test_private_workout_made_public_increments_score(self):
        driver = self.driver

        # Logs in user 6
        self.login_user(self.__class__.uniqueUsername6)

        # Creates a new workout
        self.register_workout_with_exercise("2")

        # What we expect the leaderboard to be like now
        expected_leaderboard = [
            {"rank": "1", "username": self.__class__.uniqueUsername6, "score": "80"},
            {"rank": "2", "username": self.__class__.uniqueUsername2, "score": "70"},
            {"rank": "3", "username": self.__class__.uniqueUsername3, "score": "60"},
            {"rank": "3", "username": self.__class__.uniqueUsername5, "score": "60"},
            {"rank": "5", "username": self.__class__.uniqueUsername1, "score": "50"},
        ]

        # Asserts that the observed leaderboard matches the expected leaderboard
        self.assert_leaderboard(expected_leaderboard)

        # Find and clicks the button to go to the workouts page
        workoutNavButton = driver.find_element_by_id("nav-workouts")
        workoutNavButton.click()
        time.sleep(0.5)

        self.scroll_down()

        # Finds and clicks the button that views the user's own workouts
        myWorkoutsButton = driver.find_element_by_id("list-my-workouts-list")
        myWorkoutsButton.click()
        time.sleep(1)

        # Views the workout
        workout = driver.find_elements_by_css_selector("a.list-group-item")[-1]
        workout.click()
        time.sleep(1)

        # Edits the workout
        editButton = driver.find_element_by_id("btn-edit-workout")
        editButton.click()
        time.sleep(1)

        # Changes the visiblity to private
        workoutVisibilityField = driver.find_element_by_id("inputVisibility")
        workoutVisibilityField.send_keys("PR")
        saveEditChangesButton = driver.find_element_by_id("btn-ok-workout")
        saveEditChangesButton.click()
        time.sleep(1)

        # What we expect the leaderboard to be like now
        expected_leaderboard = [
            {"rank": "1", "username": self.__class__.uniqueUsername2, "score": "70"},
            {"rank": "2", "username": self.__class__.uniqueUsername3, "score": "60"},
            {"rank": "2", "username": self.__class__.uniqueUsername5, "score": "60"},
            {"rank": "2", "username": self.__class__.uniqueUsername6, "score": "60"},
            {"rank": "5", "username": self.__class__.uniqueUsername1, "score": "50"},
        ]

        # Asserts that the observed leaderboard matches the expected leaderboard
        self.assert_leaderboard(expected_leaderboard)

        # Find and clicks the button to go to the workouts page
        workoutNavButton = driver.find_element_by_id("nav-workouts")
        workoutNavButton.click()
        time.sleep(0.5)

        self.scroll_down()

        # Finds and clicks the button that views the user's own workouts
        myWorkoutsButton = driver.find_element_by_id("list-my-workouts-list")
        myWorkoutsButton.click()
        time.sleep(1)

        # Views the workout
        workout = driver.find_elements_by_css_selector("a.list-group-item")[-1]
        workout.click()
        time.sleep(1)

        # Edits the workout
        editButton = driver.find_element_by_id("btn-edit-workout")
        editButton.click()
        time.sleep(1)

        # Changes the visiblity to public
        workoutVisibilityField = driver.find_element_by_id("inputVisibility")
        workoutVisibilityField.send_keys("PU")
        saveEditChangesButton = driver.find_element_by_id("btn-ok-workout")
        saveEditChangesButton.click()
        time.sleep(1)

        # What we expect the leaderboard to be like now
        expected_leaderboard = [
            {"rank": "1", "username": self.__class__.uniqueUsername6, "score": "80"},
            {"rank": "2", "username": self.__class__.uniqueUsername2, "score": "70"},
            {"rank": "3", "username": self.__class__.uniqueUsername3, "score": "60"},
            {"rank": "3", "username": self.__class__.uniqueUsername5, "score": "60"},
            {"rank": "5", "username": self.__class__.uniqueUsername1, "score": "50"},
        ]

        # Asserts that the observed leaderboard matches the expected leaderboard
        self.assert_leaderboard(expected_leaderboard)


    # Tests that when the user changes the visibility of a coach workout to "public", the score is incremented accordingly,
    # (the leaderboard should be correct in regard to size, rank and entrants.)
    def test11_test_coach_workout_made_public_increments_score(self):
        driver = self.driver

        # Logs in user 6
        self.login_user(self.__class__.uniqueUsername6)

        # Creates a new workout
        self.register_workout_with_exercise("4")

        # What we expect the leaderboard to be like now
        expected_leaderboard = [
            {"rank": "1", "username": self.__class__.uniqueUsername6, "score": "120"},
            {"rank": "2", "username": self.__class__.uniqueUsername2, "score": "70"},
            {"rank": "3", "username": self.__class__.uniqueUsername3, "score": "60"},
            {"rank": "3", "username": self.__class__.uniqueUsername5, "score": "60"},
            {"rank": "5", "username": self.__class__.uniqueUsername1, "score": "50"},
        ]

        # Asserts that the observed leaderboard matches the expected leaderboard
        self.assert_leaderboard(expected_leaderboard)

        # Find and clicks the button to go to the workouts page
        workoutNavButton = driver.find_element_by_id("nav-workouts")
        workoutNavButton.click()
        time.sleep(0.5)

        self.scroll_down()

        # Finds and clicks the button that views the user's own workouts
        myWorkoutsButton = driver.find_element_by_id("list-my-workouts-list")
        myWorkoutsButton.click()
        time.sleep(1)

        # Views the workout
        workout = driver.find_elements_by_css_selector("a.list-group-item")[-1]
        workout.click()
        time.sleep(1)

        # Edits the workout
        editButton = driver.find_element_by_id("btn-edit-workout")
        editButton.click()
        time.sleep(1)

        # Changes the visiblity to private
        workoutVisibilityField = driver.find_element_by_id("inputVisibility")
        workoutVisibilityField.send_keys("CO")
        saveEditChangesButton = driver.find_element_by_id("btn-ok-workout")
        saveEditChangesButton.click()
        time.sleep(1)

        # What we expect the leaderboard to be like now
        expected_leaderboard = [
            {"rank": "1", "username": self.__class__.uniqueUsername6, "score": "80"},
            {"rank": "2", "username": self.__class__.uniqueUsername2, "score": "70"},
            {"rank": "3", "username": self.__class__.uniqueUsername3, "score": "60"},
            {"rank": "3", "username": self.__class__.uniqueUsername5, "score": "60"},
            {"rank": "5", "username": self.__class__.uniqueUsername1, "score": "50"},
        ]

        # Asserts that the observed leaderboard matches the expected leaderboard
        self.assert_leaderboard(expected_leaderboard)

        # Find and clicks the button to go to the workouts page
        workoutNavButton = driver.find_element_by_id("nav-workouts")
        workoutNavButton.click()
        time.sleep(0.5)

        self.scroll_down()

        # Finds and clicks the button that views the user's own workouts
        myWorkoutsButton = driver.find_element_by_id("list-my-workouts-list")
        myWorkoutsButton.click()
        time.sleep(1)

        # Views the workout
        workout = driver.find_elements_by_css_selector("a.list-group-item")[-1]
        workout.click()
        time.sleep(1)

        # Edits the workout
        editButton = driver.find_element_by_id("btn-edit-workout")
        editButton.click()
        time.sleep(1)

        # Changes the visiblity to public
        workoutVisibilityField = driver.find_element_by_id("inputVisibility")
        workoutVisibilityField.send_keys("PU")
        saveEditChangesButton = driver.find_element_by_id("btn-ok-workout")
        saveEditChangesButton.click()
        time.sleep(1)

        # What we expect the leaderboard to be like now
        expected_leaderboard = [
            {"rank": "1", "username": self.__class__.uniqueUsername6, "score": "120"},
            {"rank": "2", "username": self.__class__.uniqueUsername2, "score": "70"},
            {"rank": "3", "username": self.__class__.uniqueUsername3, "score": "60"},
            {"rank": "3", "username": self.__class__.uniqueUsername5, "score": "60"},
            {"rank": "5", "username": self.__class__.uniqueUsername1, "score": "50"},
        ]

        # Asserts that the observed leaderboard matches the expected leaderboard
        self.assert_leaderboard(expected_leaderboard)





    # *Not a test*, just a cleanup that deletes the workout that was created during the other tests. Tried using
    # tearDownClass, but that did not let me access the website
    def test99_cleanup(self):
        driver = self.driver

        # Logs in user 1
        self.login_user(self.__class__.uniqueUsername1)

        # <---------Deletes the test exercise-------->
        # Find and clicks the button to go to the exercise page
        exerciseNavButton = driver.find_element_by_id("nav-exercises")
        exerciseNavButton.click()
        time.sleep(0.5)

        self.scroll_down()

        # Inspects the newest exercise
        exerciseToDelete = driver.find_elements_by_css_selector("a.list-group-item")[-1]
        exerciseToDelete.click()
        time.sleep(1)

        # Starts editing the exercise
        editButton = driver.find_element_by_id("btn-edit-exercise")
        editButton.click()
        time.sleep(0.5)

        # Deletes the exercise
        deleteWorkoutButton = driver.find_element_by_id("btn-delete-exercise")
        deleteWorkoutButton.click()
        time.sleep(0.5)
        # >------------------------------------------<

        # Deletes all the workouts that were created during the testing
        self.delete_all_user_workouts(self.__class__.uniqueUsername6)
        self.delete_all_user_workouts(self.__class__.uniqueUsername5)
        self.delete_all_user_workouts(self.__class__.uniqueUsername4)
        self.delete_all_user_workouts(self.__class__.uniqueUsername3)
        self.delete_all_user_workouts(self.__class__.uniqueUsername2)
        self.delete_all_user_workouts(self.__class__.uniqueUsername1)


    # Function used to register a new user
    def register_user(self, uniqueUsername):
        driver = self.driver

        # Logs out, just in case a user is already logged in
        driver.get("http://localhost:9090/logout.html")
        time.sleep(0.5)

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

        # Inputs values in all the registration fields
        usernameField.send_keys(uniqueUsername)
        emailField.send_keys(uniqueUsername + "@test.test")
        passwordField.send_keys(self.__class__.userPassword)
        repeatPasswordField.send_keys(self.__class__.userPassword)
        phoneNumberField.send_keys("12312312")
        countryField.send_keys("Norway")
        cityField.send_keys("Narvik")
        streetAddressField.send_keys("Kvartslia")

        # Finds and clicks the button that creates the account
        createAccountButton = driver.find_element_by_id("btn-create-account")
        createAccountButton.click()
        time.sleep(0.5)


    # Function used to register a new workout for the logged in user
    def register_workout_with_exercise(self, sets):
        driver = self.driver

        time.sleep(0.5)

        # Find and clicks the button to go to the workouts page
        workoutNavButton = driver.find_element_by_id("nav-workouts")
        workoutNavButton.click()
        time.sleep(0.5)

        # Finds and clicks the button that opens the page for creating a new workout
        newWorkoutButton = driver.find_element_by_id("btn-create-workout")
        newWorkoutButton.click()

        # Input fields for a new workout
        workoutNameField = driver.find_element_by_id("inputName")
        workoutDateField = driver.find_element_by_id("inputDateTime")
        workoutNotesField = driver.find_element_by_id("inputNotes")
        workoutExerciseType = driver.find_element_by_name("type")
        workoutExerciseSets = driver.find_element_by_name("sets")
        workoutExerciseNumber = driver.find_element_by_name("number")

        # Waits until fields become editable
        time.sleep(0.5)

        # Inputs values into fields
        workoutNameField.send_keys("TestWorkout")
        workoutDateField.clear();
        workoutDateField.send_keys("1111-01-01 00:01");
        workoutNotesField.send_keys("This is an auto-generated workout meant for testing")
        workoutExerciseSets.send_keys(sets)
        workoutExerciseNumber.send_keys("10")

        for option in workoutExerciseType.find_elements_by_tag_name('option'):
            if option.text == self.__class__.uniqueExercise:
                option.click()

        time.sleep(0.5)

        # Finds and clicks the button that publishes the new workout
        publishWorkoutButton = driver.find_element_by_id("btn-ok-workout")
        publishWorkoutButton.click()
        time.sleep(0.5)


    # This asserts that the leaderboard on the webpage matches the expected leaderboard given as a parameter.
    # The expected_leaderboard parameter is a list of dictionaries; each dictionary has three keys: "rank", "username",
    # and "score"
    def assert_leaderboard(self, expected_leaderboard):
        driver = self.driver

        time.sleep(0.5)

        # Find and clicks the button to go to the exercise page
        exerciseNavButton = driver.find_element_by_id("nav-exercises")
        exerciseNavButton.click()
        time.sleep(0.5)

        self.scroll_down()

        # Inspects the newest exercise
        exercise = driver.find_elements_by_css_selector("a.list-group-item")[-1]
        exercise.click()
        time.sleep(0.5)

        # All the rows in the leaderboard
        leaderboardRows = driver.find_elements_by_tag_name("tr")

        # Tests that the leaderboard has the correct amount of rows; adds 1 to the expected leaderboard length
        # because the actual leaderboard includes the table header as an extra row
        self.assertEqual(len(expected_leaderboard) + 1, len(leaderboardRows))

        leaderboard = []

        # Converts the text into a list of dictionaries for easy testing purposes
        for i in range(1, len(leaderboardRows)):
            row = leaderboardRows[i].text.split(" ")
            leaderboard.append({"rank": row[0], "username": row[1], "score": row[2]})

        # Loops through all the leaderboard rows and checks the values up against the expected leaderboard
        for i in range(0, len(leaderboard)):
            # Asserts that the rank is correct
            self.assertEqual(expected_leaderboard[i]["rank"], leaderboard[i]["rank"])

            # Asserts that the username is correct
            self.assertEqual(expected_leaderboard[i]["username"], leaderboard[i]["username"])

            # Asserts that the score is correct
            self.assertEqual(expected_leaderboard[i]["score"], leaderboard[i]["score"])

        time.sleep(0.5)


    # Deletes all workouts created by a user
    def delete_all_user_workouts(self, username):
        driver = self.driver

        self.login_user(username)

        # Scrolls to the bottom of the page; a 'problem' (due to dynamic loading) with not every workout being
        # loaded into the DOM appears when we have too many workouts. Scrolling to the bottom fixes this.
        self.scroll_down()

        # Deletes all the user's workouts
        while username in driver.page_source:
            # Finds and clicks the button that views the user's own workouts
            myWorkoutsButton = driver.find_element_by_id("list-my-workouts-list")
            myWorkoutsButton.click()
            time.sleep(0.5)

            # Views the workout
            workout = driver.find_elements_by_css_selector("a.list-group-item")[-1]
            workout.click()
            time.sleep(0.5)

            # Edits the workout
            editButton = driver.find_element_by_id("btn-edit-workout")
            editButton.click()
            time.sleep(0.5)

            # Deletes the workout
            deleteWorkoutButton = driver.find_element_by_id("btn-delete-workout")
            deleteWorkoutButton.click()
            time.sleep(0.5)

            self.scroll_down()


    # Logs in using the username-parameter and the password stored in 'self'
    def login_user(self, username):
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
        usernameField.send_keys(username)
        passwordField.send_keys(self.__class__.userPassword)

        logInButton = driver.find_element_by_id("btn-login")
        logInButton.click()
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
            time.sleep(1)

            # Calculate new scroll height and compare with last scroll height.
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height


if __name__ == "__main__":
    unittest.main()


