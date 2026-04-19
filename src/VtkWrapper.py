import vtk
import numpy as np
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class ReconstructionDraw():
    """人类"""
    def __init__(self, vtkwidget):
        self.vtk_widget = vtkwidget

    # 1. 生成模拟空间转录组数据（3D网格）
    def generate_synthetic_data(self,dimensions=(50, 50, 50),  num_genes=10, noise_level=0.2):
        """生成包含随机基因表达的3D空间数据"""
        x, y, z = dimensions
        data = np.random.rand(x, y, z, num_genes)  # 随机基因表达值

        print(data)
        # 添加空间模式（模拟真实空间分布）
        # for i in range(num_genes):
        #     data[..., i] += 0.1
        #     data[..., i] += 0.3
        # 添加噪声并归一化
        #data += np.random.normal(0, noise_level, data.shape)
        #data = np.clip(data, 0, 1)
        return data

    # 2. 创建VTK数据结构
    def create_vtk_image(self,data):
        """将numpy数组转换为vtkImageData"""
        dims = data.shape[:3]
        image = vtk.vtkImageData()
        image.SetDimensions(dims[0], dims[1], dims[2])
        image.AllocateScalars(vtk.VTK_FLOAT, 1)  # 单分量浮点数据

        # 填充数据
        for z in range(dims[2]):
            for y in range(dims[1]):
                for x in range(dims[0]):
                    image.SetScalarComponentFromFloat(x, y, z, 0,
                                                      data[x, y, z].astype(float))
        return image


    # 3. 三维重建可视化
    def visualize_3d_reconstruction(self,image_data):
        """使用Marching Cubes算法进行表面重建"""
        # Marching Cubes过滤器
        marching_cubes = vtk.vtkMarchingCubes()
        marching_cubes.SetInputData(image_data)
        marching_cubes.SetValue(0, 0.5)  # 设置等值面阈值

        # 创建mapper和actor
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(marching_cubes.GetOutputPort())
        mapper.ScalarVisibilityOff()

        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)
        self.actor.GetProperty().SetColor(0.2, 0.6, 0.9)  # 设置表面颜色
        self.actor.GetProperty().SetOpacity(0.3)  # 设置透明度

        render_window_interactor = None
        self.render_window = None
        renderer = vtk.vtkRenderer()
        if self.vtk_widget is None:
            self.render_window = vtk.vtkRenderWindow()
            self.render_window.AddRenderer(renderer)
            render_window_interactor = vtk.vtkRenderWindowInteractor()
            render_window_interactor.SetRenderWindow(self.render_window)
        else:
            print("vtk_widget is not null")
            self.vtk_widget.GetRenderWindow().AddRenderer(renderer)
            render_window_interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
            self.render_window= self.vtk_widget.GetRenderWindow()

        # 添加坐标轴
        axes = vtk.vtkAxesActor()
        renderer.AddActor(axes)

        # 添加表面到渲染器
        renderer.AddActor(self.actor)
        renderer.SetBackground(0.1, 0.1, 0.1)  # 背景颜色

        # 设置相机参数
        renderer.ResetCamera()
        renderer.GetActiveCamera().Azimuth(30)
        renderer.GetActiveCamera().Elevation(30)

        # 启动交互
        self.render_window.Render()
        render_window_interactor.Start()

# 主程序
if __name__ == "__main__":
    rd=ReconstructionDraw("")
    # 生成模拟数据（50x50x50空间，10个基因）
    synthetic_data = rd.generate_synthetic_data()
    # 创建VTK图像数据（使用第一个基因通道）
    vtk_image = rd.create_vtk_image(synthetic_data[..., 0])
    # 可视化重建结果
    rd.visualize_3d_reconstruction(vtk_image,None)