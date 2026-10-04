class KnowledgeAgent:
    """
    Provides structured waste-management knowledge
    based on the classified waste category.
    """

    KNOWLEDGE_BASE = {

        "Plastic": {
            "bin": "Dry Waste",
            "disposal": "Place clean and dry plastic in the dry/recyclable waste stream.",
            "handling": "Remove leftover contents and rinse the container if necessary.",
            "eco_tip": "Avoid single-use plastic and prefer reusable alternatives.",
        },

        "Paper": {
            "bin": "Dry Waste",
            "disposal": "Place clean and dry paper in the recyclable waste stream.",
            "handling": "Keep paper dry and separate from food-contaminated material.",
            "eco_tip": "Reuse paper whenever possible before recycling.",
        },

        "Cardboard": {
            "bin": "Dry Waste",
            "disposal": "Flatten cardboard and place it with recyclable dry waste.",
            "handling": "Remove excessive tape, plastic wrapping and food contamination.",
            "eco_tip": "Reuse cardboard boxes before sending them for recycling.",
        },

        "Glass": {
            "bin": "Dry/Recyclable Waste",
            "disposal": "Place clean glass in the appropriate recyclable waste stream.",
            "handling": "Handle broken glass carefully and wrap sharp pieces securely.",
            "eco_tip": "Reuse glass containers where practical.",
        },

        "Metal": {
            "bin": "Dry/Recyclable Waste",
            "disposal": "Place clean metal containers with recyclable dry waste.",
            "handling": "Empty and clean containers before disposal.",
            "eco_tip": "Choose reusable metal products when possible.",
        },

        "Organic": {
            "bin": "Wet Waste",
            "disposal": "Place food and organic waste in the wet/compostable waste stream.",
            "handling": "Keep organic waste separate from dry recyclables.",
            "eco_tip": "Compost suitable food and garden waste.",
        },

        "E-Waste": {
            "bin": "E-Waste",
            "disposal": "Take electronic waste to an authorized e-waste collection point.",
            "handling": "Do not place electronics in normal household bins.",
            "eco_tip": "Repair or responsibly recycle electronics instead of discarding them.",
        },

        "Textile": {
            "bin": "Textile/Donation",
            "disposal": "Donate reusable clothing or use an appropriate textile recycling channel.",
            "handling": "Keep textiles clean and dry.",
            "eco_tip": "Reuse, repair or donate clothing before recycling.",
        },

        "Hazardous": {
            "bin": "Hazardous Waste",
            "disposal": "Use an authorized hazardous-waste collection facility.",
            "handling": "Do not mix hazardous material with normal household waste.",
            "eco_tip": "Follow local hazardous-waste handling instructions.",
        },

        "General Waste": {
            "bin": "General Waste",
            "disposal": "Place only non-recyclable material in the general-waste stream.",
            "handling": "Check whether individual components can be separated and recycled.",
            "eco_tip": "Reduce, reuse and recycle before sending material to general waste.",
        },
    }

    def get_knowledge(self, category):

        return self.KNOWLEDGE_BASE.get(
            category,
            self.KNOWLEDGE_BASE["General Waste"]
        )


knowledge_agent = KnowledgeAgent()