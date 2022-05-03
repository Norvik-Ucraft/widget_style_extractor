# Widget Style Extractor 

The goal of this project is to extract computed sytle of widgets that our vision model detects their coordinates from
provided URL in command line.

To start this project first you need to clone screenshot_service repo from ucraft GitHub, then install necessary packages
using `npm install` and then run the service using `npm start`. \
After this you will be able to get screenshot of url that we will be pass in command line during execution.

to install torch, torchvision and trochaudio with correct version please run this command on your terminal: \
Windows & Ubuntu: \
`pip install torch==1.8.1+cu102 torchvision==0.9.1+cu102 torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html`

For the execution we need to run this command on your terminal: \
` python main.py --input-url URL --weights main_model/yolov5s.pt`

