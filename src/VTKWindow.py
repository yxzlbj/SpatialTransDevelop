import sys
import vtk
from PyQt5 import QtWidgets, QtCore , QtGui
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import ( QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout)
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from ReadSTData import  load_h5ad_spatial_data
import  VtkWrapper
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D可视化控制台")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("border-radius: 8px;")

        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.rd=VtkWrapper.ReconstructionDraw(self.vtk_widget)

        self.Init_UI()
        self.init_scene()
    def Init_UI(self):

        # 创建控制面板
        self.control_panel = QtWidgets.QWidget()
        self.control_layout = QtWidgets.QVBoxLayout(self.control_panel)

        # 数据加载按钮
        self.load_btn = QtWidgets.QPushButton("加载3D数据")
        self.load_btn.clicked.connect(self.load_data)
        self.control_layout.addWidget(self.load_btn)

        # 颜色选择器
        self.color_picker = QtWidgets.QColorDialog()
        color_btn = QtWidgets.QPushButton("选择颜色")
        color_btn.clicked.connect(self.change_color)
        self.control_layout.addWidget(color_btn)

        # 透明度滑块
        self.opacity_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(100)
        self.opacity_slider.valueChanged.connect(self.update_opacity)
        self.control_layout.addWidget(self.opacity_slider)


        # 创建分割布局
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.splitter.addWidget(self.vtk_widget)
        self.splitter.addWidget(self.control_panel)
        self.splitter.setStretchFactor(0, 5)  # 左侧占比75%
        self.splitter.setStretchFactor(1, 3)   # 右侧占比25%

        self.label = QLabel("左侧内容区域", self)
        self.label.setStyleSheet(
        """
        QLabel 
        {
            background: #2c3e50;
            color: white;
            font-size: 24px;
            qproperty-alignment: AlignCenter;
        } 
        """)

        self.minimize_btn = QPushButton("—", self)
        self.close_btn = QPushButton("×", self)

        self.minimize_btn.setStyleSheet(
        """
            QPushButton 
            {
                background: #34495e;
                color: white;
                border: none;
                padding: 5px 15px;
                font-size: 18px;
            }
            QPushButton:hover 
            {
                background: #2980b9;
            }
            QPushButton:pressed 
            {
                background: #1abc9c;
            }
        """)

        self.close_btn.setStyleSheet(
        """
            QPushButton 
            {
                background: #e74c3c;
                color: white;
                border: none;
                padding: 5px 15px;
                font-size: 18px;
            }
            QPushButton:hover 
            {
                background: #c0392b;
            }
            QPushButton:pressed 
            {
                background: #e74c3c;
            }
        """)

        # 创建分割布局
        self.HeaderSplitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.HeaderSplitter.addWidget(self.label)
        self.HeaderSplitter.addWidget(self.minimize_btn)
        self.HeaderSplitter.addWidget(self.close_btn)
        self.HeaderSplitter.setStretchFactor(0, 11)
        self.HeaderSplitter.setStretchFactor(1, 2)
        self.HeaderSplitter.setStretchFactor(2, 2)

        # 信号连接
        self.minimize_btn.clicked.connect(self.showMinimized)
        self.close_btn.clicked.connect(self.close)

        # 创建垂直布局
        self.Mainsplitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)

        self.Mainsplitter.addWidget(self.HeaderSplitter)
        self.Mainsplitter.addWidget( self.splitter)

        self.setCentralWidget(self.Mainsplitter)

        # 窗口属性设置
        #self.set_drag_area(self.label)  # 设置可拖动区域

    def init_scene(self):

        # 初始化VTK组件
        # self.renderer = vtk.vtkRenderer()
        # self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        # self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        # self.render_window= self.vtk_widget.GetRenderWindow()

        # 生成模拟数据（50x50x50空间，10个基因）
        synthetic_data = self.rd.generate_synthetic_data()
        # 创建VTK图像数据（使用第一个基因通道）
        vtk_image = self.rd.create_vtk_image(synthetic_data[..., 0])
        # 可视化重建结果
        self.rd.visualize_3d_reconstruction(vtk_image)

        # # 创建示例数据（圆锥体）
        # cone = vtk.vtkConeSource()
        # cone.SetResolution(50)
        #
        # mapper = vtk.vtkPolyDataMapper()
        # mapper.SetInputConnection(cone.GetOutputPort())
        #
        # self.actor = vtk.vtkActor()
        # self.actor.SetMapper(mapper)
        # self.actor.GetProperty().SetColor(0.2, 0.6, 0.2)
        #
        # self.renderer.AddActor(self.actor)
        # self.renderer.SetBackground(0.1, 0.2, 0.4)
        # self.renderer.ResetCamera()
        #
        # self.render_window.Render()
        # self.interactor.Start()

    # 扩展方法示例
    def change_color(self):
        color = self.color_picker.getColor()
        if color.isValid():
            self.rd.actor.GetProperty().SetColor(*[c/255 for c in color.getRgb()[:3]])
            self.rd.render_window.Render()

    def update_opacity(self, value):
        opacity = value / 100.0
        self.rd.actor.GetProperty().SetOpacity(opacity)
        self.rd.render_window.Render()

    def load_data(self):
        # 打开文件对话框
        path, _ = QtWidgets.QFileDialog.getOpenFileName( self,"load SpatialTranscriptome data","",
                   "SpatialTranscriptome Files (*.h5ad)" )

        if not path:
            return
        # 清除旧数据
        self.renderer.RemoveAllViewProps()

        # 根据文件扩展名选择读取器
        ext = path.split('.')[-1].lower()
        data = None

        if ext == 'h5ad':
            adata, x, y = load_h5ad_spatial_data(path)
            print(adata)
        else:
            QtWidgets.QMessageBox.warning(self, "错误", f"不支持的文件格式: .{ext}")
        # elif ext == 'vtk':
        #     reader = vtk.vtkPolyDataReader()
        # elif ext == 'obj':
        #     reader = vtk.vtkOBJReader()
        # elif ext == 'ply':
        #     reader = vtk.vtkPLYReader()
        # if reader:
        #     reader.SetFileName(path)
        #     reader.Update()
        #
        #     mapper = vtk.vtkPolyDataMapper()
        #     mapper.SetInputConnection(reader.GetOutputPort())
        #
        #     actor = vtk.vtkActor()
        #     actor.SetMapper(mapper)
        #     actor.GetProperty().SetColor(0.8, 0.8, 0.8)  # 默认灰色
        #
        #     self.renderer.AddActor(actor)
        #     self.renderer.ResetCamera()
        #     self.vtk_widget.GetRenderWindow().Render()


