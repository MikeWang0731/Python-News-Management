from db.type_dao import TypeDao


class TypeService:
    __type_dao = TypeDao()

    def print_type_list(self):
        result = self.__type_dao.print_type_list()
        return result
