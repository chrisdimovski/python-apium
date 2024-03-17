from __future__ import absolute_import
from __future__ import print_function
import subprocess
import shlex
import os
import requests
import json
from hs_logger import logger
import csv
DEFAULT_TIMEOUT = 240
LONG_TIMOUT = 4 * 60

class hsApi:
        
# API for getting all devices and its details present in  an org
    value="https://virginmo-api.virginmobile.ae"
    url_root = f"{value}/v0/"
    waterfall_url = "https://headspin.virginmobile.ae"
    device_list_url = f"{url_root}devices"
    get_auto_config = f"{url_root}devices/automation-config"

    def __init__(self, UDID, access_token):
        self.UDID = UDID
        self.access_token = access_token
        self.headers = {'Authorization': 'Bearer {}'.format(self.access_token)}
# Get the deivce details
        r = requests.get(self.device_list_url, headers=self.headers, verify=False)
        self.device_list_resp = self.parse_response(r)
        r = r.json()
        self.devices = r['devices']
        is_desired_device = False
        for device in self.devices:
            self.device_os = device['device_type']
            if self.device_os == "android" and device['serial'] == self.UDID:
                is_desired_device = True
            if self.device_os == "ios" and device['device_id'] == self.UDID:
                is_desired_device = True
            if is_desired_device:
                self.device_details = device
                self.device_hostname = device['hostname']
                self.device_address = "{}@{}".format(
                    self.UDID, self.device_hostname)
                self.device_os = device['device_type']
                break
        self.read_csv()
            
