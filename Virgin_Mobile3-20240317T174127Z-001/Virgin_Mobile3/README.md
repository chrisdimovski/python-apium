# Virgin_Mobile
Virgin Mobile scripts with POM Framework and Pytest.
---------
## POM Framework
POM framework is developed using pytest,which provides
- consistent approach for automated test scripts for web applications.
- Pytest fixtures to store test data and device capabilities for multiple browsers and multiple platforms.
- library of reusable utility functions, API’s and KPI points for verification.
- pages for all the UI views that can be reusable.
### Supported Evironment
- Test Automation Tool: Selenium,Appium
- Programming language: Python
- Supported Operating Systems: Window, MacOS, Ubuntu etc.
### Libraries
The following are python 4 libraries that need to be installed on the machine in order to execute tests properly. These requirements can also be found in the `requirements.txt` located in the projext directory.
```bash
pytest== 8.0.0
appium-python-client==2.6.0
selenium==4.16.0
requests==2.28.1
```
### Prerequisites
- Operating System  :  Window, Ubuntu, MacOs
- System level tools :  - Python 3.8 or higher
- Repository from github : Clone the repository from github from the link provided.
### Source Code
The source code for this project can be found in the following GitHub repository: https://github.com/projectxyzio/Virgin_Mobile.
If you do not have access to this repository, please contact the HeadSpin team or your colleagues to grant access or supply the source code.
### Folder structure
```bash
.
├── README.md
└── io
  └── headspin
    └── vm_pom_pytest
      ├── lib
      │   ├── args_lib.py
      │   ├── device_info.py
      │   ├── hs_api.py
      │   ├── hs_logger.py
      │   ├── kpi_names.py
      │   ├── session_visual_lib.py
      │   ├── vm_lib.py
      │   └── vouchers.txt
      ├── pages
      │   ├── __init__.py
      │   ├── base_page.py
      │   ├── boost_page.py
      │   ├── feedback_page.py
      │   ├── home_page.py
      │   ├── launch_page.py
      │   ├── login_page.py
      │   ├── password_page.py
      │   ├── payment_page.py
      │   ├── profile_page.py
      │   └── roaming_page.py
      ├── tests
      │   ├── TC002_test.py
      │   ├── TC003_test.py
      │   └── TC_POC_test.py
      ├── conftest.py
      ├── credentials.csv
      ├── requirements.txt
      └── sensitivity.json


```
## Installation
- ##### Install Git
 ```bash
 sudo apt install git-all
 ```
- ##### Install Pip3
 ```bash
 sudo apt-get install python3-pip
 ```
- ##### Install Python 3 Dependencies
 Navigate the the projects directory on your local machine, i.e `Virgin_Mobile/io/headspin/vm_pom_pytest` where `requirements.txt` is located and run the following command to install python libraries.
 ```bash
 pip3 install -r requirements.txt
 ```
### Mac OS
- ##### Install Homebrew
 ```bash
 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
 ```
- ##### Install Python3 and Pip3
 ```bash
 brew install python3
 ```
- ##### Install Python 3 Dependencies
 Navigate the the projects directory on your local machine, i.e `Virgin_Mobile/io/headspin/vm_pom_pytest` where `requirements.txt` is located and run the following command to install python libraries.
 ```bash
 pip3 install -r requirements.txt
 ```
## Test execution
Inorder to start the execution we must provide the valid credentials in the credentials.csv
```bash
 email,<email_id>
 password1,<current_password>
 password2,<old_password>
 ```
```bash
 cd Virgin_Mobile/io/headspin/vm_pom_pytest
 ```
We can start the runs manually from the command line. After cloning the repository, navigate to Virgin_Mobile/io/headspin/vm_pom_pytest
 ```bash
 cd Virgin_Mobile/io/headspin/vm_pom_pytest
 ```
### Command to run all test cases
Windows
 ```bash
 python -m pytest -s --udid <device_udid> --appium_input <device_url> --os <os> --network_type WIFI
 ```
MacOS / Linux
```bash
python3 -m pytest -s --udid <device_udid> --appium_input <device_url> --os <os> --network_type WIFI
 ```
### Command to run targeted test case
Windows
 ```bash
python -m pytest -s --udid <device_udid> --appium_input <device_url> --os <os> --network_type WIFI tests\TC001_test.py
 ```
MacOS / Linux
```bash
python3 -m pytest -s --udid <device_udid> --appium_input <device_url> --os <os> --network_type WIFI tests/TC001_test.py
 ```
Options:-
```bash
--udid     :   The device in which the test is running
--appium_input      :   The web-driver url of the device
--os          :   Test environment (Android/iOS)
--network_type     :   Internet carrier of the device (WIFI/Mobile)
--use_capture     :   Headspin session capture (True/False) (Optional) (Default - True)
--video_only      :   Headspin session capture with video only (True/False) (Optional) (Default - True)
```