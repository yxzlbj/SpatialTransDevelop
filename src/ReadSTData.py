# import scanpy as sc
#
#
# adata = sc.read_visium(path="D://data//10XVisium//Human_Breast_Cancer//",
#                        count_file='filtered_feature_bc_matrix.h5',
#                        library_id="S7", source_image_path="D://data//10XVisium//Human_Breast_Cancer//spatial//")
#
#
# print(adata)

# import stereopy  as st
# import warnings
# warnings.filterwarnings('ignore')
#
# data_path = 'D://data//stereoseq//15DPI_3//FP200000266TR.gem'
# data = st.io.read_gem(
#         file_path=data_path,
#         bin_type='bins',
#         bin_size=50,
#         is_sparse=True,
#         )
#
# print(data)
# data.tl.cal_qc()
# data.plt.spatial_scatter()



# import scanpy as sc
#
# # 读取 H5AD 文件
# adata = sc.read_h5ad("D://data//10XVisium//h5ad//10X_Visium_Juntaro2022MEK_GSM5643203_10xvisium_data.h5ad")
#
# # 查看数据基本结构
# print(adata)          # 显示 AnnData 对象摘要
# print(adata.shape)    # 显示 (细胞数, 基因数)
# print(adata.X.shape)  # 查看表达矩阵维度
#
# # 基础操作
#
# print(f"数据维度: {adata.shape}")
# print(f"barcode:\n{adata.obs['barcode'].head()}")
# print(f"in_tissue:\n{adata.obs['in_tissue'].head()}")
# print(f"array_col:\n{adata.obs['array_col'].head()}")
# print(f"前5个基因名称:\n{adata.var['gene_ids'].head()}")
#
# # 访问表达矩阵（前5细胞 × 前5基因）
# print(adata.X[:5, :5].toarray())  # 转换为密集矩阵查看
#
#
#
# # 检查 obs 数据框中的坐标列（常见列名：'x', 'y' 或 'array_row', 'array_col'）
# print("obs 列名:", adata.obs.columns.tolist())
# # 提取空间坐标（假设列名为 'x' 和 'y'）
# if 'x' in adata.obs.columns and 'y' in adata.obs.columns:
#     x_coords = adata.obs['x'].values
#     y_coords = adata.obs['y'].values
# else:
#     # 尝试其他常见列名（如 Visium 数据的像素坐标）
#     x_coords = adata.obs['array_col'].values
#     y_coords = adata.obs['array_row'].values
# # 打印前5个坐标
#
# print("前5个坐标点:")
#
# print(list(zip(x_coords[:5], y_coords[:5])))

import scanpy as sc
import matplotlib.pyplot as plt
import numpy as np

def load_h5ad_spatial_data(file_path):
    adata = sc.read_h5ad(file_path)

    # 尝试提取坐标
    coord_names = [('x', 'y'), ('array_col', 'array_row')]
    x, y = None, None

    for col_x, col_y in coord_names:
        if col_x in adata.obs.columns and col_y in adata.obs.columns:
            x = adata.obs[col_x].values
            y = adata.obs[col_y].values
            break

    if x is None or y is None:
        raise ValueError("未找到空间坐标列，请检查 obs 列名")

    return adata, x, y

# 使用示例
adata, x, y = load_h5ad_spatial_data("D://data//10XVisium//h5ad//10X_Visium_Juntaro2022MEK_GSM5643203_10xvisium_data.h5ad")

#print(adata.var.index)
#print(f"前5个基因名称:\n{adata.var['gene_ids'].head()}")
print(adata)
# 提取特定基因的表达值（例如："GeneA"）
gene_name = "Xkr4"
if gene_name in adata.var.index:
    expression_values = adata[:, adata.var.index == gene_name].X.toarray().flatten()
    print(expression_values)
    print(f"{gene_name} 表达值范围: {np.min(expression_values):.2f} ~ {np.max(expression_values):.2f}")
else:
    print(f"错误：基因 {gene_name} 不存在于数据集中")
# 提取所有基因的表达矩阵（细胞 × 基因）

expression_matrix = adata.X.toarray()  # 转换为密集矩阵（注意内存）
print("表达矩阵维度:", expression_matrix)
#from vtkmodules.util import numpy_support
# 可视化
plt.figure(figsize=(6, 6))
plt.scatter(x, y, s=5, c='blue', alpha=0.6)
plt.gca().invert_yaxis()
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.title("Spatial Transcriptomics Spots")
plt.savefig("spatial_coordinates.png", dpi=300)



