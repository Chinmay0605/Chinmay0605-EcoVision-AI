class DisposalAgent:
    """
    Local Disposal Intelligence Agent.

    Provides city-aware waste disposal guidance.
    Guidance is intentionally based on municipal-level
    waste segregation practices and avoids inventing
    specific collection-point addresses.
    """

    CITY_GUIDANCE = {

        # =====================================================
        # INDORE
        # =====================================================

        "Indore": {

            "general": (
                "In Indore, keep non-recyclable household waste "
                "separate from wet and recyclable dry waste and "
                "hand it over through the municipal collection system."
            ),

            "plastic": (
                "In Indore, keep clean and dry plastic separate "
                "with the dry/plastic waste stream. Avoid mixing "
                "plastic with wet or food waste and hand it over "
                "through the city's segregated collection system."
            ),

            "paper": (
                "In Indore, keep paper clean and dry and place it "
                "with segregated dry waste. Keep food-contaminated "
                "paper separate from recyclable paper."
            ),

            "cardboard": (
                "In Indore, flatten cardboard and keep it with "
                "segregated dry waste. Remove excessive plastic "
                "wrapping and food contamination before collection."
            ),

            "glass": (
                "In Indore, keep glass separate from wet waste and "
                "other loose household material. Wrap broken glass "
                "securely and hand it over as segregated dry/recyclable waste."
            ),

            "metal": (
                "In Indore, keep clean metal containers separate "
                "from wet waste and place them with the appropriate "
                "dry/recyclable waste stream."
            ),

            "organic": (
                "In Indore, place food and other suitable organic "
                "material in the wet/organic waste stream and keep "
                "it separate from dry recyclables."
            ),

            "e-waste": (
                "In Indore, do not mix electronic waste with normal "
                "household waste. Keep e-waste separate and use an "
                "authorized e-waste collection or recycling channel."
            ),

            "textile": (
                "In Indore, keep reusable clothing separate from "
                "household waste. Donate usable textiles or use an "
                "appropriate textile reuse/recycling channel."
            ),

            "hazardous": (
                "In Indore, do not mix hazardous material with "
                "ordinary household waste. Keep it isolated and "
                "use an appropriate authorized hazardous-waste channel."
            ),
        },


        # =====================================================
        # BHOPAL
        # =====================================================

        "Bhopal": {

            "general": (
                "In Bhopal, keep household waste separated by type "
                "and hand it over through the Bhopal Municipal Corporation "
                "collection system. Do not mix recyclable material with "
                "wet or special waste."
            ),

            "plastic": (
                "In Bhopal, keep clean and dry plastic separate from "
                "organic waste. Store it with dry recyclables and hand "
                "it over through the municipal collection system."
            ),

            "paper": (
                "In Bhopal, keep paper dry and free from food contamination. "
                "Store it separately with other recyclable dry material "
                "for municipal collection or recycling."
            ),

            "cardboard": (
                "In Bhopal, flatten cardboard before disposal and keep "
                "it with dry recyclable material. Remove excessive tape, "
                "plastic wrapping and food contamination."
            ),

            "glass": (
                "In Bhopal, keep glass separate from wet waste. Broken "
                "glass should be wrapped securely to prevent injury "
                "during handling and collection."
            ),

            "metal": (
                "In Bhopal, keep recyclable metal separate from wet waste. "
                "Empty and clean containers before placing them with "
                "other dry recyclable material."
            ),

            "organic": (
                "In Bhopal, keep food and other suitable organic waste "
                "separate from dry recyclables and hand it over through "
                "the wet/organic waste collection stream."
            ),

            "e-waste": (
                "In Bhopal, keep electronic devices and components "
                "separate from municipal household waste. Use an "
                "authorized e-waste collection or recycling channel."
            ),

            "textile": (
                "In Bhopal, reusable clothing should preferably be "
                "donated or reused. Keep unwanted textiles clean and "
                "dry before using an appropriate textile-recycling channel."
            ),

            "hazardous": (
                "In Bhopal, keep hazardous material isolated from "
                "normal household waste. Use an appropriate authorized "
                "collection or disposal channel."
            ),
        },


        # =====================================================
        # DELHI
        # =====================================================

        "Delhi": {

            "general": (
                "In Delhi, keep non-recyclable material separate from "
                "dry recyclable and biodegradable waste and hand it "
                "over through the designated MCD waste-collection system."
            ),

            "plastic": (
                "In Delhi, empty food or product contents from plastic "
                "packaging, keep plastic segregated and hand it over to "
                "the designated or authorized MCD collection channel. "
                "Do not burn or litter plastic waste."
            ),

            "paper": (
                "In Delhi, keep clean and dry paper separate with "
                "non-biodegradable dry waste. Recyclable paper can be "
                "handed over through authorized collection or recycling "
                "channels."
            ),

            "cardboard": (
                "In Delhi, flatten cardboard and keep it with dry "
                "non-biodegradable recyclable waste. Keep it away from "
                "food waste and moisture."
            ),

            "glass": (
                "In Delhi, keep glass with segregated dry waste and "
                "handle broken pieces carefully. Do not mix sharp glass "
                "with loose household material."
            ),

            "metal": (
                "In Delhi, keep recyclable metal separate from "
                "biodegradable waste and hand it over through the "
                "appropriate dry-waste collection or recycling channel."
            ),

            "organic": (
                "In Delhi, keep biodegradable food and organic waste "
                "separate from dry waste and hand it over through the "
                "designated biodegradable-waste collection system."
            ),

            "e-waste": (
                "In Delhi, electronic waste should not be mixed with "
                "ordinary municipal waste. Keep it separate and use an "
                "authorized e-waste collection or recycling facility."
            ),

            "textile": (
                "In Delhi, clean reusable clothing should preferably "
                "be donated or reused. For unusable textiles, use an "
                "appropriate textile-recycling or collection channel."
            ),

            "hazardous": (
                "In Delhi, keep hazardous material separate from "
                "ordinary municipal waste and use the appropriate "
                "authorized collection or disposal channel."
            ),
        },


        # =====================================================
        # MUMBAI
        # =====================================================

        "Mumbai": {

            "general": (
                "In Mumbai, keep waste segregated at source and "
                "separate dry, wet and special waste before handing "
                "it over to the municipal collection system."
            ),

            "plastic": (
                "In Mumbai, keep clean and dry plastic with segregated "
                "dry waste. Dry-waste collection and sorting systems "
                "channel recyclable plastic toward recycling."
            ),

            "paper": (
                "In Mumbai, keep paper clean and dry and place it "
                "with segregated dry waste. Avoid mixing paper with "
                "food-contaminated material."
            ),

            "cardboard": (
                "In Mumbai, flatten cardboard and keep it with "
                "segregated dry recyclable waste. Remove unnecessary "
                "plastic wrapping and contamination."
            ),

            "glass": (
                "In Mumbai, keep glass separate from wet waste and "
                "other loose household material. Handle broken glass "
                "carefully before handing it over."
            ),

            "metal": (
                "In Mumbai, keep recyclable metal separate from wet "
                "waste and place it with dry recyclable material for "
                "appropriate collection and sorting."
            ),

            "organic": (
                "In Mumbai, keep food and other suitable organic waste "
                "separate from dry recyclables and hand it over through "
                "the wet-waste collection stream."
            ),

            "e-waste": (
                "In Mumbai, keep electronic waste separate from "
                "municipal dry and wet waste. Use an authorized "
                "e-waste collection or recycling channel."
            ),

            "textile": (
                "In Mumbai, donate usable clothing where possible. "
                "Keep unwanted textiles clean and dry and use an "
                "appropriate reuse or textile-recycling channel."
            ),

            "hazardous": (
                "In Mumbai, keep hazardous material separate from "
                "ordinary municipal waste and use the appropriate "
                "authorized collection or disposal channel."
            ),
        },
    }


    # =========================================================
    # CATEGORY MAPPING
    # =========================================================

    CATEGORY_KEYS = {

        "Plastic":
            "plastic",

        "Paper":
            "paper",

        "Cardboard":
            "cardboard",

        "Glass":
            "glass",

        "Metal":
            "metal",

        "Organic":
            "organic",

        "E-Waste":
            "e-waste",

        "Textile":
            "textile",

        "Hazardous":
            "hazardous",

        "General Waste":
            "general",
    }


    # =========================================================
    # GET GUIDANCE
    # =========================================================

    def get_guidance(
        self,
        category,
        city="Indore"
    ):

        city = (
            str(city)
            .strip()
            .title()
        )


        if city not in self.CITY_GUIDANCE:

            city = "Indore"


        category_key = (
            self.CATEGORY_KEYS.get(
                category,
                "general"
            )
        )


        city_data = (
            self.CITY_GUIDANCE[city]
        )


        local_instruction = (
            city_data.get(
                category_key,
                city_data["general"]
            )
        )


        return {

            "city":
                city,

            "category":
                category,

            "local_instruction":
                local_instruction,

            "important_note": (
                "Local collection schedules, "
                "authorized facilities and municipal "
                "rules can change. Verify the latest "
                "guidance from the relevant municipal "
                "authority before disposal."
            ),

        }


# ============================================================
# SINGLE AGENT INSTANCE
# ============================================================

disposal_agent = DisposalAgent()