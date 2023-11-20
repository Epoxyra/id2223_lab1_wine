import os
import modal

LOCAL=False

if LOCAL == False:
   stub = modal.Stub("wine_daily")
   image = modal.Image.debian_slim().pip_install(["hopsworks"]) 

   @stub.function(image=image, schedule=modal.Period(days=1), secret=modal.Secret.from_name("id2223"))
   def f():
       g()


def generate_wine(name, sepal_len_max, sepal_len_min, sepal_width_max, sepal_width_min,
                    petal_len_max, petal_len_min, petal_width_max, petal_width_min):
    """
    Returns a single wine quality as a single row in a DataFrame
    """
    import pandas as pd
    import random

    df = pd.DataFrame({ "sepal_length": [random.uniform(sepal_len_max, sepal_len_min)],
                       "sepal_width": [random.uniform(sepal_width_max, sepal_width_min)],
                       "petal_length": [random.uniform(petal_len_max, petal_len_min)],
                       "petal_width": [random.uniform(petal_width_max, petal_width_min)]
                      })
    df['variety'] = name
    return df


def get_random_quality_wine():
    """
    Returns a DataFrame containing one random wine quality
    """
    import pandas as pd
    import random

    good_wine_df = generate_wine("good_wine", 8, 5.5, 3.8, 2.2, 7, 4.5, 2.5, 1.4)
    medium_wine_df = generate_wine("medium_wine", 7.5, 4.5, 3.5, 2.1, 3.1, 5.5, 1.8, 1.0)
    poor_wine_df =  generate_wine("poor_wine", 6, 4.5, 4.5, 2.3, 1.2, 2, 0.7, 0.3)

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

    quality_df = get_random_quality_wine()

    quality_fg = fs.get_feature_group(name="wine",version=1)
    quality_fg.insert(quality_df)

if __name__ == "__main__":
    if LOCAL == True :
        g()
    else:
        stub.deploy("wine_daily")
        with stub.run():
            f()
