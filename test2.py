import time
import threading
from utils import ReadConfig, LOG
from muffle.AICommunicate import AI_communicate      #上传时，注意改mmuffle.aicommunicate为aicommunicate


class Muffle(object):
    def __init__(self, config, log, event):
        self.protocol = AI_communicate(config['address'], config['port'], log)
        self.__state = 'ready'
        self.__cabinet_idx = config['cabinet_idx']
        self.status = dict()
        self.config = config
        self.log = log
        self.su_event = event
        self.bool_stop = False  #用于中断温控
        self.remain_time = 0
        self.next_phase = '无计划'
        # self.initialize()
    #     function: 设备初始化


    def initialize(self, config=None):
        """
        function: 设备初始化
        :return: None
        """
        if config: self.config = config
        self.su_event.wait()
        self.su_event.clear()
        self.protocol.write_commend('0x0c', self.config['dPt'])     # 设置小数点位置
        self.receive_feedback()
        time.sleep(1)
        set_ptr = int(self.config['set_ptr'] * pow(10, self.config['dPt']))
        self.protocol.write_commend('0x00', set_ptr)     # 设定温度
        self.receive_feedback()
        time.sleep(1)
        para = len(self.config['tprs'])
        self.protocol.write_commend('0x2b', para)  # 设置段数
        self.receive_feedback()
        time.sleep(1)
        for i in range(para):
            if i == 0:
                tem1 = int(self.config['tprs'][0] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x50', tem1)  # 设定温度
                self.receive_feedback()
                time.sleep(1)
                tim1 = int(self.config['durations'][0] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x51', tim1)  # 设置时间
                self.receive_feedback()
                time.sleep(1)
            elif i == 1:
                tem2 = int(self.config['tprs'][1] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x52', tem2)  # 设定温度
                self.receive_feedback()
                time.sleep(1)
                tim2 = int(self.config['durations'][1] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x53', tim2)  # 设置时间
                self.receive_feedback()
                time.sleep(1)
            elif i == 2:
                tem3 = int(self.config['tprs'][2] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x54', tem3)  # 设定温度
                self.receive_feedback()
                time.sleep(1)
                tim3 = int(self.config['durations'][2] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x55', tim3)  # 设置时间
                self.receive_feedback()
                time.sleep(1)
            elif i == 3:
                tem4 = int(self.config['tprs'][3] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x56', tem4)  # 设定温度
                self.receive_feedback()
                time.sleep(1)
                tim4 = int(self.config['durations'][3] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x57', tim4)  # 设定时间
                self.receive_feedback()
                time.sleep(1)
            elif i == 4:
                tem5 = int(self.config['tprs'][4] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x58', tem5)  # 设定温度
                self.receive_feedback()
                time.sleep(1)
                tim5 = int(self.config['durations'][4] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x59', tim5)  # 设定时间
                self.receive_feedback()
                time.sleep(1)
            elif i == 5:
                tem6 = int(self.config['tprs'][5] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x5a', tem6)  # 设定温度
                self.receive_feedback()
                time.sleep(1)
                tim6 = int(self.config['durations'][5] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x5b', tim6)  # 设定时间
                self.receive_feedback()
                time.sleep(1)
            elif i == 6:
                tem7 = int(self.config['tprs'][6] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x5c', tem7)  # 设定温度
                self.receive_feedback()
                time.sleep(1)
                tim7 = int(self.config['durations'][6] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x5d', tim7)  # 设定时间
                self.receive_feedback()
                time.sleep(1)
            elif i == 7:
                tem8 = int(self.config['tprs'][7] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x5e', tem8)  # 设定温度
                self.receive_feedback()
                time.sleep(1)
                tim8 = int(self.config['durations'][7] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x5f', tim8)  # 设定时间
                self.receive_feedback()
                time.sleep(1)
            elif i == 8:
                tem9 = int(self.config['tprs'][8] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x60', tem9)  # 设定温度
                self.receive_feedback()
                time.sleep(1)
                tim9 = int(self.config['durations'][8] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x61', tim9)  # 设定时间
                time.sleep(1)
            elif i == 9:
                tem10 = int(self.config['tprs'][9] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x62', tem10)
                self.receive_feedback()
                time.sleep(1)
                tim10 = int(self.config['durations'][9] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x63', tim10)  # 设定时间
                self.receive_feedback()
                time.sleep(1)
            elif i == 10:
                tem11 = int(self.config['tprs'][10] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x64', tem11)  # 设定温度
                self.receive_feedback()
                time.sleep(1)
                tim11 = int(self.config['durations'][10] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x65', tim11)  # 设定时间
                self.receive_feedback()
                time.sleep(1)
            elif i == 11:
                tem12 = int(self.config['tprs'][11] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x66', tem12)  # 设定温度
                self.receive_feedback()
                time.sleep(1)
                tim12 = int(self.config['durations'][11] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x67', tim12)  # 设定时间
                self.receive_feedback()
                time.sleep(1)
            elif i == 12:
                tem13 = int(self.config['tprs'][12] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x68', tem13)  # 设定温度
                self.receive_feedback()
                time.sleep(1)
                tim13 = int(self.config['durations'][12] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x69', tim13)  # 设定时间
                self.receive_feedback()
                time.sleep(1)
            elif i == 13:
                tem14 = int(self.config['tprs'][13] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x6a', tem14)  # 设定温度
                self.receive_feedback()
                time.sleep(1)
                tim14 = int(self.config['durations'][13] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x6b', tim14)  # 设定时间
                self.receive_feedback()
                time.sleep(1)
            elif i == 14:
                tem15 = int(self.config['tprs'][14] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x6c', tem15)  # 设定温度
                self.receive_feedback()
                time.sleep(1)
                tim15 = int(self.config['durations'][14] * pow(10, self.config['dPt']))
                self.protocol.write_commend('0x6d', tim15)  # 设定时间
                self.receive_feedback()
                time.sleep(1)
        self.log.record('[muffle] 温度曲线设置完成')
        self.su_event.set()  # 千万不要放到状态更新后，会形成死锁
        self.update_status()


    def get_state(self):
        """
        获取马弗炉的当前运行状态，状态为私有变量，外部只读
        :return: 马弗炉的当前运行状态
        """
        return self.__state


    def get_cabinet_idx(self):
        return self.__cabinet_idx


    def receive_feedback(self, bLog=False):
        """
        等待读取数据
        :param bLog: 是否通过日志记录数据解释
        :return: None
        """
        if self.protocol.state != 'connect':
            self.log.record('[muffle] 串口未连接')
        count, data = 0, []
        while self.protocol.state == 'connect' and count < 1.28e5:
            data_t = self.protocol.com.receive_data()
            if data_t:
                data.append(data_t)
            if len(data) == 10:
                self.status = self.protocol.explain_status(data, bLog)
                return None
            count += 1
        self.log.record('[muffle] 等待反馈超时')
        return None


    def update_status(self, bLog=False):
        """
        注意：切记调用该函数前必须先将檢查【su_event】是否为 【set】，否则会形成死锁无限等待
        更新状态字典
        :param bLog: 是否通过日志记录数据解释
        :return:None
        """
        if self.protocol.state != 'connect': return
        self.su_event.wait()
        self.su_event.clear()
        if bLog: self.log.record('[muffle] 刷新状态')     # 通过读测量值的方式，返回参数为测量温度
        self.protocol.read_commend('4a')     # 读测量值
        self.receive_feedback(bLog)
        time.sleep(1)
        self.su_event.set()
        return None


    def send_commend(self, code:str, para=None):
        """
        发送读或写命令，用于测试功能
        :param code: 要发送的命令代码
        :param para: 写命令是输入的参数值
        :return:
        """
        self.su_event.wait()
        self.su_event.clear()
        if para != None:
            self.log.record('[muffle] 指定写命令：{}，参数值：{}'.format(code, para))
            self.protocol.write_commend(code, para)
            self.receive_feedback()
            self.log.record('[muffle] 返回值：{}'.format(self.status['rw_value']))
        elif para == None:
            self.log.record('[muffle] 指定读命令：{}'.format(code))
            self.protocol.read_commend(code)
            self.receive_feedback()
            self.log.record('[muffle] 返回值：{}'.format(self.status['rw_value']))
        self.su_event.set()


    def test_working(self, bLog=False):
        self.su_event.wait()
        self.su_event.clear()
        self.protocol.read_commend('1b')  # 读运行状态
        self.receive_feedback()
        time.sleep(1)
        run_statue = list(self.status.values())[4]
        if run_statue == 0.1 and bLog:
            self.log.record('[muffle] 马弗炉未运行')
        elif run_statue == 0.0 and bLog:
            self.log.record('[muffle] 马弗炉正在运行')
        elif run_statue == 0.2 and bLog:
            self.log.record('[muffle] 马弗炉hold')
        self.su_event.set()


    def is_working(self):
        """
        检查该设备是否正在执行加热计划
        :return: bool
        """
        if self.protocol.state != 'connect':
            self.log.record('[muffle] 马弗炉未连接，不执行温控程序')
            return True
        elif self.__state == 'Executing':
            self.log.record('[muffle] 马弗炉【addr:{}】正在执行温控计划'.format(self.config['address']))
            return True
        elif self.__state == '[muffle] ready':
            self.send_commend('1b')
            if self.status['rw_value'] == 0:
                self.__state = 'running'
                self.log.record('[muffle] 马弗炉【addr:{}】正在运行状态'.format(self.config['address']))
                return True
        else:
            return False


    def set_temperature(self, tpr :float, bLog = False):
        """
        function: 设定温度
        :param tpr: 温度值
        :param bLog: 温度值
        :return: None
        """
        # -------------------------------------------------------------------------
        if tpr > self.config['upper_limit'] or tpr < self.config['lower_limit']:
            self.log.record('[muffle] 温度设定值不在限定区间内，限定区间：[ {}, {} ]，设定值：{}：'
                            .format(self.config['lower_limit'], self.config['upper_limit'], tpr))
            return None
        # -------------------------------------------------------------------------
        self.su_event.wait()   # 等待状态更新完成
        self.su_event.clear()   # 禁用状态更新
        if bLog: self.log.record('[muffle] 正在设置温度：{}'.format(tpr))
        self.protocol.write_commend('0x00', int(tpr * pow(10, self.config['dPt'])))     # 设定温度
        self.receive_feedback(bLog)  # 等待设置回传
        self.su_event.set()     # 恢复状态更新
        self.update_status(bLog)
        if bLog and self.status['set_tpr'] == tpr:
            self.log.record('[muffle] 温度设置成功，设定值：{}'.format(tpr))
        elif bLog and self.status['set_tpr'] != tpr:
            self.log.record('[muffle] 温度设置失败，请重试...')
        return None


    def run_test_plan(self):
        """
        温度的测试，需为该函数单独开启线程来运行
        :return: bool变量，是否完成温控计划
        """
        #-------------------------------------------------------------------------
        if self.protocol.state != 'connect':
            self.log.record('[muffle] 马弗炉未连接，不执行温控程序')
            return False
        elif self.__state != 'ready':
            self.log.record('[muffle] 马弗炉【id:{}】正在工作，禁止执行新的温控计划'.format(self.config['address']))
            return False
        else:
            self.test_working(True)
            self.send_commend('1b', 0)  # 设为【run】模式，开始加热
            self.test_working(True)
            run_statue = list(self.status.values())[4]
            recent_temp = list(self.status.values())[0]
            while recent_temp > 65 or run_statue == 0.0:
                time.sleep(20)
                self.test_working()
                recent_temp = list(self.status.values())[0]
                run_statue = list(self.status.values())[4]
                self.log.record('[muffle] 当前温度{}'.format(recent_temp))
            time.sleep(2)
            # ----------------------------------------------------------------------
            # 结束处理
            self.set_temperature(self.config['set_ptr'])
            self.__state = 'finished'
            self.log.record('[muffle] 温控计划全部阶段已执行完成')
            return True
        # -------------------------------------------------------------------------


    def taken_out(self):
        """
        温控完成后取出物品
        :return:
        """
        if self.is_working():
            self.log.record('[muffle] 马弗炉正在工作，请停止后再取出。')
        elif self.__state != 'finished':
            self.log.record('[muffle] 马弗炉没有完成烧制的物品，请检查。')
        else:
            self.__state = 'ready'
        return None


    def close(self):
        self.protocol.close()
        self.__state = 'close'
        self.log.record('[muffle] 马弗炉已断开连接')
        return None


if __name__ == '__main__':
    log = LOG()
    log.LogInitialize()
    log.record('==========================================')
    log.record('马弗炉温控程序正在启动...')
    config_path = './config.txt'    # 配置字典文件路径
    config = ReadConfig(config_path)        # 配置字典
    SU_EVENT = threading.Event()    # SU: Status Update 状态更新事件
    SU_EVENT.set()
    # ---------------------------------------------------------------------------
    muffle = Muffle(config, log, SU_EVENT)
    if muffle.get_state() == 'ready':
        log.record('马弗炉连接完成')
        muffle.initialize()      # 设备初始化
        muffle.run_test_plan()
        muffle.close()
    else:
        log.record('马弗炉未成功连接，程序退出。')
    # ---------------------------------------------------------------------------
    log.record('马弗炉温控程序结束')
    log.record('==========================================')