import orjson
config = {
    "host_info": {
        "host_str": "",
        "host_port": 8000
    },
    "ifconfig": {
        "url": "localhost:8001",
        "options": [],
        "cache_validtime": "none",  # "infinite", "none", "min", 秒数。
        "cache_validtime_min": 5,  # "min"的值。
        "cache_validtime_v_none_disabled": True    # True/False。此项默认为True，将使"none"等同于"min"。
    },
    "pages": {
        "homepage": {
            "display_keys": [
                "IPv6", "IPv6_Prefix"
            ]
        }
    }
}

if __name__ == "__main__":
    print('config内容: ')
    config_json = orjson.dumps(config, option=orjson.OPT_INDENT_2)
    print(config_json.decode())
    input('任意输入以确认并继续（写入文件）')
    with open('config.json', 'w') as f:
        f.write(config_json.decode())
    print('操作结束')
