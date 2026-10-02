from bedrock_agentcore.runtime import BedrockAgentCoreApp

from tools import read_claim, send_to_partner
from controls import for_partner
from store import save_record


app = BedrockAgentCoreApp()


@app.entrypoint
def invoke(payload):
    claim_id = payload.get("prompt")

    claim = read_claim(claim_id)

    if not claim:
        return {"error": f"claim not found with id: {claim_id}"}

    partner_payload = for_partner(claim)
    partner_result = send_to_partner(partner_payload)

    save_record(str(claim))

    return {
        "answer": f"claim {claim_id} is for a {claim['product']} with issue: {claim['issue']}",
        "partner_result": partner_result
    }


if __name__ == "__main__":
    app.run()