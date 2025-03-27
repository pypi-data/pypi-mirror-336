#!/usr/bin/env python
"""
Product catalog example with multiple levels of nesting.
"""

import os
import asyncio
from typing import List, Dict, Optional, Union, Literal
from pydantic import BaseModel, Field
from enum import Enum

# Import from our library
from pydantic2.agents import FormProcessor, UniversalModelFactory
from pydantic2.agents import BaseAnalyticsTools, OpenRouterProvider

# Get API key from environment
API_KEY = os.environ.get("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("Please set the OPENROUTER_API_KEY environment variable")

# Define enums for better type constraints
class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    RUB = "RUB"

class DeliveryMethod(str, Enum):
    STANDARD = "standard"
    EXPRESS = "express"
    NEXT_DAY = "next_day"
    PICKUP = "pickup"

# Define nested models (multiple levels of nesting)
class Dimension(BaseModel):
    """Product dimensions."""
    length: float = Field(default=0.0, description="Length in centimeters")
    width: float = Field(default=0.0, description="Width in centimeters")
    height: float = Field(default=0.0, description="Height in centimeters")
    weight: float = Field(default=0.0, description="Weight in kilograms")

class PriceInfo(BaseModel):
    """Product pricing details."""
    base_price: float = Field(default=0.0, description="Base price")
    discount_percent: float = Field(default=0.0, description="Discount percentage")
    currency: Currency = Field(default=Currency.USD, description="Currency")
    tax_rate: float = Field(default=0.0, description="Tax rate percentage")

    def final_price(self) -> float:
        """Calculate final price after discount."""
        discounted = self.base_price * (1 - self.discount_percent / 100)
        return discounted * (1 + self.tax_rate / 100)

class InventoryLocation(BaseModel):
    """Inventory location information."""
    warehouse_name: str = Field(default="", description="Warehouse name")
    shelf_id: str = Field(default="", description="Shelf identifier")
    quantity: int = Field(default=0, description="Quantity available")

class InventoryInfo(BaseModel):
    """Inventory information."""
    sku: str = Field(default="", description="Stock keeping unit")
    total_quantity: int = Field(default=0, description="Total quantity in all locations")
    reorder_level: int = Field(default=10, description="Level at which to reorder")
    locations: List[InventoryLocation] = Field(default_factory=list, description="Warehouse locations")

class Variant(BaseModel):
    """Product variant information."""
    name: str = Field(default="", description="Variant name (e.g., 'Blue, Large')")
    sku: str = Field(default="", description="Variant SKU")
    attributes: Dict[str, str] = Field(default_factory=dict, description="Variant attributes (e.g., color, size)")
    price_adjustment: float = Field(default=0.0, description="Price adjustment for this variant")
    inventory: InventoryInfo = Field(default_factory=InventoryInfo, description="Inventory information")
    dimensions: Optional[Dimension] = Field(default=None, description="Variant dimensions")

class ShippingOption(BaseModel):
    """Shipping option information."""
    method: DeliveryMethod = Field(default=DeliveryMethod.STANDARD, description="Delivery method")
    cost: float = Field(default=0.0, description="Shipping cost")
    estimated_days: int = Field(default=0, description="Estimated delivery time in days")
    restrictions: List[str] = Field(default_factory=list, description="Shipping restrictions")

class ProductForm(BaseModel):
    """Comprehensive product information form with multiple levels of nesting."""
    # Basic info
    name: str = Field(default="", description="Product name")
    description: str = Field(default="", description="Product description")
    brand: str = Field(default="", description="Brand name")
    categories: List[str] = Field(default_factory=list, description="Product categories")
    tags: List[str] = Field(default_factory=list, description="Product tags")

    # Nested price and inventory
    base_price_info: PriceInfo = Field(default_factory=PriceInfo, description="Base pricing information")
    default_inventory: InventoryInfo = Field(default_factory=InventoryInfo, description="Default inventory information")

    # Physical properties
    dimensions: Dimension = Field(default_factory=Dimension, description="Product dimensions")

    # Variants (can have their own pricing, inventory, dimensions)
    variants: List[Variant] = Field(default_factory=list, description="Product variants")

    # Shipping options
    shipping_options: List[ShippingOption] = Field(default_factory=list, description="Available shipping options")

    # Marketing and SEO
    meta_title: str = Field(default="", description="SEO meta title")
    meta_description: str = Field(default="", description="SEO meta description")
    featured: bool = Field(default=False, description="Whether product should be featured")

# Product analytics implementation
class ProductAnalytics(BaseAnalyticsTools):
    async def analyze_form(self, form_data, form_schema):
        """Analyze the product data with complex nested structure."""
        system_prompt = f"""
        Analyze this product catalog data and provide a comprehensive assessment.

        PRODUCT DATA:
        ```json
        {form_data}
        ```

        Generate a detailed analysis with the following components:
        1. Pricing strategy assessment
        2. Inventory management recommendations
        3. Variant optimization suggestions
        4. Shipping strategy evaluation
        5. SEO and marketing opportunities

        Return your analysis as a structured JSON object with these fields.
        """

        try:
            result = await self.provider.invoke(
                system=system_prompt,
                user="",
                temperature=0.7,
                response_format={"type": "json_object"}
            )

            content = result.choices[0].message.content
            if isinstance(content, str):
                import json
                return json.loads(content)
            return content
        except Exception as e:
            if self.verbose:
                print(f"Analysis error: {e}")
            return {
                "error": str(e),
                "pricing_strategy": "Unable to analyze",
                "inventory_management": "Unable to analyze",
                "variant_optimization": "Unable to analyze",
                "shipping_strategy": "Unable to analyze",
                "seo_marketing": "Unable to analyze"
            }

    async def generate_insights(self, form_data, analysis):
        """Generate insights based on product analysis."""
        system_prompt = f"""
        Generate actionable recommendations for this product based on the analysis.

        PRODUCT DATA:
        ```json
        {form_data}
        ```

        ANALYSIS:
        ```json
        {analysis}
        ```

        Generate 5 specific, high-impact recommendations covering:
        - Pricing optimization
        - Inventory efficiency
        - Product variant strategy
        - Shipping and logistics
        - Marketing and SEO improvement

        Each recommendation should be specific, actionable, and directly tied to the analysis data.
        """

        try:
            result = await self.provider.invoke(
                system=system_prompt,
                user="",
                temperature=0.7
            )

            content = result.choices[0].message.content

            # Split into individual insights
            insights = [line.strip() for line in content.split("\n") if line.strip()]

            # Clean up any numbering or bullets
            import re
            insights = [re.sub(r"^\d+\.\s*|\*\s+|-\s+", "", insight) for insight in insights]

            return insights
        except Exception as e:
            if self.verbose:
                print(f"Insights error: {e}")
            return ["Unable to generate insights due to an error."]

async def main():
    # Create provider
    provider = OpenRouterProvider(
        api_key=API_KEY,
        model_name="openai/gpt-4o-mini"
    )

    # Create analytics
    analytics = ProductAnalytics(provider=provider, verbose=True)

    # Create form processor
    processor = FormProcessor(
        form_class=ProductForm,
        analytics_tools=analytics,
        openrouter_api_key=API_KEY,
        verbose=True
    )

    # Initialize session
    session_id, first_question = await processor.initialize()
    print(f"\nSession: {session_id}")
    print(f"Assistant: {first_question}")

    # Simulate a conversation with deeply nested data
    messages = [
        "I want to add a new gaming laptop product called 'TechPro Gaming X5' made by TechPro. " +
        "It's a high-performance gaming laptop with a 15.6-inch display, Intel i9 processor, and RTX 3080 graphics card.",

        "The laptop belongs to categories 'Electronics', 'Computers', and 'Gaming'. " +
        "We should tag it with 'gaming', 'laptop', 'high-performance', and 'rtx3080'.",

        "The base price is $1,999.99 USD with a 5% discount and 8% tax rate. " +
        "The dimensions are 36cm length, 25cm width, 2cm height, and it weighs 2.5kg.",

        "We have two variants: one with 16GB RAM and 1TB SSD that costs the base price, " +
        "and another with 32GB RAM and 2TB SSD that costs $300 more. " +
        "The 16GB variant has SKU TGX5-16-1TB and the 32GB variant has SKU TGX5-32-2TB.",

        "For inventory, we have 25 units of the 16GB variant with 15 in the Main Warehouse on shelf G12 " +
        "and 10 in the East Warehouse on shelf E5. For the 32GB variant, we have 10 total units, " +
        "all in the Main Warehouse on shelf G13. The reorder level for both variants is 5 units.",

        "We offer three shipping options: Standard shipping for $15 that takes 3-5 days, " +
        "Express shipping for $30 that takes 1-2 days, and Next-day shipping for $50. " +
        "There's a shipping restriction that we can't ship to PO boxes with next-day delivery.",

        "The SEO meta title should be 'TechPro Gaming X5 - Ultimate Gaming Laptop | Shop TechStore' " +
        "and the meta description should be 'Experience unparalleled gaming performance with the TechPro Gaming X5 laptop. " +
        "Featuring Intel i9 processor, RTX 3080 graphics, and up to 32GB RAM. Free shipping available.'",

        "Please mark this product as featured in our store.",

        "Can you analyze this product data and provide recommendations?"
    ]

    for message in messages:
        print(f"\nUser: {message}")
        result = await processor.process_message(message, session_id)
        print(f"Assistant: {result.message}")
        print(f"Progress: {result.progress}%")

    # Get final form state
    state = await processor.get_form_state(session_id)
    print("\nFinal form data:")
    import json
    print(json.dumps(state.form, indent=2))

    # Demo UniversalModelFactory by generating fake product data
    print("\n\nGenerating random product data with ModelFactory:")
    factory = UniversalModelFactory(ProductForm, fill_data=True)
    random_product = factory.build()
    print(json.dumps(random_product.model_dump(), indent=2))

if __name__ == "__main__":
    asyncio.run(main())
