import json
temp = '{"error_no":0,"error_msg":"","result":{"is_login":1,"welfare_redpacket":{"new_guest_redpacket":[{"red_package_location":1,"money":"13","status":1,"end_date":"2018-11-03"},{"red_package_location":2,"money":"5.0","status":-1,"end_date":""},{"red_package_location":3,"money":"8.0","status":-1,"end_date":""}],"super_member_redpacket":[],"task_start_time":1540649581,"version":2},"is_completed":0,"created_date":"2018-10-27","completed_date":"","remaining_days":-19}}'
temp2 = json.loads(temp)['result']['welfare_redpacket']['new_guest_redpacket']
temp3 = temp2[1]
if temp3['end_date']== '':
    print(11)
print(temp3['end_date'])
print(temp3)
