from os import PathLike


def is_only_contains(text, arg):
    for char in text:
        if char not in arg:
            return False
    return True


def format_type(data_type: str, path: PathLike):
    text = ''
    with open(path, 'r') as file:
        text = ''.join([('' if char in (' ','\t') else char) for char in file.read()])

    text = ''.join(
        [
            ('' if text[num] == '\n' and num > 0 and text[num-1] == ':' else char) for num, char in enumerate(text)
        ]
    )

    text = ''.join(
        [
            (',' if char == '\n' else char) for char in text
        ]
    )

    text = ''.join(
        [
            ('' if text[num] == ',' and num > 0 and text[num-1] in (',', '{', '[') else char) for num, char in enumerate(text)
        ]
    )

    text = ''.join(
        [
            ('' if text[num] == ',' and num + 1 < len(text) and text[num+1] in (',', '}', ']') else char) for num, char in enumerate(text)
        ]
    )

    pos = text.find('Age_of_History')
    offset = len('Age_of_History:')
    file_type = text[pos+offset:text[pos+offset:].find(',')]

    if file_type != data_type:
        raise TypeError("this is not Technologies files")

    return define_value(text)


def define_value(text: str):
    if text.startswith('[') and text.endswith(']') or text.startswith('{') and text.endswith('}'):
        if text.startswith('[') and text.endswith(']'):
            return parse_list(text)
        return parse_dict(text)
    else:
        if text.startswith('"') and text.endswith('"'):
            return text[1:len(text)-1]
        if is_only_contains(text, '-0123456789.'):
            if '.' in text:
                return float(text)
            else:
                return int(text)
        if text in ('true','false'):
            return text == 'true'
        if text == 'null':
            return None
        return text


def parse_dict(text: str):
    content = {}
    is_read_value = False
    deep_step = 0
    key = ''
    value = ''
    for num, char in enumerate(text[1:len(text) - 1]):
        if char in ('{', '['):
            deep_step += 1
        if char in ('}', ']'):
            deep_step -= 1
        if char == ':' and deep_step == 0:
            is_read_value = True
            continue
        if is_read_value:
            if char == ',' and deep_step == 0:
                content[key] = define_value(value)
                value = ''
                key = ''
                is_read_value = False
                continue
            else:
                value += char
            if num == len(text[1:len(text) - 1]) - 1:
                content[key] = define_value(value)
                value = ''
                key = ''
                is_read_value = False
                continue
        else:
            key += char
    return content


def parse_list(text: str):
    content = []
    deep_step = 0
    value = ''
    for num, char in enumerate(text[1:len(text) - 1]):
        if char in ('[', '{'):
            deep_step += 1
        if char in (']', '}'):
            deep_step -= 1
        if char == ',' and deep_step == 0:
            content.append(define_value(value))
            value = ''
        else:
            value += char
        if num == len(text[1:len(text) - 1]) - 1:
            content.append(define_value(value))
            value = ''
    return content