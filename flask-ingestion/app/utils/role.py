def get_role_id_by_name(data, name):
    for item in data:
        if item.name.value == name:
            return item.id
        
    return None