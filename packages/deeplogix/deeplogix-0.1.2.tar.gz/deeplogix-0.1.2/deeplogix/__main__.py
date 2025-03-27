import os.path
from   os import listdir
from   os.path import isfile, join
import sys
import runpy
import pickle
import json
import logging
import time
import inspect
import uuid
import urllib.parse
import importlib.util

if importlib.util.find_spec("socketio") is None:
    logging.error("Module `python-socketio` required, but not found. Please install it using `pip install python-socketio`.")
    os._exit(1)

if importlib.util.find_spec("websocket") is None:
    logging.error("Module `websocket-client` required, but not found. Please install it using `pip install websocket-client`.")
    os._exit(1)

import socketio

WS_URI = "wss://dispatcher.deeplogix.io/?type=client&hostId={host_id}"
WAIT_RESULT_TIMEOUT = 600 # 10 min
logging.basicConfig(encoding='utf-8', level=logging.INFO)

sio = socketio.Client()
responses = {}


# module utils
def get_module_directory():
    current_frame = inspect.currentframe()
    if current_frame is not None and current_frame.f_back is not None:
        current_file = inspect.getfile(current_frame.f_back)
        return os.path.dirname(os.path.abspath(current_file))
    return None


# communications with backend
def get_request_id():
    return str(uuid.uuid4())


def set_response(req_id, res):
    if isinstance(res, list):
        res = res[0] if len(res) > 0 else {}
    responses[req_id] = res


@sio.event
def connect():
    logging.info("Successfully connected to dispatcher")


@sio.event
def disconnect():
    logging.info("Disconnected from dispatcher")


@sio.event
def ready(is_ready):
    logging.info("All events defined")
    if not is_ready:
        return
    # run client script
    try:
        if len(sys.argv) > 1:
            if("--demo" == sys.argv[1]):
                # run built-in demos if --demo specified
                module_dir = get_module_directory()
                if module_dir:
                    logging.info(f"Deeplogix module directory is: {module_dir}")
                else:
                    logging.error("Could not determine Deeplogix module directory for run demos!")
                    exit(1)
                examples_dir = module_dir+"/examples"
                print(f"Demos:")
                demo_files = [f for f in listdir(examples_dir) if isfile(join(examples_dir, f))]
                for demo_id, demo_fname in enumerate(demo_files):
                    print(f"{demo_id}. {demo_fname}")
                selected_demo_idx = int(input("Type demo number and press Enter: "))
                script = f"{examples_dir}/{demo_files[selected_demo_idx]}"
                logging.info(f"Starting: {script}")
                runpy.run_path(script, run_name="__main__")  # Execute demo script
                logging.info(f"Script finished {script}")
            else:
                # run user's script
                logging.info(f"Run script {sys.argv[1]}")
                script = sys.argv[1]  # Get script name
                sys.argv = sys.argv[1:]  # Shift arguments so next ./script.py sees the correct ones
                runpy.run_path(script, run_name="__main__")  # Execute the script
                logging.info(f"Script finished {script}")
        else:
            print(f"Usage:")
            print(f"\tpython -m deeplogix --demo")
            print(f"\tpython -m deeplogix ./path/to/your/script.py")
    except Exception as e:
        raise e
    finally:
        sio.disconnect()


@sio.event
def result(res, req_id=None):
    if(None == req_id):
        logging.error(f"It seems Agent on the host is down, so Dispatcher can't find host for process the request.")
        os._exit(1)
    response = pickle.loads(res) # TODO: filter pickle.loads() to prevent RCE at client side?
    logging.debug(f"<<< {req_id=} {response=}")
    set_response(req_id, response)


def sio_rpc_call(method, args, kwargs):
    global WAIT_RESULT_TIMEOUT

    req = pickle.dumps({
        "method": method,
        "args": args,
        "kwargs": kwargs
    })

    req_id = get_request_id()
    logging.debug(f">>> {req_id=} {req=}")
    sio.emit("transformers", {"req_id": req_id, "req": req})

    logging.info(f"Waiting RPC {method=} response ...")
    sec = 0
    while responses.get(req_id, None) is None:
        time.sleep(0.1)
        sec += 0.1
        if sec > WAIT_RESULT_TIMEOUT:
            raise ValueError("Timeout waiting for response")
    res = responses[req_id]
    responses.pop(req_id)
    return res


