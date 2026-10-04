from PIL import Image
from transformers import pipeline


class VisionAgent:
    """
    EcoVision AI Vision Agent

    Uses CLIP zero-shot image classification
    to identify household waste categories.
    """

    def __init__(self):
        print("Loading EcoVision Vision Agent...")

        self.classifier = pipeline(
            "zero-shot-image-classification",
            model="openai/clip-vit-base-patch32"
        )

        self.candidate_labels = [
            "plastic waste",
            "paper waste",
            "cardboard waste",
            "glass waste",
            "metal waste",
            "organic food waste",
            "electronic waste",
            "textile waste",
            "hazardous waste",
            "general household waste"
        ]

        print("Vision Agent loaded successfully!")

    def get_confidence_level(self, confidence):
        """
        Converts raw confidence into a user-friendly
        confidence level.
        """

        if confidence >= 70:
            return {
                "level": "High",
                "status": "trusted",
                "message": "The AI is highly confident in this prediction."
            }

        if confidence >= 55:
            return {
                "level": "Moderate",
                "status": "review",
                "message": "The AI has moderate confidence. Consider reviewing the image."
            }

        return {
            "level": "Low",
            "status": "uncertain",
            "message": "The AI is not sufficiently confident. Try uploading a clearer image."
        }

    def analyze(self, image_path: str):

        image = Image.open(image_path).convert("RGB")

        results = self.classifier(
            image,
            candidate_labels=self.candidate_labels
        )

        best_result = results[0]

        confidence = round(
            best_result["score"] * 100,
            2
        )

        confidence_info = self.get_confidence_level(
            confidence
        )

        return {
            "label": best_result["label"],

            "confidence": confidence,

            "confidence_level": confidence_info["level"],

            "confidence_status": confidence_info["status"],

            "confidence_message": confidence_info["message"],

            "alternatives": [
                {
                    "label": result["label"],
                    "confidence": round(
                        result["score"] * 100,
                        2
                    )
                }
                for result in results[1:4]
            ]
        }


vision_agent = VisionAgent()