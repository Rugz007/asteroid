import jupyter_client
from flask import Flask, request
from queue import Queue
import queue
import threading

app = Flask(__name__)


kernel_manager, kernel_client = jupyter_client.manager.start_new_kernel(
    kernel_name="python3"
)


def handle_output(msg):
    msg_type = msg["header"]["msg_type"]
    if msg_type in {"display_data", "execute_result"}:
        data = msg["content"]["text"]
        print("mimetypes: %s" % sorted(data.keys()))

request_queue = Queue()
executing = False

def process_queue():
    global executing
    while True:
        if not request_queue.empty() and not executing:
            code, result_queue = request_queue.get()
            executing = True
            result = execute_code(code)
            result_queue.put(result)
            executing = False


def execute_code(code):
    print(type(code))
    print(code)
    kernel_client.execute(code)
    reply = kernel_client.get_shell_msg()
    io_msg_content = kernel_client.get_iopub_msg()["content"]
    if (
        "execution_state" in io_msg_content
        and io_msg_content["execution_state"] == "idle"
    ):
        return "no output"
    # get the output from the kernel
    while True:
        temp = io_msg_content
        try:
            io_msg_content = kernel_client.get_iopub_msg()["content"]
            if (
                "execution_state" in io_msg_content
                and io_msg_content["execution_state"] == "idle"
            ):
                break
        except queue.Empty:
            break
    if "data" in temp:
        if "image/png" in temp["data"]:
            out = temp["data"]["image/png"]
        else:
            out = temp["data"]["text/plain"]
    elif "name" in temp and temp["name"] == "stdout":
        out = temp["text"]
    elif "traceback" in temp:
        print(temp)
        out = "\n".join(temp["traceback"])
    else:
        out = ""
    return out

thread = threading.Thread(target=process_queue)
thread.start()


@app.route("/run_code", methods=["POST"])
def run_code():
    # get the code to run from the request
    code = request.json["code"]
    result_queue = Queue()
    request_queue.put((code, result_queue))
    result = result_queue.get()
    return result


if __name__ == "__main__":
    app.run()
