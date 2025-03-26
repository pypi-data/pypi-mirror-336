from dmstockapi.api_client import ApiClient
from dmstockapi.constant import FutureStrategyEnum, SellStypeEnum, FutureOpenCloseEnum
from dmstockapi.exceptions import DMStockRequestException
from dmstockapi.future_model import FutureTradeModel, FutureAlgoExec


class FutureClient(ApiClient):

    def future_trade_planning(
        self, account_id="", portfolio_id="", isdataframe=True, **kwargs
    ):
        params = self._merge_two_dicts(
            {
                "account": account_id,
                "portfolioid": portfolio_id,
                "isdataframe": isdataframe,
            },
            kwargs,
        )
        r = self._get("/api/v3/future-plan/plans", params=params)
        return r

    def future_trade_plan(self, plan_id="", isdataframe=True, **kwargs):
        params = self._merge_two_dicts(
            {
                "planid": plan_id,
                "isdataframe": isdataframe,
            },
            kwargs,
        )
        r = self._get("/api/v3/future-plan/plan", params=params)
        return r

    def future_trade_portfolio(self, account_id="", isdataframe=True, **kwargs):
        params = self._merge_two_dicts(
            {
                "account": account_id,
                "isdataframe": isdataframe,
            },
            kwargs,
        )
        r = self._get("/api/v3/future-plan/account-portfolios", params=params)
        return r

    def future_trade_accountinfo(self, account_id="", isdataframe=True, **kwargs):
        params = self._merge_two_dicts(
            {
                "account": account_id,
                "isdataframe": isdataframe,
            },
            kwargs,
        )
        r = self._get("/api/v3/account-info/future-accounts", params=params)
        return r

    def future_trade_order(self, params: FutureTradeModel, isdataframe=False, **kwargs):

        if params.volume <= 0:
            raise DMStockRequestException(
                f"非法参数: 仓位 ({params.volume}) <= 0.0, {params.__dict__}"
            )

        if (
            params.strategy
            in [
                FutureStrategyEnum.LIMITP.value,
                FutureStrategyEnum.LIMITV.value,
                FutureStrategyEnum.LIMITS.value,
            ]
            and params.price == 0.00
        ):
            raise DMStockRequestException(
                f"非法参数: 限价指令的价格 ({params.price}) <= 0.0, {params.__dict__}"
            )

        position_ids = list(set(params.position_ids))
        if (
            params.openclose
            in [
                FutureOpenCloseEnum.CloseLong.value,
                FutureOpenCloseEnum.CloseShort.value,
            ]
            and params.sell_stype == SellStypeEnum.Positionid.value
            and len(position_ids) == 0
        ):
            raise DMStockRequestException(
                f"非法参数: 按仓位卖出 未指定仓位ID ({params.positionids}) 为空, {params.__dict__}"
            )

        req_params = self._merge_two_dicts(
            {
                "account": params.account,
                "portfolioid": params.portfolioid,
                "planid": params.planid,
                "sid": params.sid,
                "openclose": params.openclose,
                "volume": params.volume,
                "strategy": params.strategy,
                "strategyid": params.strategyid,
                "price": params.price,
                "ordtype": params.ordtype,
                "remark": params.remark,
                "sell_stype": params.sell_stype,
                "position_ids": ",".join(position_ids),
                "position_order": params.position_order,
                "isdataframe": isdataframe,
            },
            kwargs,
        )
        r = self._post("/api/v3/future-trade/trade", params=req_params)
        return r

    def future_algo_orders(self, isdataframe=False, **kwargs):
        params = self._merge_two_dicts(
            {
                "isdataframe": isdataframe,
            },
            kwargs,
        )
        r = self._get("/api/v3/future-trade/orders", params=params)
        return r

    def future_trade_singleorder(self, order_id="", isdataframe=False, **kwargs):
        params = self._merge_two_dicts(
            {
                "oid": order_id,
                "isdataframe": isdataframe,
            },
            kwargs,
        )
        r = self._get("/api/v3/future-trade/single-order", params=params)
        return r

    def future_algo_exec(self, params: FutureAlgoExec, isdataframe=False, **kwargs):

        if params.exec_price <= 0 or params.exec_volume <= 0:
            raise DMStockRequestException(f"非法参数: {params.__dict__}")

        req_params = self._merge_two_dicts(
            {
                "oid": params.oid,
                "orderStatus": params.order_status,
                "execPrice": params.exec_price,
                "execVol": params.exec_volume,
                "errMsg": params.err_msg,
                "isdataframe": isdataframe,
            },
            kwargs,
        )
        r = self._post("/api/v3/future-trade/algo-exec", params=req_params)
        return r
