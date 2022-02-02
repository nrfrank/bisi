

import bisi.resources as bsr

d1 = bsr.Dockerfile(build_args={'TEST_BUILD_ARG': 'TEST_BUILD_ARG_VALUE'})
d2 = bsr.Dockerfile(file='other.Dockerfile')

bsr.Job(name='test_bash', entrypoint='test.sh', dockerfile=d1)
bsr.Job(name='test_python', entrypoint='test.py', dockerfile=d2)
