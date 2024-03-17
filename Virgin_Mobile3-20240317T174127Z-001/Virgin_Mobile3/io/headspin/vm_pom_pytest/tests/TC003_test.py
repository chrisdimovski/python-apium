class Test003:
    test_name = "TC003"
    KPI_COUNT = 5
    file_path = __file__

    
    def test_003(self,launch):
        LaunchPageObject = launch
        LoginPageObject=LaunchPageObject.go_to_login_page()
        HomePageObject = LoginPageObject.login_to_home_page()
        PaymentPageObject = HomePageObject.go_to_payment_page()
        PaymentPageObject.add_payment_card()