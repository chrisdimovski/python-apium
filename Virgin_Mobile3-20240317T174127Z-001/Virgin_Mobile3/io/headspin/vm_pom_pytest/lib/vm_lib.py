from kpi_names import *

def init_timing(session_data):
    # initialising variables
    session_data.status = "Fail_launch"
    session_data.pass_count = 0
    session_data.fail_count = 0
    session_data.connection_status= ""
    session_data.data_kpi = True
    session_data.fail_label_key = None
    session_data.debug = False

    # Categories
    session_data.KPI_LABEL_CATEGORY = "Virgin Mobile"
    session_data.genre_id = "Virgin Mobile"
    
    #Data KPIs
    session_data.data_kpis = {}

    # KPI Labels
    session_data.kpi_labels = {}
    session_data.kpi_labels[LAUNCH_TIME] = {'start': None, 'end': None}
    session_data.kpi_labels[LOGIN_PAGE_LOAD_TIME] = {'start': None, 'end': None}
    session_data.kpi_labels[HOME_PAGE_LOAD_TIME] = {'start': None, 'end': None}
    session_data.kpi_labels[ROAMING_PAGE_LOAD_TIME] = {'start': None, 'end': None}
    session_data.kpi_labels[ROAMING_DATE_SET_TIME] = {'start': None, 'end': None}
    session_data.kpi_labels[FEEDBACK_PAGE_LOAD_TIME] = {'start': None, 'end': None}
    session_data.kpi_labels[FEEDBACK_SUBMISSION_TIME] = {'start': None, 'end': None}
    session_data.kpi_labels[ BOOST_PAGE_LOAD_TIME] = {'start': None, 'end': None}
    
   