# broker-api-integration-examples

The **broker-as-a-plugin** pattern: keep your strategy broker-agnostic and swap venues by changing one adapter. This repo shows the *shape* of a clean integration layer — interface + two stub adapters — not real credentials or proprietary code.

> Educational skeleton. Adapters are stubs; wire official broker SDKs yourself and test on sandbox. Not advice. MIT, no warranty.

## Idea
```
Strategy  ->  emits Intent("buy", symbol, qty)
                 |
           Risk gate (vetoes if needed)
                 |
           BrokerAdapter (one per broker)  ->  official API
```
Switching Zerodha -> Fyers -> Dhan should be: change the adapter, not the strategy.

## Files
- `broker_adapter.py` — the `BrokerAdapter` interface + an `Intent` dataclass + two stub adapters + a tiny risk gate

Real adapters should handle: auth/session refresh, reconnects, product types, partial fills, rate limits, and logging (see our blog/YouTube).
