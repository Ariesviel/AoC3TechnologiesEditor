# I wrote this code a long time ago. That's why it is a bit shit

def isOnlyContains(text, arg):
    for char in text:
        if char not in arg:
            return False
    return True


def formatType(data_type: str, path: str):
    text = ''
    with open(path, 'r') as file:
        content = file.read().strip()
        text = ''
        is_str = False
        for num, char in enumerate(content):
            if char == '"' and num > 0 and content[num-1] != '\\':
                is_str = False if is_str else True
            if is_str:
                if char not in "\\":
                    text += char
            else:
                if char not in ' \t':
                    text += char
    text = ''.join(     [('' if text[num] == '\n' and num > 0 and text[num-1] == ':' else char) for num, char in enumerate(text)]   )
    text = ''.join(     [('' if char == '\n' else char) for char in text]   )
    text = ''.join(     [('' if text[num] == ',' and num > 0 and text[num-1] in (',', '{', '[') else char) for num, char in enumerate(text)]    )
    text = ''.join(     [('' if text[num] == ',' and num + 1 < len(text) and text[num+1] in (',', '}', ']') else char) for num, char in enumerate(text)]    )

    pos = text.find('Age_of_History')
    offset = len('Age_of_History:')
    file_type = text[pos+offset:text[pos+offset:].find(',')]

    if file_type != data_type:
        raise TypeError(f"this is not {data_type} file")

    return defineValue(text)


def defineValue(text: str):
    if text.startswith('[') and text.endswith(']') or text.startswith('{') and text.endswith('}'):
        if text.startswith('[') and text.endswith(']'):
            return parseList(text)
        return parseDict(text)
    else:
        if text.startswith('"') and text.endswith('"'):
            return text[1:len(text)-1]
        if isOnlyContains(text, '-0123456789.'):
            if '.' in text:
                return float(text)
            else:
                return int(text)
        if text in ('true','false'):
            return text == 'true'
        if text == 'null':
            return None
        return text


def parseDict(text: str):
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
                content[key] = defineValue(value)
                value = ''
                key = ''
                is_read_value = False
                continue
            else:
                value += char
            if num == len(text[1:len(text) - 1]) - 1:
                content[key] = defineValue(value)
                value = ''
                key = ''
                is_read_value = False
                continue
        else:
            key += char
    return content


def parseList(text: str):
    content = []
    deep_step = 0
    value = ''
    for num, char in enumerate(text[1:len(text) - 1]):
        if char in ('[', '{'):
            deep_step += 1
        if char in (']', '}'):
            deep_step -= 1
        if char == ',' and deep_step == 0:
            content.append(defineValue(value))
            value = ''
        else:
            value += char
        if num == len(text[1:len(text) - 1]) - 1:
            content.append(defineValue(value))
            value = ''
    return content