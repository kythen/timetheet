timesheetApp.controller('timesheetCtrl',['$scope','$http',timesheet]);
function timesheet(scope,http){
        //初始化上下班时间
        if(localStorage.getItem('timeRange')){
            scope.timeRange = JSON.parse(localStorage.getItem('timeRange'));
        }else{
            scope.timeRange = {officeTime:"09:00:59.0",closingTime:"17:30:00.0",addTime:"19:00:00.0"};
        }
        scope.getTimesheet = function(){
                localStorage.setItem('timeRange',JSON.stringify(scope.timeRange));
                var file = document.querySelector('#file1').files[0];

                if(!file){
                    alert("请选择一个excel表！")
                    return
                }

                http({
                         method:'get',
                         url:'/about',
                         charset:'utf-8',
                         params:{'fileName':file.name,'timeRange':scope.timeRange}

                     }).success(function(data){
                                     if(data.errCode == 0){
                                        alert('请确认选择了E:/table/下的Excel表格');
                                     }else{
                                        scope.timesheet = data;
                                     }

                                })
                        .error(function(e){
                                    console.log(e)
                                })
        };

        scope.jumptoDetail = function(job_number){

           window.open('detail.html?job_number='+job_number);
        };

}
detailApp.controller("detailCtrl",['$scope','$http',detail])
function detail(scope,http){
    scope.timeRange = GetUrlParameters('timeRange');
    console.log(JSON.stringify(scope.timeRange));
    http({
        method:'get',
        url:'/detail',
        params:{'job_number':GetUrlParameters('job_number')}
    }).success(function(data){

        scope.detail = data;

    })
    scope.timeCompare = function(tt,apm){

            scope.timeRange = JSON.parse(localStorage.getItem('timeRange'));
            time = tt.replace(/(^\s*)/,"");
            date = time.split(' ')[0];
            timeOffice = date + ' '+scope.timeRange.officeTime;
            timeClosing = date + ' ' + scope.timeRange.closingTime;
            timeAdd = date + ' ' + scope.timeRange.addTime;

            timeStamp = timetoStamp(time);
            timeOfficeStamp = timetoStamp(timeOffice);
            timeClosingStamp = timetoStamp(timeClosing);
            timeAddStamp = timetoStamp(timeAdd);

            if(apm == 'am'){
                if(timeStamp > timeOfficeStamp){
                    return 'bad';
                }
            }else if(apm == 'pm'){
                if(timeStamp < timeClosingStamp){
                    return 'bad';
                }else if(timeStamp > timeAddStamp){
                    return 'well';
                }
            }

        }
}
function GetUrlParameters(name){
     var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
     var r = window.location.search.substr(1).match(reg);
     if(r!=null)
           return  unescape(r[2]);
     return null;
 }

function timetoStamp(str){

    return new Date(str).getTime();
}