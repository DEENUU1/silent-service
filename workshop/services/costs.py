from workshop.models import Costs, RepairItem
from typing import Dict


def calculate_total_costs_by_repair_item(repair_item: RepairItem) -> Dict[str, float]:
    costs = Costs.objects.filter(repair_item=repair_item)

    total_cost, total_profit, total = 0, 0, 0

    for cost in costs:
        if cost.cost_type == "cost":
            total_cost += float(cost.amount)

        if cost.cost_type == "profit":
            total_profit += float(cost.amount)

    return {
        "cost": total_cost,
        "profit": total_profit,
        "total": total_profit - total_cost
    }