# https://huggingface.co/docs/transformers/v4.49.0/en/pipeline_tutorial
class Tokenizer():
    def apply_chat_template(self, *args, **kwargs):
        res = sio_rpc_call(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}", args, kwargs)
        return res["retval"]


class Pipeline():
    def __init__(self, *args, **kwargs):
        self.tokenizer = Tokenizer()

    def __call__(self, *args, **kwargs):
        res = sio_rpc_call(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}", args, kwargs)
        return res["retval"]


def pipeline(*args, **kwargs) -> Pipeline:
    sio_rpc_call(sys._getframe().f_code.co_name, args, kwargs)
    return Pipeline(*args, **kwargs)


# https://huggingface.co/docs/transformers/v4.49.0/en/model_doc/auto
class AutoModelForCausalLM():
    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        res = sio_rpc_call(f"{cls.__name__}.{sys._getframe().f_code.co_name}", args, kwargs)
        return cls()

    def generate(self, *args, **kwargs):
        res = sio_rpc_call(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}", args, kwargs)
        return res["retval"]


class AutoTokenizer():
    def __call__(self, *args, **kwargs):
        res = sio_rpc_call(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}", args, kwargs)
        return res["retval"]

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        res = sio_rpc_call(f"{cls.__name__}.{sys._getframe().f_code.co_name}", args, kwargs)
        return cls()

    def decode(self, *args, **kwargs):
        res = sio_rpc_call(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}", args, kwargs)
        return res["retval"]


# https://huggingface.co/docs/diffusers/main/en/api/pipelines/stable_diffusion/stable_diffusion_3
class StableDiffusion3Pipeline():
    def __call__(self, *args, **kwargs):
        res = sio_rpc_call(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}", args, kwargs)
        return res["retval"]

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        res = sio_rpc_call(f"{cls.__name__}.{sys._getframe().f_code.co_name}", args, kwargs)
        return cls()


# https://huggingface.co/docs/diffusers/main/en/api/pipelines/flux
class FluxPipeline():
    def __call__(self, *args, **kwargs):
        res = sio_rpc_call(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}", args, kwargs)
        return res["retval"]

    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        res = sio_rpc_call(f"{cls.__name__}.{sys._getframe().f_code.co_name}", args, kwargs)
        return cls()


def main():
    # Check credentials for access Deeplogix features
    if not os.path.exists('./credentials.json'):
        host_id = input("Enter hostId: ")
        token = input("Enter token: ")
        with open('./credentials.json', 'w+') as f:
            json.dump({'host_id': host_id, 'token': token}, f)
    else:
        with open('./credentials.json', 'r') as f:
            credentials = json.load(f)
            host_id = credentials['host_id']
            token = credentials['token']
    # MonkeyPatch AI modiules with our overrides
    if importlib.util.find_spec("transformers") is None:
        logging.warning("Module `transformers` not found.\nIf you want to use Deeplogix Transformers RPC please install it also locally using `pip install transformers`.")
    else:
        import transformers
        transformers.pipeline = pipeline
        transformers.AutoModelForCausalLM = AutoModelForCausalLM
        transformers.AutoTokenizer = AutoTokenizer
    if importlib.util.find_spec("diffusers") is None:
        logging.warning("Module `diffusers` not found.\nIf you want to use Deeplogix Diffusers RPC please install it also locally using `pip install diffusers`.")
    else:
        import diffusers
        diffusers.StableDiffusion3Pipeline = StableDiffusion3Pipeline
        diffusers.FluxPipeline = FluxPipeline
    if importlib.util.find_spec("torch") is None:
        logging.warning("Module `torch` not found.\nIf you want to use Deeplogix RPC please install it also locally using `pip install torch`.")
    # Connect to dispatcher
    try:
        logging.info("Connecting to dispatcher ...")
        sio.connect(WS_URI.format(host_id=urllib.parse.quote(host_id)), transports=["websocket"], headers={
            'token': token
        })
        sio.wait()
    except socketio.exceptions.ConnectionError:
        logging.error("Error connecting to dispatcher!")
        os._exit(1)

if __name__ == "__main__":
    logging.info("DeepLogix module loaded!")
    main()
