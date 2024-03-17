class Test002:
    test_name = "TC002"
    KPI_COUNT = 9
    file_path = __file__

    
    def test_002(self,launch):
        LaunchPageObject = launch
        LoginPageObject = LaunchPageObject.go_to_login_page()
        HomePageObject = LoginPageObject.login_to_home_page()
        ProfilePageObject = HomePageObject.go_to_profile_page()
        PasswordPageObject = ProfilePageObject.direct_to_password_page()
        PasswordPageObject.reset_password()
        PasswordPageObject.logout()
        LoginPageObject = LaunchPageObject.go_to_login_page()
        HomePageObject = LoginPageObject.login_to_home_page()

