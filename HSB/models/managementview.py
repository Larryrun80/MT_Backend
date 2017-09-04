

class ManagementView(object):
    """docstring for ManagementView"""

    def __init__(self, user_object):
        super(ManagementView, self).__init__()
        self.user_object = user_object
        self.columns = []
        self.edit = True

    @classmethod
    def get_mgt_list(cls):
        ''' return a result for admin list
            must override this in inherit objs
        '''
        raise NotImplementedError(
            'management list function must be implemented')

    @classmethod
    def get_mgt_list_data(cls):
        ''' return a result for admin list
            must override this in inherit objs
        '''

        if not hasattr(cls, 'mgt_columns'):
            raise NotImplementedError(
                'management list function must be implemented')
        else:
            rows = []
            columns = [col for col in cls.mgt_columns.keys()]

            result = cls.query.all()

            for item in result:
                row = [item.id]
                for col in columns:
                    item_tmp = item
                    attrs = cls.get_obj_attr(item.mgt_columns, col).split('.')
                    for attr in attrs:
                        if item_tmp:
                            item_tmp = getattr(item_tmp, attr)
                        else:
                            break
                    row.append(cls.generate_content(
                        item_tmp, item.mgt_columns[col]))
                rows.append(row)

            return {
                'columns': columns,
                'rows': rows,
            }

    @classmethod
    def get_obj_attr(cls, columns, key):
        if key not in columns.keys():
            return None

        column = columns.get(key, None)
        if isinstance(column, str):
            return column
        elif isinstance(column, dict) and 'name' in column.keys():
            return column['name']

        return None

    @classmethod
    def generate_content(cls, data, column_info):
        if not isinstance(column_info, dict):
            return data

        col_type = column_info['type']
        if col_type == 'link':
            showname = data
            if 'params' in column_info.keys() and\
                    'showname' in column_info['params'].keys():
                showname = column_info['params']['showname']

            link = data
            if 'endpoint' in column_info.keys():
                link = "{{{{ url_for({}) }}}}".format(column_info['endpoint'])
                print(link)

            return '<a href="{}">{}</a>'.format(link, showname)
