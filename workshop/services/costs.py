from workshop.models import Costs, RepairItem, Estimate
from typing import Dict, List


def calculate_total_costs_by_repair_item(costs: List[Costs]) -> Dict[str, float]:
    total_cost, total_profit, total = 0, 0, 0

    for cost in costs:
        if cost.cost_type == "cost":
            total_cost += float(cost.amount)

        if cost.cost_type == "profit":
            total_profit += float(cost.amount)

    return {
        "cost": total_cost,
        "profit": total_profit,
        "total": total_profit + total_cost
    }


def calculate_total_costs_by_estimate(costs: List[Costs]) -> Dict[str, float]:
    total_cost, total_profit, total = 0, 0, 0

    for cost in costs:
        if cost.cost_type == "cost":
            total_cost += float(cost.amount)

        if cost.cost_type == "profit":
            total_profit += float(cost.amount)

    return {
        "cost": total_cost,
        "profit": total_profit,
        "total": total_profit + total_cost
    }
