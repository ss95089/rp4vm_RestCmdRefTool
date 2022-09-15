import base64
import datetime
import json
import pandas as pd
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

def AuthEncode(uid, upass):
    CredentialsText = f'{uid}:{upass}'
    EncodedCredentials = base64.b64encode(CredentialsText.encode())
    EncodedCredentials = str(EncodedCredentials)[2:len(str(EncodedCredentials)) - 1]
    headers = {'Authorization': f'Basic {EncodedCredentials}'}
    return headers

def defDfRpclusters(rp, rpSystemId):
    r = rp.get_rpsystems_rpclusters(rpSystemId)
    df_rpclusters = pd.read_json(r.text, dtype='object')
    df_rpclusters = df_rpclusters.sort_values('name')
    df_rpclusters = df_rpclusters.reset_index(drop=True)
    return df_rpclusters

def defDfvmDatastores(rp, df_rpclusters):
    df_vmDatastores = {}
    for i in df_rpclusters[['id', 'name']].values:
        r = rp.get_platforms_vcs(i[0])
        vcRep = r.json()[0]['id']
        r = rp.get_platforms_vcs_datastores(i[0], vcRep)
        df_vmDatastores[i[1]] = pd.read_json(r.text, dtype={4: 'int64', 5: 'int64'})
        df_vmDatastores[i[1]] = df_vmDatastores[i[1]].sort_values('name')
        df_vmDatastores[i[1]] = df_vmDatastores[i[1]].reset_index(drop=True)
    return df_vmDatastores

def defDfProtectVms(rp):
    r = rp.get_vms_protect_candidates()
    df_protect_vms = pd.read_json(r.text, dtype='object')
    df_protect_vms = df_protect_vms.sort_values('name')
    df_protect_vms = df_protect_vms.reset_index(drop=True)
    return df_protect_vms

def defDfRpsystemsVms(rp, rpSystemId):
    r = rp.get_rpsystems_vms(rpSystemId)
    df_rpsystems_vms = pd.read_json(r.text, dtype='object')
    if len(df_rpsystems_vms) != 0:
        df_rpsystems_vms = df_rpsystems_vms[df_rpsystems_vms['role'] == 'PRODUCTION']
        df_rpsystems_vms = df_rpsystems_vms.sort_values(['rpClusterName', 'groupName', 'name'])
        df_rpsystems_vms = df_rpsystems_vms.reset_index(drop=True)
    return df_rpsystems_vms

def defDfGroupsRecoveryActivities(rp):
    r = rp.get_groups_recovery_activities()
    df_groupsRecoveryActivities = pd.read_json(r.text, dtype='object')
    return df_groupsRecoveryActivities

def defDfTransactions(rp, gmtTimeDifferenceHour):
    r = rp.get_transactions()
    df_transactions = pd.read_json(r.text, dtype={'progressPercentage': 'int64'})
    if len(df_transactions) != 0:
        df_transactions['timeCreated'] = pd.to_datetime(df_transactions['timeCreated'], format='%Y-%m-%dT%H:%M:%S') + datetime.timedelta(hours=gmtTimeDifferenceHour)
        df_transactions = df_transactions.sort_values('timeCreated', ascending=False)
        df_transactions['timeCreated2'] = df_transactions['timeCreated'].dt.strftime('%Y-%m-%d %H:%M:%S')
    return df_transactions

def defDfCgSnapshot(rp, groupId, copyId, gmtTimeDifferenceHour):
    r = rp.get_snapshots(groupId, copyId)
    df_cgSnapshot = pd.read_json(r.text, dtype={'id': 'object', 'timestamp': 'datetime', 'sizeInBytes': 'int64',
                                                'bookmarkName': 'object', 'consistencyType': 'object'})
    df_cgSnapshot['timestamp2'] = df_cgSnapshot['timestamp'] + datetime.timedelta(hours=gmtTimeDifferenceHour)
    df_cgSnapshot['timestamp2'] = df_cgSnapshot['timestamp2'].dt.strftime('%Y/%m/%d %H:%M:%S')
    return df_cgSnapshot

