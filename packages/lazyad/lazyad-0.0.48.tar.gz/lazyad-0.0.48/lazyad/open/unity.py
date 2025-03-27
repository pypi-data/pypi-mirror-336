from lazysdk import lazyrequests
from lazysdk import lazybase64


def make_auth(
        keyid,
        secret_key
):
    """
    生成校验字符串
    :param keyid:
    :param secret_key:
    :return:
    """
    authorization = f"{keyid}:{secret_key}"
    return f"Basic {lazybase64.lazy_b64encode(authorization)}"


def apps(
        organization_id,
        keyid,
        secret_key
):
    """
    获取app列表
    https://services.docs.unity.com/advertise/v1/index.html#section/Get-Started/First-Call:-List-Apps
    :param organization_id:
    :param keyid:
    :param secret_key:
    :return:
    """
    url = f"https://services.api.unity.com/advertise/v1/organizations/{organization_id}/apps"
    headers = {"Authorization": make_auth(keyid=keyid, secret_key=secret_key)}
    return lazyrequests.lazy_requests(
        method="GET",
        url=url,
        headers=headers
    )


def list_campaigns(
        organization_id,
        app_id,
        keyid,
        secret_key
):
    """
    获取Campaigns列表
    https://services.docs.unity.com/advertise/v1/index.html#tag/Campaigns
    :param organization_id:
    :param app_id:
    :param keyid:
    :param secret_key:
    :return:
    """
    url = f"https://services.api.unity.com/advertise/v1/organizations/{organization_id}/apps/{app_id}/campaigns"
    headers = {"Authorization": make_auth(keyid=keyid, secret_key=secret_key)}
    return lazyrequests.lazy_requests(
        method="GET",
        url=url,
        headers=headers
    )


def get_campaign(
        organization_id,
        app_id,
        campaign_id,
        keyid,
        secret_key,
        include_fields: list = None
):
    """
    获取Campaign信息
    https://services.docs.unity.com/advertise/v1/index.html#tag/Campaigns/operation/advertise_getCampaign
    :param organization_id:
    :param app_id:
    :param campaign_id:
    :param keyid:
    :param secret_key:
    :param include_fields: ["cpiBids", "sourceBids", "roasBids", "retentionBids", "eventOptimizationBids", "budget"]
    :return:
    """
    default_include_fields = ["cpiBids", "sourceBids", "roasBids", "retentionBids", "eventOptimizationBids", "budget"]
    url = f"https://services.api.unity.com/advertise/v1/organizations/{organization_id}/apps/{app_id}/campaigns/{campaign_id}"
    headers = {"Authorization": make_auth(keyid=keyid, secret_key=secret_key)}
    if include_fields:
        pass
    else:
        include_fields = default_include_fields
    params_list = list()
    for each in include_fields:
        params_list.append(f"includeFields={each}")
    params_str = "&".join(params_list)
    return lazyrequests.lazy_requests(
        method="GET",
        url=f"{url}?{params_str}",
        headers=headers
    )


def get_budget(
        organization_id,
        app_id,
        campaign_id,
        keyid,
        secret_key
):
    """
    获取 Campaign budget
    https://services.docs.unity.com/advertise/v1/index.html#tag/Campaigns/operation/advertise_getCampaignBudget
    :param organization_id:
    :param app_id:
    :param campaign_id:
    :param keyid:
    :param secret_key:
    :return:
    """
    url = f"https://services.api.unity.com/advertise/v1/organizations/{organization_id}/apps/{app_id}/campaigns/{campaign_id}/budget"
    headers = {"Authorization": make_auth(keyid=keyid, secret_key=secret_key)}
    return lazyrequests.lazy_requests(
        method="GET",
        url=url,
        headers=headers
    )


def get_targeting_options(
        organization_id,
        app_id,
        campaign_id,
        keyid,
        secret_key
):
    """
    Get targeting options
    https://services.docs.unity.com/advertise/v1/index.html#tag/Campaigns/operation/advertise_getTargeting
    :param organization_id:
    :param app_id:
    :param campaign_id:
    :param keyid:
    :param secret_key:
    :return:
    """
    url = f"https://services.api.unity.com/advertise/v1/organizations/{organization_id}/apps/{app_id}/campaigns/{campaign_id}/targeting"
    headers = {"Authorization": make_auth(keyid=keyid, secret_key=secret_key)}
    return lazyrequests.lazy_requests(
        method="GET",
        url=url,
        headers=headers
    )


def update_targeting_options(
        organization_id,
        app_id,
        campaign_id,
        keyid,
        secret_key,
        allow_list: list = None,
        block_list: list = None,
        iso_os_min: str = None
):
    """
    Update targeting options
    https://services.docs.unity.com/advertise/v1/index.html#tag/Campaigns/operation/advertise_updateTargeting
    :param organization_id:
    :param app_id:
    :param campaign_id:
    :param keyid:
    :param secret_key:

    :param allow_list:
    :param block_list:
    :param iso_os_min:
    :return:
    """
    url = f"https://services.api.unity.com/advertise/v1/organizations/{organization_id}/apps/{app_id}/campaigns/{campaign_id}/targeting"
    headers = {"Authorization": make_auth(keyid=keyid, secret_key=secret_key)}
    data = {}
    if allow_list or block_list:
        data["appTargeting"] = {}
        if allow_list:
            data["appTargeting"]["allowList"] = allow_list
        if block_list:  # 黑名单
            data["appTargeting"]["blockList"] = block_list
    if iso_os_min:
        data["deviceTargeting"] = {}
        if iso_os_min:
            data["deviceTargeting"]["osMin"] = iso_os_min
    return lazyrequests.lazy_requests(
        method="PATCH",
        url=url,
        headers=headers,
        json=data
    )
