#coding:utf-8
from model3 import *
from course_manip import *
import re,time

#result = a.query.order_by('id desc').filter_by(id=1).first()
#print 'Result status is %s' % result.status
#a.modify_status_with_id(1,3)
#print 'Result status is %s' % result.status


a=Mua()
while True:
    start_time=time.time()
    #add to the working list
    ls0 = a.query.order_by('id desc').filter_by(status=0).all()
    status0_id_list=[]
    for x in ls0:
        status0_id_list.append(x.id)
    print status0_id_list
    for status_id in status0_id_list:
        print a.modify_status_with_id(status_id,1)
    #very important!记得提交修改
    db.session.commit()
    ls1 = a.query.order_by('id desc').filter_by(status=1).all()
    for x in ls1:
        # 如果except超过5次，标记为失败
        if x.errorcount>=5:
            a.modify_status_with_sid(x.sid,3)
            print 'except more than 5 times'
            continue

        instance=course_manip(x.sid,x.cookies)
        try:
            selected_list=instance.get_selected_course_unselected_course_unselected_empty(eval(x.mode))['selected_course_number']
            unselected_course_number=instance.get_selected_course_unselected_course_unselected_empty(eval(x.mode))['unselected_course_number']
            unselected_course_empty=instance.get_selected_course_unselected_course_unselected_empty(eval(x.mode))['unselected_course_empty']
        except:
            a.modify_errorcount_with_sid_add_one(x.sid)
            print 'ERROR +1 !'
            continue
        # 【只抢不退】
        if x.drop=='omit':
            position=unselected_course_number.index(x.select)
            # 如果有空位，选课，并检查
            if eval(unselected_course_empty[position])>0:
                # 选课
                instance.select_course(x.select)
                # 更新列表！注意！用新的instance覆盖旧的
                instance=course_manip(x.sid,x.cookies)
                # 获取新的列表
                selected_list=instance.get_selected_course_unselected_course_unselected_empty(eval(x.mode))['selected_course_number']
                # 如果选课成功，更新状态为2(成功)，否则不更新状态
                if x.select in selected_list:
                    a.modify_status_with_sid(x.sid,2)
                    db.session.commit()
                # 不成功，不检查
                else:
                    pass
            # 没空位，跳过
            else:
                pass
        # 【先退后抢】，1 检查是否有空位 没有跳过  2 有空位，退课，立刻选课  3.检查是否选课成功，如果成功更新状态 4选课失败，选回原课程
        else:
            position=unselected_course_number.index(x.select)
            # 如果有空位，先退课，后选课
            if eval(unselected_course_empty[position])>0:
                instance.drop_course(x.drop)
                instance.select_course(x.select)
                # 获取新的已选课列表
                instance=course_manip(x.sid,x.cookies)
                selected_list=instance.get_selected_course_unselected_course_unselected_empty(eval(x.mode))['selected_course_number']
                # 如果选成功了，更新状态到2成功态
                if x.select in selected_list:
                    a.modify_status_with_sid(x.sid,2)
                    db.session.commit()
                # 如果一开始就没退成功
                elif x.drop in selected_list:
                    pass
                # 选回原来的课程
                else:
                    instance.select_course(x.drop)
        # final commit
        db.session.commit()
        end_time=time.time()
        time_interval=end_time-start_time
        # 减少提交频率
        time.sleep(1)
        if time_interval<8:
            time.sleep(8-time_interval)
        elif time_interval<12:
            time.sleep(12-time_interval)
        else:
            pass



# 已选 //*[@id="elected"]/tbody/tr[1]/td[9]

# exp: //*[@id="courses"]/tbody/tr/td[8]/text()
# //*[@id="courses"]/tbody/tr[2]/td[8]
# //*[@id="courses"]/tbody/tr[20]/td[8]

# //*[@id="courses"]/tbody/tr[1]/td[8]