import pandas as pd


def filter_excel(input_file, output_file, keyword_column_index, keyword, local_index, local_name):
    xls = pd.ExcelFile(input_file)
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')

    for sheet_name in xls.sheet_names:
        # 读取每个页的数据
        df = pd.read_excel(xls, sheet_name)

        # 检查指定的列是否存在于 DataFrame 中
        # if keyword_column_index >= len(df.columns):
        #     print(f"在表 '{sheet_name}' 中不存在第 {keyword_column_index + 1} 列。跳过。")
        #     continue
        # elif local_index >= len(df.columns):
        #     print(f"在表 '{sheet_name}' 中不存在第 {local_index + 1} 列。跳过。")
        #     continue

        # 保留每一页的原始格式，包括第一行和第二行
        df.iloc[:1].to_excel(writer, sheet_name, index=False)

        # 使用逻辑运算符 & 表示两个条件同时成立
        filtered_df = df[
            (df.iloc[:, keyword_column_index].str.contains(keyword, na=False)) &  # 第13列包含关键词
            (df.iloc[:, local_index].str.contains('|'.join(local_name), case=False, na=False))  # 第21列地址包含关键词列表中的任意一个
            ]

        # 检查过滤后的 DataFrame 是否为空
        if filtered_df.empty:
            print(f"在表 '{sheet_name}' 中未找到关键词 '{keyword}' 的行，并且该行无符合地址。跳过。")
            continue

        # 将过滤后的数据追加到新的 Excel 文件
        filtered_df.to_excel(writer, sheet_name, startrow=2, index=False, header=False)

    # 关闭写入器
    writer.close()
    print("筛选完成。")


# 示例调用，替换为你的实际文件和参数
input_excel_file = '2024公务员.xls'
output_excel_file = 'output.xlsx'
keyword_col_index = 12  # 第13列作为关键词列
keyword_value = '电子信息'
local_index = 20  # 第21列作为地址搜索关键列
local_name = ['西安', '陕西']  # 地址关键词包含西安或者陕西的

filter_excel(input_excel_file, output_excel_file, keyword_col_index, keyword_value, local_index, local_name)
