from workshop.models import RepairItem
from typing import Dict, Any


def get_repair_item_statistics() -> Dict[str, Any]:
    repair_items = RepairItem.objects.all()

    num_todo = repair_items.filter(status=False).count()
    num_done = repair_items.filter(status=True).count()
    num_total = repair_items.count()

    priority_low = repair_items.filter(priority="low", status=False).count()
    priority_mid = repair_items.filter(priority="medium", status=False).count()
    priority_high = repair_items.filter(priority="high", status=False).count()

    return {
        "num_todo": num_todo if num_todo > 0 else 0,
        "num_done": num_done if num_done > 0 else 0,
        "num_total": num_total if num_total > 0 else 0,
        "priority_low": priority_low if priority_low > 0 else 0,
        "priority_mid": priority_mid if priority_mid > 0 else 0,
        "priority_high": priority_high if priority_high > 0 else 0,
    }