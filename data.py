from requests.models import Response
import schoolopy
import yaml
from api import get_paged_data
import string
from typing import Dict, List, Optional

BASE_URL = 'https://api.schoology.com/v1'
save_file = 'saved.yml'

# Load staff names from file
with open('staff.yml') as file:
    # STAFF is a list of lists containing first and last names. Decoding as tuples might require extra effort
    # E.x. [['First', 'Last']]
    STAFF = yaml.load(file, Loader=yaml.FullLoader)

with open('keys.yml', 'r') as f:
    keys = yaml.load(f, Loader=yaml.FullLoader)

sc = schoolopy.Schoology(schoolopy.Auth(keys['public'], keys['secret']))

def schoology_req(endpoint: str, data: Optional[Dict] = None) -> Response:
    if data is not None:
        res = sc.schoology_auth.oauth.post(endpoint, headers=sc.schoology_auth._request_header(), auth=sc.schoology_auth.oauth.auth, json=data)
    else:
        res = sc.schoology_auth.oauth.get(endpoint, headers=sc.schoology_auth._request_header(), auth=sc.schoology_auth.oauth.auth)
    return res


def request_last_name_letters() -> List[str]:
    users = get_paged_data(schoology_req, BASE_URL + '/users?limit=200', data_key='user')
    users = list(filter(lambda user: user['position'] is None or 'teacher' not in user['position'].lower(), users))
    users = list(filter(lambda user: [user['name_first'], user['name_last']] not in STAFF, users))
    last_name_letters = [user['name_last'][0].upper() for user in users]
    last_name_letters = list(filter(lambda letter: letter in string.ascii_uppercase, last_name_letters))

    with open(save_file, 'w') as f:
        yaml.dump(last_name_letters, f)

    return last_name_letters


def saved_last_name_letters() -> List[str]:
    with open(save_file, 'r') as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def last_name_letters() -> List[str]:
    return saved_last_name_letters() or request_last_name_letters()