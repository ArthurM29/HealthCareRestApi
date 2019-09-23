import sqlite3
from random import choice
from string import ascii_lowercase


def random_string(length, charset=None):
    """Return random string of given length from elements of charset, which defaults to lowercase ascii characters"""
    if not isinstance(length, int) or length <= 0:
        raise ValueError("Invalid value: '{}'. Length must be a positive integer.".format(length))

    if charset:
        alphabet = charset
    else:
        alphabet = ascii_lowercase

    new_str = ''.join(choice(alphabet) for s in range(length))

    assert len(new_str) == length, "Generated string does not match specified length"
    return new_str


def run_db_query(db_file, sql, params=()):
    """ take sql query as string and parameters as tuple """
    connection = cursor = None
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute(sql, params)
        # make the changes to the database persistent
        connection.commit()
        rows = cursor.fetchall()
        return rows
    except sqlite3.DatabaseError as err:
        print(err)
    finally:
        # close communication with the database
        if cursor:
            cursor.close()
        if connection:
            connection.close()
