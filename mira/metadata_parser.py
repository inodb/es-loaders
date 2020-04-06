import pickle
import os
import collections
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import csv

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SAMPLE_SPREADSHEET_ID = '1plhIL1rH2IuQ8b_komjAUHKKrnYPNDyhvNNRsTv74u8'
SAMPLE_RANGE_NAME = 'sample_metadata'


SORT_ENCODER = {'singlet, live, CD45+': 'CD45P',
                'singlet, live, CD45-': 'CD45N', 'singlet, live, U': 'U'}


class MiraMetadata(object):

    def __init__(self):
        # data = self.open_file()
        # header = data.pop(0)

        # df = pd.DataFrame.from_records(
        #     [dict(zip(header, row)) for row in data])

        # df['sort_parameters'] = df['sort_parameters'].map(
        #     SORT_ENCODER)

        # self.data = df.to_dict('records')

        self.data = [{"project": "SPECTRUM", "unique_id": "Sample_045LA_CD45N_IGO_09443_X_4", "nick_unique_id": "SPECTRUM-OV-045_S1_CD45N_LEFT_ADNEXA", "aliquot_id": "OV-045-LAdnx-CD45N-S1", "sample_id": "OV-045-LAdnx",
                      "patient_id": "SPECTRUM-OV-045",	"cancer_type": "hgsoc", "tumour_site": "left adnexa", "tumour_subsite": "", "tumour_type": "primary", "sort_parameters": "CD45N", "therapy": "pre-Rx", "time": "S1", "qc_status": "Pass"},
                      {"project": "human_liver_nature_2019", "unique_id": "patient1_sample1", "nick_unique_id": "patient1_sample1", "aliquot_id": "045-LAdnx-CD45N-S1", "sample_id": "sample1",
                      "patient_id": "patient1",	"cancer_type": "liver", "tumour_site": "liver", "tumour_subsite": "", "tumour_type": "primary", "sort_parameters": "sample1", "therapy": "pre-Rx", "time": "T1", "qc_status": "Pass"}
                      ]

    def open_file(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('sheets', 'v4', credentials=creds,
                        cache_discovery=False)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        return values

    def sample_ids(self):
        return [row["nick_unique_id"] for row in self.data]

    def patient_ids(self):
        df = pd.DataFrame.from_records(self.data)

        patient_df = df[['patient_id']].drop_duplicates()

        return [str(row[0]) for row in patient_df.values.tolist()]

    def support_sample_ids(self, patient_id):
        return [row['nick_unique_id'] for row in self.data if row['patient_id'] == patient_id]

    def get_data(self, sample_ids):
        data = dict(zip(self.sample_ids(), self.data))

        return [data[sample_id] for sample_id in sample_ids]

    def get_igo_to_sample_id(self, igo_id):
        [sample_id] = [record['nick_unique_id']
                       for record in self.data if igo_id == record['unique_id']]

        return sample_id


# metadata = MiraMetadata()
# print(metadata.get_igo_to_sample_id('Sample_042AS_CD45P_IGO_09443_V_3'))
# print(metadata.patient_ids())
# print(metadata.data)
# print(metadata.get_data(['SPECTRUM-OV-054_S1_CD45N_INFRACOLIC_OMENTUM']))
# print(metadata.support_sample_ids("SPECTRUM-OV-014_CD45P"))
