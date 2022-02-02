
from .provider import Provider
from .local import Local
from .aws import Aws

all_providers = {
    'local': Local,
    'aws': Aws
}
