#coding:utf-8
import xlrd,json,time,datetime
# get data from an excel
class deal_data(object):
    def __init__(self):
        self.timesheet = []
        self.disposal_data = {}
    def testXlrd(self,filename):
        book = xlrd.open_workbook(filename)
        sh = book.sheet_by_index(0)
        nrows = sh.nrows
        colnames_en = ['company_name', 'area', 'product_line', 'product_line_second', 'pdu', 'job_number', 'name',
                       'office_time', 'closing_time']
        timesheet = []
        # print sh.row_values(1)
        for rownum in range(1, nrows):
            row = sh.row_values(rownum)
            if row:
                app = {}
                for i in range(len(colnames_en)):
                    app[colnames_en[i]] = row[i]

                timesheet.append(app)

        self.timesheet = timesheet

    # classify data
    def classify(self):
        lst = self.timesheet
        disposal_data = {}
        for item in range(0, len(lst)):
            temp = lst[item]
            if temp['job_number'] in disposal_data.keys():

                disposal_data[temp['job_number']].append(  {'closing_time': temp['closing_time'], 'office_time': temp['office_time']})
            else:
                disposal_data[temp['job_number']] = [
                    {'company_name': temp['company_name'], 'area': temp['area'], 'product_line': temp['product_line'],
                     'product_line_second': temp['product_line_second'], 'pdu': temp['pdu'],
                     'job_number': temp['job_number'], 'name': temp['name'], 'closing_time': temp['closing_time'],
                     'office_time': temp['office_time']}]

        self.disposal_data = disposal_data


    def timestamp_compare(self,lst,timeRange):

        main_info = {'count': len(lst), 'company_name': lst[0]['company_name'], 'area': lst[0]['area'],
                     'product_line': lst[0]['product_line'], 'product_line_second': lst[0]['product_line_second'],
                     'pdu': lst[0]['pdu'], 'job_number': lst[0]['job_number'], 'name': lst[0]['name'], 'late_times': 0,
                     'quit_times': 0, 'late_time': 0, 'quit_time': 0, 'add_time': 0,'nci':0}

        for index in range(0, len(lst)):
            temp = lst[index]
            if len(temp['office_time']) > 6:
                # 迟到时间
                office_time = temp['office_time']
                job_office_time = office_time.split()[0] + ' ' + timeRange['officeTime']
                office_time = timeTostamp(office_time)
                job_office_time = timeTostamp(job_office_time)

                # 迟到
                if office_time > job_office_time:
                    main_info['late_times'] += 1
                    temp_time = office_time - job_office_time
                    if temp_time % 1800 != 0:
                        main_info['late_time'] += (temp_time // 1800 + 1) * 0.5
                    else:
                        main_info['late_time'] += (temp_time // 1800) * 0.5
            else:
                main_info['nci'] += 1

            # 早退、 加班
            if len(temp['closing_time']) > 6:
                closing_time = temp['closing_time']
                job_closing_time = closing_time.split()[0] + ' ' + timeRange['closingTime']
                job_add_time = closing_time.split()[0] + ' ' + timeRange['addTime']
                job_add_time = timeTostamp(job_add_time)
                closing_time = timeTostamp(closing_time)
                job_closing_time = timeTostamp(job_closing_time)
                # 早退
                if closing_time < job_closing_time:
                    main_info['quit_times'] += 1
                    temp_time = job_closing_time - closing_time

                    if temp_time % 1800 != 0:
                        main_info['quit_time'] += (temp_time // 1800 + 1) * 0.5
                    else:
                        main_info['quit_time'] += (temp_time // 1800) * 0.5
                # 加班
                if closing_time > job_add_time:
                    main_info['add_time'] += (closing_time - job_add_time)
            else:
                main_info['nci'] += 1


        main_info['add_time'] = round(main_info['add_time'] / 3600,2)
        return main_info

#create a json file based on lst
def dump(lst):
    fp = open("lst.json", "w")
    fp.write(json.dumps(lst, encoding='UTF-8', ensure_ascii=False))
    fp.close()

# string to timestamp
def timeTostamp(sometime):
    sometime = sometime[:-2].strip()
    return time.mktime(datetime.datetime.strptime(sometime, '%Y-%m-%d %H:%M:%S').timetuple())





