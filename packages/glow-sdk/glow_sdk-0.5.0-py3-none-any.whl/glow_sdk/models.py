# Copyright Gustav Ebbers
import datetime

from pydantic import BaseModel


class Member(BaseModel):
    id: int
    user_id: int
    platform_id: int
    email: str
    first_name: str | None
    last_name: str | None
    point_balance: int
    lifetime_points: int
    birthday: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    referral_code: str | None
    referred_by: str | None
    multiplier: str
    vip_tier_id: int
    current_vip_tier_id: None
    current_vip_tier_name: None
