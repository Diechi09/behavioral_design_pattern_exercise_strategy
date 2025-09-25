from __future__ import annotations
from domain.pricing import PricingStrategy, NoDiscount, PercentageDiscount, BulkItemDiscount, CompositeStrategy


def choose_strategy(kind: str, **kwargs) -> PricingStrategy:
    # TODO: Implement strategy selection logic based on the 'kind' parameter
    # Should support: "none", "percent", "bulk", "composite"
    # Each strategy type needs different parameters from **kwargs
    # Return the appropriate strategy instance or raise an error for unknown types
    match kind:
        case "none":
            return NoDiscount()
        case "percent":
            percent = kwargs.get("percent", 0.0)
            return PercentageDiscount(percent)
        case "bulk":
            sku = kwargs.get("sku", "")
            threshold = kwargs.get("threshold", 0)
            per_item_off = kwargs.get("per_item_off", 0.0)
            return BulkItemDiscount(sku, threshold, per_item_off)
        case "composite":
            strategies = []
            percent = kwargs.get("percent", 0.0)
            if percent > 0:
                strategies.append(PercentageDiscount(percent))
            sku = kwargs.get("sku", "")
            threshold = kwargs.get("threshold", 0)
            per_item_off = kwargs.get("per_item_off", 0.0)
            if sku and threshold > 0 and per_item_off > 0:
                strategies.append(BulkItemDiscount(sku, threshold, per_item_off))
            return CompositeStrategy(strategies)
        case _:
            raise ValueError(f"Unknown strategy kind: {kind}")
