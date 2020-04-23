from database.blogYY.immigrant.table_article import immigrant_article
from database.blogYY.immigrant.table_category import immigrant_category


def immigrant():
    control_dict = {
        "is_create": False,
        "is_insert": False,
        "is_select": True,
    }
    immigrant_article(**control_dict)
    immigrant_category(**control_dict)


if __name__ == '__main__':
    immigrant()
