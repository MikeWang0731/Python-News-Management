from db.user_dao import UserDao


class UserService:
    __user_dao = UserDao()

    # 调用登陆服务接口
    def login(self, username, password):
        result = self.__user_dao.login(username, password)
        return result

    # 调用查询用户角色接口
    def search_user_role(self, username):
        result = self.__user_dao.search_user_role(username)
        return result

    # 调用添加用户的接口
    def add_user(self, username, password, email, role_id):
        self.__user_dao.add_user(username, password, email, role_id)

    # 调用计算用户可以显示几页的接口（分页输出）
    def user_count_page(self):
        page = self.__user_dao.user_count_page()
        return page

    # 调用打印所有用户的接口
    def print_all_users(self, page):
        result = self.__user_dao.print_all_user(page)
        return result

    # 调用更新用户信息的接口
    def update_user_information(self, user_id, username, password, email, role_id):
        self.__user_dao.update_user_information(user_id, username, password, email, role_id)

    # 调用删除用户的接口
    def delete_user(self, user_id):
        self.__user_dao.delete_user(user_id)

    # 调用查询用户id的接口
    def search_user_id(self, username):
        result = self.__user_dao.search_user_id(username)
        return result
