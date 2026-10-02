import boto3
from config import AWS_REGION, GUARDRAIL_ID, GUARDRAIL_VERSION


comprehend = boto3.client("comprehend", AWS_REGION)
bedrock_runtime = boto3.client("bedrock-runtime", AWS_REGION)


PARTNER_ALLOW = []

STORAGE_ALLOW = []


def for_partner(claim: dict) -> dict:

    payload = {
        "claim_id": claim.get("claim_id"),
        "product": claim.get("product"),
        "issue": claim.get("issue")
    }

    text = str(payload)

    response = bedrock_runtime.apply_guardrail(
        guardrailIdentifier=GUARDRAIL_ID,
        guardrailVersion=GUARDRAIL_VERSION,
        source="OUTPUT",
        content=[
            {
                "text": {
                    "text": text
                }
            }
        ]
    )
    if response.get("action") == "GUARDRAIL_INTERVENED":
        raise ValueError("Outbound payload blocked by guardrail")

    return payload

    # 1. allow-list only the fields the partner needs
    # 2. run ApplyGuardrail
    # 3. return safe payload



def for_storage(text: str) -> str:
    # 1. call Comprehend detect_pii_entities
    # 2. replace detected PII with [REDACTED]
    # 3. return safe text
    response = comprehend.detect_pii_entities(
        Text=text,
        LanguageCode="en"
    )

    entities = response.get("Entities", [])

    redacted = text

    # Replace from end to beginning so character indexes stay correct.
    for entity in sorted(
            entities,
            key=lambda e: e["BeginOffset"],
            reverse=True
    ):
        start = entity["BeginOffset"]
        end = entity["EndOffset"]

        redacted = (
                redacted[:start]
                + "[REDACTED]"
                + redacted[end:]
        )

    return redacted