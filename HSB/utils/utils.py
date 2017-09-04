import arrow


def print_log(message, log_type='INFO'):
    log_types = ('INFO', 'WARNING', 'ERROR')
    prefix = '[ {} ]'.format(arrow.now().format('YYYY-MM-DD HH:mm:ss:SSS'))
    if str(log_type).upper() in log_types:
        log_type = str(log_type).upper()
    else:
        raise RuntimeError('Invalid log type: {}'.format(log_type))

    print('{} -{}- {}'.format(prefix, log_type, message))
