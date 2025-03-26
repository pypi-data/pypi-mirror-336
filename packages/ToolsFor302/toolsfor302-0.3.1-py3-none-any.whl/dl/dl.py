import os
import pydicom
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, IntSlider
import SimpleITK as sitk
import pymedphys

def load_mhd_dose(mhd_file_path):
    """
    读取 .mhd 文件，并返回对应的剂量图像数组。
    Args:
        mhd_file_path(str): 包含剂量图像的文件路径。
    Returns:
        dose_image_array(numpy.ndarray): 剂量图像数组。
    """
    dose_image = sitk.ReadImage(mhd_file_path)
    dose_image_array = sitk.GetArrayFromImage(dose_image)
    
    return dose_image_array

def show_double_dose_slice(dose1, dose2, slice_num, cmap_1, cmap_2, alpha=0.5):
    """
    显示两个剂量分布的叠加切片。
    Args:
        dose1(numpy.ndarray): 第一个剂量分布。
        dose2(numpy.ndarray): 第二个剂量分布。
        slice_num(int): 切片索引, 显示当前要显示的切片。
        cmap_1(str): 第一个剂量分布的colormap。
        cmap_2(str): 第二个剂量分布的colormap。
        alpha(float): 透明度, 默认值是0.5
    """
    fig, ax = plt.subplots(figsize=(6, 6), dpi=100)
    ax.imshow(dose1[slice_num], cmap=cmap_1, interpolation='none')
    dose_img = ax.imshow(dose2[slice_num], cmap=cmap_2, interpolation='none', alpha=alpha)

    cbar = plt.colorbar(dose_img, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(labelsize=10)

    plt.title(f'Slice {slice_num}', fontsize=14)
    plt.axis('off')
    plt.show()
    
def show_single_dose_slice(dose, slice_num, dose_min, dose_max):
    """
    显示单个剂量分布的切片。
    Args:
        dose(numpy.ndarray): 剂量分布。
        slice_num(int): 切片索引, 显示当前要显示的切片。
        dose_min(double): 剂量最小值, 用于控制colorBar的显示范围。
        dose_max(double): 剂量最大值, 用于控制colorBar的显示范围。
    """
    fig, ax = plt.subplots(figsize=(6, 6), dpi=100)
    img = ax.imshow(dose[slice_num], cmap='jet', interpolation='none', vmin=dose_min, vmax=dose_max)
    cbar = plt.colorbar(img, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(labelsize=10)
    
    plt.title(f'Dose at Slice {slice_num}', fontsize=14)
    plt.axis('off')
    plt.show()

def load_folder_dose(folder_path):
    """
    读取文件夹下所有 .mhd 文件，并返回对应的剂量图像数组。
    Args:
        folder_path(str): 包含 .mhd 文件的文件夹路径。
    Returns:
        dose_image_array(numpy.ndarray): 剂量图像数组。
    """
    # 获取目录下所有 .mhd 文件
    mhd_files = [f for f in os.listdir(folder_path) if f.endswith('.mhd')]

    final_dose = np.zeros_like(mc_dose)  # 初始化为零矩阵

    for file_name in mhd_files:
        file_path = os.path.join(mc_dose_dir, file_name)
        final_dose = final_dose + load_moqui_dose(file_path)
    
    return final_dose

def load_bin_dose(bin_file_path, type):
    """
    读取 .bin 文件，并返回对应的剂量图像数组。
    Args:
        bin_file_path(str): 包含剂量图像的文件路径。
        type(str): 剂量图像数据类型, 包括 'float', 'double', 'int'。
    Returns:
        bin_dose(numpy.ndarray): 剂量图像数组, 返回的是一维数组, 需要自己reshape形状。
    """
    with open(bin_file_path, 'rb') as f:
        if type == 'float':
            bin_dose = np.fromfile(f, dtype=np.float32)
        elif type == 'double':
            bin_dose = np.fromfile(f, dtype=np.float64)
        elif type == 'int':
            bin_dose = np.fromfile(f, dtype=np.int32)
        else:
            print('Invalid data type')
            return None
        
    return bin_dose

def show_single_slice_interactive(dose):
    """
    显示单个剂量分布的切片, 交互式版本。
    Args:
        dose(numpy.ndarray): 要显示的剂量分布。
    """
    num_slices = dose.shape[0]
    interact(lambda slice_num: show_single_dose_slice(dose, slice_num, dose.min(), dose.max()),
         slice_num=IntSlider(min=0, max=num_slices - 1, step=1, value=num_slices // 2))
    
def show_range_in_line(dose1, dose2, x_idx, y_start, y_end, z_idx):
    """
    显示两个剂量分布的射程图。
    Args:
        dose1(numpy.ndarray): 第一个剂量分布。
        dose2(numpy.ndarray): 第二个剂量分布。
        x_idx(int): 显示的x方向的索引。
        y_start(int): 显示的y方向的起始索引。
        y_end(int): 显示的y方向的结束索引。
        z_idx(int): 显示的z方向的索引。
    """
    
    dose1_slice = dose1[z_idx]
    dose2_slice = dose2[z_idx]
    
    x = np.arange(y_start, y_end)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, dose1_slice[y_start:y_end,x_idx], label='Dose1', marker='o')
    plt.plot(x, dose2_slice[y_start:y_end,x_idx], label='Dose2', marker='x')
    plt.xlabel('Y Index')
    plt.ylabel('Dose Value')
    plt.title(f'idd at z= {z_idx}, x={x_idx}, y={y_start} to {y_end}')
    plt.legend()
    plt.grid(True)
    plt.show()
    
def show_range_in_slice(dose1, dose2, y_start, y_end, z_idx):
    """
    显示两个剂量分布的射程图。
    Args:
        dose1(numpy.ndarray): 第一个剂量分布。
        dose2(numpy.ndarray): 第二个剂量分布。
        y_start(int): 显示的y方向的起始索引。
        y_end(int): 显示的y方向的结束索引。
        z_idx(int): 显示的z方向的索引。
    """
    
    dose1_slice = dose1[z_idx]
    dose2_slice = dose2[z_idx]
    
    x = np.arange(y_start, y_end)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, np.sum(dose1_slice, axis=1)[y_start:y_end], label='Dose1', marker='o')
    plt.plot(x, np.sum(dose2_slice, axis=1)[y_start:y_end], label='Dose2', marker='x')
    plt.xlabel('Y Index')
    plt.ylabel('Dose Value')
    plt.title(f'idd at z= {z_idx}, y={y_start} to {y_end}')
    plt.legend()
    plt.grid(True)
    plt.show()
    
def show_line_dose(dose1, dose2, x_start, x_end, y_idx, z_idx):
    """
    显示line dose, 横向的拉一条线, 这条线上的dose分布
    Args:
        dose1(numpy.ndarray): 第一个剂量分布。
        dose2(numpy.ndarray): 第二个剂量分布。
        x_start(int): 显示的x方向的起始索引。
        x_end(int): 显示的x方向的结束索引。
        y_idx(int): 显示的y方向的索引。
        z_idx(int): 显示的z方向的索引。
    """
    dose1_slice   = dose1[z_idx]
    dose2_slice   = dose2[z_idx]

    dose1_line   = dose1_slice[y_idx]
    dose2_line   = dose2_slice[y_idx]

    x = np.arange(x_start, x_end)  

    plt.plot(x, dose1_line[x_start:x_end], label='Dose1', color='blue', linestyle='-')
    plt.plot(x, dose2_line[x_start:x_end], label='Dose2', color='red', linestyle='--')
    plt.xlabel('X Index')
    plt.ylabel('Dose Value')
    plt.title(f'Line Dose at z= {z_idx}, y={y_idx}, x={x_start} to {x_end}')
    plt.legend()
    plt.grid(True)
    plt.show()
    
def create_cubeMask(shape, edge_size, mask_value):
    """
    创建一个cube mask, 在shape大小的矩阵内, 正中心的位置生成一个边长为edge_size的mask。
    Args:
        shape(tuple): 矩阵的大小。
        edge_size(int): 边长大小。
        mask_value(double): 填充的数值。
    Returns:
        mask(numpy.ndarray): 填充了mask_value的矩阵。
    """
    mask = np.zeros(shape)
    mask[shape[0]//2-edge_size//2:shape[0]//2+edge_size//2, shape[1]//2-edge_size//2:shape[1]//2+edge_size//2, shape[2]//2-edge_size//2:shape[2]//2+edge_size//2] = mask_value
    
    return mask

def show_gamma(dose_ref, dose_eval, dose_threshold, distance_threshold, dose_cutoff, interp_fraction, ram_available):
    """
    计算Gamma通过率
    Args:
        dose_ref (numpy.ndarray): 第一个剂量分布。
        dose_eval (numpy.ndarray): 第二个剂量分布。
        dose_threshold (double): 剂量差异百分比阈值
        distance_threshold (double): 空间距离阈值 (mm)
        dose_cutoff (double): 剂量截断百分比
        interp_fraction (int): 插值精度, 建议至少10
        ram_available (int): 可用内存（单位字节）
    """
    z_ref = np.arange(dose_ref.shape[0])
    y_ref = np.arange(dose_ref.shape[1])
    x_ref = np.arange(dose_ref.shape[2])
    axes_ref = (z_ref, y_ref, x_ref)

    z_eval = np.arange(dose_eval.shape[0])
    y_eval = np.arange(dose_eval.shape[1])
    x_eval = np.arange(dose_eval.shape[2])
    axes_eval = (z_eval, y_eval, x_eval)
    
    gamma_options = {
    'dose_percent_threshold': dose_threshold,      
    'distance_mm_threshold': distance_threshold,        
    'lower_percent_dose_cutoff': dose_cutoff,    
    'interp_fraction': interp_fraction,             
    'max_gamma': 2,                     
    'random_subset': None,
    'local_gamma': True,
    'ram_available': ram_available     
    }

    # 计算 gamma 指数，此处 axes 传入的是一维坐标轴元组
    gamma = pymedphys.gamma(
        axes_ref, dose_ref, 
        axes_eval, dose_eval, 
        **gamma_options
    )
    
    # 过滤掉 NaN 值
    valid_gamma = gamma[~np.isnan(gamma)]

    num_bins = gamma_options['interp_fraction'] * gamma_options['max_gamma']
    bins = np.linspace(0, gamma_options['max_gamma'], int(num_bins) + 1)

    plt.hist(valid_gamma, bins, density=True)
    plt.xlim([0, gamma_options['max_gamma']])
    plt.ylim([0, 10])
    plt.xlabel('gamma index')
    plt.ylabel('probability density')

    pass_ratio = np.sum(valid_gamma <= 1) / len(valid_gamma)

    if gamma_options['local_gamma']:
        gamma_norm_condition = 'Local gamma'
    else:
        gamma_norm_condition = 'Global gamma'

    plt.title(
        f"Dose cut: {gamma_options['lower_percent_dose_cutoff']}% | {gamma_norm_condition} "
        f"({gamma_options['dose_percent_threshold']}%/{gamma_options['distance_mm_threshold']}mm) | "
        f"Pass Rate(γ<=1): {pass_ratio*100:.2f}% \n ref pts: {dose_ref.size} | valid γ pts: {len(valid_gamma)}"
    )

    plt.show()
    
def cal_gamma(dose_ref, dose_eval, dose_threshold, distance_threshold, dose_cutoff, interp_fraction, ram_available):
    """
    计算Gamma通过率
    Args:
        dose_ref (numpy.ndarray): 第一个剂量分布。
        dose_eval (numpy.ndarray): 第二个剂量分布。
        dose_threshold (double): 剂量差异百分比阈值
        distance_threshold (double): 空间距离阈值 (mm)
        dose_cutoff (double): 剂量截断百分比
        interp_fraction (int): 插值精度, 建议至少10
        ram_available (int): 可用内存（单位字节）
    """
    z_ref = np.arange(dose_ref.shape[0])
    y_ref = np.arange(dose_ref.shape[1])
    x_ref = np.arange(dose_ref.shape[2])
    axes_ref = (z_ref, y_ref, x_ref)

    z_eval = np.arange(dose_eval.shape[0])
    y_eval = np.arange(dose_eval.shape[1])
    x_eval = np.arange(dose_eval.shape[2])
    axes_eval = (z_eval, y_eval, x_eval)
    
    gamma_options = {
    'dose_percent_threshold': dose_threshold,      
    'distance_mm_threshold': distance_threshold,        
    'lower_percent_dose_cutoff': dose_cutoff,    
    'interp_fraction': interp_fraction,             
    'max_gamma': 2,                     
    'random_subset': None,
    'local_gamma': True,
    'ram_available': ram_available     
    }

    # 计算 gamma 指数，此处 axes 传入的是一维坐标轴元组
    gamma = pymedphys.gamma(
        axes_ref, dose_ref, 
        axes_eval, dose_eval, 
        **gamma_options
    )
    
    # 过滤掉 NaN 值
    valid_gamma = gamma[~np.isnan(gamma)]

    num_bins = gamma_options['interp_fraction'] * gamma_options['max_gamma']
    bins = np.linspace(0, gamma_options['max_gamma'], int(num_bins) + 1)

    pass_ratio = np.sum(valid_gamma <= 1) / len(valid_gamma)
    
    return pass_ratio*100