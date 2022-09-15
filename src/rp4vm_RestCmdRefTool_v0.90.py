import PySimpleGUI as sg
import configparser
import pandas as pd
import time
from package import utils

sg.theme('BrownBlue')
config = configparser.RawConfigParser()

def windows_main():
    config.read('config.ini')
    section1 = "Section1"
    server_id = config.get(section1, 'server_ip')
    user = config.get(section1, 'user')
    password = config.get(section1, 'password')
    gmt_time_difference = config.get(section1, 'gmt_time_difference')

    col1 = [[sg.Text('Plugin-Server-IP')], [sg.Text('User')], [sg.Text('Password')], [sg.Text('GMT')]]
    col2 = [
        [sg.InputText(default_text=server_id, size=(30, 1), key='m1f01')],
        [sg.InputText(default_text=user, size=(30, 1), key='m1f02')],
        [sg.InputText(default_text=password, password_char="*", size=(30, 1), key='m1f03')],
        [sg.Combo(['+12', '+11', '+10', '+9', '+8', '+7', '+6', '+5', '+4', '+3', '+2', '+1', '0', '-1', '-2', '-3', '-4', '-5', '-6', '-7', '-8', '-9', '-10', '-11', '-12'], default_value=gmt_time_difference, readonly=True, key='m1f04'), sg.Text('H')]
    ]
    main_layout = [
            [sg.Column(col1), sg.Column(col2)],
            [sg.Button("CONNECT"), sg.Button("SAVE VALUES"), sg.Button("EXIT")],
    ]
    return sg.Window("Login", main_layout, finalize=True)

