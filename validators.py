def validate_search_criteria(criteria, available_columns):
    invalid = [key for key in criteria.keys() if key not in available_columns]
    if invalid:
        raise ValueError(f"معايير بحث غير صالحة: {invalid}")
