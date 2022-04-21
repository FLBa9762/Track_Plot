# 第二次课后作业
# 轨迹与混合轨迹
import matplotlib.pyplot as plt
import numpy as np
import os
# from os import open

path = os.path.join(os.getcwd(), 'figure')
if not os.path.isdir(path):
    os.makedirs(path)
index_path = os.path.join(os.getcwd(), 'figure', 'index.txt')
if not os.path.exists(index_path):
    fp = open('./figure/index.txt', 'w')
    fp.write('index: 0')
    fp.close()


class Models:
    def __init__(self):
        self.config = {
            'uniform_speed': {'v_x': 0, 'v_y': 0},
            'Accelerate': {'a_x': 0, 'a_y': 0},   # 匀加速
            'uniform_circle': {'a': 0, 'w': 0}      # 匀速圆周
            }   # 默认参数，没有使用到
        self.fig = plt.figure(figsize=[10, 10]).add_subplot(111)
        self.fig.axis('equal')
        self.fig.set_xlabel('X')
        self.fig.set_ylabel('Y')
        self._x = 0
        self._y = 0
        self._vx = 0
        self._vy = 0
        self.x_data, self.y_data = np.empty(0), np.empty(0)

    def _uniform_speed(self, t):    # 匀速运动
        t = np.arange(0, t)
        x_uniform = t * (self.config['uniform_speed']['v_x']+self._vx) + self._x
        y_uniform = t * (self.config['uniform_speed']['v_y']+self._vy) + self._y
        self.x_data = np.append(self.x_data, x_uniform)
        self.y_data = np.append(self.y_data, y_uniform)
        self._x = x_uniform[-1]
        self._y = y_uniform[-1]
        self._vx += self.config['uniform_speed']['v_x']
        self._vy += self.config['uniform_speed']['v_y']

    def _accelerate(self, t):   # 匀加速运动
        t = np.arange(0, t)
        x_accelerate = 0.5 * t * t * self.config['Accelerate']['a_x'] + self._vx*t + self._x
        y_accelerate = 0.5 * t * t * self.config['Accelerate']['a_y'] + self._vy*t + self._y
        self.x_data = np.append(self.x_data, x_accelerate)
        self.y_data = np.append(self.y_data, y_accelerate)
        self._x = x_accelerate[-1]
        self._y = y_accelerate[-1]
        self._vx += self.config['Accelerate']['a_x'] * t[-1]
        self._vy += self.config['Accelerate']['a_y'] * t[-1]
        # self.fig.plot(x_accelerate, y_accelerate, 'm.-', label='ax1', linewidth=0.5)

    def _uniform_circle(self, t):   # 圆周运动
        t = np.arange(0, t)
        x_circle = self.config['uniform_circle']['a'] * np.sin(self.config['uniform_circle']['w'] * t) \
                   + self._vx*t + self._x
        y_circle = self.config['uniform_circle']['a'] * np.cos(self.config['uniform_circle']['w'] * t) \
                   + self._vy*t + self._y
        self.x_data = np.append(self.x_data, x_circle)
        self.y_data = np.append(self.y_data, y_circle)
        self._vx += self.config['uniform_circle']['a'] * self.config['uniform_circle']['w'] * \
                    np.cos(self.config['uniform_circle']['w'] * t[-1])
        self._vy += -1 * self.config['uniform_circle']['a'] * self.config['uniform_circle']['w'] * \
                    np.sin(self.config['uniform_circle']['w'] * t[-1])
        self._x = x_circle[-1]
        self._y = y_circle[-1]
        # self.fig.plot(x_circle, y_circle, 'm.-', label='ax1', linewidth=0)

    def _fig_show(self):
        self.fig.plot(self.x_data, self.y_data, 'm.-', label='ax1', linewidth=0)

        # f = open(index_path, 'r+')
        with open(index_path, 'r+') as f:
            information = f.read()
            index = int(information.split(' ')[1])
            index += 1
        with open(index_path, 'w+') as f:
            f.write('index: {}'.format(index))
            # f.close()
        plt.savefig(os.path.join(path, 'single_uniform'+str(index)))
        plt.show()