def defDfJournalDatastores(rp, df_rpclusters):
    df_journalDatastores = {}
    for i in df_rpclusters[['id', 'name']].values:
        r = rp.get_cluster_journal_datastores(i[0])
        df_journalDatastores[i[1]] = pd.read_json(r.text, dtype={7: 'int64', 8: 'int64'})
        df_journalDatastores[i[1]] = df_journalDatastores[i[1]].sort_values('name')
        df_journalDatastores[i[1]] = df_journalDatastores[i[1]].reset_index(drop=True)
    return df_journalDatastores

def defDfGroups(rp):
    r = rp.get_groups()
    df_groups = pd.read_json(r.text, dtype='object')
    if len(df_groups) != 0:
        df_groups = df_groups.sort_values('name')
        df_groups = df_groups.reset_index(drop=True)
    return df_groups

class Reprp(object):
    def __init__(self, host, headers, hideGetRequest):
        self.host = host
        self.headers = headers
        self.hideGetRequest = hideGetRequest

    def delete_group(self, groupId):
        uri = f"https://{self.host}/api/v1/groups/{groupId}"
        self.requests_delete(uri)
        return self.r

    def delete_stop_testcopy(self, groupId, copyId):
        uri = f"https://{self.host}/api/v1/groups/{groupId}/copies/{copyId}/test-copy"
        self.requests_delete(uri)
        return self.r

    def get_cluster_journal_datastores(self, clusterRep):
        uri = f"https://{self.host}/api/v1/rp-clusters/{clusterRep}/journal-datastores"
        self.requests_get(uri)
        return self.r

    def get_transactions(self):
        uri = f"https://{self.host}/api/v1/transactions"
        self.requests_get(uri)
        return self.r

    def get_transactions_transactionid(self, transactionId):
        uri = f"https://{self.host}/api/v1/transactions/{transactionId}"
        self.requests_get(uri)
        return self.r

    def get_groups(self):
        uri = f"https://{self.host}/api/v1/groups"
        self.requests_get(uri)
        return self.r

    def get_groups_copies(self, groupId):
        uri = f"https://{self.host}/api/v1/groups/{groupId}/copies"
        self.requests_get(uri)
        return self.r

    def get_groups_recovery_activities(self):
        uri = f"https://{self.host}/api/v1/groups/recovery-activities"
        self.requests_get(uri)
        return self.r

    def get_platforms_vcs(self, clusterRep):
        uri = f"https://{self.host}/api/v1/rp-clusters/{clusterRep}/platforms/vcs"
        self.requests_get(uri)
        return self.r

    def get_platforms_vcs_datastores(self, clusterRep, vcRep):
        uri = f"https://{self.host}/api/v1/rp-clusters/{clusterRep}/platforms/vcs/{vcRep}/datastores"
        self.requests_get(uri)
        return self.r

    def get_rpsystems(self):
        uri = f"https://{self.host}/api/v1/rp-systems"
        self.requests_get(uri)
        return self.r

    def get_rpsystems_rpclusters(self, rpSystemId):
        uri = f"https://{self.host}/api/v1/rp-systems/{rpSystemId}/rp-clusters"
        self.requests_get(uri)
        return self.r

    def get_rpsystems_vms(self, rpSystemId):
        uri = f"https://{self.host}/api/v1/rp-systems/{rpSystemId}/vms"
        self.requests_get(uri)
        return self.r

    def get_snapshots(self, groupId, copyId):
        uri = f"https://{self.host}/api/v1/groups/{groupId}/copies/{copyId}/snapshots"
        self.requests_get(uri)
        return self.r

    def get_vms_protect_candidates(self):
        uri = f"https://{self.host}/api/v1/vms/protect/candidates?vms=&name="
        self.requests_get(uri)
        return self.r

    def get_version(self):
        uri = f"https://{self.host}/api/v1/version"
        self.requests_get(uri)
        return self.r

    def post_create_bookmarks(self, groupId, bookmarkName, consistencyType, consolidationPolicy):
        uri = f"https://{self.host}/api/v1/groups/{groupId}/bookmarks"
        jsondata = {
            "bookmarkName": f"{bookmarkName}",
            "consistencyType": f"{consistencyType}",
            "consolidationPolicy": f"{consolidationPolicy}"
        }
        self.requests_post(uri, jsondata)
        return self.r

    def post_failover(self, groupId, copyId):
        uri = f"https://{self.host}/api/v1/groups/{groupId}/copies/{copyId}/failover"
        jsondata = {
            "applyFailoverNetworks": True
        }
        self.requests_post(uri, jsondata)
        return self.r

    def post_recover_production(self, groupId, copyId):
        uri = f"https://{self.host}/api/v1/groups/{groupId}/copies/{copyId}/recover-production"
        jsondata = ""
        self.requests_post(uri, jsondata)
        return self.r

    def post_testcopy(self, groupId, copyId, snapshotId, scenario, testNetworkType):
        uri = f"https://{self.host}/api/v1/groups/{groupId}/copies/{copyId}/test-copy"
        if snapshotId == 'latest':
            jsondata = {
                "imageAccessScenario": f"{scenario}",
                "powerOnVms": True,
                "testNetworkType": f"{testNetworkType}"
            }
        else:
            jsondata = {
                "imageAccessScenario": f"{scenario}",
                "powerOnVms": True,
                "snapshotId": f"{snapshotId}",
                "testNetworkType": f"{testNetworkType}"
            }
        self.requests_post(uri, jsondata)
        return self.r

    def post_vms_add(self, groupId, jsondata):
        uri = f"https://{self.host}/api/v1/groups/{groupId}/add-vm?validate-only=False"
        self.requests_post(uri, json.loads(jsondata))
        return self.r

    def post_vms_add_defaults(self, prodClusterId, protectVmId, groupId):
        uri = f"https://{self.host}/api/v1/groups/{groupId}/add-vm/defaults"
        jsondata = {
            "vm": f"{protectVmId}",
            "rpCluster": f"{prodClusterId}"
        }
        self.requests_post(uri, jsondata)
        return self.r

    def post_vms_protect(self, jsondata):
        uri = f"https://{self.host}/api/v1/vms/protect?validate-only=False"
        self.requests_post(uri, json.loads(jsondata))
        return self.r

    def post_vms_protect_defaults(self, prodClusterId, protectVmId, prodJournalDatastoreId, copyClusterId, copyDatastoreId, copyJournalDatastoreId):
        uri = f"https://{self.host}/api/v1/vms/protect/defaults"
        jsondata = {
            "groupConfiguration": {
                "copies": [
                    {
                        "journalDatastore": f"{copyJournalDatastoreId}",
                        "rpCluster": f"{copyClusterId}",
                        "vmDatastore": f"{copyDatastoreId}"
                    }
                ],
                "productionJournalDatastore": f"{prodJournalDatastoreId}"
            },
            "rpCluster": f"{prodClusterId}",
            "vm": f"{protectVmId}"
        }
        self.requests_post(uri, jsondata)
        return self.r

    def requests_delete(self, uri):
        self.r = requests.delete(uri, headers=self.headers, verify=False, timeout=(6.0, 9.0))
        print(f"\n--- {datetime.datetime.now()} ---")
        t01 = self.headers['Authorization']
        print(f'Curl(Sample) : \ncurl -k -X DELETE "{uri}" -H "accept: application/json" -H "authorization: {t01}"')
        print(f"Status Code : {self.r.status_code}")
        if str(self.r.status_code)[:2] != '20':
            print(f"Response Text : {self.r.text}")

    def requests_get(self, uri):
        try:
            self.r = requests.get(uri, headers=self.headers, verify=False, timeout=(6.0, 9.0))
        except requests.exceptions.RequestException as e:
            self.r = str(e)
        else:
            if self.hideGetRequest == True:
                print(f"\n--- {datetime.datetime.now()} ---")
                t01 = self.headers['Authorization']
                print(f'Curl(Sample) : \ncurl -k -X GET "{uri}" -H "accept: application/json" -H "authorization: {t01}"')
                print(f"Status Code : {self.r.status_code}")
                if str(self.r.status_code)[:2] != '20':
                    print(f"Response Text : {self.r.text}")

    def requests_post(self, uri, jsondata):
        self.r = requests.post(uri, headers=self.headers, json=jsondata, verify=False, timeout=(6.0, 9.0))
        print(f"\n--- {datetime.datetime.now()} ---")
        t01 = self.headers['Authorization']
        t02 = json.dumps(jsondata).replace('"', chr(92)+chr(34))
        print(f'Curl(Sample) : \ncurl -k -X POST "{uri}" -H "accept: application/json" -H "authorization: {t01}" -H "Content-Type: application/json" -d "{t02}"')
        print(f"Status Code : {self.r.status_code}")
        if str(self.r.status_code)[:2] != '20':
            print(f"Response Text : {self.r.text}")
