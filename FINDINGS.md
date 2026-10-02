# Findings


| Leak | Where the data crossed | Where I closed it | What it still misses |
|---|---|---|---|
| OUT | From the agent to the partner | Using `for_partner()`, an allow-list of approved fields, and `ApplyGuardrail` | The guardrail may not detect every sensitive pattern, so some PII could still leak unless additional patterns or validation are added |
| IN | From the store into the agent | *(not closed)* | PII can still appear in free-text fields such as `notes` before the agent sees it |
| STORED | From the agent to the log file | Using `for_storage()` with Comprehend `detect_pii_entities` to redact PII before writing | Comprehend may miss unusual formats or PII types that it does not recognize |


## Fail open or fail closed? 
If Comprehend or the guardrail is unavailable when a record is about to be written,
what does your code do — and is that what you intended? Say which you chose and why.

I chose to fail closed. If Comprehend is unavailable, 
the application does not write the raw record to the log. If the Bedrock guardrail
is unavailable or blocks the outbound payload, the application does not send the data to 
the partner. I chose this because preventing a PII leak is more important than completing
the write or send operation.


## What I would do with another day
I would add an inbound control before data reaches the agent so
unexpected PII in fields like notes can be detected or redacted earlier.
I would also add more tests for different PII types and service failures.