def windows_sub():
    outputwin = [
        [sg.Checkbox("Hide GET Request", default=False, enable_events=True, key='t0f01')],
        [sg.Output(size=(150, 10), font=('MS Gothic', 11), background_color='black', text_color='white')],
    ]
    tab1col1 = [
        [sg.Text('Production RP Cluster')],
        [sg.Listbox([''], size=(40, 4), enable_events=True, key='t1f01')],
        ]
    tab1col2 = [
        [sg.Text('Protect VM')],
        [sg.Listbox([''], size=(40, 4), enable_events=True, key='t1f02')],
        ]
    tab1col3 = []
    tab1col4 = [
        [sg.Text('Production Journal Datastore')],
        [sg.Table(values=[""], headings=['Datastore', 'Cap(MB)', 'FreeCap(MB)'],
                  select_mode=sg.TABLE_SELECT_MODE_BROWSE, vertical_scroll_only=False, def_col_width=11,
                  enable_events=True, auto_size_columns=False, justification='right', num_rows=3, key='t1f03')],
        ]
    tab1col5 = [
        [sg.Text('Copy RP Cluster')],
        [sg.Listbox(['GUI tool to check REST curl command'], size=(20, 4), enable_events=True, key='t1f04')],
        ]
    tab1col6 = [
        [sg.Text('Datastore for Copy VM')],
        [sg.Table(values=[""], headings=['Datastore', 'Cap(MB)', 'FreeCap(MB)'],
                  select_mode=sg.TABLE_SELECT_MODE_BROWSE, vertical_scroll_only=False, def_col_width=11,
                  enable_events=True, auto_size_columns=False, justification='right', num_rows=3, key='t1f05')],
        ]
    tab1col7 = [
        [sg.Text('Copy Journal Datastore')],
        [sg.Table(values=[""], headings=['Datastore', 'Cap(MB)', 'FreeCap(MB)'],
                  select_mode=sg.TABLE_SELECT_MODE_BROWSE, vertical_scroll_only=False, def_col_width=11,
                  enable_events=True, auto_size_columns=False, justification='right', num_rows=3, key='t1f06')]
    ]
    tab1col8 = [
        [sg.Text('Add-To Consistency Groups')],
        [sg.Table(values=[""],
                  headings=['cgName', 'prodRpClusterName', 'transferStatus', 'status', 'prodVcName'],
                  select_mode=sg.TABLE_SELECT_MODE_BROWSE, vertical_scroll_only=False, def_col_width=18,
                  enable_events=True, auto_size_columns=False, justification='center', num_rows=3, key='t1f07')],
        ]
    tab1col9 = [
        [sg.Text('Datastore for Copy VM')],
        [sg.Table(values=[""], headings=['Datastore', 'Cap(MB)', 'FreeCap(MB)'],
                  select_mode=sg.TABLE_SELECT_MODE_BROWSE, vertical_scroll_only=False, def_col_width=11,
                  enable_events=True, auto_size_columns=False, justification='right', num_rows=3, key='t1f08')],
        ]
    tab1 = sg.Tab('Protect VM', [
            [sg.Frame('Production', [
                [sg.Column(tab1col1, vertical_alignment='top'), sg.Column(tab1col2, vertical_alignment='top'), sg.Column(tab1col3, vertical_alignment='top')],
            ])],
            [sg.Frame('Copy', [
                [sg.Column(tab1col4, vertical_alignment='top'), sg.Column(tab1col5, vertical_alignment='top'), sg.Column(tab1col6, vertical_alignment='top'), sg.Column(tab1col7, vertical_alignment='top')],
                [sg.Submit('PROTECT VM', disabled=True)]
            ])],
            [sg.Frame('Add VM to existing consistency group', [
                [sg.Column(tab1col8, vertical_alignment='top'), sg.Column(tab1col9, vertical_alignment='top')],
                [sg.Submit('ADD VM', disabled=True)]
            ])],
    ])
    tab2col1 = [[sg.Text('bookmarkName')], [sg.Text('consistencyType')], [sg.Text('consolidationPolicy')]]
    tab2col2 = [[sg.InputText(default_text='TEST BOOKMARK', size=(30, 1), key='t2f02')],
                [sg.Combo(['CRASH_CONSISTENT', 'APPLICATION_CONSISTENT'], default_value='APPLICATION_CONSISTENT',
                          size=(30, 1), readonly=True, key='t2f03')],
                [sg.Combo(['NEVER_CONSOLIDATE', 'ALWAYS_CONSOLIDATE', 'DAILY_CONSOLIDATION', 'WEEKLY_CONSOLIDATION',
                           'MONTHLY_CONSOLIDATION'], default_value='NEVER_CONSOLIDATE', size=(30, 1), readonly=True,
                          key='t2f04')]]
    tab2 = sg.Tab('Create Bookmark',
        [
            [sg.Frame('Consistency Groups', [
                [sg.Table(values=[""],
                          headings=['cgName', 'prodRpClusterName', 'transferStatus', 'status', 'prodVcName'],
                          select_mode=sg.TABLE_SELECT_MODE_BROWSE, vertical_scroll_only=False, def_col_width=22,
                          enable_events=True, auto_size_columns=False, justification='center', num_rows=5, key='t2f01')],
                ])],
            [sg.Frame('Bookmark', [
                [sg.Column(tab2col1, vertical_alignment='top'), sg.Column(tab2col2, vertical_alignment='top')],
                [sg.Submit('CREATE BOOKMARK', disabled=True)],
            ])],
        ])
    tab3col1 = [[sg.Listbox([''], size=(20, 2), enable_events=True, key='t3f02')]]
    tab3col2 = [[sg.Table(values=[""],
                      headings=['date', 'bookmarkName', 'consistencyType', 'snapshotId'],
                      select_mode=sg.TABLE_SELECT_MODE_BROWSE, vertical_scroll_only=True, def_col_width=21,
                      enable_events=True, auto_size_columns=False, justification='center', num_rows=5, key='t3f03')]]
    tab3 = sg.Tab('Test a Copy',
        [
            [sg.Frame('Consistency Groups', [
                [sg.Table(values=[""],
                          headings=['cgName', 'prodRpClusterName', 'transferStatus', 'status', 'prodVcName'],
                          select_mode=sg.TABLE_SELECT_MODE_BROWSE, vertical_scroll_only=False, def_col_width=22,
                          enable_events=True, auto_size_columns=False, justification='center', num_rows=5, key='t3f01')]
            ])],
            [sg.Frame('Snapshots', [
                [sg.Column(tab3col1, vertical_alignment='top'), sg.Column(tab3col2, vertical_alignment='top')],
                [sg.Checkbox('Use the latest snapshot (If select individual snapshots and the latest snapshot, the latest snapshot will be selected.)', default=True, enable_events=True, key='t3f04')]
            ])],
            [sg.Frame('Test copy scenario',[
                [sg.Radio('TEST_COPY', group_id='t31', key='t3f05', default=True), sg.Radio('FAILOVER', group_id='t31', key='t3f06'), sg.Radio('RECOVER_PRODUCTION', group_id='t31', key='t3f07')]
            ])],
            [sg.Frame('Test network type', [
                [sg.Radio('ISOLATED_PER_CG', group_id='t32', key='t3f08', default=True),
                 sg.Radio('ISOLATED_PER_CG', group_id='t32', key='t3f09'),
                 sg.Radio('SHARED_PER_ESX', group_id='t32', key='t3f10'),
                 sg.Radio('FAILOVER_NETWORK', group_id='t32', key='t3f11')]
            ])],
            [sg.Submit('TEST A COPY', disabled=True)]
        ])
    tab4 = sg.Tab('Recovery Activities',
        [
            [sg.Frame('Recovery Activities', [
                [sg.Table(values=[""],
                          headings=['activityType', 'groupName', 'rpClusterName', 'status'],
                          select_mode=sg.TABLE_SELECT_MODE_BROWSE, vertical_scroll_only=False, def_col_width=29,
                          enable_events=True, auto_size_columns=False, justification='center', num_rows=5, key='t4f01')],
                [sg.Submit('STOP ACTIVITY', disabled=True), sg.Submit('FAILOVER', disabled=True), sg.Submit('RECOVER PRODUCTION', disabled=True)],
            ])],
            [sg.Frame('Transactions', [
                [sg.Table(values=[""],
                          headings=['timeCreated', 'type', 'status', 'progressPercentage', 'id'],
                          select_mode=sg.TABLE_SELECT_MODE_BROWSE, vertical_scroll_only=False, def_col_width=26,
                          enable_events=True, auto_size_columns=False, justification='center', num_rows=5, key='t4f02')],
            ])],
            [sg.Frame('VMs', [
                [sg.Table(values=[""],
                          headings=['vmName', 'rpClusterName', 'groupName', 'status', 'role'],
                          select_mode=sg.TABLE_SELECT_MODE_BROWSE, vertical_scroll_only=False, def_col_width=26,
                          enable_events=True, auto_size_columns=False, justification='center', num_rows=5, key='t4f03')],
            ])],
        ])
    tab5 = sg.Tab('Remove CG',
        [
            [sg.Frame('Consistency Groups', [
                [sg.Table(values=[""],
                          headings=['cgName', 'prodRpClusterName', 'transferStatus', 'status', 'prodVcName'],
                          select_mode=sg.TABLE_SELECT_MODE_BROWSE, vertical_scroll_only=False, def_col_width=22,
                          enable_events=True, auto_size_columns=False, justification='center', num_rows=5, key='t5f01')],
                ])],
            [sg.Submit('REMOVE', disabled=True)],
        ])
    sub_layout = [
        [sg.Submit('REFRESH'), sg.Submit('EXIT')],
        [sg.TabGroup([[tab1, tab2, tab3, tab4, tab5]], tab_background_color='#ccc', selected_title_color='#ff0', selected_background_color='#000')],
        [sg.Frame('Output', layout=outputwin)]
    ]
    return sg.Window("", sub_layout, finalize=True)

