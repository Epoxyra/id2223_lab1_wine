import os
import modal

LOCAL=False

if LOCAL == False:
   stub = modal.Stub("wine_daily")
   image = modal.Image.debian_slim().pip_install(["hopsworks"]) 

   @stub.function(image=image, schedule=modal.Period(days=1), secret=modal.Secret.from_name("id2223"))
   def f():
       g()


def generate_wine(quality, fixed_acidity_min, fixed_acidity_max, volatile_acidity_min, volatile_acidity_max,
                    citric_acid_min, citric_acid_max, residual_sugar_min, residual_sugar_max,
                    chlorides_min, chlorides_max, free_sulfur_dioxide_min, free_sulfur_dioxide_max,
                    density_min, density_max, ph_min, ph_max, sulphates_min, sulphates_max,
                    alcohol_min, alcohol_max):
    """
    Returns a single wine as a single row in a DataFrame
    """
    import pandas as pd
    import random

    df = pd.DataFrame({ "type": random.choice([0, 1]),
                        "fixed_acidity": [random.uniform(fixed_acidity_min, fixed_acidity_max)],
                        "volatile_acidity": [random.uniform(volatile_acidity_min, volatile_acidity_max)],
                        "citric_acid": [random.uniform(citric_acid_min, citric_acid_max)],
                        "residual_sugar": [random.uniform(residual_sugar_min, residual_sugar_max)],
                        "chlorides": [random.uniform(chlorides_min, chlorides_max)],
                        "free_sulfur_dioxide": [random.uniform(free_sulfur_dioxide_min, free_sulfur_dioxide_max)],
                        "density": [random.uniform(density_min, density_max)],
                        "ph": [random.uniform(ph_min, ph_max)],
                        "sulphates": [random.uniform(sulphates_min, sulphates_max)],
                        "alcohol": [random.uniform(alcohol_min, alcohol_max)]
                      })
    df['quality_label'] = quality
    return df

def get_random_wine():
    """
    Returns a DataFrame containing one random wine
    """
    import pandas as pd
    import random

    good_wine_df = generate_wine("good", 3.9, 15.6, 0.08, 0.915, 0, 0.76, 0.8, 19.25, 0.012, 0.358, 3, 108, 0.98711, 1.0032, 2.84, 3.82, 0.22, 1.36, 8.5, 14.2)
    medium_wine_df = generate_wine("medium", 3.8, 15.9, 0.08, 1.33, 0, 1.66, 0.6, 65.8, 0.009, 0.611, 1, 131, 0.98722, 1.03898, 2.72, 4.01, 0.23, 1.98, 8, 14.9)
    poor_wine_df =  generate_wine("poor", 4.2, 12.5, 0.11, 1.58, 0, 1, 0.7, 17.55, 0.013, 0.61, 3, 289, 0.9892, 1.001, 2.74, 3.9, 0.25, 2, 8, 13.5)

    # randomly pick one of these 3 and write it to the featurestore
    pick_random = random.uniform(0,3)
    if pick_random >= 2:
        quality_df = good_wine_df
        print("good_wine added")
    elif pick_random >= 1:
        quality_df = medium_wine_df
        print("medium_wine added")
    else:
        quality_df = poor_wine_df
        print("poor_wine added")

    return quality_df


def g():
    import hopsworks
    import pandas as pd

    project = hopsworks.login()
    fs = project.get_feature_store()

    quality_df = get_random_wine()

    quality_fg = fs.get_feature_group(name="wine",version=2)
    quality_fg.insert(quality_df)

if __name__ == "__main__":
    if LOCAL == True :
        g()
    else:
        stub.deploy("wine_daily")
        with stub.run():
            f()
