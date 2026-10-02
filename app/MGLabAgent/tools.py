CLAIMS = {
    "C-0001": {
        "claim_id": "C-0001",
        "name": "Amy Jo",
        "email": "amye@gmail.com",
        "phone": "123-456-7890",
        "product": "Keurig coffee machine",
        "issue": "Broke",
        "notes": "Payment reference number 4111111111111111"
    }
}


def read_claim(claim_id: str):
    return CLAIMS.get(claim_id)


def send_to_partner(payload: dict):
    return {"sent": True, "payload": payload}