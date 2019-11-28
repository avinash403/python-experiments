#!/usr/bin/env python

import subprocess
from collections import namedtuple
import prettytable
import optparse

Product = namedtuple("Product", "branch agentLimit productName aplSalt productId aplIncludeKeyConfig productKey status")

faveo_base_path = "/var/www/html/faveo-helpdesk-advance/"

# enterprise configurations
enterprise = Product(
    branch="master-test",
    agentLimit=0,
    productName="Enterprise",
    aplSalt="b047c04cde662b7a",
    productId=8,
    aplIncludeKeyConfig="515548a88b8ab641",
    productKey="N85CeR7zL1J9zW5n",
    status='PENDING'
)

# freelancer configurations
freelancer = Product(
    branch="freelancer-test",
    agentLimit=2,
    productName="Freelancer",
    aplSalt="9bc4e8ab7841d09e",
    productId=28,
    aplIncludeKeyConfig="280ee05dbd04371e",
    productKey="m32kI0NyKGyx2bFM",
    status='PENDING'
)

sme = Product(
    branch="SME-test",
    agentLimit=10,
    productName="SME",
    aplSalt="7915c5620b3fc87b",
    productId=47,
    aplIncludeKeyConfig="7a61e5c370996340",
    productKey="Hn1Ow0w36qo7MjhW",
    status='PENDING'
)

company = Product(
    branch="company-test",
    agentLimit=0,
    productName="Company",
    aplSalt="065d04198a83297a",
    productId=15,
    aplIncludeKeyConfig="649ba008fe6093da",
    productKey="ygoJNQgg03q7sTdG",
    status='PENDING'
)

startup = Product(
    branch="startup-test",
    agentLimit=5,
    productName="Startup",
    aplSalt="e7a3af2fc36bb880",
    productId=14,
    aplIncludeKeyConfig="ffec04f977c87bed",
    productKey="JjXPKXA3RZbnwZjT",
    status='PENDING'
)


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
    return [product.productName, product.productId, product.branch, product.agentLimit,
            product.aplSalt, product.aplIncludeKeyConfig, product.productKey, product.status]


def git(*args):
    """
    Performs git operations based on the params passed
    :param args:
    :return:
    """
    default_params = ["git", "-C", faveo_base_path]
    all_params = default_params + list(args)
    subprocess.call(all_params, stdout=open('./faveo_release.log', 'a'), stderr=open('./faveo_release.log', 'a'))


def find_and_replace(file_path, needle, replacement):
    """
    Finds and replaces text in file in base path of faveo directory
    :param file_path:
    :param needle:
    :param replacement:
    :return:
    """
    print("[+] Replacing " + needle + " with "+replacement+" in "+file_path)

    file_absolute_path = faveo_base_path + file_path
    # Read in the file
    with open(file_absolute_path, 'r') as file:
        file_data = file.read()

    # Replace the target string
    file_data = file_data.replace(needle, replacement)

    # Write the file out again
    with open(file_absolute_path, 'w') as file:
        file.write(file_data)

    print("[+] Replaced " + needle + " with "+replacement+" in "+file_path+" successfully")


def remove_plugins():
    subprocess.call(["rm", "-r", faveo_base_path + "app/Plugins"])


def checkout_to_development():
    git("stash")
    git("clean", "-fd")
    git("checkout", "development", "-f")
    git("fetch")
    git("reset", "--hard", "origin/development")


def update_file_replacements(product):
    # replacing in config/app.php
    find_and_replace("config/app.php", enterprise.productName, product.productName)

    # replacing in config/auth.php
    find_and_replace("config/auth.php", "'agent_limit'=>" + str(enterprise.agentLimit),
                     "'agent_limit'=>" + str(product.agentLimit))

    # replacing in config/self-update.php
    find_and_replace("config/self-update.php", enterprise.productName, product.productName)

    # replacing in public/script/apl_core_configuration.php
    find_and_replace("public/script/apl_core_configuration.php", enterprise.aplSalt, product.aplSalt)
    find_and_replace("public/script/apl_core_configuration.php", '"APL_PRODUCT_ID", ' + str(enterprise.productId),
                     '"APL_PRODUCT_ID", ' + str(product.productId))
    find_and_replace("public/script/apl_core_configuration.php", enterprise.aplIncludeKeyConfig,
                     product.aplIncludeKeyConfig)

    # replacing public/script/update_core_configuration.php
    find_and_replace("public/script/update_core_configuration.php", '"AUS_PRODUCT_ID", ' + str(enterprise.productId),
                     '"AUS_PRODUCT_ID", ' + str(product.productId))
    find_and_replace("public/script/update_core_configuration.php", enterprise.productKey, product.productKey)


