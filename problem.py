import numpy as np
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random

class Problem:
    def __init__(self, filename):
        self.space = self.load_state_space(filename)
        
    ''' Tải không gian ảnh '''
    def load_state_space(self, filename):
        img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        img = cv2.GaussianBlur(img, (5, 5), 0)
        self.h, self.w = img.shape
        self.X = np.arange(self.w)
        self.Y = np.arange(self.h)
        self.Z = img
        return self.X, self.Y, self.Z

    ''' In ảnh ra màn hình'''
    def show(self):
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(self.X, self.Y, self.Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
        plt.show()

    ''' Vẽ đường đi dựa trên path từ các thuật toán tìm kiếm '''
    def draw_path(self, path):
        X, Y, Z = self.X, self.Y, self.Z
        X, Y = np.meshgrid(X, Y)
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
        
        path_x = [state[0] for state in path]
        path_y = [state[1] for state in path]
        path_z = [state[2] for state in path]
    
        ax.plot(path_x, path_y, path_z, 'r-', zorder=3, linewidth=0.5)
        plt.show()

    ''' Trả về list các node con của node hiện tại '''
    def get_successors(self, node):
        successors = []
        x, y, z = node.state
        
        if y > 0:
            successors.append(Node((x, y-1, self.Z[y-1, x]), node))
        if y < self.h - 1:
            successors.append(Node((x, y+1, self.Z[y+1, x]), node))
        if x > 0:
            successors.append(Node((x-1, y, self.Z[y, x-1]), node))
        if x < self.w - 1:
            successors.append(Node((x+1, y, self.Z[y, x+1]), node))
            
        return successors
        
    ''' Tạo ngẫu nhiên một initial state '''
    def get_initial_state(self):
        x = random.randint(0, self.w - 1)
        y = random.randint(0, self.h - 1)
        return (x, y, self.Z[y, x])
    
    ''' Chọn child node tốt nhất từ list successors '''
    def get_best_successor(self, successors):
        successors.sort(key=lambda node: node.get_value(), reverse=True)   
        return successors[0].state
    
    ''' Nếu current là localmax thì các successors của current có value nhỏ hơn current'''
    def is_local_max(self, current):
        successors = self.get_successors(current)
        best_succ = Node(self.get_best_successor(successors))
        return best_succ.get_value() <= current.get_value()
    
    ''' Hàm schedule sử dụng cho thuật toán SA '''
    def schedule(self):
        return lambda t: 1 / (t ** 2)

    ''' Hàm get_best_local_max trả về local max tốt nhất tìm được trong path'''
    def get_best_local_max(self, path: tuple) -> int:
        best_local_max = float('-inf') 
        for n in path:
            if n[2] > best_local_max:  
                best_local_max = n[2]
        return best_local_max

    ''' Hàm get_path trả về path từ vị trí current ngược lại'''
    def get_path(self, current):
        path = []
        while current is not None:
            path.append(current.state)
            current = current.parent
        path.reverse()  
        return path

class Node:
    ''' Object node để lưu trữ thông tin từng state '''
    def __init__(self, state, parent = None):
        self.state = state
        self.parent = parent
    
    def __str__(self):
        return str(self.state)
    
    ''' Lấy z value của state '''
    def get_value(self):
        return self.state[2]