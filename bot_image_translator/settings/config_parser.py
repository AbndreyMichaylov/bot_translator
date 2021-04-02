import toml

config = toml.load('settings/bot_config.toml')

VK_TOKEN = config['vk_bot_data']['VK_TOKEN']
GROUP_ID = config['vk_bot_data']['GROUP_ID']
SAVE_PATH = config['save_files_data']['SAVE_PATH']
LING_TOKEN = config['lingvanex_api']['LING_TOKEN']
JSON_SAVE_PATH = config['save_files_data']['JSON_SAVE_PATH']