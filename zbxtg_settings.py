# -*- coding: utf-8 -*-

tg_key = "gsdfgdfsgsdfgsdfgdfsgdsfg"  # telegram bot api key

zbx_tg_prefix = "zbxtg"  # variable for separating text from script info
zbx_tg_tmp_dir = "/var/tmp/" + zbx_tg_prefix  # directory for saving caches, uids, cookies, etc.
zbx_tg_signature = False

zbx_tg_update_messages = True
zbx_tg_matches = {
    "problem": "PROBLEM: ",
    "ok": "OK: "
}

zbx_server = "https://gdgdsfg"  # zabbix server full url
zbx_api_user = "gdsgsdfg"
zbx_api_pass = "gsdfgsdfg?S"
zbx_api_verify = False  # True - do not ignore self signed certificates, False - ignore

zbx_basic_auth = False
zbx_basic_auth_user = "gsdfgsdfg"
zbx_basic_auth_pass = "gsdfgdsfg"

proxy_to_zbx = None
proxy_to_tg = None



google_maps_api_key = None  # get your key, see https://developers.google.com/maps/documentation/geocoding/intro

zbx_tg_daemon_enabled = False
zbx_tg_daemon_wl_ids = [gdsfgsdfgsdfg, ]
zbx_tg_daemon_wl_u = ["@sgsdfgsdfgdsfgd", ]

zbx_db_host = ""
zbx_db_database = ""
zbx_db_user = ""
zbx_db_password = ""


emoji_map = {
    "OK": "✅",
    "PROBLEM": "❗",
    "info": "ℹ️",
    "WARNING": "⚠️",
    "DISASTER": "❌",
    "bomb": "💣",
    "fire": "🔥",
    "hankey": "💩",
}
