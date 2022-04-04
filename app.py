from colorama import Fore, Style
from getpass import getpass
from service.user_service import UserService
from service.news_service import NewsService
from service.role_service import RoleService
from service.type_service import TypeService
import os
import sys
import time

__user_service = UserService()
__news_service = NewsService()
__role_service = RoleService()
__type_service = TypeService()

while True:
    # 清空控制台内容 - macOS系统是clear
    os.system("clear")
    print(Fore.LIGHTBLUE_EX, "================")
    print(Fore.LIGHTBLUE_EX, "欢迎使用新闻管理系统")
    print(Fore.LIGHTBLUE_EX, "================")
    print(Fore.LIGHTGREEN_EX, "\n\t1. 登陆系统\n\t2. 退出系统")
    print(Style.RESET_ALL)

    option = input("请输出操作编号: ")

    # 大菜单 - 登陆系统
    if option == '1':
        username = input("用户名: ")
        password = getpass("密码: ")
        # 调用用户登录接口
        result = __user_service.login(username, password)
        # 如果登陆成功
        if result:
            # 查询身份
            role = __user_service.search_user_role(username)
            # 清屏并进入下一级菜单
            os.system("clear")

            while True:
                os.system('clear')
                if role == '新闻编辑':
                    print(Fore.LIGHTGREEN_EX, "======== 登陆成功，欢迎您{name} ========\n".format(name=username))
                    print(Fore.LIGHTGREEN_EX, '\t1. 发表新闻')
                    print(Fore.LIGHTGREEN_EX, '\t2. 编辑新闻')
                    print(Fore.LIGHTGREEN_EX, '\tback. 退出登陆')
                    print(Fore.LIGHTGREEN_EX, '\texit. 退出系统')
                    print(Style.RESET_ALL)
                    option = input("请输入操作编号：")

                    # 新闻编辑菜单 - 发表新闻
                    if option == '1':
                        os.system('clear')
                        title = input("请输入新闻标题：")
                        print(Fore.LIGHTBLUE_EX, "===== 请选择新闻类别 =====")
                        user_id = __user_service.search_user_id(username)
                        result = __type_service.print_type_list()
                        for index in range(len(result)):
                            one = result[index]
                            print(Fore.LIGHTBLUE_EX, '\t{}.{}'.format(index + 1, one[1]))
                        print(Style.RESET_ALL)
                        option = input("请输入新闻类别编号：")
                        type_id = result[int(option) - 1][0]
                        print("> 所有新闻均存放在: SampleNews/xxx.html")
                        path = input("请输入文件路径")
                        with open(path, 'r') as f:
                            content = f.read()
                        is_top = input("置顶级别(0~5): ")
                        is_commit = input("是否提交? (Y/N): ")
                        if is_commit.lower() == 'y':
                            __news_service.insert(title, user_id, type_id, content, is_top)
                            print("保存成功，即将自动返回")
                            time.sleep(2)
                        else:
                            print("放弃保存，即将返回")
                            time.sleep(2)

                    # 新闻编辑菜单 - 编辑新闻
                    elif option == '2':
                        current_page = 1
                        while True:
                            os.system('clear')
                            print(Fore.LIGHTRED_EX, "======== 编辑新闻 ========\n")
                            count_page = __news_service.count_news_pages()
                            result = __news_service.print_all_news(current_page)
                            for index in range(len(result)):
                                one = result[index]
                                print(Fore.LIGHTBLUE_EX,
                                      '\t%d\t%s\t%s\t%s' % (index + 1, one[1], one[2], one[3]))
                            print(Fore.LIGHTGREEN_EX, '======================')
                            print(Fore.LIGHTGREEN_EX, '\t第%d页，共%d页' % (current_page, count_page))
                            print(Fore.LIGHTGREEN_EX, '======================')
                            print(Fore.LIGHTGREEN_EX, '\n\tback.返回上一层\n\tprev.上一页\n\tnext.下一页')
                            print(Style.RESET_ALL)
                            option = input("请输入操作编号：")

                            if option == 'back':
                                break
                            elif option == 'prev' and current_page > 1:
                                current_page = current_page - 1
                            elif option == 'next' and current_page <= count_page:
                                current_page = current_page + 1
                            # 这里做一下error-handle，例如恶意输入字母以及超范围的数据
                            elif option.isdigit() and 1 <= int(option) <= 10:
                                os.system('clear')
                                try:
                                    news_id = result[int(option) - 1][0]
                                    result = __news_service.search_news_by_id(news_id)
                                    # result -> n.title,t.type,n.is_top
                                    title = result[0]
                                    news_type = result[1]
                                    is_top = result[2]
                                    print("\t新闻原标题：", title)
                                    new_title = input("请输入新的标题：")
                                    print("\t新闻原类型：", news_type)
                                    result = __type_service.print_type_list()
                                    print("===== 新闻类型选择 =====")
                                    for index in range(len(result)):
                                        one = result[index]
                                        print(Fore.LIGHTBLUE_EX, '\t{}.{}'.format(index + 1, one[1]))
                                    print(Style.RESET_ALL)
                                    option = input("请输入新的类型：")
                                    new_type_id = result[int(option) - 1][0]

                                    path = input("请输入内容路径(SampleNews/xxx.html)")
                                    with open(path, 'r') as f:
                                        content = f.read()

                                    print("\t新闻原置顶级别：", is_top)
                                    new_is_top = input("请输入新的置顶级别：(0-5)")
                                    if new_is_top.isdigit() and 0 <= int(new_is_top) <= 5:
                                        is_commit = input("\t是否提交? Y/N")
                                        if is_commit.lower() == 'y':
                                            __news_service.update_news(news_id, new_title, new_type_id, content,
                                                                       new_is_top)
                                            print(Fore.LIGHTGREEN_EX, '修改成功，即将自动返回')
                                            print(Style.RESET_ALL)
                                            time.sleep(2)
                                        else:
                                            print(Fore.LIGHTRED_EX, '操作取消！即将自动返回')
                                            time.sleep(2)
                                    else:
                                        print(Fore.LIGHTRED_EX, '序号有误！即将自动返回')
                                        time.sleep(2)
                                except ValueError as e:
                                    print(Fore.LIGHTRED_EX, '发生错误！无法执行！请检查序号是否正确')
                                    time.sleep(2)
                            else:
                                print(Fore.LIGHTRED_EX, "指令错误，请检查拼写或页码是否达到上限，请重新输入!")
                                time.sleep(2)
                    elif option == 'back':
                        break
                    elif option == 'exit':
                        sys.exit(0)
                    else:
                        print("操作指令有误！即将自动返回")
                        time.sleep(2)
                elif role == '管理员':
                    print(Fore.LIGHTGREEN_EX, "======== 登陆成功，欢迎您{name} ========\n".format(name=username))
                    print(Fore.LIGHTBLUE_EX, '\t1. 新闻管理')
                    print(Fore.LIGHTBLUE_EX, '\t2. 用户管理')
                    print(Fore.LIGHTRED_EX, '\tback.退出登陆')
                    print(Fore.LIGHTRED_EX, '\texit.退出系统')
                    print(Style.RESET_ALL)
                    option = input("请输入操作编号：")

                    # 管理员菜单 - 新闻管理
                    if option == '1':
                        while True:
                            os.system("clear")
                            print(Fore.LIGHTBLUE_EX, '===== 新闻管理 =====')
                            print(Fore.LIGHTBLUE_EX, '\t1. 审批新闻')
                            print(Fore.LIGHTBLUE_EX, '\t2. 删除新闻')
                            print(Fore.LIGHTRED_EX, '\tback.返回上一层')
                            print(Style.RESET_ALL)
                            option = input("请输入操作编号：")

                            # 新闻管理菜单 - 审批新闻
                            if option == '1':
                                current_page = 1
                                while True:
                                    os.system('clear')
                                    print(Fore.LIGHTGREEN_EX, "======== 审批新闻 ========\n")
                                    # 查看待审批的新闻列表和它们需要几页来展示
                                    count_page = __news_service.search_un_review_count_page()
                                    result = __news_service.search_un_review_list(current_page)
                                    # result -> [(1, '新闻标题1', '要闻', 'scott')]
                                    # 打印这一"页"包含的结果
                                    for index in range(len(result)):
                                        one = result[index]
                                        print(Fore.LIGHTBLUE_EX,
                                              '\t%d\t%s\t%s\t%s' % (index + 1, one[1], one[2], one[3]))
                                    print(Fore.LIGHTGREEN_EX, '======================')
                                    print(Fore.LIGHTGREEN_EX, '\t第%d页，共%d页' % (current_page, count_page))
                                    print(Fore.LIGHTGREEN_EX, '======================')
                                    print(Fore.LIGHTGREEN_EX, '\n\tback.返回上一层\n\tprev.上一页\n\tnext.下一页')
                                    print(Style.RESET_ALL)
                                    option = input("请输入操作编号：")

                                    if option == 'back':
                                        break
                                    elif option == 'prev' and current_page > 1:
                                        current_page = current_page - 1
                                    elif option == 'next' and current_page <= count_page:
                                        current_page = current_page + 1
                                    # 这里做一下error-handle，例如恶意输入字母以及超范围的数据，其中digit判断要先执行
                                    elif option.isdigit() and 1 <= int(option) <= 10:
                                        # 更新新闻状态，并将新闻缓存到Redis
                                        try:
                                            news_id = result[int(option) - 1][0]
                                            result = __news_service.search_target_cache(news_id)
                                            # result -> n.title,u.username,t.type,n.content_id,n.is_top,n.create_time
                                            title = result[0]
                                            username = result[1]
                                            news_type = result[2]
                                            content_id = result[3]
                                            news_content = __news_service.search_content_by_id(content_id)
                                            is_top = result[4]
                                            create_time = str(result[5])
                                            __news_service.cache_news(news_id, title, username, news_type, news_content,
                                                                      is_top, create_time)
                                            __news_service.update_un_review_news(news_id)
                                        except Exception as e:
                                            print(Fore.LIGHTRED_EX, '发生错误！无法执行！请检查序号是否正确')
                                            print("Error: ", e)
                                            time.sleep(2)
                                    else:
                                        print(Fore.LIGHTRED_EX, "指令错误，请检查拼写或页码是否达到上限，请重新输入!")
                                        time.sleep(2)

                            # 新闻管理菜单 - 删除新闻
                            if option == '2':
                                current_page = 1
                                while True:
                                    os.system('clear')
                                    print(Fore.LIGHTRED_EX, "======== 删除新闻 ========\n")
                                    count_page = __news_service.count_news_pages()
                                    result = __news_service.print_all_news(current_page)
                                    for index in range(len(result)):
                                        one = result[index]
                                        print(Fore.LIGHTBLUE_EX,
                                              '\t%d\t%s\t%s\t%s' % (index + 1, one[1], one[2], one[3]))
                                    print(Fore.LIGHTGREEN_EX, '======================')
                                    print(Fore.LIGHTGREEN_EX, '\t第%d页，共%d页' % (current_page, count_page))
                                    print(Fore.LIGHTGREEN_EX, '======================')
                                    print(Fore.LIGHTGREEN_EX, '\n\tback.返回上一层\n\tprev.上一页\n\tnext.下一页')
                                    print(Style.RESET_ALL)
                                    option = input("请输入操作编号：")

                                    if option == 'back':
                                        break
                                    elif option == 'prev' and current_page > 1:
                                        current_page = current_page - 1
                                    elif option == 'next' and current_page <= count_page:
                                        current_page = current_page + 1
                                    # 这里做一下error-handle，例如恶意输入字母以及超范围的数据
                                    elif option.isdigit() and 1 <= int(option) <= 10:
                                        # 删除新闻：MongoDB,Redis和MySQL都要删除
                                        try:
                                            news_id = result[int(option) - 1][0]
                                            __news_service.delete_news_by_id(news_id)
                                            __news_service.delete_cache(news_id)
                                        except ValueError as e:
                                            print(Fore.LIGHTRED_EX, '发生错误！无法执行！请检查序号是否正确')
                                            time.sleep(2)
                                    else:
                                        print(Fore.LIGHTRED_EX, "指令错误，请检查拼写或页码是否达到上限，请重新输入!")
                                        time.sleep(2)
                            if option == 'back':
                                break

                    # 管理员菜单 - 用户管理
                    elif option == '2':
                        while True:
                            os.system('clear')
                            print(Fore.LIGHTGREEN_EX, "======== 用户管理 ========\n")
                            print(Fore.LIGHTBLUE_EX, '\t1. 添加用户')
                            print(Fore.LIGHTBLUE_EX, '\t2. 修改用户')
                            print(Fore.LIGHTBLUE_EX, '\t3. 删除用户')
                            print(Fore.LIGHTRED_EX, '\tback.返回上一层')
                            print(Style.RESET_ALL)
                            option = input("请输入操作编号：")
                            # 用户管理菜单 - 添加用户
                            if option == '1':
                                os.system('clear')
                                name_input = input(" 请输入用户名：")
                                pass_input = getpass(" 请输入密码：")
                                re_pass_input = getpass(" 请再次输入密码：")
                                if pass_input != re_pass_input:
                                    print(Fore.LIGHTRED_EX, '\t两次密码不一致，即将自动返回!')
                                    print(Style.RESET_ALL)
                                    time.sleep(2)
                                    # 这里不是停止循环，是直接进入下一次循环重新开始
                                    continue
                                email_input = input(" 请输入邮箱：")
                                role_list = __role_service.print_role_list()
                                print('===== 用户角色选项 =====\n')
                                for index in range(len(role_list)):
                                    one = role_list[index]
                                    print(Fore.LIGHTBLUE_EX, '{}  {}'.format(index + 1, one[1]))
                                print(Style.RESET_ALL)
                                role_input = input(" 请输入角色对应的序号：")
                                if role_input.isdigit() and 1 <= int(role_input) <= len(role_list):
                                    role_id = role_list[int(role_input) - 1][0]
                                    __user_service.add_user(name_input, pass_input, email_input, role_id)
                                    print(Fore.LIGHTGREEN_EX, '===== 新用户{}保存成功！即将自动返回! ====='.format(username))
                                    time.sleep(2)
                                else:
                                    print(Fore.LIGHTRED_EX, '===== 序号输入错误，即将自动返回 =====')
                                    time.sleep(2)

                            # 用户管理菜单 - 修改用户
                            if option == '2':
                                current_page = 1
                                while True:
                                    os.system('clear')
                                    print(Fore.LIGHTRED_EX, "======== 修改用户 ========\n")
                                    count_page = __user_service.user_count_page()
                                    result = __user_service.print_all_users(current_page)
                                    for index in range(len(result)):
                                        one = result[index]
                                        print(Fore.LIGHTBLUE_EX,
                                              '\t%d\t%s\t%s' % (index + 1, one[1], one[2]))
                                    print(Fore.LIGHTGREEN_EX, '======================')
                                    print(Fore.LIGHTGREEN_EX, '\t第%d页，共%d页' % (current_page, count_page))
                                    print(Fore.LIGHTGREEN_EX, '======================')
                                    print(Fore.LIGHTGREEN_EX, '\n\tback.返回上一层\n\tprev.上一页\n\tnext.下一页')
                                    print(Style.RESET_ALL)
                                    option = input("请输入操作编号：")

                                    if option == 'back':
                                        break
                                    elif option == 'prev' and current_page > 1:
                                        current_page = current_page - 1
                                    elif option == 'next' and current_page <= count_page:
                                        current_page = current_page + 1
                                    # 这里做一下error-handle，例如恶意输入字母以及超范围的数据
                                    elif option.isdigit() and 1 <= int(option) <= 10:
                                        os.system('clear')
                                        # 获取这个用户对应的主键id
                                        user_primary_key = result[int(option) - 1][0]
                                        new_name = input(" 请输入新用户名：")
                                        new_pass = getpass(" 请输入新密码：")
                                        new_re_pass = getpass(" 请再次输入新密码：")
                                        if new_pass != new_re_pass:
                                            print(Fore.LIGHTRED_EX, "两次密码不一致！请重新输入！")
                                            print(Style.RESET_ALL)
                                            break
                                        new_email = input(" 请输入新邮箱：")
                                        role_list = __role_service.print_role_list()
                                        print('===== 用户角色选项 =====\n')
                                        for index in range(len(role_list)):
                                            one = role_list[index]
                                            print(Fore.LIGHTBLUE_EX, '{}  {}'.format(index + 1, one[1]))
                                        print(Style.RESET_ALL)
                                        new_role = input(" 请输入角色对应的序号：")
                                        role_id = role_list[int(new_role) - 1][0]
                                        print("===== 信息确认 =====")
                                        print(" 名称：{}\n 密码：{}\n 邮箱：{}\n 角色：{} {}".format(new_name, new_pass, new_email,
                                                                                         new_role,
                                                                                         role_list[int(new_role) - 1][
                                                                                             1]))
                                        choice = input("===== 是否保存(Y/N) =====\n")
                                        if choice.lower() == 'y':
                                            __user_service.update_user_information(user_primary_key, new_name, new_pass,
                                                                                   new_email, role_id)
                                            print(Fore.LIGHTGREEN_EX,
                                                  "====== 用户{}信息保存成功，即将自动返回 ======".format(new_name))
                                            print(Style.RESET_ALL)
                                            time.sleep(2)
                                    else:
                                        print(Fore.LIGHTRED_EX, "指令错误，请检查拼写或页码是否达到上限，请重新输入!")
                                        time.sleep(2)
                            # 用户管理菜单 - 删除用户
                            if option == '3':
                                current_page = 1
                                while True:
                                    os.system('clear')
                                    print(Fore.LIGHTRED_EX, "======== 删除用户 ========\n")
                                    count_page = __user_service.user_count_page()
                                    result = __user_service.print_all_users(current_page)
                                    for index in range(len(result)):
                                        one = result[index]
                                        print(Fore.LIGHTBLUE_EX,
                                              '\t%d\t%s\t%s' % (index + 1, one[1], one[2]))
                                    print(Fore.LIGHTGREEN_EX, '======================')
                                    print(Fore.LIGHTGREEN_EX, '\t第%d页，共%d页' % (current_page, count_page))
                                    print(Fore.LIGHTGREEN_EX, '======================')
                                    print(Fore.LIGHTGREEN_EX, '\n\tback.返回上一层\n\tprev.上一页\n\tnext.下一页')
                                    print(Style.RESET_ALL)
                                    option = input("请输入操作编号：")
                                    if option.isdigit() and 1 <= int(option) <= 10:
                                        user_primary_key = result[int(option) - 1][0]
                                        __user_service.delete_user(user_primary_key)
                                        print(Fore.LIGHTRED_EX, '===== 用户已删除，即将自动返回 =====')
                                        print(Style.RESET_ALL)
                                        time.sleep(2)
                                    elif option == 'back':
                                        break
                                    elif option == 'prev' and current_page > 1:
                                        current_page = current_page - 1
                                    elif option == 'next' and current_page <= count_page:
                                        current_page = current_page + 1
                                    else:
                                        print(Fore.LIGHTRED_EX, "指令错误，请检查拼写或页码是否达到上限，请重新输入!")
                                        time.sleep(2)
                            if option == 'back':
                                break
                    elif option == 'back':
                        break
                    elif option == 'exit':
                        sys.exit(0)
                    else:
                        print(Fore.LIGHTRED_EX, "指令错误，请重新输入")
                        time.sleep(1)
        else:
            print(Fore.LIGHTRED_EX, "登陆失败！(2秒自动返回)")
            time.sleep(2)

    # 大菜单 - 退出系统
    elif option == '2':
        sys.exit(0)