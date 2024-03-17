class TestSample:
    test_name = "TC POC"
    KPI_COUNT = 7
    file_path = __file__


    def test_poc(self,launch):
        LaunchPageObject = launch
        LoginPageObject=LaunchPageObject.go_to_login_page()
        HomePageObject = LoginPageObject.login_to_home_page()
        BoostPageObject=HomePageObject.go_to_boost_page()
        RoamingPageObject=BoostPageObject.boost_plan()
        FeedbackPageObject=RoamingPageObject.adding_roaming_pass()
        FeedbackPageObject.app_feedback()
       