class RecommendationAgent:
    """
    Converts waste-management knowledge into
    simple user-facing recommendations.
    """

    def generate(self, classification, knowledge):

        return {
            "recommended_bin": knowledge["bin"],

            "disposal_instruction": knowledge["disposal"],

            "handling_instruction": knowledge["handling"],

            "eco_tip": knowledge["eco_tip"],

            "recyclable": classification["recyclable"],
        }


# Create the Recommendation Agent instance
recommendation_agent = RecommendationAgent()