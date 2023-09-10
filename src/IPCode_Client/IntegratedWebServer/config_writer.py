import orjson
config = {
    "host_info": {
        "host_str": "",
        "host_port": 8000
    },
    "ifconfig": {
        "url": "6.ipw.cn",
        "options": [],
        "cache_validtime": "5"  # "infinite", "none", 秒数
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
