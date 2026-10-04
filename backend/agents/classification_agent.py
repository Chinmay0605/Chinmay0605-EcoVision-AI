class ClassificationAgent:
    """
    Normalizes the Vision Agent's prediction into
    a standard EcoVision waste category.
    """

    CATEGORY_MAP = {
        "plastic waste": {
            "category": "Plastic",
            "material": "Plastic",
            "recyclable": True,
        },

        "paper waste": {
            "category": "Paper",
            "material": "Paper",
            "recyclable": True,
        },

        "cardboard waste": {
            "category": "Cardboard",
            "material": "Cardboard",
            "recyclable": True,
        },

        "glass waste": {
            "category": "Glass",
            "material": "Glass",
            "recyclable": True,
        },

        "metal waste": {
            "category": "Metal",
            "material": "Metal",
            "recyclable": True,
        },

        "organic food waste": {
            "category": "Organic",
            "material": "Organic",
            "recyclable": False,
        },

        "electronic waste": {
            "category": "E-Waste",
            "material": "Electronic",
            "recyclable": False,
        },

        "textile waste": {
            "category": "Textile",
            "material": "Fabric",
            "recyclable": False,
        },

        "hazardous waste": {
            "category": "Hazardous",
            "material": "Hazardous Material",
            "recyclable": False,
        },

        "general household waste": {
            "category": "General Waste",
            "material": "Mixed",
            "recyclable": False,
        },
    }

    def classify(self, vision_result):

        label = vision_result["label"].lower().strip()

        waste_info = self.CATEGORY_MAP.get(
            label,
            {
                "category": "General Waste",
                "material": "Unknown",
                "recyclable": False,
            }
        )

        return {
            "waste_type": label,
            "category": waste_info["category"],
            "material": waste_info["material"],
            "recyclable": waste_info["recyclable"],
            "confidence": vision_result["confidence"],
        }


classification_agent = ClassificationAgent()