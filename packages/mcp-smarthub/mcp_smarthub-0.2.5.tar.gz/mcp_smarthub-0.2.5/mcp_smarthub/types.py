"""Common types used across the SmartHub extension."""
from typing import Dict, List, Optional, Union
from typing_extensions import TypedDict

class MerchantOwnership(TypedDict):
    merchant_token: str
    business_id: str
    active_owner_id: str
    has_unexpired_dm: bool
    time_start: str
    time_end: Optional[str]
    is_current: bool

class AMInfo(TypedDict):
    merchant_token: str
    treatment_group: str
    am_team: str
    am_name: str
    sfdc_owner_id: str
    treatment_month: str
    treatment_quarter: str

class BusinessInfo(TypedDict):
    business_id: str
    business_name: str
    merchant_cluster_name: str
    user_token: str
    ultimate_parent_account_id: str
    account_id: str
    is_ultimate_parent: bool

class MerchantSummary(TypedDict):
    merchant_token: Optional[str]
    business_id: Optional[str]
    business_name: Optional[str]
    current_am: Optional[str]
    am_team: Optional[str]
    is_current: Optional[bool]
    last_updated: Optional[str]

class MerchantResponse(TypedDict):
    status: str
    summary: Optional[MerchantSummary]
    details: Optional[Dict[str, Union[MerchantOwnership, AMInfo, BusinessInfo]]]
    data_sources: List[str]
    message: Optional[str]

class TableInfo(TypedDict):
    name: str
    schema: str
    database: str
    kind: str

class TablesResponse(TypedDict):
    status: str
    tables: Optional[List[TableInfo]]
    message: Optional[str]

class ConnectionResponse(TypedDict):
    status: str
    role: Optional[str]
    message: Optional[str]