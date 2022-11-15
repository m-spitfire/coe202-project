# Object detection based target following
Authors: Murad Bashirov, Mehdi Aghakishiyev, Khadija Rajabova

## Getting Started
### Requirements
**Python** >= 3.8 and **PyTorch**>=1.7 (see https://pytorch.org/get-started/locally)
1. Clone the repository
```shell
git clone https://github.com/m-spitfire/coe202-project
```
### For server
1. Download the `best.pt` pre-trained model from the [Releases](https://github.com/m-spitfire/coe202-project/releases) tab.
2. Install the requirements for `yolov5`:
```shell
pip install -qr https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt
```
3. Install the requirements for server:
```shell
pip install -r requirements-server.txt
```
4. Get your local IP address and set it in the [`.env`](./.env) file
5. Run the server:
```shell
python server.py
```
### For client
1. Install the dependencies for client:
```shell
pip install -r requirements-client.txt
```
2. Run the client
```shell
python client.py
```

## Acknowledgements
* [WelkinU/yolov5-fastapi-demo](https://github.com/WelkinU/yolov5-fastapi-demo) for basic fastapi server-client example