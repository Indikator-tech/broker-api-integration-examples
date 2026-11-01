"""Broker-as-a-plugin pattern (stubs only). Educational, MIT, no warranty.
No real credentials, no real orders — wire official SDKs on sandbox yourself.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Intent:
    side: str          # "buy" | "sell"
    symbol: str
    qty: float
    product: str = "intraday"
    price: float | None = None   # None => market


class BrokerAdapter(ABC):
    """Every broker implements this; the strategy never sees broker specifics."""
    @abstractmethod
    def connect(self) -> None: ...
    @abstractmethod
    def place(self, intent: Intent) -> str: ...   # returns order id
    @abstractmethod
    def status(self, order_id: str) -> str: ...


class ZerodhaAdapterStub(BrokerAdapter):
    def connect(self) -> None:
        # real: exchange request_token -> access_token (daily), store in a vault
        print("[zerodha] connect stub (use <ACCESS_TOKEN> from env, never hard-code)")
    def place(self, intent: Intent) -> str:
        print(f"[zerodha] place stub: {intent}")
        return "ZRD-STUB-1"
    def status(self, order_id: str) -> str:
        return "COMPLETE"   # real: poll/stream order updates


class FyersAdapterStub(BrokerAdapter):
    def connect(self) -> None:
        print("[fyers] connect stub (API v3; free API access)")
    def place(self, intent: Intent) -> str:
        print(f"[fyers] place stub: {intent}")
        return "FYR-STUB-1"
    def status(self, order_id: str) -> str:
        return "COMPLETE"


def risk_gate(intent: Intent, *, max_qty: float) -> bool:
    """Veto before any order reaches a broker. Extend with loss/exposure/time checks."""
    if intent.qty <= 0 or intent.qty > max_qty:
        print(f"[risk] blocked: qty {intent.qty} outside (0, {max_qty}]")
        return False
    return True


def route(adapter: BrokerAdapter, intent: Intent, max_qty: float = 1000) -> str | None:
    adapter.connect()
    if not risk_gate(intent, max_qty=max_qty):
        return None
    oid = adapter.place(intent)
    print(f"[route] order {oid} -> {adapter.status(oid)}")
    return oid


if __name__ == "__main__":
    i = Intent("buy", "NIFTY", 50)
    route(ZerodhaAdapterStub(), i)   # swap for FyersAdapterStub() — strategy unchanged
    route(FyersAdapterStub(), i)
