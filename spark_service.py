from flask import Flask, request, jsonify
import sparknlp
from pyspark.ml import PipelineModel
import itertools

# Start Spark session
spark = sparknlp.start(gpu=False, memory="2G")

# Load the pre-trained and saved pipeline model
prediction_model = PipelineModel.load("pipeline_model")

app = Flask(__name__)

# Route to process text with Spark NLP pipeline
@app.route('/process', methods=['POST'])
def process_text():
    try:
        # Expect text in the JSON body
        input_data = request.json.get("text", [])
        
        # If the text is empty, return an error
        if not input_data:
            return jsonify({"error": "No text provided"}), 400
        
        # Create a DataFrame with the input text
        input_df = spark.createDataFrame([(text,) for text in input_data]).toDF("text")
        
        # Perform the NER predictions using the preloaded model
        preds = prediction_model.transform(input_df)
        preds = preds.select('ner_span.result').collect()
        # preds = list(itertools.chain(*[row.result for row in preds]))

        return jsonify({"predictions": preds, "error": ""})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=False, use_reloader=False)