def rp_get_status(rp, window, gmtTimeDifferenceHour):
    r = rp.get_rpsystems()
    rpSystemId = r.json()[0]['id']
    df_rpclusters = utils.defDfRpclusters(rp, rpSystemId)
    window['t1f01'].update([i[0] for i in df_rpclusters[['name']].values])
    window['t1f04'].update([i[0] for i in df_rpclusters[['name']].values])
    df_vmDatastores = utils.defDfvmDatastores(rp, df_rpclusters)
    df_protect_vms = utils.defDfProtectVms(rp)
    df_journalDatastores = utils.defDfJournalDatastores(rp, df_rpclusters)
    df_groups = utils.defDfGroups(rp)
    if len(df_groups) != 0:
        window['t1f07'].update(
            df_groups[['name', 'prodRpClusterName', 'transferStatus', 'status', 'prodVcName']].values.tolist())
        window['t2f01'].update(
            df_groups[['name', 'prodRpClusterName', 'transferStatus', 'status', 'prodVcName']].values.tolist())
        window['t3f01'].update(
            df_groups[['name', 'prodRpClusterName', 'transferStatus', 'status', 'prodVcName']].values.tolist())
        window['t5f01'].update(
            df_groups[['name', 'prodRpClusterName', 'transferStatus', 'status', 'prodVcName']].values.tolist())
    df_groupsRecoveryActivities = utils.defDfGroupsRecoveryActivities(rp)
    if len(df_groupsRecoveryActivities) == 0:
        window['t4f01'].update([''])
    else:
        window['t4f01'].update(
            df_groupsRecoveryActivities[['activityType', 'groupName', 'rpClusterName', 'status']].values.tolist())
    df_transactions = utils.defDfTransactions(rp, gmtTimeDifferenceHour)
    if len(df_transactions) != 0:
        window['t4f02'].update(df_transactions[['timeCreated2', 'type', 'status', 'progressPercentage', 'id']].values.tolist())
    df_rpsystemsVms = utils.defDfRpsystemsVms(rp, rpSystemId)
    if len(df_rpsystemsVms) != 0:
        window['t4f03'].update(df_rpsystemsVms[['name', 'rpClusterName', 'groupName', 'status', 'role']].values.tolist())
    return df_rpclusters, df_vmDatastores, df_protect_vms, df_journalDatastores, df_groups, df_groupsRecoveryActivities, df_transactions

