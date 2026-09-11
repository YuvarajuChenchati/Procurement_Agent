from app.services.candidate_selector import select_candidates


def test_select_candidates_limits_each_geography():
    vendors = [{"vendor_name": f"A{i}", "geographic_category": "ahmedabad"} for i in range(7)]
    vendors += [{"vendor_name": f"I{i}", "geographic_category": "india"} for i in range(6)]
    vendors += [{"vendor_name": f"G{i}", "geographic_category": "global"} for i in range(4)]

    selected = select_candidates(vendors, limit_per_category=5)

    assert len(selected) == 14
    assert sum(item["geographic_category"] == "ahmedabad" for item in selected) == 5
    assert sum(item["geographic_category"] == "india" for item in selected) == 5
    assert sum(item["geographic_category"] == "global" for item in selected) == 4
