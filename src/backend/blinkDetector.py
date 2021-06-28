import torch
from torchvision import transforms
from torch.autograd import Variable
import cv2 as cv

from classDefinitions import BlinkAndCropNet

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = torch.load('../backend/saved_models/blinkingFaces.pth')
model.eval()

transform = transforms.Compose(
    [transforms.ToTensor()])


def test(image):
    try:
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image = cv.resize(image, (80, 80), interpolation=cv.INTER_AREA)

        image_tensor = transform(image)
        image_tensor = image_tensor.unsqueeze(0)

        input_var = Variable(image_tensor)
        input_var = input_var.to(device)
        output = model(input_var)
        output = torch.round(output)

        return output.data.cpu().numpy()[0][0]

    except Exception as e:
        print(e)
        return 0


test(cv.imread('../resources/blinkset/blinkers/closed_eye_0059.jpg_face_2.jpg'))
