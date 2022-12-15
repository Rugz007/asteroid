import jupyter_client
from flask import Flask, request
import queue

app = Flask(__name__)

kernel_manager, kernel_client = jupyter_client.manager.start_new_kernel(kernel_name="python3")



def handle_output(msg):
    msg_type = msg["header"]["msg_type"]
    if msg_type in {"display_data", "execute_result"}:
        data = msg["content"]["text"]
        print("mimetypes: %s" % sorted(data.keys()))


@app.route("/run_code", methods=["POST"])
def run_code():
    # get the code to run from the request
    code = request.json["code"]
    # run the code in the kernel
    kernel_client.execute(code)
    io_msg_content = kernel_client.get_iopub_msg(timeout=10)['content']
    if 'execution_state' in io_msg_content and io_msg_content['execution_state'] == 'idle':
        return "no output"
    print(dir(kernel_client.get_iopub_msg))
    # get the output from the kernel
    while True:
      temp = io_msg_content
      try:
        io_msg_content = kernel_client.get_iopub_msg(timeout=10)['content']
        if 'execution_state' in io_msg_content and io_msg_content['execution_state'] == 'idle':
          break
      except queue.Empty:
        break
    if 'data' in temp:
      if 'image/png' in temp['data']:
        out = temp['data']['image/png']
      else:
        out = temp['data']['text/plain']
    elif 'name' in temp and temp['name'] == "stdout":
      out = temp['text']
    elif 'traceback' in temp:
      print(temp)
      out = '\n'.join(temp['traceback'])
    else:
      out = ''
    return out


if __name__ == "__main__":
    app.run()
