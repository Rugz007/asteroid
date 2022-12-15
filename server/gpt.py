from flask import Flask, request
from jupyter_client import BlockingKernelClient

app = Flask(__name__)

# Create a blocking kernel client
client = BlockingKernelClient()
client.start_channels()

@app.route("/run_code", methods=["POST"])
def run_code():
    # Get the code to run from the request data
    code = request.json["code"]

    # Run the code and get the result
    result = client.execute_interactive(code)

    # Return the result as JSON
    return result["content"]["data"]["text/plain"]

if __name__ == "__main__":
    app.run()