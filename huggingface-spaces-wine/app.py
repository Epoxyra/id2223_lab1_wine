import gradio as gr
from PIL import Image
import requests
import hopsworks
import joblib
import pandas as pd
import os

os.environ['HOPSWORKS_API_KEY'] = 'cKV1tKzokpcwviY6.uP2qcFV2wWI8xxNu1I0UxyeqlRHqSEanLgKFjf5R1ypSy8A3AUnRkRpi0R9Gc5l0'

""
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


demo = gr.Interface(
    fn=wine,
    title="Wine quality predictive analytics",
    description="Experiment with different properties of wine to predict what is its quality.",
    allow_flagging="never",
    inputs=[
        gr.inputs.Number(default=1, label="wine color (1 for red, 0 for white)"),
        gr.inputs.Number(default=8.0, label="fixed acidity (g/L)"),
        gr.inputs.Number(default=8.0, label="volatile acidity (g/L)"),
        gr.inputs.Number(default=8.0, label="citric acid (g/L)"),
        gr.inputs.Number(default=2.5, label="residual sugar (g/L)"),
        gr.inputs.Number(default=2.5, label="chlorides (g/L)"),
        gr.inputs.Number(default=16.0, label="free_sulfur_dioxide (mg/l)"),
        gr.inputs.Number(default=46.0, label="density (g/mL)"),
        gr.inputs.Number(default=46.0, label="ph"),
        gr.inputs.Number(default=46.0, label="sulphates (mg/L)"),
        gr.inputs.Number(default=10.0, label="alcohol(°)"),
    ],
    outputs=gr.Image(type="pil"))

demo.launch(debug=True)
