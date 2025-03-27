from typing import Literal

MONEY_CONFIG_EXTENSION_ID: Literal['money-config'] = 'money-config'
GROUND_TRUTH_EXTENSION_ID: Literal['ground-truth'] = 'ground-truth'
QUALITY_CONFIG_EXTENSION_ID: Literal['quality-management'] = 'quality-management'
QUALIFICATION_EXTENSION_ID: Literal['qualification'] = 'qualification'
WEBHOOK_EXTENSION_ID: Literal['annotation-studio-webhooks'] = 'annotation-studio-webhooks'
ExtensionId = Literal[
    'money-config',
    'ground-truth',
    'quality-management',
    'qualification',
    'annotation-studio-webhooks',
]
