# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class NNInterface(metaclass=ABCMeta):
    
    @classmethod
    @abstractmethod
    def create_model(cls):
        raise NotImplementedError
        
    @abstractmethod
    def fit(self):
        raise NotImplementedError
    
    @abstractmethod
    def get_prediction(self):
        raise NotImplementedError
        
    @abstractmethod
    def predict(self):
        raise NotImplementedError
        
    @abstractmethod
    def update_plot(self):
        raise NotImplementedError
        
    @abstractmethod
    def update_progress(self):
        raise NotImplementedError
        
    @abstractmethod
    def update_info(self):
        raise NotImplementedError
        
    @abstractmethod
    def load_weight(self):
        raise NotImplementedError
        
    @abstractmethod
    def save_weight(self):
        raise NotImplementedError
        
    @abstractmethod
    def save_train_data(self):
        raise NotImplementedError
        
    @abstractmethod
    def load_train_data(self):
        raise NotImplementedError
        
    @abstractmethod
    def split_data(self):
        raise NotImplementedError
            
        
        
class NNScreenInterface(metaclass=ABCMeta):
    
    @abstractmethod
    def create_model(self):
        raise NotImplementedError
        
    @abstractmethod
    def set_position(self):
        raise NotImplementedError
        
    @abstractmethod
    def fit(self):
        raise NotImplementedError
        
    @abstractmethod
    def predict(self):
        raise NotImplementedError
        
    @abstractmethod
    def set_info(self):
        raise NotImplementedError
        
    @abstractmethod
    def set_maximum_progress(self):
        raise NotImplementedError
        
class ScreenInterface(metaclass=ABCMeta):
    
    @abstractmethod
    def set_position(self):
        raise NotImplementedError
    
    @abstractmethod
    def create_model(self):
        raise NotImplementedError
        
    