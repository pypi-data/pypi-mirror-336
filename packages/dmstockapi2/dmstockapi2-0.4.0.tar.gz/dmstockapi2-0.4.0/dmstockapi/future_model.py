from pydantic import BaseModel, Field

from dmstockapi.constant import (
    FutureOpenCloseEnum,
    FutureStrategyEnum,
    FutureOrderTypeEnum,
    SellStypeEnum,
    PositionOrderEnum,
    OrdStatus,
)


class FutureTradeModel(BaseModel):
    """
    期货指令参数
    """

    account: str = Field(..., title="投资账号")
    portfolioid: str = Field(..., title="组合ID")
    planid: str = Field(..., title="计划ID")

    sid: str = Field(..., title="合约代码")
    openclose: FutureOpenCloseEnum = Field(..., title="开仓/平仓")
    volume: int = Field(0.0, title="数量")
    strategy: FutureStrategyEnum = Field(..., title="交易策略")
    strategyid: str = Field("", title="量化策略")
    price: float = Field(0.00, title="价格", description="strategy为限价时有效")
    ordtype: FutureOrderTypeEnum = Field(
        FutureOrderTypeEnum.Normal.value, title="指令类型"
    )

    remark: str = Field("", title="备注")

    sell_stype: SellStypeEnum = Field(
        SellStypeEnum.Positionid.value, title="卖出仓位方式"
    )

    position_order: PositionOrderEnum = Field(
        PositionOrderEnum.DateAsc.value,
        title="仓位排序, stype 为 SellStypeEnum.Volume 有效, 自动匹配仓位进行卖出",
    )
    position_ids: list = Field(
        [],
        title="卖出的仓位ID, stype 为 SellStypeEnum.Positionid 有效, 手动选择仓位进行卖出",
    )

    class Config:
        # Will remove whitespace from string and byte fields
        str_strip_whitespace = True
        use_enum_values = True


class FutureAlgoExec(BaseModel):
    """
    期货成交回报
    """

    oid: str = Field(..., title="algoOid")
    order_status: OrdStatus = Field(..., title="状态")
    exec_price: float = Field(0.0, title="成交价格")
    exec_volume: int = Field(0.0, title="卖量")
    err_msg: str = Field("", title="错误提示")

    class Config:
        # Will remove whitespace from string and byte fields
        str_strip_whitespace = True
