from dmstockapi.api_client import ApiClient
from dmstockapi.exceptions import DMStockRequestException
from dmstockapi.stock_model import *


class StockClient(ApiClient):

    def query_algo(self, isdataframe=True, **kwargs) -> List[OrderModel]:
        params = self._merge_two_dicts(
            {
                "isdataframe": isdataframe,
            },
            kwargs,
        )

        r = self._get("/api/v3/stock-trade/orders", params=params)
        return r

    def query_algo_summary(self, isdataframe=True, **kwargs) -> List[OrderSummaryModel]:
        params = self._merge_two_dicts(
            {
                "isdataframe": isdataframe,
            },
            kwargs,
        )

        r = self._get("/api/v3/stock-trade/order-summary", params=params)
        return r

    def query_algo_netstat(self, isdataframe=True, **kwargs) -> List[OrderNetstatModel]:
        params = self._merge_two_dicts(
            {
                "isdataframe": isdataframe,
            },
            kwargs,
        )

        r = self._get("/api/v3/stock-trade/order-netstat", params=params)
        return r

    def query_account(self, isdataframe=True, **kwargs) -> List[InvestAccountModel]:
        params = self._merge_two_dicts(
            {
                "isdataframe": isdataframe,
            },
            kwargs,
        )

        r = self._get("/api/v3/account-info/stock-accounts", params=params)
        return r

    def query_account_planning(
        self, params: QueryAccountPlans, isdataframe=True, **kwargs
    ) -> List[PlanModel]:
        if params.account == "":
            raise DMStockRequestException(f"Invalid Request Params: {params.__dict__}")

        req_params = self._merge_two_dicts(
            {
                "account": params.account,
                "isdataframe": isdataframe,
            },
            kwargs,
        )

        r = self._get("/api/v3/stock-plan/plans", params=req_params)
        return r

    def query_plan_position(
        self, params: QueryPlanPosition, isdataframe=True, **kwargs
    ):
        if params.planid == "":
            raise DMStockRequestException(f"Invalid Request Params: {params.__dict__}")

        req_params = self._merge_two_dicts(
            {
                "planId": params.planid,
                "isdataframe": isdataframe,
            },
            kwargs,
        )
        r = self._get("/api/v3/stock-plan/plan-position", params=req_params)
        return r

    def check_plan(self, account: str, portfolioid: str, planid: str, sid: str):
        plans_resp = self.query_account_planning(
            QueryAccountPlans(account=account), isdataframe=False
        )
        if plans_resp["status"] == 200:
            for plan in plans_resp["data"]:
                if (
                    plan["portfolioid"] == portfolioid
                    and plan["planid"] == planid
                    and plan["sym"] == sid
                ):
                    return True
        return False

    def stock_buy(self, params: StockTradeBuyModel, isdataframe=False, **kwargs):
        if params.amount <= 0:
            raise DMStockRequestException(
                f"非法参数: 金额 ({params.amount}) <= 0, {params.__dict__}"
            )

        # if params.order_type in [OrderTypeEnum.DTO.value, OrderTypeEnum.GTD.value] and params.condition == "":
        #     raise DMStockRequestException(f"Invalid Request Params: (condition), {params.__dict__}")
        #
        if (
            params.strategy
            in [
                StrategyEnum.LIMITP.value,
                StrategyEnum.LIMITV.value,
                StrategyEnum.LIMITS.value,
            ]
            and params.price <= 0.00
        ):
            raise DMStockRequestException(
                f"非法参数: 限价指令的价格 ({params.price}) <= 0.0, {params.__dict__}"
            )

        if not self.check_plan(
            params.account, params.portfolioid, params.planid, params.sid
        ):
            raise DMStockRequestException(
                f"交易计划不存在或填写错误: {params.__dict__}"
            )

        req_params = self._merge_two_dicts(
            {
                "account": params.account,
                "portfolioid": params.portfolioid,
                "planid": params.planid,
                "sid": params.sid,
                "credit": params.credit,
                "amount": params.amount,
                "strategy": params.strategy,
                "strategyid": params.strategyid,
                "price": params.price,
                "ordtype": params.ordtype,
                "condition": params.condition,
                "remark": params.remark,
                "isdataframe": isdataframe,
            },
            kwargs,
        )
        r = self._post("/api/v3/stock-trade/trade-buy", params=req_params)
        if r["status"] != 200:
            raise DMStockRequestException(f"{r}")
        return r

    def stock_sell(self, params: StockTradeSellModel, isdataframe=False, **kwargs):
        if params.volume <= 0:
            raise DMStockRequestException(
                f"非法参数: 仓位 ({params.volume}) <= 0.0, {params.__dict__}"
            )

        # if params.order_type in [OrderTypeEnum.DTO.value, OrderTypeEnum.GTD.value] and params.condition == "":
        #     raise DMStockRequestException(f"Invalid Request Params: (condition), {params.__dict__}")
        #
        if (
            params.strategy
            in [
                StrategyEnum.LIMITP.value,
                StrategyEnum.LIMITV.value,
                StrategyEnum.LIMITS.value,
            ]
            and params.price == 0.00
        ):
            raise DMStockRequestException(
                f"非法参数: 限价指令的价格 ({params.price}) <= 0.0, {params.__dict__}"
            )

        positionids = list(set(params.positionids))
        if (
            params.sell_stype == SellStypeEnum.Positionid.value
            and len(positionids) == 0
        ):
            raise DMStockRequestException(
                f"非法参数: 按仓位卖出 未指定仓位ID ({params.positionids}) 为空, {params.__dict__}"
            )

        if not self.check_plan(
            params.account, params.portfolioid, params.planid, params.sid
        ):
            raise DMStockRequestException(
                f"交易计划不存在或填写错误: {params.__dict__}"
            )

        req_params = self._merge_two_dicts(
            {
                "account": params.account,
                "portfolioid": params.portfolioid,
                "planid": params.planid,
                "sid": params.sid,
                "strategy": params.strategy,
                "strategyid": params.strategyid,
                "price": params.price,
                "ordtype": params.ordtype,
                "condition": params.condition,
                "remark": params.remark,
                "volume": params.volume,
                "sell_stype": params.sell_stype,
                "positionids": ",".join(positionids),
                "position_order": params.position_order,
                "isdataframe": isdataframe,
            },
            kwargs,
        )
        r = self._post("/api/v3/stock-trade/trade-sell", params=req_params)
        if r["status"] != 200:
            raise DMStockRequestException(f"{r}")
        return r

    def modify_algo_limit_price(
        self, params: ModifyLimitPriceReq, isdataframe=False, **kwargs
    ):

        req_params = self._merge_two_dicts(
            {
                "oid": params.oid,
                "price": params.price,
                "isdataframe": isdataframe,
            },
            kwargs,
        )
        r = self._post("/api/v3/stock-trade/modify-limit-price", params=req_params)
        return r

    def cancel_algo(self, params: CancelAlgoReq, isdataframe=False, **kwargs):

        req_params = self._merge_two_dicts(
            {
                "orderIds": params.oid,
                "ordStatus": OrdStatus.PendingCancel.value,
                "nonOrder": False,
                "isdataframe": isdataframe,
            },
            kwargs,
        )
        r = self._post("/api/v3/stock-trade/modify-status", params=req_params)
        return r

    def stock_trade_plans(
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
        r = self._get("/api/v3/stock-plan/plans", params=params)
        return r

    def stock_trade_plan(self, plan_id="", isdataframe=True, **kwargs):
        params = self._merge_two_dicts(
            {
                "planid": plan_id,
                "isdataframe": isdataframe,
            },
            kwargs,
        )
        r = self._get("/api/v3/stock-plan/plan", params=params)
        return r

    def stock_trade_portfolio(self, account_id="", isdataframe=True, **kwargs):
        plans = self.stock_trade_plans(account_id=account_id, isdataframe=isdataframe)
        plans["status"] = 0
        plans["portfolioname"] = plans["portfolioid"]
        r = plans[
            ["account", "portfolioname", "portfolioid", "status"]
        ].drop_duplicates()
        return r
