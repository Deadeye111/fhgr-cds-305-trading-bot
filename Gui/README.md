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
- To start the GUI simply run ```streamlit run app.py```