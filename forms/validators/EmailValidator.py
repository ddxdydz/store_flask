def is_email_valid(email: str) -> bool:
    if not email:
        return False
    a_id = email.find('@')
    dot_id = email.find('.')
    if a_id != email.rfind('@') or dot_id != email.rfind('.'):
        return False
    if not 0 < a_id < dot_id - 1 < len(email) - 2:
        return False
    return True


if __name__ == "__main__":
    print(is_email_valid("ffjmasd@r.u"))
    print(is_email_valid("") is False)
    print(is_email_valid("@d.") is False)
    print(is_email_valid("@ffjmasdr.u") is False)
    print(is_email_valid("ffjmas.d@ru") is False)
    print(is_email_valid("ffjmasd@.ru") is False)
    print(is_email_valid("ffjmasd.ru") is False)
    print(is_email_valid("ffjma@sdru.") is False)
    print(is_email_valid("f.fjma@sdru") is False)
