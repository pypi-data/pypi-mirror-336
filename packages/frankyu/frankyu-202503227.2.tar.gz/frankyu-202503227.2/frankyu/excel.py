import frankyu.tex
# 导入 frankyu.tex 模块

import datetime
# 导入 datetime 模块

import win32com.client
# 导入 win32com.client 模块

def get_current_time():
    # 获取当前时间
    return datetime.datetime.now()
    # 返回当前时间

def format_time(time):
    # 替换特定标点符号
    tex_module = frankyu.tex
    # 获取 frankyu.tex 模块
    return tex_module.replace_specific_punctuation(
        # 调用 replace_specific_punctuation 方法
        input_string=str(time),
        # 将时间转换为字符串并传递给 input_string 参数
        punctuation_string=r"-,:,."
        # 指定要替换的标点符号
    )

def initialize_excel():
    # 创建 Excel 应用程序的实例
    excel_app = win32com.client.gencache.EnsureDispatch("Excel.Application")
    # 创建 Excel 应用程序的实例
    excel_app.Visible = 1
    # 设置 Excel 应用程序的可见性为 1
    return excel_app
    # 返回 Excel 应用程序实例

def create_workbook(excel_app):
    # 新建一个 Excel 工作簿
    return excel_app.Workbooks.Add()
    # 返回新建的工作簿

def get_paste_values_constant():
    # 获取 Excel 常量
    return win32com.client.constants.xlPasteValues
    # 返回 Excel 常量 xlPasteValues 的值

def get_worksheet(workbook):
    # 获取工作簿中的第一个工作表
    return workbook.Worksheets(1)
    # 返回第一个工作表

def get_range(worksheet):
    # 获取工作表中 A1 到 E2 范围的单元格
    return worksheet.Range("A1:E2")
    # 返回单元格范围

def generate_file_name(time):
    # 生成文件名
    return "T:\\" + time + r'.xlsx'
    # 返回生成的文件名

def save_workbook(workbook, file_name):
    # 将工作簿保存为指定的文件名
    workbook.SaveAs(file_name)
    # 保存工作簿

def update_single_cell(worksheet, file_name):
    # 将文件名赋值给 D1 单元格
    single_cell = worksheet.Range("D1")
    # 获取 D1 单元格
    single_cell.Value = file_name
    # 将文件名赋值给 D1 单元格

def print_range_values(range_values):
    # 打印单元格范围中的值
    print(list(range_values))
    # 打印值列表

def main():
    # 主函数，调用其他函数完成所有操作
    current_time = get_current_time()
    # 获取当前时间
    formatted_time = format_time(current_time)
    # 替换特定标点符号
    print(formatted_time)
    # 打印格式化时间
    
    excel_app = initialize_excel()
    # 初始化 Excel 应用程序
    paste_values_constant = get_paste_values_constant()
    # 获取 Excel 常量
    print(paste_values_constant)
    # 打印常量值
    
    workbook = create_workbook(excel_app)
    # 创建 Excel 工作簿
    worksheet = get_worksheet(workbook)
    # 获取第一个工作表
    cell_range = get_range(worksheet)
    # 获取单元格范围
    
    file_name = generate_file_name(formatted_time)
    # 生成文件名
    print(file_name)
    # 打印文件名
    
    save_workbook(workbook, file_name)
    # 保存工作簿
    update_single_cell(worksheet, file_name)
    # 更新单元格值
    
    print_range_values(cell_range.Value)
    # 打印单元格范围中的值

if __name__ == "__main__":
    main()
    # 调用主函数