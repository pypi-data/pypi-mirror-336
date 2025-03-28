import os
import sys
import json
from typing import Dict, List, Optional, Union, Literal
from enum import Enum

from pydantic import BaseModel, Field


from pydantic2.agents.utils.model_factory import UniversalModelFactory


# Define models for testing (simplified version of product catalog models)
class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"
    CAD = "CAD"

class DeliveryMethod(str, Enum):
    standard = "standard"
    express = "express"
    overnight = "overnight"
    pickup = "pickup"

class Dimension(BaseModel):
    length: float = Field(description="Length in centimeters")
    width: float = Field(description="Width in centimeters")
    height: float = Field(description="Height in centimeters")
    weight: Optional[float] = Field(None, description="Weight in kilograms")

class InventoryLocation(BaseModel):
    warehouse_name: str = Field(description="Name of the warehouse")
    shelf_id: str = Field(description="Shelf identifier")
    quantity: int = Field(description="Quantity at this location")

class InventoryInfo(BaseModel):
    sku: str = Field(description="Stock keeping unit")
    total_quantity: int = Field(description="Total quantity available")
    reorder_level: int = Field(description="Level at which to reorder")
    locations: List[InventoryLocation] = Field(description="Warehouse locations")

class ShippingOption(BaseModel):
    method: DeliveryMethod = Field(description="Shipping method")
    cost: float = Field(description="Shipping cost")
    estimated_days: int = Field(description="Estimated delivery time in days")
    restrictions: Optional[List[str]] = Field(None, description="Shipping restrictions")

class TestCatalogItem(BaseModel):
    name: str = Field(description="Product name")
    description: str = Field(description="Product description")
    price: float = Field(description="Base price")
    currency: Currency = Field(description="Price currency")
    inventory: InventoryInfo = Field(description="Inventory information")
    dimensions: Optional[Dimension] = Field(None, description="Product dimensions")
    categories: List[str] = Field(description="Product categories")
    shipping_options: List[ShippingOption] = Field(description="Shipping options")
    attributes: Dict[str, str] = Field(description="Product attributes")


def main():
    # Create a model factory
    factory = UniversalModelFactory(TestCatalogItem)  # Use seed for reproducible results

    # Generate test data
    print("Generating test catalog item...")
    catalog_item = factory.build()

    # Pretty print the generated data
    catalog_json = catalog_item.model_dump()
    print(json.dumps(catalog_json, indent=2))

    # Validate that our data looks realistic
    print("\nValidation checks:")
    print(f"- Inventory has {len(catalog_item.inventory.locations)} locations")
    print(f"- Warehouse names look realistic: {all('Distribution' in loc.warehouse_name or 'Center' in loc.warehouse_name or 'Warehouse' in loc.warehouse_name or 'Facility' in loc.warehouse_name for loc in catalog_item.inventory.locations)}")
    print(f"- Shelf IDs follow pattern: {all(loc.shelf_id[0].isalpha() and '-' in loc.shelf_id for loc in catalog_item.inventory.locations)}")
    print(f"- Shipping days are reasonable: {all(option.estimated_days <= 10 for option in catalog_item.shipping_options)}")
    print(f"- Dimensions are not null: {catalog_item.dimensions is not None}")
    print(f"- Currency is an enum value: {catalog_item.currency in Currency}")
    print(f"- Price is a reasonable value: {1 <= catalog_item.price <= 1000}")

    # Generate multiple instances to check variance
    print("\nGenerating 5 more instances...")
    for i in range(5):
        item = factory.generate(TestCatalogItem)
        print(f"\nItem {i+1}:")
        print(f"  Name: {item.name}")
        print(f"  Price: {item.price} {item.currency}")
        print(f"  Categories: {', '.join(item.categories)}")
        print(f"  Attributes: {len(item.attributes)} attributes")
        if item.dimensions:
            print(f"  Dimensions: L{item.dimensions.length} x W{item.dimensions.width} x H{item.dimensions.height}")
        else:
            print("  Dimensions: None")


if __name__ == "__main__":
    main()