def sync_branch_with_development(branch):

    print("[+] checking out to development")

    checkout_to_development()

    print("[+] checked out to development")

    print("[+] pushing development code to "+branch)

    git("push", "origin", "development:" + branch, "-f")

    print("[+] "+branch+" updated successfully")

    git("fetch")

    print("[+] checking out to "+branch)

    git("checkout", branch, "-f")

    print("[+] checked out to "+branch)

    git("reset", "--hard", "origin/" + branch)


def publish_release_branch(branch):

    print("[+] Committing all changes")

    git("add", ".")

    git("commit", "-m", "product configuration updated", "-n")

    print("[+] Committed all changes")

    print("[+] Pushing to "+branch)

    git("push", "origin", branch)

    print("[+] "+branch+" updated successfully")


def enterprise_update():

    print("--------------------------------------Updating Enterprise-----------------------------------------")

    print("[+] checking out to development")

    checkout_to_development()

    print("[+] checked out to development")

    print("[+] pushing development code to "+enterprise.branch)

    git("push", "origin", "development:" + enterprise.branch, "-f")

    print("[+] "+enterprise.branch+" updated successfully")


def freelancer_update():
    """
    Updates freelancer branch with required release code
    :return:
    """
    print("\n\n--------------------------------------Updating Freelancer-----------------------------------------")

    # syncing product branch with development
    sync_branch_with_development(freelancer.branch)

    # make required file changes
    update_file_replacements(freelancer)

    print("[+] deleting plugins")

    # Delete all plugins
    remove_plugins()

    print("[+] Plugins deleted successfully")

    # update remote branch with changes
    publish_release_branch(freelancer.branch)


def company_update():
    """
    Updates company branch with required release code
    :return:
    """
    print("\n\n--------------------------------------Updating Company-----------------------------------------")

    # syncing product branch with development
    sync_branch_with_development(company.branch)

    # make required file changes
    update_file_replacements(company)

    # update remote branch with changes
    publish_release_branch(company.branch)


def sme_update():
    """
    Updates SME branch with required release code
    :return:
    """
    print("\n\n--------------------------------------Updating SME-----------------------------------------")
    # syncing product branch with development
    sync_branch_with_development(sme.branch)

    # make required file changes
    update_file_replacements(sme)

    # update remote branch with changes
    publish_release_branch(sme.branch)


def startup_update():
    """
    Updates startup branch with required release code
    :return:
    """
    print("\n\n--------------------------------------Updating Startup-----------------------------------------")

    # syncing product branch with development
    sync_branch_with_development(startup.branch)

    # make required file changes
    update_file_replacements(startup)

    # update remote branch with changes
    publish_release_branch(startup.branch)


def set_faveo_base_path():
    global faveo_base_path
    parser = optparse.OptionParser()
    parser.add_option("-p", "--path", dest="path", help="Path to faveo installation directory", default=faveo_base_path)
    options = parser.parse_args()[0]
    faveo_base_path = options.path


set_faveo_base_path()

progress_status()

enterprise_update()

enterprise = enterprise._replace(status="COMPLETED")

freelancer_update()

freelancer = freelancer._replace(status="COMPLETED")

company_update()

company = company._replace(status="COMPLETED")

sme_update()

sme = sme._replace(status="COMPLETED")

startup_update()

startup = startup._replace(status="COMPLETED")

progress_status()

# def progress_bar(value, endvalue, bar_length=20):
#     percent = float(value) / endvalue
#     arrow = '-' * int(round(percent * bar_length) - 1) + '>'
#     spaces = ' ' * (bar_length - len(arrow))
#
#     sys.stdout.write("\rPercent: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
#     sys.stdout.flush()
#
# progress_bar(10, 100)
