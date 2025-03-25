from blue_options.env import load_config, load_env, get_env

load_env(__name__)
load_config(__name__)


DAMAGES_TEST_DATASET_OBJECT_NAME = get_env("DAMAGES_TEST_DATASET_OBJECT_NAME")

ENCODED_BLOB_SAS_TOKEN = get_env("ENCODED_BLOB_SAS_TOKEN")

SAGESEMSEG_COMPLETED_JOB_pascal_voc_v1_debug_v2 = get_env(
    "SAGESEMSEG_COMPLETED_JOB_pascal_voc_v1_debug_v2"
)

SAGESEMSEG_COMPLETED_JOB_pascal_voc_v1_full_v2 = get_env(
    "SAGESEMSEG_COMPLETED_JOB_pascal_voc_v1_full_v2"
)

GROQ_API_KEY = get_env("GROQ_API_KEY", "")

VISUALYZE_PORT = get_env("VISUALYZE_PORT")

WEBDAV_HOSTNAME = get_env("WEBDAV_HOSTNAME")
WEBDAV_LOGIN = get_env("WEBDAV_LOGIN")
WEBDAV_PASSWORD = get_env("WEBDAV_PASSWORD")
