# Django Blip
<img src="https://github.com/NeurlAP/Images/assets/105038093/c25be39a-16c0-4b80-ac64-e06cae172512" width="300">   

Django Blip is a python package that mocks any external API(s) call when running Django test(s). It allows to set global   
mocked response and status code for these external API(s) calls. Notably, if you've previously used @httpretty.activate 
to mock a test, Django Blip will not overwrite that behavior, ensuring backward compatibility.   


# How to configure: 
1) `pip install django-blip` to install in your virtual env.
2) Add `TEST_RUNNER = "blip.custom_test_runner.BlipTestRunner"` in your Django's `settings.py`.  

Optionally  
3) Add,  
```python
BLIP_CONFIG = {
                "blip_status_code": 500,  # Default 200
                "blip_response": '{"key": "value"}',  # Default {}
                "blip_verbose": False,  # Default True
                "blip_silently_bypass": False  # Default True, If set to False, it will raise an exception if any
                                               # external API call is encountered within the test
            }
```
   in your `settings.py`. 

Also if you wanna register any additional url you can do it like this,
```python  
    from blip.service import BlipService 
    import httpretty
    import json
    BLIP_CONFIG = {
    "blip_additional_global_mocks": [
        BlipService.BlipAdditionalGlobalMocks(
            request_uri="https://xyz.com",
            request_method=httpretty.POST,
            response_status_code=200,
            response=json.dumps({"key": "value"}),
        )
    ]
}
``` 
Blip will give first priority to urls passed via `blip_additional_global_mocks`.


    
# Basic Usage

```python
import httpretty 
from django.test import TestCase 
import requests  
import json
class TestBlipWorks(TestCase):
    @httpretty.activate(verbose=True, allow_net_connect=False)
    def test_blip_do_not_alter_the_behaviour_of_existing_mocked_apis_with_httpretty(self):
        url = "https://google.com"
        httpretty.register_uri(httpretty.GET, url, body=json.dumps({"key": "value"}), status=500)
        # blip's default behaviour is it mocks any api call and return status code = 200 and response={}
        # this test will ensure blip don't override existing test which is already decorated with @httpretty.activate
        res = requests.get(url)
        self.assertEqual(res.json()["key"], "value")  # blip returns response = {}
        self.assertEqual(res.status_code, 500)  # blip returns default 200 status code

    def test_blip_works_and_mock_any_api_call(self):
        url = "https://google.com"
        # blip's default behaviour is it mocks any api call and return status = 200 and response={}
        res = requests.get(url)
        self.assertEqual(res.json(), {})  # blip returns response = {}
        self.assertEqual(res.status_code, 200)  # blip returns default 200 status code
```

In the provided code examples, `test_blip_works_and_mock_any_api_call` shows that Blip returns a mocked status_code of 200 and an empty response {}. Additionally, in `test_blip_do_not_alter_the_behaviour_of_existing_mocked_apis_with_httpretty`, you can see how Blip is designed to work seamlessly with @httpretty.activate decorators, ensuring that it doesn't override existing behaviors.
