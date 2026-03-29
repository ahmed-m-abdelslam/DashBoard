def validate_project(data):
    warnings = []

    if data["packages_completed"] > data["total_packages"] and data["total_packages"] > 0:
        warnings.append(f"Completed packages ({data['packages_completed']}) exceed total ({data['total_packages']})")
        data["packages_completed"] = data["total_packages"]

    if data["delivered_pos"] > data["total_pos"] and data["total_pos"] > 0:
        warnings.append(f"Delivered POs ({data['delivered_pos']}) exceed total ({data['total_pos']})")
        data["delivered_pos"] = data["total_pos"]

    if data.get("overall_completion", 0) > 100:
        warnings.append(f"Overall completion was {data['overall_completion']}%, capped to 100%")
        data["overall_completion"] = 100

    budget = data.get("effective_budget", 0)
    orders = data.get("orders_placed", 0)
    if budget > 0 and orders > budget * 2:
        warnings.append(f"Orders placed ({orders:,.0f}) are over 2x the budget ({budget:,.0f})")

    for field in ["proposed_budget", "client_budget", "orders_placed", "total_packages", "total_pos"]:
        if data.get(field, 0) < 0:
            warnings.append(f"Negative value in {field}: {data[field]}")
            data[field] = 0

    data["_warnings"] = warnings
    return data
