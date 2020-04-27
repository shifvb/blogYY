from database.blogYY.immigrant.table_article import immigrant_article
from database.blogYY.immigrant.table_category import immigrant_category
from database.blogYY.immigrant.table_user import immigrant_user


def immigrant():
    immigrant_article(is_create=False, is_insert=False, is_select=False)
    immigrant_category(is_create=False, is_insert=False, is_select=False)
    immigrant_user(is_create=False, is_insert=False, is_select=True)


if __name__ == '__main__':
    immigrant()
