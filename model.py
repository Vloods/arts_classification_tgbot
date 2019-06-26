from fastai.vision import *

# В данном классе мы хотим полностью производить всю обработку картинок, которые поступают к нам из телеграма.
# Это всего лишь заготовка, поэтому не стесняйтесь менять имена функций, добавлять аргументы, свои классы и
# все такое.
def load_model():
    learn = load_learner('model')
    return learn

class ArtPredictor:
    def __init__(self):
        self.model = load_model()

    def predict(self, stream):
        img = (open_image(stream))
        img = img.resize(229)
        img.refresh()
        pred, percent= self.evaluate_image(img)
        return pred, to_float(percent)

    def evaluate_image(self, img)->(str, float):
        pred_class, pred_idx, outputs = self.model.predict(img)
        return pred_class, outputs.max()*100
