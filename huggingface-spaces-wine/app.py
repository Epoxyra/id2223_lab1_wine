import gradio as gr
from PIL import Image
import requests
import hopsworks
import joblib
import pandas as pd

project = hopsworks.login()
fs = project.get_feature_store()

mr = project.get_model_registry()
model = mr.get_model("wine_model", version=1)
model_dir = model.download()
model = joblib.load(model_dir + "/wine_model.pkl")
print("Model downloaded")


def wine(type, fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides, free_sulfur_dioxide, density,
         ph, sulphates, alcohol):
    print("Calling function")
    #     df = pd.DataFrame([[sepal_length],[sepal_width],[petal_length],[petal_width]],
    df = pd.DataFrame([[type, fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides,
                        free_sulfur_dioxide, density, ph, sulphates, alcohol]],
                      columns=["type", "fixed_acidity", "volatile_acidity", "citric_acid", "residual_sugar", "chlorides"
                          , "free_sulfur_dioxide", "density", "ph", "sulphates", "alcohol"])
    print("Predicting")
    print(df)
    # 'res' is a list of predictions returned as the label.
    res = model.predict(df)
    # We add '[0]' to the result of the transformed 'res', because 'res' is a list, and we only want 
    # the first element.
    #     print("Res: {0}").format(res)
    print(res)
    wine_url = "https://raw.githubusercontent.com/Epoxyra/id2223_lab1_wine/main/images/" + res[0] + ".jpg"
    img = Image.open(requests.get(wine_url, stream=True).raw)            
    return img


demo = gr.Interface(
    fn=wine,
    title="Wine quality predictive analytics",
    description="Experiment with different properties of wine to predict what is its quality.",
    allow_flagging="never",
    inputs=[
        gr.Number(value=1, label="wine color (1 for red, 0 for white)"),
        gr.Number(value=8.0, label="fixed acidity (g/L)"),
        gr.Number(value=8.0, label="volatile acidity (g/L)"),
        gr.Number(value=8.0, label="citric acid (g/L)"),
        gr.Number(value=2.5, label="residual sugar (g/L)"),
        gr.Number(value=2.5, label="chlorides (g/L)"),
        gr.Number(value=16.0, label="free_sulfur_dioxide (mg/l)"),
        gr.Number(value=46.0, label="density (g/mL)"),
        gr.Number(value=46.0, label="ph"),
        gr.Number(value=46.0, label="sulphates (mg/L)"),
        gr.Number(value=10.0, label="alcohol(°)"),
    ],
    outputs=gr.Image(type="pil"))

demo.launch(debug=True)
