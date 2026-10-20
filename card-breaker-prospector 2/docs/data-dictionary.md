# Output data dictionary

Primary CSV `prospects.csv` fields, in order:

1. `Breaker / Brand`: Public business or selling display name.
2. `Whatnot / Fanatics / eBay`: Pipe-separated platform-specific public storefront URLs, prefix each with Whatnot:, Fanatics:, eBay: as applicable. Other selling links go into evidence.
3. `Instagram / YouTube`: Pipe-separated profile URLs, prefixed with Instagram: or YouTube:.
4. `Audience size and promotion`: Observed platform-specific audience counts plus how recent breaks are promoted, with sources in evidence. No guessed counts.
5. `Business Email`: Public, plausibly business-use published email only; blank if unavailable.
6. `Email Source URL`: Exact URL where the email is displayed. Blank if email unavailable.
7. `Website / Linktree`: Official website or owned link-in-bio URL, separated by ` | `.
8. `SMS Program`: Yes / No / Unknown. Yes requires an actual evidenced signup/promotion; No only where explicit source confirms absence (rare). Otherwise Unknown.
9. `Recent Activity`: Explicit public activity date (YYYY-MM-DD) and description. Blank if not verified.
10. `Priority Score`: Numeric 0-100 calculated reproducibly per `docs/scoring.md`.

Additional columns for audit and workflow:
- `Email Status`: Published / Unverified / Missing. `Published` is NOT inbox or deliverability validation.
- `Email Verification`: Deliverability verified / Not checked / Failed (only use verified if a legitimate verifier has returned result).
- `Activity Source URL`: Link with the dated activity.
- `SMS Source URL`: Link showing SMS opt-in when SMS Program=Yes.
- `Identity Source URL`: Link substantiating seller-brand identification.
- `Score Rationale`: Explanation of calculated factors.
- `Research Date`: YYYY-MM-DD of review.
- `Review Status`: Ready / Needs review. Set to Needs review by failed checks or by any text in the optional JSONL `review_flags` list (researcher or auditor caveats).
- `Notes`: Brief factual gaps or caveats.

`evidence.csv` records prospect brand, claim type, value, source URL, observed date and notes. `review_queue.csv` contains rows with missing or conflicting critical evidence.
