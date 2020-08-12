def to_max_size(max_size):
    return "@Size(min = 0, max = " + max_size + ")"

def to_lower_camel_case(snake_str):
    words = snake_str.split('_')
    if len(words) == 1:
        return words[0].lower()
    return words[0].lower() + ''.join(word.title() for word in words[1:])

def to_upper_camel_case(snake_str):
    words = snake_str.split('_')
    return ''.join(word.title() for word in words[0:])

sql_to_java_types = {
    "int": "int",
    "varchar": "String",
    "bigint": "Long",
    "bigserial": "Long"
}

def to_java_type(sql_type):
    return sql_to_java_types[sql_type.lower()]

def to_not_nullable(dummy):
    return "@NonNull"

def to_nullable(dummy):
    return "@Nullable"

def to_id(dummy):
    return "@Id"

def no_translation(input):
    return input