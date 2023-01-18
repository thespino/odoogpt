# odoogpt_base

Base addon with utils to make OdooGPT work fine


## Requirements

The module requires the OpenAI python library named `openai`
```
pip install openai
```


## Installation instructions 

1. Install required **python modules**:

```
pip install openai
```

2. Place all downloaded **modules** into your Odoo's addons folder (pay attention: odoogpt_base is included in all modules, so copy it only one time and keep it updated)

3. Go to **"Apps"** (in debug mode) and click **"Update Apps List"**. Accept at confirmation.

4. Search for "odoogpt" in Apps list and install needed apps. 

> NOTE: you don't need to manually install `odoogpt_base`: it's an automatic dependency of all other modules


## Configuration

1. Go to **"Settings → OdooGPT"** and fill your OpenAI Api token. Get it from there: https://beta.openai.com/account/api-keys

2. Save configurations

3. Click "Test" near the api token. If message "Everything properly set up! You're good to go!" appears, the configuration is done. 

4. If needed, play with the **"OpenAI Parameters"**. To understand how they work, refer to OpenAi official docs at https://beta.openai.com/docs 

> NOTE: by default, the system will use the model "text-davinci-003". You can change it in settings