def complex_track():    # 混合运动轨迹
    demo = Models()
    step = 0
    time = 0
    print('每段默认运动时间50s！')
    while True:

        model_type = input('请输入第{}个运动模型类型: 1: 匀速直线运动     2: 匀加速运动     3: 圆周运动\n'.format(step+1))
        if model_type not in ['1', '2', '3']:
            print('\n输入有误，请重新选择。')
            continue

        if model_type == '1':
            try:
                v_x, v_y, t = map(float, (input('请输入x, y 方向速度以及运动时间t， 用空格隔开\n').split(' ')))
            except ValueError as e:
                print('输入格式有误！{}\n'.format(e))
                continue
            demo.config['uniform_speed']['v_x'], demo.config['uniform_speed']['v_y'] = v_x, v_y
            demo._uniform_speed(t)
            time += t
        elif model_type == '2':
            try:
                a_x, a_y, t = map(float, (input('请输入x, y 方向加速度以及运动时间t， 用空格隔开\n').split(' ')))
            except ValueError as e:
                print('输入格式有误！{}\n'.format(e))
                continue
            demo.config['Accelerate']['a_x'], demo.config['Accelerate']['a_y'] = a_x, a_y
            demo._accelerate(t)
            time += t

        elif model_type == '3':
            try:
                a, w, t = map(float, (input('请输入圆周运动参数a, w以及运动时间t， 用空格隔开\n').split(' ')))
            except ValueError as e:
                print('输入格式有误！{}\n'.format(e))
                continue
            demo.config['uniform_circle']['a'], demo.config['uniform_circle']['w'] = a, w
            demo._uniform_circle(t)
            time += t
        step += 1
        flag = np.float64(input('是否继续？(输入0停止)\n'))
        if flag:
            print('\n进行下一段轨迹的绘制')
        else:
            print('轨迹绘制完成！')
            demo._fig_show()
            break


def single_track():     # 单独运动轨迹
    while True:
        demo = Models()
        model_type = input('请输入运动模型类型: 1: 匀速直线运动     2: 匀加速运动     3: 圆周运动\n')

        if model_type == '1':
            try:
                v_x, v_y, t = map(float, (input('请输入x, y 方向速度以及时间t， 用空格隔开\n').split(' ')))
            except ValueError as e:
                print('输入格式有误！{}\n'.format(e))
                continue
            demo.config['uniform_speed']['v_x'], demo.config['uniform_speed']['v_y'] = v_x, v_y
            demo._uniform_speed(t)
            demo._fig_show()

        elif model_type == '2':
            try:
                a_x, a_y, t = map(float, (input('请输入x, y 方向加速度以及时间t， 用空格隔开\n').split(' ')))
            except ValueError as e:
                print('输入格式有误！{}\n'.format(e))
                continue
            demo.config['Accelerate']['a_x'], demo.config['Accelerate']['a_y'] = a_x, a_y
            demo._accelerate(t)
            demo._fig_show()
        elif model_type == '3':
            try:
                a, w, t = map(float, (input('请输入圆周运动参数a, w以及时间t， 用空格隔开\n').split(' ')))
            except ValueError:
                print('输入格式有误！{}\n'.format(e))
                continue
            demo.config['uniform_circle']['a'], demo.config['uniform_circle']['w'] = a, w
            demo._uniform_circle(t)
            demo._fig_show()
        else:
            print('输入有误，请重新输入！')
        print('\n')


def run():

    print('****************************************************************************')
    print('**                            请选择操作模式                                 **')
    print('**           输入 1 选择单轨迹操作模式       输入 2 选择混合轨迹操作模式           **')
    print('**                               即将开始！！！                              **')
    print('****************************************************************************')
    type = input()
    assert type in ['1', '2']
    if type == '1':
        single_track()
    else:
        complex_track()


if __name__ == '__main__':
    run()

