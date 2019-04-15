python selenim example trying to figure out how to share a config dictionary established in conftest to be used in class and test files via pytest command line arguments

clone the repo then in terminal install dependencies
`pip install -r requirements`

### Example usages currently
`pytest -q --randomly-seed=1555368693 test_sample.py --aut="app1" --base_url="https://www.example.com"`

`pytest -q test_base.py --aut="app1" --base_url="https://www.example.com"`