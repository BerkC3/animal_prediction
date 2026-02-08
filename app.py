"""Gradio web interface for animal classification."""

import gradio as gr
from PIL import Image
from backend import Predictor
import os

predictor = None


def initialize_predictor():
    global predictor
    model_path = "ResNet18_Animals_Best_Acc87.38.pth"

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    predictor = Predictor(model_path)
    print("[OK] Application ready!")
    return predictor


def classify_image(image: Image.Image) -> dict:
    if image is None:
        return {"Error": "Please upload an image first!"}

    if predictor is None:
        return {"Error": "Model not loaded. Please restart the application."}

    try:
        predictions = predictor.get_top_predictions(image, top_k=5)
        return {label.title(): float(score) for label, score in predictions.items()}
    except Exception as e:
        return {"Error": f"Prediction failed: {str(e)}"}


def create_interface() -> gr.Blocks:
    custom_css = """
    .gradio-container { font-family: 'IBM Plex Sans', sans-serif; }
    .gr-button { color: white; border-color: #4CAF50; background: #4CAF50; font-weight: 600; }
    .gr-button:hover { background: #45a049; }
    footer { display: none !important; }
    """

    theme = gr.themes.Soft(
        primary_hue="emerald",
        secondary_hue="blue",
        neutral_hue="slate",
    ).set(
        body_background_fill="*neutral_950",
        body_background_fill_dark="*neutral_950",
        block_background_fill="*neutral_900",
        block_background_fill_dark="*neutral_900",
        input_background_fill="*neutral_800",
        button_primary_background_fill="*primary_600",
        button_primary_background_fill_hover="*primary_500",
    )

    with gr.Blocks(theme=theme, css=custom_css, title="Animal Classification AI") as interface:
        gr.Markdown(
            """
            # 🦁 Animal Classification AI
            ### ResNet18 Deep Learning Model
            
            Classifies **50 different animal species** with 87.38% accuracy.
            Upload an animal photo and see the AI prediction!
            """
        )

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📷 Upload Image")
                image_input = gr.Image(
                    type="pil",
                    label="Animal Photo",
                    sources=["upload", "clipboard"],
                    height=400,
                )
                classify_btn = gr.Button("🔍 Classify", variant="primary", size="lg")
                gr.Markdown(
                    """
                    **💡 Tips:**
                    - Drag and drop or click to upload
                    - Clear photos give better results
                    - Single animal images recommended
                    """
                )

            with gr.Column(scale=1):
                gr.Markdown("### 📊 Prediction Results")
                output_label = gr.Label(label="AI Prediction", num_top_classes=5)
                gr.Markdown(
                    """
                    **📌 Supported Animals (50 Species):**
                    
                    `Antelope`, `Bat`, `Beaver`, `Blue Whale`, `Bobcat`, `Buffalo`,
                    `Chihuahua`, `Chimpanzee`, `Collie`, `Cow`, `Dalmatian`, `Deer`,
                    `Dolphin`, `Elephant`, `Fox`, `German Shepherd`, `Giant Panda`,
                    `Giraffe`, `Gorilla`, `Grizzly Bear`, `Hamster`, `Hippopotamus`,
                    `Horse`, `Humpback Whale`, `Killer Whale`, `Leopard`, `Lion`,
                    `Mole`, `Moose`, `Mouse`, `Otter`, `Ox`, `Persian Cat`, `Pig`,
                    `Polar Bear`, `Rabbit`, `Raccoon`, `Rat`, `Rhinoceros`, `Seal`,
                    `Sheep`, `Siamese Cat`, `Skunk`, `Spider Monkey`, `Squirrel`,
                    `Tiger`, `Walrus`, `Weasel`, `Wolf`, `Zebra`
                    """
                )

        classify_btn.click(fn=classify_image, inputs=image_input, outputs=output_label, api_name="classify")
        image_input.upload(fn=classify_image, inputs=image_input, outputs=output_label)

        gr.Markdown(
            """
            ---
            <div style='text-align: center; color: #888; padding: 20px;'>
                <p>🤖 Powered by PyTorch & ResNet18 | Accuracy: 87.38%</p>
            </div>
            """
        )

    return interface


def main():
    print("=" * 50)
    print("Starting Animal Classification AI")
    print("=" * 50)

    try:
        initialize_predictor()
        interface = create_interface()
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True,
        )
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        raise


if __name__ == "__main__":
    main()
