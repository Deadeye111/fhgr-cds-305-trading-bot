# Imports
import pandas as pd
import numpy as np
import joblib
import os
from tensorflow import keras
import matplotlib.pyplot as plt
keras.backend.set_image_data_format('channels_first')


def preprocess_data(merged_df, scaler_path='models/scaler.pkl'):
    merged_df = merged_df.loc[:, 'Open':'adx_neg_21']

    if os.path.exists(scaler_path):
        scaler = joblib.load(scaler_path)
    else:
        print(f"Scaler {scaler_path} not found!")

    # Transform the data using the loaded scaler
    scaled_data = scaler.transform(merged_df.to_numpy())

    print("Data preprocessed..")

    return scaled_data


def select_features(preprocessed_data, feature_indices):
    if feature_indices:
        preprocessed_data = preprocessed_data[:, feature_indices]
    
    print("Features selected..")
    print(preprocessed_data.shape)

    return preprocessed_data


def image_creation(x, number_of_features=64):

    dim = int(np.sqrt(number_of_features))
    img_height = dim
    img_width = dim

    x_temp = np.zeros((len(x), img_height, img_width))
    for i in range(x.shape[0]):
        # print(type(x), type(x_temp), x.shape)
        x_temp[i] = np.reshape(x[i], (img_height, img_width))

    x = np.stack((x_temp,) * 3, axis=-1)

    print("Image creation done..")
    print(f'Shape of x: {x.shape}')

    return x


def plot_images(x, save_path="test_image.png"):
    fig, axs = plt.subplots(1, 6, figsize=(15, 10))

    for i in range(6):
        sample = np.random.randint(0, x.shape[0])
        axs[i].imshow(x[sample])
        axs[i].set_title(f"Picture{i}")
        axs[i].axis('off')

    plt.tight_layout()
    fig.suptitle('Example Images', fontsize=18, y=0.68)
    plt.savefig(save_path)


def get_predictions(x, model_path='models/stock_prediction_model.h5'):
    if os.path.exists(model_path):
        model = keras.models.load_model('models/stock_prediction_model.h5')
        print(model.summary())
    else:
        print(f"Model {model_path} not found!")
        return

    y_pred = model.predict(x)
    print("Prediction of model done..")
    return y_pred


def add_predictions_to_df(df, y_pred, folder_name='predicted_data'):
    for i, row in df.iterrows():
        for j, pred in enumerate(y_pred[i]):
            column_name = f'Prediction_{j+1}'
            if column_name not in df.columns:
                df[column_name] = None  # Initialize the column if it doesn't exist
            df.at[i, column_name] = pred

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print("Created Folder:", folder_name)

    merged_df.to_csv(os.path.join(folder_name, 'predicted_data.csv'))

    print('Predicted data')
    print("DataFrame saved to:", folder_name)
    print("BUY: 0 | SELL: 1 | HOLD: 2")
    return df


merged_df = pd.read_csv('merged_data/merged_data_large.csv')

feature_indices = [33, 34, 35, 36, 37, 38, 39, 40, 42, 43, 44, 
           45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 
           56, 57, 58, 59, 78, 79, 80, 81, 82, 83, 84, 
           85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 
           111, 112, 113, 121, 122, 124, 125, 127, 128, 
           130, 131, 133, 134, 136, 137, 139, 140, 142, 143, 146]


preprocessed_data = preprocess_data(merged_df)
preprocessed_data = select_features(preprocessed_data, feature_indices)
image_data = image_creation(preprocessed_data)
plot_images(image_data)
y_pred = get_predictions(image_data)
predicted_df = add_predictions_to_df(merged_df, y_pred)
print(predicted_df)