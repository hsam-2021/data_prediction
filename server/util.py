
import pickle
import json
import numpy as np
import warnings
warnings.filterwarnings("ignore")


def get_predict_customer(job, marital_status, education, contact, month, poutcome, age, balance, day, duration, campaign,
                     previous, housing, loan):
    __jobs = None
    __marital_status = None
    __education = None
    __contact = None
    __month = None
    __poutcome = None
    __data_columns = None
    __model = None

    print("loading saved artifacts...start")

    with open("/data_prediction/server/artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __jobs = __data_columns[6:17]
        __marital_status = __data_columns[17:19]
        __education = __data_columns[19:22]
        __contact = __data_columns[22:24]
        __month = __data_columns[24:35]
        __poutcome = __data_columns[35:38]


    if __model is None:
        with open('/data_prediction/server/artifacts/Customer_pred_pickle_model.pickle', 'rb') as f:
            __model = pickle.load(f)
            # __model = joblib.load(f)
    print("loading saved artifacts...done")
    try:
        loc_index_job = __data_columns.index(job.lower())
        loc_index_marital = __data_columns.index(marital_status.lower())
        loc_index_education = __data_columns.index(education.lower())
        loc_index_contact = __data_columns.index(contact.lower())
        loc_index_month = __data_columns.index(month.lower())
        loc_index_poutcome = __data_columns.index(poutcome.lower())
    except:
        loc_index_job = -1
        loc_index_marital = -2
        loc_index_education = -3
        loc_index_contact = -4
        loc_index_month = -5
        loc_index_poutcome = -6

    x = np.zeros(len(__data_columns))

    x[0] = age
    x[1] = balance
    x[2] = day
    x[3] = duration
    x[5] = campaign
    x[6] = previous
    if loc_index_job >= 0:
        x[loc_index_job] = 1
    elif loc_index_marital >= 0:
        x[loc_index_marital] = 2
    elif loc_index_education >= 0:
        x[loc_index_education] = 3
    elif loc_index_contact >= 0:
        x[loc_index_contact] = 4
    elif loc_index_month >= 0:
        x[loc_index_month] = 5
    elif loc_index_poutcome >= 0:
        x[loc_index_poutcome] = 6

    return str(__model.predict([x])[0])
    

def get_jobs_names():
    return __jobs
def get_marital_status():
    return __marital_status
def get_education():
    return __education
def get_contact():
    return __contact
def get_month():
    return __month
def get_poutcome():
    return __poutcome


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns
    global __jobs
    global __marital_status
    global __education
    global __contact
    global __month
    global __poutcome

    with open("/data_prediction/server/artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __jobs = __data_columns[6:17]
        __marital_status = __data_columns[17:19]
        __education = __data_columns[19:22]
        __contact = __data_columns[22:24]
        __month = __data_columns[24:35]
        __poutcome = __data_columns[35:38]

    global __model
    if __model is None:
        with open('/data_prediction/server/artifacts/Customer_pred_pickle_model.pickle', 'rb') as f:
            __model = pickle.load(f)
            # __model = joblib.load(f)
    print("loading saved artifacts...done")

# def get_jobs_names():
#     return __jobs

def get_data_columns():
    return __data_columns

if __name__ == '__main__':
    load_saved_artifacts()
    print(__data_columns[:])
    print(get_jobs_names())
    print(get_marital_status())
    print(get_education())
    print(get_contact())
    print(get_month())
    print(get_poutcome())
    print('test data='+str(get_predict_customer('blue-collar', 'married', 'primary', 'contact_unknown', 'dec', 'poutcome_unknown', 55, 1000.00, 29.00, 300, 13, 200.00, 1, 0)))
