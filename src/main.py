import sqlparse
from sqlparse.tokens import Keyword, DDL, Whitespace
from sqlparse.sql import Identifier
import custom_functions
import re
import xml.etree.ElementTree as ET
import csv

base_path = "C:\\Users\\witzk\\Desktop\\WorkReport\\"
input_folder_path = base_path + "input\\"
output_folder_path = base_path + "output\\"
templates_folder_path = base_path + "templates\\"

input_file_name = "test_table_1.sql"
token_regex_table_file = base_path + "token_regex_table.csv"
lang = "java"
lang_file_ending = ".java"
input_sql_file = input_folder_path + input_file_name
template_file = templates_folder_path + lang + "_template.xml"

# replaces all "\n \n"s with "\n" recursivly
def remove_excess_new_lines(text, removed_none_last=False):
    if removed_none_last:
        return text;
    new_text = text
    new_text = re.sub(r"\n\s*\n", "\n", new_text)
    return remove_excess_new_lines(new_text, new_text == text)

def is_create_table_statement(statement):
    create_table = re.search(r"(?i)^(CREATE TABLE)", statement)
    if create_table == None:
        return False
    else:
        return True


def get_token_regex_for_sql(token_name):
    with open(token_regex_table_file, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        for row in csv_reader:
            if(row[0] == token_name):
                return row[1]
        return None


# returns raw_xml_template with the string that should exist in the place that a <token /> tag is
def handle_token(token_name, token_func, sql_str, raw_xml_template):
    sql_regex = get_token_regex_for_sql(token_name)
    sql_regex_search = re.search(sql_regex, sql_str)
    if sql_regex_search is None:
        return re.sub(r"\<token[^/>]*/\>", "", raw_xml_template, 1)
    val_from_sql = sql_regex_search.group(1)
    if (token_func == ""):
        return re.sub(r"\<token[^/>]*/\>", val_from_sql, raw_xml_template, 1)
    else:
        # get a custom function
        method_to_call = getattr(custom_functions, token_func)
        new_val = method_to_call(val_from_sql)
        x = re.sub(r"\<token[^/>]*/\>", new_val, raw_xml_template, 1)
        return x


# returns the string that should exist in the place that the <field>...</field> tag is
def handle_fields(fields_root, sql_fields, raw_xml_template):
    # gets rid of the parentheses surrounding the sql text
    sql_field_str = sql_fields.value[1:len(sql_fields.value) - 2]
    # loop thru the fields given in the sql CREATE TABLE
    final_fields_str = ""
    for field_str in sql_field_str.split(","):
        # new template
        raw_xml_field_template = re.search(r"\<field\>((\n|.)*)\</field\>", raw_xml_template).group(1)
        # gets rid of leading whitespace
        field_str = re.sub(r"^[\s]*", "", field_str)
        # loop thru the tokens found in the <field> ... </ filed> tags
        for child in fields_root:
            if(child.tag == 'token'):
                token_name = ""
                token_func = ""
                if 'name' in child.attrib.keys():
                    token_name = child.attrib['name']
                if 'func' in child.attrib.keys():
                    token_func = child.attrib['func']
                raw_xml_field_template = handle_token(token_name, token_func, field_str, raw_xml_field_template)
        final_fields_str += raw_xml_field_template
    field_tags_replacement = re.sub(r"\<field\>(\n|.)*\</field\>", final_fields_str, raw_xml_template, 1)
    field_tags_replacement = remove_excess_new_lines(field_tags_replacement)
    return field_tags_replacement

# does the bulk of the work
def translate_table(create_table_statement):
    # find the lines in create_table_statement that define fields
    sql_parsed = sqlparse.parse(create_table_statement)[0]
    sql_fields = None
    for token in sql_parsed.tokens:
        if(token.is_group):
            sql_fields = token

    # go thru the xml template file. Replace the tags with translated code as we go along
    template_tree = ET.parse(template_file).getroot()
    with open(template_file) as xml_template_file:
        # clean up the raw xml
        raw_xml_template = xml_template_file.read()
        raw_xml_template = re.sub(r"\<\?xml.*\>", "", raw_xml_template)
        raw_xml_template = re.sub(r"\<.*class\>", "", raw_xml_template)

        for child in template_tree:
            if(child.tag == 'token'):
                raw_xml_template = handle_token(child.attrib['name'], child.attrib['func'], create_table_statement, raw_xml_template)
            elif(child.tag == 'field'):
                raw_xml_template = handle_fields(child, sql_fields, raw_xml_template)
        return(raw_xml_template)

# returns the name of the table in the given "CREATE TABLE" statement
def get_table_name(statement):
    return re.search(r"(?i)[\n\r.]*CREATE TABLE\s*([^\n\r ]*)", statement).group(1)

def write_output(translation_str, table_name):
    f = open(output_folder_path + table_name + "_translation" + lang_file_ending, "w")
    f.write(translation_str)
    f.close()

with open(input_sql_file) as file:
    sql_code = file.read()
    statements = sqlparse.split(sql_code)
    for statement in statements:
        if is_create_table_statement(statement):
            translation_str = translate_table(statement)
            table_name = get_table_name(statement)
            write_output(translation_str, table_name)
            print("translation for " + table_name + " complete.")

