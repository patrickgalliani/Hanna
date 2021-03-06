# Ricky Galliani
# Hanna
# onboard.py

from typing import Any, Dict, List, Tuple

import logging
import os
import json
import robin_stocks as r


def ask_user_input(prompt: str) -> str:
    """
    Asks the user the prompt and returns the response.
    """
    return input(prompt)


def ask_security(ac_name: str) -> Tuple[str, str]:
    """
    Asks the user for the symbol of a security to add and returns the
    security's id and name.
    """
    sec_sym: str = ask_user_input(
        "\t\tEnter the symbol for the new {} security: ".format(ac_name)
    )
    instrument: Dict[str, Any] = r.get_instruments_by_symbols([sec_sym])[0]
    return (instrument["id"], instrument["name"])


def ask_confirm_security(sec_name: str) -> bool:
    """
    Asks the user to confirm the name of a security. Returns True if the user
    confirms and False otherwise.
    """
    confirm_security_str: str = ask_user_input(
        "\t\t\tConfirm {}: [Y/n] ".format(sec_name)
    )
    return confirm_security_str.lower() == "y" or confirm_security_str == ""


def ask_allow_purchase() -> bool:
    """
    Asks the user whether to allow purchasing (of a previously displayed
    security). Returns True if the user confirms and False otherwise.
    """
    allow_purchase_str: str = ask_user_input("\t\t\tAllow purchase: [Y/n] ")
    return allow_purchase_str.lower() == "y" or allow_purchase_str == ""


def ask_asset_class_name(first: bool) -> str:
    """
    Asks the user for an asset class name and returns the user's response.
    """
    ac_name: str = ask_user_input(
        "Enter the name of {} asset class: ".format(
            "an" if first else "the next"
        )
    )
    if ac_name == "":
        ask_asset_class_name(first)
    return ac_name


def ask_target_pct(ac_name: str, pct_left: float) -> float:
    """
    Asks the user for a target percentage for an asset class and returns the
    user's response.
    """
    ac_target_pct_str: str = ask_user_input(
        "\tEnter target percentage of the {} (min: 0.0, max: {}): ".format(
            ac_name, pct_left
        )
    )
    ac_target_pct: float = 0.0
    try:
        ac_target_pct = float(ac_target_pct_str)
    except ValueError as e:
        print("\t{}".format(e))
        ask_target_pct(ac_name, pct_left)
    if ac_target_pct < 0 or ac_target_pct > pct_left:
        print("\tTarget percentage must be in [0.0, {}]".format(pct_left))
        ask_target_pct(ac_name, pct_left)
    return ac_target_pct


def setup_security(ac_name: str) -> Tuple[str, bool]:
    """
    Collects user input to set up a security".
    """
    security: Tuple[str, str] = ask_security(ac_name)
    security_id: str = security[0]
    security_name: str = security[1]
    confirm_security: bool = ask_confirm_security(security_name)
    if not confirm_security:
        setup_security(ac_name)
    allow_purchase: bool = ask_allow_purchase()
    return (security_id, allow_purchase)


def setup_asset_class(
    first: bool, existing_total_pct: float
) -> Dict[str, str]:
    """
    Collects user input to set up an asset class.
    """
    asset_class: Dict[str, Any] = {}

    # Get name
    ac_name: str = ask_asset_class_name(first)
    asset_class["name"] = ac_name

    # Get target percentage
    pct_left: float = 1.0 - existing_total_pct
    ac_target_pct: float = ask_target_pct(ac_name, pct_left)
    asset_class["target_percentage"] = ac_target_pct

    # Get securities and buy restrictions
    asset_class["securities"] = []
    asset_class["buy_restrictions"] = []
    add_sec: bool = True
    while add_sec:
        security: Tuple[str, bool] = setup_security(ac_name)
        security_id: str = security[0]
        allow_purchase: bool = security[1]
        asset_class["securities"].append(security_id)
        if not allow_purchase:
            asset_class["buy_restrictions"].append(security_id)
        add_sec_str: str = ask_user_input(
            "\tAdd another security to {}? [Y/n] ".format(ac_name)
        )
        add_sec = add_sec_str.lower() == "y" or add_sec_str == ""
    return asset_class


if __name__ == "__main__":

    logging.basicConfig(
        format="%(asctime)-15s %(levelname)s: %(message)s", level=logging.INFO
    )
    log = logging.getLogger("onboard")

    # Get portfolio configuration from user
    portfolio_config_file = os.path.join(
        os.getcwd(), "config", "test_portfolio.json"
    )
    portfolio_config: List[Dict[str, Any]] = []
    first: bool = True
    total_pct: float = 0.0
    while total_pct < 1:
        ac: Dict[str, Any] = setup_asset_class(first, total_pct)
        portfolio_config.append(ac)
        total_pct += ac["target_percentage"]
        first = False

    # Get Robinhood credentials from user (only to store locally)
    credentials_config_file = os.path.join(
        os.getcwd(), "config", "test_credentials.json"
    )
    credentials_config: Dict[str, str] = {}
    credentials_config["username"] = ask_user_input(
        "Enter Robinhood username/email: "
    )
    credentials_config["password"] = ask_user_input(
        "Enter Robinhood password: "
    )

    # Write config data to local machine
    with open(portfolio_config_file, "w") as f:
        f.write(json.dumps(portfolio_config, indent=4))
    print("\nPortfolio config written to {}".format(portfolio_config_file))
    with open(credentials_config_file, "w") as f:
        f.write(json.dumps(credentials_config, indent=4))
    print("\nCredentials written to {}".format(credentials_config_file))
