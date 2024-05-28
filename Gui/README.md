# Trading Bot

## Prepare Data
The data has to be prepared as follows:
- First run ```python prepare_test_data.py```
    - This downloads all csv files for the specified stocks and prepares the data
    - Output is a merged dataframe saved to a CSV File
- Then run ```python predict_test_data.py```
    - This preprocesses the data from the merged dataframe and adds predictions
    - Output is a dataframe with predictions from the CNN model

## GUI
There are several versions of the GUI:
- app_V1.py: First version and protoype
- app_V2.py: Final version for prediction of stocks
- app_V3.py: Final version for prediction of stocks and crypto
\

The GUI does use csv files from /predicted_data folder where the predictions of models are represented (csv files have to be prepared before using the GUI -> see chapter above).
### Run GUI
- To start the GUI simply run ```streamlit run app_V2.py```