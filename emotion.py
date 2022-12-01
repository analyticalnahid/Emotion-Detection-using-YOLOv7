import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
import torchvision.transforms as transforms

from PIL import Image
from vgg import create_RepVGG_A0 as create

# Load model
model = create(deploy=True)

# 8 Emotions
emotions = ("anger","contempt","disgust","fear","happy","neutral","sad","surprise")

def init(device):
    # Initialise model
    global dev
    dev = device
    model.to(device)
    checkpoint = torch.load("weights/vgg.pth")
    if 'state_dict' in checkpoint:
        checkpoint = checkpoint['state_dict']
    ckpt = {k.replace('module.', ''):v for k,v in checkpoint.items()}
    model.load_state_dict(ckpt)
    
    # Change to classify only 8 features
    model.linear.out_features = 8
    model.linear._parameters["weight"] = model.linear._parameters["weight"][:8,:]
    model.linear._parameters["bias"] = model.linear._parameters["bias"][:8]

    # Save to eval
    cudnn.benchmark = True
    model.eval()

def detect_emotion(images,conf=True):
    with torch.no_grad():
        # Normalise and transform images
        normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                        std=[0.229, 0.224, 0.225])
        x = torch.stack([transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                normalize,
            ])(Image.fromarray(image)) for image in images])
        # Feed through the model
        y = model(x.to(dev))
       
        for i in range(y.size()[0]):
            
            # Add emotion to result
            emotion = (max(y[i]) == y[i]).nonzero().item()
            another = []
            
            def f(x):
                 match x:
                    case 0:
                        another.append("Facial Expression")
                    case 1:
                        another.append("Facial Expression")
                    
                    case 2:
                        another.append("Facial Expression")
                    case 3:
                        another.append("Facial Expression")
                    
                    case 6:
                        another.append("Facial Expression")
                    case 7:
                        another.append("Facial Expression")
                    
                    case _:
                        another.append("No Facial Expression")
            f(emotion)
            
        
    return another