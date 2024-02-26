from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Endpoint for receiving time series data via POST request
@app.route('/timeseries', methods=['POST'])
def handle_timeseries():
    # Check if the request contains JSON data
    if request.is_json:
        try:
            data = request.get_json()  # Get JSON data from the request
            # Assuming the JSON data contains a list of time series data points
            time_series_data = data.get('time_series', [])


            date = '2023-06-01'
            dateEnd = '2023-07-01'
            
            timestamp1 = pd.Timestamp(date)
            timestamp2 = pd.Timestamp(dateEnd)
            with open('sarimax_model without exog.pkl', 'rb') as f:
                loaded_model = pickle.load(f)
            predictions = loaded_model.get_prediction(start=timestamp1, end=timestamp2,dynamic=True,step=30)

            # Extract the predicted values
            predicted_values = predictions.predicted_mean
            pred = predicted_values
            
            # Here you can perform any processing or analysis on the time series data
            # For example, you could pass it to your SARIMAX model for prediction
            
            # Dummy response indicating successful processing
            response = {
                'status': 'success',
                'message': str(pred)
            }
            return jsonify(response), 200
        except Exception as e:
            # Handle any exceptions that occur during processing
            error_response = {
                'status': 'error',
                'message': 'An error occurred while processing the time series data',
                'error_details': str(e)
            }
            return jsonify(error_response), 500
    else:
        # Return error response if the request does not contain JSON data
        return jsonify({'error': 'Request must contain JSON data'}), 400

if __name__ == '__main__':
    app.run(debug=True)
