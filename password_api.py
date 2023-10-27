import requests
import hashlib
import sys


def request_api_data(query):
    url = 'https://api.pwnedpasswords.com/range/'+query
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}')
    return res


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first_five_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first_five_char)
    return get_leakt_passwords_count(response, tail)


def get_leakt_passwords_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, c in hashes:
        if h == hash_to_check:
            return c
    return 0


def main(file):
    with open(file, 'r') as pw:
        text = pw.readlines()
    text = [password.strip() for password in text]

    for password in text:
        count = pwned_api_check(password)
        if count:
            print(
                f'{password} was found {count} times. You should consider use another password')
        else:
            print('Your password has not been hacked, yet.')


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
