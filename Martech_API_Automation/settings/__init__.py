import os
import yaml
from enum import Enum

# env_key = key_to_env(os.environ['environment'])
# locale_key = key_to_env(os.environ['locale'])
# platform_key = os.environ['platform']
env_key = "sandbox"
locale_key = "us"
platform_key = "iOS"


def read_yaml_file(current_path):
    print("current directory -> %s" % os.getcwd())
    yml_file = os.path.abspath(current_path + "/config.yaml")
    yml = open(yml_file, 'r', encoding='utf-8')
    if os.path.isfile(yml_file):
        return yml.read()
    else:
        print(yml_file + 'file not exist')


current_path = os.path.dirname(__file__)
yaml_cfg = yaml.full_load(read_yaml_file(current_path))


def get_current_env(specific_env):
    env = ''
    try:
        env = yaml_cfg.get(specific_env)[str.upper(env_key)]
    except Exception as e:
        print("{0} do not define in {1} env, just skip it, please double check if it's necessary".format(specific_env,
                                                                                                         env_key))
    finally:
        return env


class Locale:
    AU = "au"
    US = "us"
    UK = "uk"


class Platform:
    ANDROID = "android"
    IOS = "iOS"


def key_to_env(key):
    envs = {
        "QA": "QA",
        "STG": "Staging",
        "Sandbox": "sandbox",
        "Production": "production",
    }
    return envs.get(key, None)


def get_app_name(env_key, locale_key, platform_ley):
    if platform_ley == Platform.ANDROID:
        name_patthen = "com.{0}mobile.{1}"
    elif platform_ley == Platform.IOS:
        name_patthen = "com.{0}.{0}-consumer-{1}"

    if locale_key == Locale.UK:
        app_name = "clearpay"
    else:
        app_name = "afterpay"

    internal_app_name = name_patthen.format(app_name, env_key)

    if locale_key == Locale.AU:
        return internal_app_name
    else:

        if platform_ley == Platform.ANDROID:
            # com.afterpaymobile.sanbox.us
            return internal_app_name + "." + locale_key
        else:
            # com.afterpay.afterpay-consumer-sandbox-us
            return internal_app_name + "-" + locale_key


app_name = get_app_name(env_key, locale_key, platform_key)

# need to install app before run
Need_Install_APP = True
