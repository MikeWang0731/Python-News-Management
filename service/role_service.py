from db.role_dao import RoleDao


class RoleService:
    __role_dao = RoleDao()

    # 调用打印用户角色的接口
    def print_role_list(self):
        result = self.__role_dao.print_role_list()
        return result
