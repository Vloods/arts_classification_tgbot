from fastai.vision import *

def load_model():
    learn = load_learner('model')
    return learn

class ArtPredictor:
    def __init__(self):
        self.model = load_model()
        self.labels = ['Albrecht Dürer', 'Alfred Sisley', 'Amedeo Modigliani', 'Andrei Rublev', 'Andy Warhol',
               'Camille Pissarro', 'Caravaggio',
               'Claude Monet', 'Diego Rivera', 'Diego Velazquez', 'Edgar Degas', 'Edouard Manet', 'Edvard Munch',
               'El Greco', 'Eugene Delacroix',
               'Francisco Goya', 'Frida Kahlo', 'Georges Seurat', 'Giotto di Bondone', 'Gustav Klimt',
               'Gustave Courbet', 'Henri Matisse', 'Henri Rousseau',
               'Henri de Toulouse-Lautrec', 'Hieronymus Bosch', 'Jackson Pollock', 'Jan van Eyck', 'Joan Miro',
               'Kazimir Malevich', 'Leonardo da Vinci',
               'Marc Chagall', 'Michelangelo', 'Mikhail Vrubel', 'Pablo Picasso', 'Paul Cezanne', 'Paul Gauguin',
               'Paul Klee', 'Peter Paul Rubens', 'Pierre-Auguste Renoir',
               'Piet Mondrian', 'Pieter Bruegel', 'Raphael', 'Rembrandt', 'Rene Magritte', 'Salvador Dali',
               'Sandro Botticelli', 'Titian', 'Vasiliy Kandinskiy', 'Vincent van Gogh', 'William Turner']
    def predict(self, stream):
        img = (open_image(stream))
        img = img.resize(229)
        img.refresh()
        percent= self.evaluate_image(img)
        preds = zip(self.labels, percent)
        preds = sorted(preds, key = lambda t: t[1].item(), reverse=True)
        preds = [list(t) for t in zip(*kek)]
        return preds

    def evaluate_image(self, img)->(str, float):
        pred_class, pred_idx, outputs = self.model.predict(img)
        return outputs*100