def main():
    window = windows_main()
    while True:
        #event, values = window.read(timeout=1000 * 60, timeout_key='-TIMEOUT-')
        event, values = window.read(timeout_key='-TIMEOUT-')
        if event == sg.WIN_CLOSED or event == 'EXIT':
            break
        elif event == 'SAVE VALUES':
            section1 = "Section1"
            config.set(section1, 'server_ip', values['m1f01'])
            config.set(section1, 'user', values['m1f02'])
            config.set(section1, 'password', values['m1f03'])
            config.set(section1, 'gmt_time_difference', values['m1f04'])
            with open('config.ini', 'w') as file:
                config.write(file)

        elif event == 'CONNECT':
            headers = utils.AuthEncode(values['m1f02'], values['m1f03'])
            pluginServerIp = values['m1f01']
            gmtTimeDifferenceHour = int(values['m1f04'])
            rp = utils.Reprp(pluginServerIp, headers, True)
            r = rp.get_rpsystems()
            if type(r) is str:
                sg.Popup(f'Connection Error.\n{r}')
            elif str(r.status_code)[:2] != '20':
                sg.Popup('HTTP Error. Please check your user ID and password.')
            else:
                # メインウィンドウを閉じて、サブウィンドウを作成して表示する
                window.close()
                window = windows_sub()
                df_rpclusters, df_vmDatastores, df_protect_vms, df_journalDatastores, df_groups, df_groupsRecoveryActivities, df_transactions = rp_get_status(rp, window, gmtTimeDifferenceHour)

        elif event == 'REFRESH' or event == '-TIMEOUT-':
            df_rpclusters, df_vmDatastores, df_protect_vms, df_journalDatastores, df_groups, df_groupsRecoveryActivities, df_transactions = rp_get_status(rp, window, gmtTimeDifferenceHour)

        elif event == 'PROTECT VM':
            prodClusterName = values['t1f01'][0]
            prodClusterId = df_rpclusters['id'][df_rpclusters['name'] == prodClusterName].values[0]
            protectVmName = values['t1f02'][0]
            protectVmId = df_protect_vms['id'][df_protect_vms['name'] == protectVmName].values[0]
            prodJournalDatastoreName = df_journalDatastores[prodClusterName].loc[values['t1f03'][0], 'name']
            prodJournalDatastoreId = df_journalDatastores[prodClusterName].loc[values['t1f03'][0], 'id']
            copyClusterName = values['t1f04'][0]
            copyClusterId = df_rpclusters['id'][df_rpclusters['name'] == copyClusterName].values[0]
            copyDatastoreName = df_vmDatastores[copyClusterName].loc[values['t1f05'][0], 'name']
            copyDatastoreId = df_vmDatastores[copyClusterName].loc[values['t1f05'][0], 'id']
            copyJournalDatastoreName = df_journalDatastores[copyClusterName].loc[values['t1f06'][0], 'name']
            copyJournalDatastoreId = df_journalDatastores[copyClusterName].loc[values['t1f06'][0], 'id']
            r = rp.post_vms_protect_defaults(prodClusterId, protectVmId, prodJournalDatastoreId, copyClusterId, copyDatastoreId, copyJournalDatastoreId)
            r = rp.post_vms_protect(r.text)

        elif event == 'ADD VM':
            prodClusterName = values['t1f01'][0]
            prodClusterId = df_rpclusters['id'][df_rpclusters['name'] == prodClusterName].values[0]
            protectVmName = values['t1f02'][0]
            protectVmId = df_protect_vms['id'][df_protect_vms['name'] == protectVmName].values[0]
            groupId = df_groups.loc[values['t1f07'][0], 'id']
            vmDatastoreId = df_vmDatastores[addVmCopyClusterName] .loc[values['t1f07'][0], 'id']
            r = rp.post_vms_add_defaults(prodClusterId, protectVmId, groupId)
            t01 = r.text
            t01 = t01.replace(r.json()['replicaChangesConfiguration'][0]['vmDatastore'], vmDatastoreId)
            r = rp.post_vms_add(groupId, t01)

        elif event == 'CREATE BOOKMARK':
            bookmarkName = values['t2f02']
            consistencyType = values['t2f03']
            consolidationPolicy = values['t2f04']
            groupId = df_groups.loc[values['t2f01'][0], 'id']
            r = rp.post_create_bookmarks(groupId, bookmarkName, consistencyType, consolidationPolicy)

        elif event == 'TEST A COPY':
            if values['t3f04'] == True:
                snapshotId = 'latest'
            else:
                snapshotId = df_cgSnapshot.loc[values['t3f03'][0], 'id']
            groupId = df_groups.loc[values['t3f01'][0], 'id']
            r = rp.get_groups_copies(groupId)
            df = pd.read_json(r.text)
            copyId = df['id'][df['copyRole'] == values['t3f02'][0]].values[0]
            if values['t3f05'] == True:
                scenario = 'TEST_COPY'
            elif values['t3f06'] == True:
                scenario = 'FAILOVER'
            elif values['t3f07'] == True:
                scenario = 'RECOVER_PRODUCTION'
            if values['t3f08'] == True:
                testNetworkType = 'ISOLATED_PER_CG'
            elif values['t3f09'] == True:
                testNetworkType = 'ISOLATED_PER_CG'
            elif values['t3f10'] == True:
                testNetworkType = 'SHARED_PER_ESX'
            elif values['t3f11'] == True:
                testNetworkType = 'FAILOVER_NETWORK'
            r = rp.post_testcopy(groupId, copyId, snapshotId, scenario, testNetworkType)

        elif event == 'STOP ACTIVITY':
            groupId = df_groupsRecoveryActivities.loc[values['t4f01'][0], 'groupId']
            copyId = df_groupsRecoveryActivities.loc[values['t4f01'][0], 'copyId']
            r = rp.delete_stop_testcopy(groupId, copyId)
            time.sleep(3)
            df_groupsRecoveryActivities = utils.defDfGroupsRecoveryActivities(rp)
            if len(df_groupsRecoveryActivities) == 0:
                window['t4f01'].update([''])
            else:
                window['t4f01'].update(df_groupsRecoveryActivities[['activityType', 'groupName', 'rpClusterName', 'status']].values.tolist())

        elif event == 'FAILOVER':
            groupId = df_groupsRecoveryActivities.loc[values['t4f01'][0], 'groupId']
            copyId = df_groupsRecoveryActivities.loc[values['t4f01'][0], 'copyId']
            r = rp.post_failover(groupId, copyId)
            time.sleep(3)
            df_groupsRecoveryActivities = utils.defDfGroupsRecoveryActivities(rp)
            if len(df_groupsRecoveryActivities) == 0:
                window['t4f01'].update([''])
            else:
                window['t4f01'].update(df_groupsRecoveryActivities[['activityType', 'groupName', 'rpClusterName', 'status']].values.tolist())

        elif event == 'RECOVER PRODUCTION':
            groupId = df_groupsRecoveryActivities.loc[values['t4f01'][0], 'groupId']
            copyId = df_groupsRecoveryActivities.loc[values['t4f01'][0], 'copyId']
            r = rp.post_recover_production(groupId, copyId)
            time.sleep(3)
            df_groupsRecoveryActivities = utils.defDfGroupsRecoveryActivities(rp)
            if len(df_groupsRecoveryActivities) == 0:
                window['t4f01'].update([''])
            else:
                window['t4f01'].update(df_groupsRecoveryActivities[['activityType', 'groupName', 'rpClusterName', 'status']].values.tolist())

        elif event == 'REMOVE':
            groupId = df_groups.loc[values['t5f01'][0], 'id']
            r = rp.delete_group(groupId)
            time.sleep(3)
            df_groups = utils.defDfGroups(rp)
            if len(df_groups) != 0:
                window['t1f07'].update(df_groups[['name', 'prodRpClusterName', 'transferStatus', 'status', 'prodVcName']].values.tolist())
                window['t2f01'].update(df_groups[['name', 'prodRpClusterName', 'transferStatus', 'status', 'prodVcName']].values.tolist())
                window['t3f01'].update(df_groups[['name', 'prodRpClusterName', 'transferStatus', 'status', 'prodVcName']].values.tolist())
                window['t5f01'].update(df_groups[['name', 'prodRpClusterName', 'transferStatus', 'status', 'prodVcName']].values.tolist())

        elif event == 't0f01':
            if values['t0f01'] == True:
                rp = utils.Reprp(pluginServerIp, headers, False)
            else:
                rp = utils.Reprp(pluginServerIp, headers, True)

        elif event == 't1f01':
            rpClusterName = values['t1f01'][0]
            t01 = df_protect_vms['name'][df_protect_vms['rpClusterName'] == rpClusterName].values
            window['t1f02'].update(t01)
            t02 = df_journalDatastores[rpClusterName][['name', 'capacityInMB', 'freeSpaceInMB']].values.tolist()
            window['t1f03'].update(t02)

        elif event == 't1f04':
            rpClusterName = values['t1f04'][0]
            t01 = df_vmDatastores[rpClusterName][['name', 'capacityInMB', 'freeSpaceInMB']].values.tolist()
            window['t1f05'].update(t01)
            t02 = df_journalDatastores[rpClusterName][['name', 'capacityInMB', 'freeSpaceInMB']].values.tolist()
            window['t1f06'].update(t02)

        elif event == 't1f07':
            if len(values['t1f01']) == 0 or len(values['t1f02']) == 0:
                sg.popup('First select Production RP Cluster and Protect VM.')
            else:
                prodClusterName = values['t1f01'][0]
                prodClusterId = df_rpclusters['id'][df_rpclusters['name'] == prodClusterName].values[0]
                protectVmName = values['t1f02'][0]
                protectVmId = df_protect_vms['id'][df_protect_vms['name'] == protectVmName].values[0]
                groupId = df_groups.loc[values['t1f07'][0], 'id']
                r = rp.post_vms_add_defaults(prodClusterId, protectVmId, groupId)
                vmDatastoreId = r.json()['replicaChangesConfiguration'][0]['vmDatastore']
                for i in df_vmDatastores:
                    if len(df_vmDatastores[i][df_vmDatastores[i]['id'] == vmDatastoreId]) != 0:
                        t01 = df_vmDatastores[i][['name', 'capacityInMB', 'freeSpaceInMB']].values.tolist()
                        addVmCopyClusterName = i
                window['t1f08'].update(t01)

        elif event == 't3f01':
            if len(values['t3f01']) != 0:
                groupId = df_groups.loc[values['t3f01'][0], 'id']
            r = rp.get_groups_copies(groupId)
            df = pd.read_json(r.text)
            t01 = df['copyRole'][df['copyRole'].str.contains('REPLICA')].values.tolist()
            window['t3f02'].update(t01)
            window['t3f03'].update([""])

        elif event == 't3f02':
            if len(values['t3f01']) != 0:
                groupId = df_groups.loc[values['t3f01'][0], 'id']
            r = rp.get_groups_copies(groupId)
            df = pd.read_json(r.text)
            copyId = df['id'][df['copyRole'] == values['t3f02'][0]].values[0]
            df_cgSnapshot = utils.defDfCgSnapshot(rp, groupId, copyId, gmtTimeDifferenceHour)
            window['t3f03'].update(df_cgSnapshot[['timestamp2', 'bookmarkName', 'consistencyType', 'id']].values.tolist())

        ### submit button : enable / disable ###
        for i in values:
            if i == 't1f01':
                if len(values['t1f01']) == 0 or len(values['t1f02']) == 0 or len(values['t1f03']) == 0 or len(values['t1f04']) == 0 or len(values['t1f05']) == 0 or len(values['t1f06']) == 0:
                    window['PROTECT VM'].update(disabled=True)
                else:
                    window['PROTECT VM'].update(disabled=False)
                if len(values['t1f01']) == 0 or len(values['t1f02']) == 0 or len(values['t1f07']) == 0 or len(values['t1f08']) == 0:
                    window['ADD VM'].update(disabled=True)
                else:
                    window['ADD VM'].update(disabled=False)
                if len(values['t2f01']) == 0:
                    window['CREATE BOOKMARK'].update(disabled=True)
                else:
                    window['CREATE BOOKMARK'].update(disabled=False)
                if len(values['t3f01']) == 0 or len(values['t3f02']) == 0:
                    window['TEST A COPY'].update(disabled=True)
                else:
                    window['TEST A COPY'].update(disabled=False)
                if len(values['t4f01']) == 0:
                    window['STOP ACTIVITY'].update(disabled=True)
                    window['RECOVER PRODUCTION'].update(disabled=True)
                    window['FAILOVER'].update(disabled=True)
                else:
                    if  len(df_groupsRecoveryActivities) != 0:
                        window['STOP ACTIVITY'].update(disabled=False)
                        if df_groupsRecoveryActivities.loc[values['t4f01'][0], 'activityType'] == "RECOVER_PRODUCTION" and df_groupsRecoveryActivities.loc[values['t4f01'][0], 'status'] == "READY_FOR_TESTING":
                            window['RECOVER PRODUCTION'].update(disabled=False)
                        if df_groupsRecoveryActivities.loc[values['t4f01'][0], 'activityType'] == "FAILOVER" and df_groupsRecoveryActivities.loc[values['t4f01'][0], 'status'] == "READY_FOR_TESTING":
                            window['FAILOVER'].update(disabled=False)
                if len(values['t5f01']) == 0:
                    window['REMOVE'].update(disabled=True)
                else:
                    window['REMOVE'].update(disabled=False)
    window.close()

if __name__ == '__main__':
    main()
