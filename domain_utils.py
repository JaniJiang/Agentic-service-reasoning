DOMAIN_MAP = {
    "gpt_chat": {
        "api_map": {
            "": "非RAG",
            "QASearch": "QASearch",
            "AUTOSearch": "AUTOSearch",
            "MEDIASearch": "MEDIASearch"
        },
        "default": "RAG其他"
    },
    "gpt_autoqa": "汽车问答",
    "in_car_assistant": "服务专家",
    "taskmaster": "任务大师",
    "default": "NONE"
}


def get_real_domain(msg_dict):
    """统一处理领域映射逻辑"""
    domain = msg_dict["domain"]
    mapping = DOMAIN_MAP.get(domain, DOMAIN_MAP["default"])
    if isinstance(mapping, dict):  # 需要处理API名称的情况
        api_name = msg_dict["api_name"]
        return mapping["api_map"].get(api_name, mapping["default"])
    return mapping