# Read credentials.csv
    def read_csv(self):
        cur = os.getcwd()
        actualdir = os.path.join(cur,'credentials.csv')
        if not os.path.exists(actualdir):
            logger.info("Credentials file does not exist")
            exit()
        else:
            with open('credentials.csv','r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row==[]:
                        continue
                    if row[0]=='email':
                        self.email = row[1]
                    if row[0]=='password1':
                        self.current_password = row[1]
                    if row[0]=='password2':
                        self.old_password = row[1]
            return (self.email,self.current_password,self.old_password)
    
# Update credentials.csv file
    def  update_password(self):
        with open('credentials.csv','w') as file:
            writer = csv.writer(file)
            writer.writerow(['email',self.email])
            writer.writerow(['password1',self.old_password])
            writer.writerow(['password2',self.current_password])
        logger.info("Password updated in credentials.csv ")
        

    def get_automation_config(self):
        capabilities = {}
        r = requests.get(self.get_auto_config, headers={
                         'Authorization': 'Bearer {}'.format(self.access_token)},verify=False)
        appium_config = r.json()
        self.capabilities = appium_config[self.device_address]["capabilities"]
        return self.capabilities
    

    def parse_response(self, response):
        try:
            if response.ok:       
                try:
                    return response.json()
                except:
                    return response.text
            else:
                logger.info((response.status_code))
                logger.info('something went wrong')
                logger.info((response.text))
        except:
            pass
            
# Adb devices
    def get_android_device_list(self):
        request_url = f"{self.url_root}adb/devices".format(
            self.UDID)
        r = requests.get(request_url, headers=self.headers, verify=False)
        data = r.json()
        logger.info(data)
        return data

# List of ios devices
    def get_ios_device_list(self):
        request_url = f"{self.url_root}idevice/{self.UDID}/installer/list?json"
        r = requests.get(request_url, headers=self.headers, verify=False)
        data = r.json()
        logger.info(data)
        return data

# Install app
    def install_apk(self, filename):
        data = open(filename, 'rb').read()
        request_url = f'{self.url_root}adb/{self.UDID}/install'
        response = requests.post(request_url, data=data, headers=self.headers, verify=False)
        logger.info(response.text)

# Install app for iOS
    def install_ipa(self, filename):
        data = open(filename, 'rb').read()
        request_url = f'{self.url_root}idevice/{self.UDID}/installer/install'
        response = requests.post(request_url, data=data, headers=self.headers, verify=False)
        logger.info(response.text)

# Uninstall app Androd
    def uninstall_app_android(self, package_name):
        request_url = f"{self.url_root}adb/{self.UDID}/uninstall?package={package_name}"
        r = requests.post(url=request_url, headers=self.headers, verify=False)
        logger.info(r.text)
    
# Uninstall ios app
    def uninstall_app_ios(self, bundle_id):
        request_url = f"{self.url_root}idevice/{self.UDID}/installer/uninstall?appid={bundle_id}"
        r = requests.post(url=request_url, headers=self.headers, verify=False)
        logger.info(r.text)
   
# adb Commands
    def run_adb_command(self,  commmand_to_run):
        api_endpoint = f"{self.url_root}adb/{self.UDID}/shell"
        r = requests.post(url=api_endpoint, data=commmand_to_run,
                          headers=self.headers, verify=False, timeout=120)
        result = r.json()
        stdout = result['stdout'].encode('utf-8').strip()
        return stdout
    
# Pull file from android device
    def pull_file_android(self, source, destination):
        api_endpoint = f"{self.url_root}adb/{self.UDID}/pull?remote={source}"
        r = requests.get(url=api_endpoint,  headers=self.headers, verify=False)
        logger.info(f'Status code: {r.status_code}')
        with open(destination, 'wb') as f:
            f.write(r.content)

# adb screenshot
    def get_adb_screenshot(self, filename):
        api_endpoint = f"{self.url_root}adb/{self.UDID}/screenshot"
        r = requests.get(url=api_endpoint,  headers=self.headers, verify=False)
        logger.info(f'Status code: {r.status_code}')
        with open(filename, 'wb') as f:
            f.write(r.content)

# iOS screenshot
    def get_ios_screenshot(self, filename):
        api_endpoint = f"{self.url_root}idevice/{self.UDID}/screenshot"
        r = requests.get(url=api_endpoint,  headers={
                         'Authorization': 'Bearer {}'.format(self.access_token)}, verify=False)
        logger.info(f'Status code: {r.status_code}')
        with open(filename, 'wb') as f:
            f.write(r.content)

# iOS deivice info
    def get_idevice_info(self):
        headers = {
            "Authorization": "Bearer {}".format(self.access_token)
        }

        request_url = f"{self.url_root}idevice/{self.UDID}/info?json"
        r = requests.get(request_url, headers=headers, verify=False)
        data = r.json()
        logger.info(data)
        return data

# iOS get list of all apps installed
    def get_app_list_ios(self):
        headers = {
            "Authorization": "Bearer {}".format(self.access_token)
        }

        request_url = f"{self.url_root}idevice/{self.UDID}/installer/list?json"
        r = requests.get(request_url, headers=headers, verify=False)
        data = self.parse_response(r)
        return data
    
# Dismiss pop up ios
    def dismiss_ios_popup(self):
        api_endpoint = f"{self.url_root}idevice/{self.UDID}/poptap"
        r = requests.post(url=api_endpoint,  headers={
                          'Authorization': 'Bearer {}'.format(self.access_token)},verify=False)
        result = r.json()
        logger.info(r.text)

# iOS device restart
    def restart_ios_device(self):
        api_endpoint = f"{self.url_root}idevice/{self.UDID}/diagnostics/restart"
        r = requests.post(url=api_endpoint,  headers={
                          'Authorization': 'Bearer {}'.format(self.access_token)}, verify=False)
        result = r.json()
        logger.info(result)

    ##################################### Platform APIs #############################################
    def start_session_capute(self):
        api_endpoint = f"{self.url_root}sessions"
        pay_load = {"session_type": "capture",
                    "device_address": self.device_address}
        r = requests.post(url=api_endpoint, data=json.dumps(pay_load), headers={
                          'Authorization': 'Bearer {}'.format(self.access_token)}, verify=False)
        result = r.json()
        logger.info(r.text)
        session_id = result['session_id']
        return session_id

    def sync_perf_test(self,perf_test_id):
        api_endpoint = f"{self.url_root}perftests/{perf_test_id}/dbsync"
        r = requests.post(url = api_endpoint,  headers={'Authorization': 'Bearer {}'.format(self.access_token)}, verify=False)
        result = r.json()
        logger.info(r.text)

    def stop_session_capture(self, session_id):
        # curl_comand = sh.Command('curl')
        # curl_comand( '-X','PATCH', 'https://{}@virginmo-api.virginmobile.ae/v0/sessions/{}'.format(self.access_token, session_id), '-d', '{"active":false}')
        
        request_url = self.url_root + 'sessions/' + session_id
        data_payload = {}
        data_payload['active'] = False
        response = requests.patch(
            request_url, headers=self.headers, verify=False, json=data_payload, timeout=DEFAULT_TIMEOUT)
        return self.parse_response(response)

    def add_session_tags(self, session_id, **kwargs):
        # followed by any number of tags , syntax:<tag_key="tag_value">. eg: type1="test_session",type2="test_session"
        # Function call example:
        # hs_class.add_session_tags("3da744a6-c269-11e9-b708-0641978974b8",type="test_session")
       
        api_endpoint = f"{self.url_root}sessions/tags/{session_id}"
        pay_load = []
        for key, value in kwargs.items():
            pay_load.append({"%s" % key: value})
        r = requests.post(url=api_endpoint, json=pay_load, headers={
                          'Authorization': 'Bearer {}'.format(self.access_token)},verify=False)
        logger.info(r)
        
    def add_kpi_session_tags(self, session_id, session_data):
        #for adding kpi as tags to sessions 
        # session_data  will be 
        # [{'key': 'bundle_id', 'value': 'com.hopper.flights'},{......}   format
       
        api_endpoint = f"{self.url_root}sessions/tags/{session_id}"
        pay_load = []
        for data in session_data:
            pay_load.append({"%s" % data['key']: data['value']})
        r = requests.post(url=api_endpoint, json=pay_load, headers={
                          'Authorization': 'Bearer {}'.format(self.access_token)}, verify=False)

# Add data to existing session
    def add_session_data(self, session_data):
        # Expecting the input dictionary as the argument
        # Sample
        # {"session_id": "<session_id>", "test_name": "<test_name>", "data":[{"key":"bundle_id","value":"com.example.android"}] }
        
        request_url = self.url_root + "perftests/upload"
        response = requests.post(
            request_url, headers=self.headers, verify=False, json=session_data, timeout=DEFAULT_TIMEOUT)
        return self.parse_response(response)

# Audio APIs
    def prepare_audio(self, audio_id_to_inject):

        logger.info("Prepare")

        # defining the api-endpoint
        prepare_api_endpoint= f"{self.url_root}audio/prepare"

        #Prepare
        pay_load= {'hostname': self.device_hostname ,  'audio_ids':[audio_id_to_inject] }

        # sending post request for prepare
        r= requests.post(url = prepare_api_endpoint, data = json.dumps(pay_load), headers={'Authorization': 'Bearer {}'.format(self.access_token)})
        logger.info(r.text)

    def inject_audio(self, audio_id_to_inject):

        logger.info("Inject")
        inject_api_endpoint= f"{self.url_root}audio/inject/start"
        pay_load= {'device_address':self.device_address, 'audio_id':audio_id_to_inject }
        r = requests.post(url = inject_api_endpoint, data = json.dumps(pay_load), headers={'Authorization': 'Bearer {}'.format(self.access_token)})
        logger.info(r.text)

    def capture_audio(self, duration, tag=None):
        api_endpoint= f"{self.url_root}audio/capture/start"
        pay_load= {'device_address': self.device_address, 'max_duration':'%s'%duration, 'tag':tag}
        r = requests.post(url = api_endpoint,  data = json.dumps(pay_load),  headers={'Authorization': 'Bearer {}'.format(self.access_token)})
        result= r.json()
        results= json.dumps(result)
        logger.info(results)
        audio_id = result['audio_id']
        logger.info(audio_id)
        return audio_id

    def add_annotation(self, session_id, data_payload):
        request_url = self.url_root + 'sessions/' + session_id + '/label/add'
        response = requests.post(
            request_url, headers=self.headers, verify=False, json=data_payload, timeout=DEFAULT_TIMEOUT)
        return self.parse_response(response)

    def get_sessions(self, num_of_sessions=30):
        request_url = self.url_root + \
            'sessions?include_all=true&num_sessions=' + str(num_of_sessions)
        response = requests.get(
            request_url, headers=self.headers, verify=False, timeout=DEFAULT_TIMEOUT)
        return self.parse_response(response)

    def update_session_name_and_description(self, session_id, name, description):
        logger.info("Adding description")
        request_url = self.url_root + 'sessions/' + session_id + '/description'
        data_payload = {}
        data_payload['name'] = name
        data_payload['description'] = description
        response = requests.post(
            request_url, headers=self.headers, verify=False, json=data_payload, timeout=DEFAULT_TIMEOUT)
        return self.parse_response(response)

    def get_appium_log(self, session_id, working_dir):
        logger.info('get_appium_log')
        request_url = self.url_root + 'sessions/' + session_id + '.appium.log'
        logger.info(f'request_url: {request_url}')
        r = requests.get(url=request_url,  headers=self.headers, verify=False)
        logger.info(f'Status code: {r.status_code}')
        if r.ok:
            outfile = os.path.join(working_dir, session_id + '.appium.log')
            with open(outfile, 'wb') as f:
                f.write(r.content)
            return outfile

    def download_captured_audio(self, audio_id_to_download, file_name):
        cmd = shlex.split("curl -X GET https://{}@api-dev.headspin.io/v0/audio/{}/download?channels=mono -o {}".format(
            self.access_token, audio_id_to_download, file_name+".wav"))
        logger.info("Downloading")
        logger.info(cmd)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        logger.info(process.stdout)

    def get_capture_timestamp(self, session_id):
        request_url = self.url_root + 'sessions/' + session_id+'/timestamps'
        response = requests.get(request_url, headers=self.headers, verify=False)
        response.raise_for_status()
        return self.parse_response(response)

    def add_label(self, session_id, name, category, start_time, end_time, pinned=False, label_type='user', data=None):
        '''
        add annotations to session_id with name, category, start_time, end_time
        '''
        request_url = self.url_root + 'sessions/' + session_id + '/label/add'
        data_payload = {}
        data_payload['name'] = name
        data_payload['category'] = category
        data_payload['start_time'] = str(start_time)
        data_payload['end_time'] = str(end_time)
        data_payload['data'] = data
        data_payload['pinned'] = pinned
        data_payload['label_type'] = label_type
        response = requests.post(
            request_url, headers=self.headers, verify=False, json=data_payload)
        response.raise_for_status()
        return self.parse_response(response)

    # Get the session video metadata
    def get_session_video_metadata(self, session_id):
        request_url = f"{self.url_root}sessions/{session_id}/video/metadata"
        response = requests.get(
                request_url, headers=self.headers, verify=False)
        logger.info(f'video metadata {response.json()}')
        return response.json()

    def get_pageloadtime(self, session_id, name, start_time, end_time, start_sensitivity=None, end_sensitivity=None, video_box=None):
        request_url = self.url_root + 'sessions/analysis/pageloadtime/'+session_id
        data_payload = {}
        region_times = []
        start_end = {}
        start_end['start_time'] = str(start_time/1000)
        start_end['end_time'] = str(end_time/1000)
        start_end['name'] = name
        region_times.append(start_end)
        data_payload['regions'] = region_times
        data_payload['wait_timeout_sec'] = 3600
        if(start_sensitivity is not None):
            data_payload['start_sensitivity'] = start_sensitivity
        if(end_sensitivity is not None):
            data_payload['end_sensitivity'] = end_sensitivity
        if(video_box is not None):
            data_payload['video_box'] = video_box
        logger.info(f"Data_payload of {name}: {data_payload}")#add
        response = requests.post(
            request_url, headers=self.headers, verify=False, json=data_payload)
        response.raise_for_status()
        results = self.parse_response(response)
        return results
    
# Manage device state on HS platform 
    def get_dbinfo(self):
        request_url = self.url_root + 'perftests/dbinfo'
        response = requests.get(request_url, headers=self.headers, verify=False)
        return self.parse_response(response)

    def get_label(self, label_id):
        request_url = self.url_root + 'sessions/label/' + label_id
        response = requests.get(request_url, headers=self.headers, verify=False)
        return self.parse_response(response)

    def get_labels(self, session_id):
        request_url = self.url_root + 'sessions/' + session_id + '/label/list'
        response = requests.get(request_url, headers=self.headers, verify=False)
        return self.parse_response(response)

    def get_user_flows(self):
        request_url = self.url_root + 'perftests'
        response = requests.get(request_url, headers=self.headers, verify=False)
        return self.parse_response(response)
    
    def session_details(self,session_id):
        #fetch user flow details from session
        request_url = self.url_root + 'userflows/session/'+ session_id
        response = requests.get(request_url, headers=self.headers, verify=False)
        return self.parse_response(response)
    
    def sec_start_time(self,session_id):
        #unix time stamp for start time of session
        request_url = self.url_root + 'sessions/'+session_id
        response = requests.get(request_url, headers=self.headers, verify=False)
        r = response.json()
        return r['start_time']
        
    def sync_user_flow(self, user_flow_id):
        request_url = self.url_root + 'perftests/' + user_flow_id + '/dbsync'
        response = requests.post(request_url, headers=self.headers, verify=False)
        return self.parse_response(response)
    
    def get_screenshot_url(self):
        request_url = self.url_root + "adb/{}/screenshot_url".format(self.UDID)
        r = requests.get(url = request_url, headers=self.headers, verify=False,timeout=DEFAULT_TIMEOUT)
        return self.parse_response(r)
    
    def get_screenshot_url_ios(self):
        request_url = self.url_root + "idevice/{}/screenshot_url".format(self.UDID)
        r = requests.get(url = request_url, headers=self.headers, verify=False,timeout=DEFAULT_TIMEOUT)
        return self.parse_response(r)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--udid', '--udid', dest='udid',
                        type=str, nargs='?',
                        default=None,
                        required=False,
                        help="udid")
    parser.add_argument('--access_token', '--access_token', dest='access_token',
                        type=str, nargs='?',
                        default=None,
                        required=False,
                        help="access_token")
    
    args = parser.parse_args()
    udid = args.udid
    access_token = args.access_token
    hs_api = hsApi(udid, access_token)
    
    with open('data.txt', 'w') as outfile:
        json.dump(hs_api.device_list_resp, outfile)
