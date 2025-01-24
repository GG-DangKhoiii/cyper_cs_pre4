lstDemo = [
    {
        "id": 1,
        "value": [
            {
                "id": 2,
                "value": [
                    {
                        "id": 3,
                        "value": [
                            {
                                "id": 4,
                                "value": []
                            }
                        ]
                    }
                ]
            }
        ]
    },
    {
        "id": 5,
        "value": []
    }
]


def extract_ids(data):
    ids = []
    for item in data:
        ids.append(item["id"])
        
        if item["value"]:
            ids.extend(extract_ids(item["value"]))
    
    return ids

# Gọi hàm
result = extract_ids(lstDemo)
print(result)
