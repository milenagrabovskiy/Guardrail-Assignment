from app.MGLabAgent.controls import for_partner
from app.MGLabAgent.store import save_record
from app.MGLabAgent.tools import CLAIMS


def test_partner_payload_has_no_raw_pii():
    claim = CLAIMS["C-0001"]

    payload = for_partner(claim)
    payload_text = str(payload)

    assert claim["name"] not in payload_text, f"Error. Name leaked into partner"
    assert claim["email"] not in payload_text, f"Error. Email leaked into partner"
    assert claim["phone"] not in payload_text, f"Error. Phone leaked into partner"
    assert "4111111111111111" not in payload_text, f"Error. Card # leaked into partner"


def test_storage_has_no_raw_pii(tmp_path):
    claim = CLAIMS["C-0001"]

    log_path = tmp_path / "agent.log"

    save_record(str(claim), path=str(log_path))

    stored_text = log_path.read_text() #reading from the written log

    assert claim["name"] not in stored_text, f"Error. Name leaked into storage"
    assert claim["email"] not in stored_text, f"Error. Email leaked into storage"
    assert claim["phone"] not in stored_text, f"Error. Phone leaked into storage"