#!/usr/bin/env python

import subprocess
from collections import namedtuple
import prettytable
import optparse
import git
import dotini

Product = namedtuple("Product", "branch agent_limit name apl_salt product_id apl_include_key_config product_key status")

faveo_base_path = dotini.read('config/app.ini').fs.base_path

git_obj = git.Git(faveo_base_path)


def get_config(product):
    product_config = dotini.read('config/product.ini')
    config = product_config[product]
    config.status = 'PENDING'
    return config


enterprise = get_config('enterprise')

freelancer = get_config('freelancer')

sme = get_config('sme')

company = get_config('company')

startup = get_config('startup')


def progress_status():
    table = prettytable.PrettyTable(["Product Name", "Product Id", "Branch", "Agent limit", "APL_SALT",
                                     "APL_INCLUDE_KEY_CONFIG", "PRODUCT_KEY", "status"])
    table.add_row(get_row_by_product(enterprise))
    table.add_row(get_row_by_product(freelancer))
    table.add_row(get_row_by_product(company))
    table.add_row(get_row_by_product(sme))
    table.add_row(get_row_by_product(startup))

    print("\n")
    print(table)
    print("\n")


def get_row_by_product(product):
    return [product.name, product.product_id, product.release_branch, product.agent_limit,
            product.apl_salt, product.apl_include_key_config, product.product_key, product.status]


def find_and_replace(file_path, needle, replacement):
    """
    Finds and replaces text in file in base path of faveo directory
    :param file_path:
    :param needle:
    :param replacement:
    :return:
    """
    print("[+] Replacing " + needle + " with " + replacement + " in " + file_path)

    file_absolute_path = faveo_base_path + file_path
    # Read in the file
    with open(file_absolute_path, 'r') as file:
        file_data = file.read()

    # Replace the target string
    file_data = file_data.replace(needle, replacement)

    # Write the file out again
    with open(file_absolute_path, 'w') as file:
        file.write(file_data)

    print("[+] Replaced " + needle + " with " + replacement + " in " + file_path + " successfully")


def remove_plugins():
    print("[+] deleting plugins")

    subprocess.call(["rm", "-r", faveo_base_path + "app/Plugins"])

    print("[+] Plugins deleted successfully")


def update_file_replacements(product):
    # replacing in config/app.php
    find_and_replace("config/app.php", enterprise.name, product.name)

    # replacing in config/auth.php
    find_and_replace("config/auth.php", "'agent_limit'=>" + str(enterprise.agent_limit),
                     "'agent_limit'=>" + str(product.agent_limit))

    # replacing in config/self-update.php
    find_and_replace("config/self-update.php", enterprise.name, product.name)

    # replacing in public/script/apl_core_configuration.php
    find_and_replace("public/script/apl_core_configuration.php", enterprise.apl_salt, product.apl_salt)
    find_and_replace("public/script/apl_core_configuration.php", '"APL_PRODUCT_ID", ' + str(enterprise.product_id),
                     '"APL_PRODUCT_ID", ' + str(product.product_id))
    find_and_replace("public/script/apl_core_configuration.php", enterprise.apl_include_key_config,
                     product.apl_include_key_config)

    # replacing public/script/update_core_configuration.php
    find_and_replace("public/script/update_core_configuration.php", '"AUS_PRODUCT_ID", ' + str(enterprise.product_id),
                     '"AUS_PRODUCT_ID", ' + str(product.product_id))
    find_and_replace("public/script/update_core_configuration.php", enterprise.product_key, product.product_key)


def sync_branch_with_development(branch):
    git_obj.checkout('development')

    git_obj.sync_remote_branch_with_current_branch(branch)

    git_obj.checkout(branch)


def release(product):
    """
    Updates freelancer branch with required release code
    :return:
    """
    print("\n--------------------------------------Releasing "+product.name+"-----------------------------------------")

    # syncing product branch with development
    sync_branch_with_development(product.release_branch)

    # make required file changes
    if product.name != 'enterprise':
        update_file_replacements(product)

    if product.has_plugins:
        # Delete all plugins
        remove_plugins()

    # update remote branch with changes
    git_obj.commit_and_publish(product.release_branch)

    product.status = 'COMPLETED'

    print("\n--------------------------------Released "+product.name+" Successfully----------------------------------\n")


progress_status()

release(enterprise)

release(company)

release(sme)

release(startup)

release(freelancer)

progress_status()
