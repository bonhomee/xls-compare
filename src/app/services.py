from __future__ import annotations

import re
from dataclasses import dataclass
from typing import BinaryIO, Iterable

import pandas as pd

BASE_BALANCE_PREFIX = 400_000_000


@dataclass
class ProviderRecord:
    provider_id: str
    provider_name: str
    amount: float


@dataclass
class ComparisonResult:
    matches: list[dict]
    differences: list[dict]
    only_in_balance: list[ProviderRecord]
    only_in_ddp: list[ProviderRecord]
    totals: dict


def _extract_digits(value) -> str | None:
    if pd.isna(value):
        return None
    text = str(value).strip()
    if not text:
        return None
    digits = "".join(ch for ch in text if ch.isdigit())
    return digits or None


def _normalize_balance_id(value) -> str | None:
    digits = _extract_digits(value)
    if not digits:
        return None
    return digits.zfill(9)


def normalize_ddp_id(value) -> str | None:
    digits = _extract_digits(value)
    if not digits:
        return None
    trimmed = digits[-4:] if len(digits) > 4 else digits
    number = int(trimmed)
    if number == 0:
        number = 1
    if number < 1000:
        number += 1000
    return f"40000{number:04d}"


def _clean_amount(value) -> float:
    if pd.isna(value):
        return 0.0
    text = str(value).strip()
    if not text:
        return 0.0
    text = text.replace(",", "")
    try:
        return float(text)
    except ValueError:
        return 0.0


def load_balance_records(file_stream: BinaryIO) -> list[ProviderRecord]:
    df = pd.read_excel(
        file_stream,
        skiprows=7,
        header=None,
        usecols=[0, 1, 5],
        names=["provider_id", "provider_name", "amount"],
        dtype={0: str, 1: str},
    )
    df["provider_id"] = df["provider_id"].apply(_normalize_balance_id)
    df["provider_name"] = df["provider_name"].fillna("").astype(str).str.strip()
    df["amount"] = df["amount"].apply(_clean_amount)
    df = df.dropna(subset=["provider_id"])
    df = df.drop_duplicates(subset=["provider_id"], keep="first")

    return [
        ProviderRecord(
            provider_id=row.provider_id,
            provider_name=row.provider_name,
            amount=row.amount,
        )
        for row in df.itertuples(index=False)
    ]


def load_ddp_records(file_stream: BinaryIO) -> list[ProviderRecord]:
    df = pd.read_excel(
        file_stream,
        skiprows=2,
        header=None,
        usecols=[1, 2, 3],
        names=["provider_name", "provider_number", "amount"],
        dtype={1: str, 2: str},
    )
    df["provider_id"] = df["provider_number"].apply(normalize_ddp_id)
    df["provider_name"] = df["provider_name"].fillna("").astype(str).str.strip()
    df["amount"] = df["amount"].apply(_clean_amount)
    df = df.dropna(subset=["provider_id"])

    def _first_non_empty(series: Iterable[str]) -> str:
        for item in series:
            if item:
                return item
        return ""

    grouped = df.groupby("provider_id", as_index=False).agg(
        {"amount": "sum", "provider_name": _first_non_empty}
    )

    return [
        ProviderRecord(
            provider_id=row.provider_id,
            provider_name=row.provider_name,
            amount=row.amount,
        )
        for row in grouped.itertuples(index=False)
    ]


def compare_records(balance_file, ddp_file) -> ComparisonResult:
    balance_records = load_balance_records(balance_file)
    ddp_records = load_ddp_records(ddp_file)

    balance_map = {record.provider_id: record for record in balance_records}
    ddp_map = {record.provider_id: record for record in ddp_records}

    matches: list[dict] = []
    differences: list[dict] = []
    only_in_balance: list[ProviderRecord] = []
    only_in_ddp: list[ProviderRecord] = []

    # Sólo procesamos proveedores que existan en ambos archivos
    common_provider_ids = sorted(set(balance_map) & set(ddp_map))

    for provider_id in common_provider_ids:
        balance_record = balance_map[provider_id]
        ddp_record = ddp_map[provider_id]

        # DDP puede venir en positivo y Balance en negativo: sumamos para obtener la diferencia neta
        diff = ddp_record.amount + balance_record.amount
        observations = (
            "De más en DDP" if diff > 0 else "De más en BALANCE" if diff < 0 else "Equilibrado"
        )
        record = {
            "provider_id": provider_id,
            "provider_name": balance_record.provider_name or ddp_record.provider_name,
            "balance_amount": balance_record.amount,
            "ddp_amount": ddp_record.amount,
            "difference": diff,
            "observation": observations,
        }
        matches.append(record)
        if abs(diff) > 0.0001:
            differences.append(record)

    totals = {
        "balance": sum(record.amount for record in balance_records),
        "ddp": sum(record.amount for record in ddp_records),
    }

    return ComparisonResult(
        matches=matches,
        differences=differences,
        only_in_balance=only_in_balance,
        only_in_ddp=only_in_ddp,
        totals=totals,
    )
